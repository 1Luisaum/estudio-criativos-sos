"""Estilos dos anuncios do Caio protetor (CP 54 e CP 1027) aplicados a um video validado (29/10/2026).
A fala real fica inteira (igual ao video validado); por cima: gancho em caixa sobre b-roll forte, cortes para b-roll
nas pausas, legenda no estilo do Caio, faixa de CTA no fim e a marca @soshumanhelppt.
Uso: python -I caio.py "<pasta do plano>\plano.json"
Plano: estilo ("cp54"|"cp1027"), base {arquivo, inicio, fim, tx}, musica?, gancho {linhas, ate, cena},
       cenas [[t0, t1, arquivo, inicio]], cta {de, linhas}, faixa {de, linhas} (so cp1027)."""
import json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
K = os.path.expanduser(r"~\.claude\skills\criativo-reportagem-ong\scripts")
sys.path.insert(0, K)
import comum as C  # noqa: E402
import marca  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

PP = os.path.abspath(sys.argv[1]); P = os.path.dirname(PP); R = os.path.join(P, "render"); os.makedirs(R, exist_ok=True)
p = json.load(open(PP, encoding="utf-8"))
W, H, FPS = 1080, 1920, 30
FD = os.path.join(os.environ["LOCALAPPDATA"], r"Microsoft\Windows\Fonts")
BOLD, BLACK = os.path.join(FD, "Poppins-Bold.ttf"), os.path.join(FD, "Poppins-Black.ttf")
RED, WHITE, BLK = (226, 6, 19), (255, 255, 255), (0, 0, 0)
DESTAQUE = ["dor", "dor.", "dor,", "cura", "cura,", "aguento", "ajuda,", "feridas.", "providência,", "muita", "mais.", "senhor.", "senhor,"]


def png(nome, im):
    f = os.path.join(R, nome + ".png"); im.save(f); return f


