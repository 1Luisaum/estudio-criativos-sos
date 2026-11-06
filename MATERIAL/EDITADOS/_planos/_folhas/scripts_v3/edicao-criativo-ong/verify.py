"""Confere o MP4 FINAL (nunca um intermediario: no primeiro video o aroll estava certo e o final nao).

1. buracos no audio do arquivo final
2. retranscreve o audio final e compara cada palavra falada com a legenda na tela naquele instante
3. vicios ("é,", "aaa"...) que sobraram e pausas maiores que 0,45 s entre palavras
4. ate quando ha fala x inicio da tela final

Uso: python -I verify.py <final.mp4> <legendas.ass> [--from 0] [--tela-final 35.93]
"""
import argparse, difflib, json, os, re, subprocess, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transcribe import transcribe  # noqa: E402

FILLER = re.compile(r"^(é+|eh+|e{2,}|a{2,}|ã+|hum+|hm+|ah+|uh+)$", re.I)


def norm(s):
    s = unicodedata.normalize("NFD", s.upper())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^A-Z0-9$]", "", s)


def same(a, b):
    a, b = norm(a), norm(b)
    if a == b or a.rstrip("S") == b.rstrip("S"):
        return True
    if len(a) >= 3 and len(b) >= 3 and (a.startswith(b) or b.startswith(a)):
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.75


def sec(s):
    h, m, x = s.split(":")
    return int(h) * 3600 + int(m) * 60 + float(x)


def caption_events(ass):
    ev = []
    for line in open(ass, encoding="utf-8-sig"):
        if ",Cap,," not in line:
            continue
        p = line.split(",", 9)
        vis = [w for a, w in re.findall(r"\{([^}]*)\}([^{ \n]+)", p[9]) if "1a&H00&" in a]
        if vis:
            ev.append((sec(p[1]), sec(p[2]), vis))
    return ev


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("ass")
    ap.add_argument("--from", dest="start", type=float, default=0.0)
    ap.add_argument("--tela-final", dest="end_start", type=float, default=None)
    a = ap.parse_args()
    problems = 0

    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
                        "packet=pts_time,duration_time", "-of", "csv=p=0", a.video], capture_output=True, text=True)
    pk = [tuple(map(float, l.split(",")[:2])) for l in r.stdout.split() if l]
    holes = [(round(x[0], 2), round(y[0], 2)) for x, y in zip(pk, pk[1:]) if y[0] - x[0] - x[1] > 0.02]
    print(f"[audio] {pk[-1][0] + pk[-1][1]:.2f}s, buracos: {holes or 'nenhum'}")
    problems += len(holes)

    data = transcribe(a.video, start=a.start)
    spoken = [w for w in data["words"] if w["type"] == "word"]
    caps = caption_events(a.ass)
    print(f"[fala] {data.get('text', '')}")

    # cada palavra falada precisa aparecer na legenda ate 0,3 s antes/depois, e vice-versa.
    # Palavras de ate 2 letras ("o", "e", "da") nao contam: a retranscricao as perde ou desloca a toa.
    # Um audio fora de sincronia de verdade gera dezenas de diferencas, nao uma ou duas.
    reveals = [(c[0], c[2][-1]) for c in caps]
    bad = []
    for w in spoken:
        if len(norm(w["text"])) <= 2:
            continue
        near = [r for r in reveals if abs(r[0] - w["start"]) <= 0.3]
        if not any(same(w["text"], r[1]) for r in near):
            shown = min(reveals, key=lambda r: abs(r[0] - w["start"]))[1] if reveals else "-"
            bad.append(f"  {w['start']:6.2f}s falou '{w['text'].strip()}' / legenda '{shown}'")
    orphan = [f"  {t:6.2f}s legenda '{wd}' sem fala perto" for t, wd in reveals if t >= a.start
              and len(norm(wd)) > 2 and not any(abs(w["start"] - t) <= 0.5 and same(w["text"], wd) for w in spoken)]
    print(f"[sincronia] {len(spoken)} palavras faladas, {len(bad)} diferentes da legenda, {len(orphan)} legendas sem fala")
    for line in bad[:25] + orphan[:25]:
        print(line)
    isolated = len(bad) + len(orphan)
    if isolated > 4:
        problems += isolated
        print("  -> muitas diferencas seguidas: audio fora de sincronia ou legenda errada")
        isolated = 0

    fillers = [f"{w['start']:.2f}s '{w['text'].strip()}'" for w in spoken
               if FILLER.match(w["text"].strip().strip(",.!?").lower()) and
               (w["text"].strip().strip(".!?").lower() != "é" or w["text"].strip().endswith(","))]
    gaps = [f"{x['end']:.2f}-{y['start']:.2f}s ({y['start'] - x['end']:.2f}s)" for x, y in zip(spoken, spoken[1:])
            if y["start"] - x["end"] > 0.45]
    print(f"[vicios] {fillers or 'nenhum'}")
    print(f"[pausas > 0,45s] {gaps or 'nenhuma'}")
    if spoken:
        last = spoken[-1]["end"]
        msg = f"[fim da fala] {last:.2f}s"
        if a.end_start is not None:
            msg += f" / tela final em {a.end_start:.2f}s"
            if a.end_start - last > 1.0:
                msg += "  <- fala acaba cedo demais (audio cortado?)"; problems += 1
        print(msg)
    if problems:
        print(f"RESULTADO: {problems} problema(s); corrija antes de entregar")
    elif isolated:
        print(f"RESULTADO: OK, com {isolated} diferenca(s) isolada(s); veja se e so variacao da transcricao")
    else:
        print("RESULTADO: OK")


if __name__ == "__main__":
    main()
