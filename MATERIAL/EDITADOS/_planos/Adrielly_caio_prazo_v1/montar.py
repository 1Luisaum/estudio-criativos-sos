"""Clone do anuncio do Drive 1vlTjZ ("nosso prazo esta acabando", 23,6 s) para o Pedrinho.
Mesmo molde: 3 caixas paradas o video todo (vermelha no alto, branca no meio, vermelha embaixo), Poppins Bold,
11 tomadas cruas de ~1-3 s com fusao de 0,3 s, a tomada "larga" voltando entre as outras, e a mesma musica.
Uso: python -I montar.py   (le plano.json ao lado)"""
import json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
K = os.path.expanduser(r"~\.claude\skills\criativo-reportagem-ong\scripts")
sys.path.insert(0, K)
import comum as C  # noqa: E402
import marca  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

PP = os.path.join(AQUI, "plano.json")
p = json.load(open(PP, encoding="utf-8"))
W, H, FPS, XF = 1080, 1920, 30, 0.3
FONT = os.path.join(os.environ["LOCALAPPDATA"], r"Microsoft\Windows\Fonts\Poppins-Bold.ttf")
if not os.path.exists(FONT):
    FONT = r"C:\Windows\Fonts\Poppins-Bold.ttf"
RED, WHITE, BLACK = tuple(p["cor_vermelha"]), (255, 255, 255), (0, 0, 0)


TRACK, TRACO = 0.05, 1  # a referencia tem letras mais espacadas (~5% do tamanho) e um pouco mais grossas


def larg(f, t):
    return sum(f.getlength(c) for c in t) + TRACK * f.size * (len(t) - 1)


def fit(ref_text, ref_w):
    """Tamanho de fonte que deixa a frase da referencia com a largura medida na referencia."""
    for s in range(30, 140):
        if larg(ImageFont.truetype(FONT, s), ref_text) > ref_w:
            return s - 1
    return 139


def caixa(dr, linhas, size, cx, top, pitch, fg, bg, padx, pady):
    f = ImageFont.truetype(FONT, size)
    w = max(larg(f, l) for l in linhas)
    x0, x1 = cx - w / 2 - padx, cx + w / 2 + padx
    y1 = top + pitch * len(linhas) + pady * 2
    dr.rectangle([x0, top, x1, y1], fill=bg)
    for i, l in enumerate(linhas):
        yc = top + pady + pitch * (i + 0.5)
        x = cx - larg(f, l) / 2
        for ch in l:
            dr.text((x, yc), ch, font=f, fill=fg, anchor="lm", stroke_width=TRACO, stroke_fill=fg)
            x += f.getlength(ch) + TRACK * size
    return [round(x0), top, round(x1), round(y1)]


def overlay(sem_topo=False):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    bx = {}
    for k in (("meio", "baixo") if sem_topo else ("topo", "meio", "baixo")):
        c = p[k]
        size = fit(c["ref_frase"], c["ref_largura"])
        fg, bg = (WHITE, RED) if k != "meio" else (BLACK, WHITE)
        bx[k] = caixa(dr, c["linhas"], size, c["cx"], c["y"], c["passo"], fg, bg, c["padx"], c["pady"])
        print(f"{k}: fonte {size}px caixa {bx[k]}")
    out = os.path.join(AQUI, "render", "caixas_sem_topo.png" if sem_topo else "caixas.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out)
    return out


def main():
    ov = overlay()
    ov2 = overlay(sem_topo=True)  # take com o rosto no alto: a caixa de cima some so nele
    tomadas = p["tomadas"]
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for t in tomadas:
        if t["arquivo"].lower().endswith((".jpg", ".jpeg", ".png")):  # foto parada: endireita pela rotacao da camera
            from PIL import ImageOps
            png = os.path.join(AQUI, "render", "foto_" + os.path.splitext(os.path.basename(t["arquivo"]))[0] + ".png")
            ImageOps.exif_transpose(Image.open(t["arquivo"])).convert("RGB").save(png)
            cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{t['dur'] + XF:.3f}", "-i", png]
        else:
            cmd += ["-ss", str(t["inicio"]), "-t", f"{t['dur'] + XF:.3f}", "-i", t["arquivo"]]
    tot = sum(t["dur"] for t in tomadas) + 1
    cmd += ["-loop", "1", "-t", f"{tot:.2f}", "-i", ov, "-i", p["musica"], "-loop", "1", "-t", f"{tot:.2f}", "-i", ov2]
    n = len(tomadas)
    fc = []
    for i, t in enumerate(tomadas):
        z = t.get("zoom_topo", 1.0)  # aproxima preso ao topo: o rosto desce para baixo da caixa de cima
        zz = f",scale={round(W * z / 2) * 2}:{round(H * z / 2) * 2},crop={W}:{H}:(iw-{W})/2:0" if z > 1 else ""
        fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}{zz},fps={FPS},"
                  f"setsar=1,format=yuv420p,trim=0:{t['dur'] + XF:.3f},setpts=PTS-STARTPTS[v{i}]")
    acc, off = "v0", tomadas[0]["dur"]
    for i in range(1, n):
        fc.append(f"[{acc}][v{i}]xfade=transition=fade:duration={XF}:offset={off - XF / 2:.3f}[x{i}]")
        acc, off = f"x{i}", off + tomadas[i]["dur"]
    total = sum(t["dur"] for t in tomadas)
    t, rng = 0.0, []
    for tt in tomadas:
        if tt.get("sem_topo"): rng.append(f"between(t,{max(0, t - XF):.3f},{t + tt['dur'] + XF / 2:.3f})")
        t += tt["dur"]
    sem = "+".join(rng) or "0"
    fc.append(f"[{acc}][{n}:v]overlay=0:0:shortest=1:enable='not({sem})'[ov1]")
    fc.append(f"[ov1][{n + 2}:v]overlay=0:0:shortest=1:enable='{sem}',trim=0:{total:.3f},format=yuv420p[v]")
    fc.append(f"[{n + 1}:a]atrim={p.get('musica_inicio', 0)}:{p.get('musica_inicio', 0) + total:.3f},asetpts=PTS-STARTPTS,"
              f"afade=t=out:st={total - 0.6:.3f}:d=0.6[a]")
    saida = C.destino(PP, p, p["estilo"])
    print("saida:", saida)
    cmd += ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-r", str(FPS), *C.enc_final(),
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(r.stderr[-2000:]); sys.exit("ffmpeg falhou")
    marca.no_fim(p, saida)  # logo SOS obrigatoria
    p["saida"] = saida
    json.dump(p, open(PP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK {saida} duracao={total:.2f}s")


main()