def caixa(linhas, font, size, fg, bg, padx=18, pady=10, lh=1.12):
    f = ImageFont.truetype(font, size)
    w = max(f.getlength(l) for l in linhas); h = int(size * lh)
    im = Image.new("RGBA", (int(w + padx * 2), h * len(linhas) + pady * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); d.rectangle([0, 0, im.width - 1, im.height - 1], fill=bg)
    for i, l in enumerate(linhas):
        d.text((im.width / 2, pady + h * (i + 0.5)), l, font=f, fill=fg, anchor="mm")
    return im


def legenda_cp54(palavras, size=58):
    """Branco com contorno preto; a palavra forte vai numa caixinha vermelha (como no CP 54)."""
    f = ImageFont.truetype(BOLD, size); sp = f.getlength(" ")
    alvo = next((i for i, w in enumerate(palavras) if w.lower() in DESTAQUE), None)
    ws = [f.getlength(w) for w in palavras]; tw = sum(ws) + sp * (len(ws) - 1)
    im = Image.new("RGBA", (int(tw + 40), int(size * 1.6)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x, yc = 20, im.height / 2
    for i, (w, l) in enumerate(zip(palavras, ws)):
        if i == alvo:
            d.rectangle([x - 6, yc - size * 0.62, x + l + 6, yc + size * 0.62], fill=RED)
            d.text((x, yc), w, font=f, fill=WHITE, anchor="lm")
        else:
            d.text((x, yc), w, font=f, fill=WHITE, anchor="lm", stroke_width=4, stroke_fill=BLK)
        x += l + sp
    return im


def palavras_base():
    b = p["base"]; d = json.load(open(b["tx"], encoding="utf-8"))
    return [(w["start"] - b["inicio"], w["end"] - b["inicio"], w["text"]) for w in d["words"]
            if w.get("type", "word") == "word" and b["inicio"] <= w["start"] < b["fim"]]


def blocos(ws, maxp):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) >= maxp or re.search(r"[.,?!]$", w[2]):
            out.append(cur); cur = []
    if cur: out.append(cur)
    res = []
    for i, g in enumerate(out):
        a = g[0][0]; b = out[i + 1][0][0] if i + 1 < len(out) else g[-1][1] + 0.4
        res.append((a, min(b, g[-1][1] + 0.9), [w[2].upper() for w in g]))
    return res


def main():
    b = p["base"]; total = b["fim"] - b["inicio"]; est = p["estilo"]
    cmd = ["ffmpeg", "-y", "-v", "error", "-ss", str(b["inicio"]), "-t", f"{total:.3f}", "-i", b["arquivo"]]
    cenas = [(0.0, p["gancho"]["ate"], p["gancho"]["cena"][0], p["gancho"]["cena"][1])] + [tuple(c) for c in p.get("cenas", [])]
    for t0, t1, arq, ini in cenas:
        cmd += ["-ss", str(ini), "-t", f"{t1 - t0 + 0.1:.3f}", "-i", arq]
    fc = [f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,format=yuv420p[base]"]
    acc = "base"
    for i, (t0, t1, arq, ini) in enumerate(cenas, start=1):
        fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,format=yuv420p,"
                  f"setpts=PTS-STARTPTS+{t0}/TB[c{i}]")
        fc.append(f"[{acc}][c{i}]overlay=0:0:eof_action=pass:enable='between(t,{t0},{t1})'[o{i}]"); acc = f"o{i}"
    n = len(cenas) + 1
    ovs = []  # (png, x, y, t0, t1)
    g = p["gancho"]
    if est == "cp54":
        hk = caixa(g["linhas"], BOLD, 62, BLK, WHITE, padx=22, pady=12)
    else:
        hk = caixa(g["linhas"], BLACK, 60, WHITE, RED, padx=22, pady=12)
    ovs.append((png("gancho", hk), (W - hk.width) // 2, g.get("y", 1000) - hk.height // 2, 0, g["ate"]))
    for i, (a, c, ws) in enumerate(blocos(palavras_base(), 3 if est == "cp54" else 6)):
        if c <= g["ate"]: continue
        a = max(a, g["ate"])
        im = legenda_cp54(ws) if est == "cp54" else caixa(_quebra(ws), BLACK, 50, WHITE, RED, padx=16, pady=8)
        ovs.append((png(f"leg{i:02d}", im), (W - im.width) // 2, p.get("legenda_y", 1160) - im.height // 2, a, c))
    for k in ("faixa", "cta"):
        if p.get(k):
            ct = p[k]; im = caixa(ct["linhas"], BLACK, ct.get("size", 40), WHITE, RED, padx=16, pady=8, lh=1.1)
            ovs.append((png(k, im), (W - im.width) // 2, ct["y"], ct["de"], total))
    for j, (f, x, y, t0, t1) in enumerate(ovs):
        cmd += ["-loop", "1", "-t", f"{total:.3f}", "-i", f]
        fc.append(f"[{acc}][{n + j}:v]overlay={x}:{y}:enable='between(t,{t0:.2f},{t1:.2f})'[x{j}]"); acc = f"x{j}"
    fc.append(f"[{acc}]trim=0:{total:.3f},setpts=PTS-STARTPTS,format=yuv420p[v]")
    a_in = n + len(ovs)
    fc.append(f"[0:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,loudnorm=I=-15:TP=-1.5:LRA=9[voz]")
    if p.get("musica"):
        cmd += ["-stream_loop", "-1", "-i", p["musica"]]
        fc.append(f"[{a_in}:a]atrim=0:{total:.3f},volume={p.get('musica_volume', 0.08)},afade=t=out:st={total - 1.5:.3f}:d=1.5[m]")
        fc.append("[voz][m]amix=inputs=2:normalize=0[a]")
    else:
        fc.append("[voz]anull[a]")
    saida = C.destino(PP, p, p["pasta_estilo"]); print("saida:", saida)
    cmd += ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-r", str(FPS), *C.enc_final(),
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(r.stderr[-2500:]); sys.exit("ffmpeg falhou")
    marca.no_fim(p, saida)
    p["saida"] = saida; json.dump(p, open(PP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK {saida} duracao={total:.2f}s")


def _quebra(ws, maxc=22):
    linhas, cur = [], ""
    for w in ws:
        if cur and len(cur) + 1 + len(w) > maxc: linhas.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    return linhas + [cur]


main()
