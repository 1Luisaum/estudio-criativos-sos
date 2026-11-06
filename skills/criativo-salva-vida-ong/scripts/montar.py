"""Copia da edicao do anuncio 1473150411323796 da Ampara Brasil, pedida pelo usuario em 26/10/2026.

- sem fala: so musica (a referencia usa um louvor cantado; aqui vai trilha instrumental);
- no alto, o video todo: o valor grande (branco com contorno) e, embaixo, uma faixa branca com o pedido
  em letra preta condensada e um emoji;
- cenas intimas e lentas (4 a 6 s), em cor, que se misturam na troca (xfade).

Uso: python -I montar.py plano.json
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
from comum import enc_antes_da_logo  # noqa: E402  passada antes da logo: rapida e quase sem perda (27/10/2026)

W, H, FPS = 1080, 1920, 30
F = "C:/Windows/Fonts/"
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS)]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(r.stderr[-2500:])
        sys.exit("ffmpeg falhou")
    return r


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout)


def bahn(size, var="Bold Condensed"):
    f = ImageFont.truetype(F + "bahnschrift.ttf", size)
    f.set_variation_by_name(var)
    return f


def partes(s):
    out, cur, emo = [], "", None
    for ch in s:
        e = ord(ch) >= 0x1F000 or 0x2600 <= ord(ch) <= 0x27BF or ch in "\u200d\ufe0f"
        if emo is None or e == emo:
            cur += ch
        else:
            out.append((cur, emo)); cur = ch
        emo = e
    if cur:
        out.append((cur, emo))
    return out


def topo_png(valor, pedido, path):
    """Valor grande branco com contorno preto; embaixo faixa branca com o pedido em preto + emoji."""
    fv = bahn(150)
    fp, fe = bahn(52), ImageFont.truetype(F + "seguiemj.ttf", 44)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    vw = tmp.textlength(valor, font=fv)
    pw = sum(tmp.textlength(t, font=fe if e else fp) for t, e in partes(pedido))
    im = Image.new("RGBA", (W, 250), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text(((W - vw) / 2, 0), valor, font=fv, fill="white", stroke_width=6, stroke_fill=(20, 20, 20))
    x0, y0 = (W - pw) / 2, 172
    d.rounded_rectangle([x0 - 16, y0 - 4, x0 + pw + 16, y0 + 62], radius=10, fill="white")
    x = x0
    for t, e in partes(pedido):
        if e:
            d.text((x, y0 + 4), t, font=fe, embedded_color=True)
            x += d.textlength(t, font=fe)
        else:
            d.text((x, y0), t, font=fp, fill="black")
            x += d.textlength(t, font=fp)
    im.save(path)


def main():
    pp = os.path.abspath(sys.argv[1])
    P = os.path.dirname(pp)
    p = json.load(open(pp, encoding="utf-8"))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import comum as C
    saida = C.destino(pp, p, p.get("pasta_saida", "SALVA VIDA"))
    WK = os.path.join(P, "render")
    os.makedirs(WK, exist_ok=True)
    xf = p.get("transicao", 0.6)

    # 1. cenas (zoom opcional preso no topo, para descer um rosto que fica embaixo do texto)
    arqs = []
    for i, c in enumerate(p["cenas"]):
        z = c.get("zoom", 1.0)
        foto = c["src"].lower().endswith((".jpg", ".jpeg", ".png"))
        base = f"scale={round(W * z)}:{round(H * z)}:force_original_aspect_ratio=increase"
        cx = {"direita": f"iw-{W}", "esquerda": "0"}.get(c.get("lado"), f"(iw-{W})/2")
        crop = f"crop={W}:{H}:{cx}:{'0' if c.get('topo') else f'(ih-{H})/2'}"
        nf = round(c["dur"] * FPS)
        vf = (f"{base},{crop},scale={W * 2}:{H * 2},zoompan=z='1+0.05*on/{nf}':x='iw/2-(iw/zoom/2)':"
              f"y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}" if foto else f"fps={FPS},{base},{crop}")
        inp = (["-loop", "1", "-framerate", str(FPS), "-t", f"{c['dur'] + 0.2:.3f}", "-i", c["src"]] if foto
               else ["-ss", f"{c['start']:.2f}", "-t", f"{c['dur'] + 0.2:.3f}", "-an", "-i", c["src"]])
        out = os.path.join(WK, f"c{i:02d}.mp4")
        run(["ffmpeg", "-y"] + inp + ["-vf", vf + f",setsar=1,trim=duration={c['dur']:.3f}", "-an", *ENC, out])
        arqs.append((out, c["dur"]))

    # 2. junta com transicao que mistura uma cena na outra
    cmd, fc, last, t = ["ffmpeg", "-y"], [], "[0:v]", arqs[0][1]
    for a, _ in arqs:
        cmd += ["-i", a]
    for i in range(1, len(arqs)):
        fc.append(f"{last}[{i}:v]xfade=transition=fade:duration={xf}:offset={t - xf:.3f}[x{i}]")
        last, t = f"[x{i}]", t - xf + arqs[i][1]
    video = os.path.join(WK, "video.mp4")
    run(cmd + ["-filter_complex", ";".join(fc), "-map", last, *ENC, video])
    total = dur(video)

    # 3. texto parado no alto + musica (sem fala)
    png = os.path.join(WK, "topo.png")
    topo_png(p["valor"], p["pedido"], png)
    # a musica soa ja no 1o segundo (27/10/2026): pula o silencio do comeco da trilha e o fade de entrada e curto
    ms = p.get("musica_inicio", C.inicio_do_som(p["musica"]))
    run(["ffmpeg", "-y", "-i", video, "-i", png, "-ss", f"{ms:.2f}", "-stream_loop", "-1", "-i", p["musica"],
         "-filter_complex",
         f"[0:v][1:v]overlay=0:{p.get('topo_y', 180)},format=yuv420p[v];"
         f"[2:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total:.3f},afade=t=in:d=0.3,"
         f"afade=t=out:st={total - 1.8:.3f}:d=1.8,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
         "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}", *enc_antes_da_logo(),
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida])
    import marca  # logo SOS andando pela tela, opacidade baixa (26/10/2026)
    marca.no_fim(p, saida)
    print(f"OK {saida} duracao={total:.1f}s")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
