"""Le a transcricao do bruto e ajuda a decidir os cortes.

  --words          lista palavra a palavra com tempos, pausas e marcas (V = vicio, F = falso comeco,
                   R = repeticao, C = conector solto, ? = vocativo/muleta para avaliar)
  --draft          rascunho de segmentos (JSON) ja sem vicios, gaguejadas e pausas >= 0,30 s
  --env 7.0-7.4,12-12.8 --media bruto.mp4
                   volume a cada 20 ms nesses trechos (dB abaixo do maximo: ~50+ = silencio,
                   ~30-40 = fala) para acertar cortes colados em vicio

Uso: python -I inspect_tx.py transcricao.json --words --draft
"""
import argparse, array, json, math, os, re, subprocess, sys, tempfile, wave

FILLER = re.compile(r"^(é+|eh+|e{2,}|a{2,}|ã+|hum+|hm+|ah+|uh+|ham+)$", re.I)
SOFT = {"pessoal", "galera", "assim", "então", "tipo", "né", "gente", "sabe"}
GAP_SPLIT = 0.30


def core(t):
    return t.strip().strip(",.!?…\"'").lower()


def classify(words):
    """Marca cada palavra. Retorna lista de (palavra, marca, cortar?)."""
    out = []
    for i, w in enumerate(words):
        t, c = w["text"].strip(), core(w["text"])
        nxt = words[i + 1] if i + 1 < len(words) else None
        gap_after = (nxt["start"] - w["end"]) if nxt else 9
        gap_before = (w["start"] - words[i - 1]["end"]) if i else 9
        tag, cut = "", False
        # "é"/"ó" sem virgula costumam ser verbo ou vocativo; com virgula sao muleta ("aqui, ó,")
        if (FILLER.match(c) and c != "é") or (c in ("é", "ó") and t.endswith(",")):
            tag, cut = "V", True
        elif c.endswith("-"):
            tag, cut = "F", True
        elif nxt and core(nxt["text"]) == c and t.endswith(","):
            tag, cut = "R", True                                   # "na, na carne" -> fica o segundo
        elif c == "e" and (gap_after >= 0.25 or gap_before >= 0.6):
            tag, cut = "C", True                                   # "E" solto abrindo frase depois de pausa
        elif c == "e" and (i == 0 or words[i - 1]["text"].strip()[-1:] in ".!?"):
            tag = "C"
        elif c in SOFT:
            tag = "?"
        out.append([w, tag, cut])
    # recomeco: "os meus fe- os meus ferimentos" -> corta o primeiro "os meus" junto com o "fe-"
    for i, (w, tag, _) in enumerate(out):
        if tag != "F":
            continue
        for k in range(4, 0, -1):
            before = [core(x[0]["text"]) for x in out[max(0, i - k):i]]
            after = [core(x[0]["text"]) for x in out[i + 1:i + 1 + k]]
            if len(before) == k and before == after:
                for x in out[i - k:i]:
                    x[1], x[2] = "R", True
                break
    return [tuple(x) for x in out]


def draft(marked):
    segs, cur = [], []
    allw = [m[0] for m in marked]
    for idx, (w, tag, cut) in enumerate(marked):
        if cut:
            if cur:
                segs.append(cur); cur = []
            continue
        if cur and w["start"] - cur[-1][1]["end"] >= GAP_SPLIT:
            segs.append(cur); cur = []
        cur.append((idx, w))
    if cur:
        segs.append(cur)
    res = []
    for s in segs:
        i0, first = s[0]
        i1, last = s[-1]
        prev_end = allw[i0 - 1]["end"] if i0 > 0 else 0.0
        next_start = allw[i1 + 1]["start"] if i1 + 1 < len(allw) else last["end"] + 0.5
        t_in = max(first["start"] - 0.06, prev_end + 0.02)
        t_out = min(last["end"] + 0.08, next_start - 0.02)
        res.append({"in": round(t_in, 2), "out": round(t_out, 2),
                    "txt": " ".join(w["text"].strip() for _, w in s)})
    return res


def envelope(media, windows):
    tmp = tempfile.mkdtemp(prefix="env_")
    wav = os.path.join(tmp, "a.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", media, "-vn", "-ac", "1", "-ar", "16000",
                    "-c:a", "pcm_s16le", wav], check=True)
    w = wave.open(wav)
    sr = w.getframerate()
    a = array.array("h", w.readframes(w.getnframes()))
    hop = int(sr * 0.02)
    for s, e in windows:
        vals, t = [], s
        while t < e:
            i = int(t * sr)
            chunk = a[i:i + hop]
            r = math.sqrt(sum(x * x for x in chunk) / len(chunk)) if chunk else 0
            vals.append(f"{int(-20 * math.log10(r / 32768 + 1e-9)):2d}")
            t += 0.02
        print(f"{s:6.2f}: " + " ".join(vals))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("tx")
    ap.add_argument("--words", action="store_true")
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--env", default="")
    ap.add_argument("--media", default="")
    a = ap.parse_args()
    words = [w for w in json.load(open(a.tx, encoding="utf-8"))["words"] if w["type"] == "word"]
    marked = classify(words)
    if a.words:
        prev = None
        for w, tag, cut in marked:
            if prev is not None and w["start"] - prev >= 0.25:
                print(f"            ---- pausa {w['start'] - prev:.2f}s")
            print(f"{w['start']:6.2f}-{w['end']:6.2f} {tag or ' '}{'x' if cut else ' '} {w['text'].strip()}")
            prev = w["end"]
    if a.draft:
        segs = draft(marked)
        print(json.dumps(segs, ensure_ascii=False, indent=1))
        print(f"# {len(segs)} segmentos, {sum(s['out'] - s['in'] for s in segs):.1f}s de fala")
    if a.env:
        if not a.media:
            sys.exit("--env precisa de --media")
        envelope(a.media, [tuple(map(float, p.split("-"))) for p in a.env.split(",")])


if __name__ == "__main__":
    main()
