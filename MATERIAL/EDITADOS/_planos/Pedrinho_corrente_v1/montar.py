"""Copia da edicao do anuncio 1444789200923601 da Causas do Bem (Kaue), pedida pelo usuario em 26/10/2026.

- texto fixo no alto o video todo, branco com contorno fino e trechos em amarelo (sem caixa, sem legenda);
- voz real da crianca nos primeiros segundos, depois so musica (mais alta);
- b-roll em tela cheia, com passagens rapidas pelo preto onde a cena pede (fade_in / fade_out).

Uso: python -I montar.py plano.json
"""
import glob
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FONTE = r"C:\Windows\Fonts\seguisb.ttf"
AMARELO = (246, 232, 20)
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS)]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(r.stderr[-2500:])
        sys.exit("ffmpeg falhou")
    return r


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout)


def texto_png(segs, path, size=50):
    """segs: [[texto, "y" ou ""], ...]; um item com texto vazio quebra a linha."""
    linhas, cur = [], []
    for t, c in segs:
        if t == "":
            linhas.append(cur); cur = []
        else:
            cur.append((t, c == "y"))
    if cur:
        linhas.append(cur)
    f = ImageFont.truetype(FONTE, size)
    lh = int(size * 1.18)
    im = Image.new("RGBA", (W, lh * len(linhas) + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(linhas):
        tw = sum(d.textlength(t, font=f) for t, _ in ln)
        x = (W - tw) / 2
        for t, am in ln:
            d.text((x + 2, 8 + i * lh + 3), t, font=f, fill=(0, 0, 0, 150))  # sombra leve
            d.text((x, 8 + i * lh), t, font=f, fill=AMARELO if am else "white", stroke_width=3, stroke_fill="black")
            x += d.textlength(t, font=f)
    im.save(path)


def main():
    pp = os.path.abspath(sys.argv[1])
    P = os.path.dirname(pp)
    p = json.load(open(pp, encoding="utf-8"))
    sys.path.insert(0, os.path.expanduser(r"~\.claude\skills\criativo-caixas-pedido-ong\scripts"))
    import comum as C
    saida = C.destino(pp, p, "CORRENTE DO BEM")
    WK = os.path.join(P, "render")
    os.makedirs(WK, exist_ok=True)

    # 1. cenas em tela cheia, com passagem pelo preto onde marcado
    partes = []
    for i, c in enumerate(p["cenas"]):
        d = c["dur"]
        foto = c["src"].lower().endswith((".jpg", ".jpeg", ".png"))
        nf = round(d * FPS)
        vf = (f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
              f"zoompan=z='1+0.06*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}"
              if foto else f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}")
        vf += ",setsar=1"
        if c.get("fade_in"):
            vf += ",fade=t=in:st=0:d=0.3"
        if c.get("fade_out"):
            vf += f",fade=t=out:st={d - 0.3:.3f}:d=0.3"
        inp = (["-loop", "1", "-framerate", str(FPS), "-t", f"{d + 0.2:.3f}", "-i", c["src"]] if foto
               else ["-ss", f"{c['start']:.2f}", "-t", f"{d + 0.2:.3f}", "-an", "-i", c["src"]])
        out = os.path.join(WK, f"cena{i:02d}.mp4")
        run(["ffmpeg", "-y"] + inp + ["-vf", vf + f",trim=duration={d:.3f}", "-an", *ENC, out])
        partes.append(out)
    lst = os.path.join(WK, "lista.txt")
    open(lst, "w", encoding="utf-8").writelines(f"file '{x}'\n" for x in partes)
    video = os.path.join(WK, "video.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video])
    total = dur(video)

    # 2. texto fixo no alto
    png = os.path.join(WK, "texto.png")
    texto_png(p["texto"], png)

    # 3. audio: falas reais coladas no comeco + musica que sobe depois da voz
    cmd, fc, labels = ["ffmpeg", "-y"], [], ""
    for i, f in enumerate(p["falas"]):
        a, b = f["corte"]
        cmd += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", f["fonte"]]
        fc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=mono,highpass=f=80,afftdn=nf=-25,"
                  f"afade=t=in:d=0.02,afade=t=out:st={b - a - 0.04:.3f}:d=0.04,apad=pad_dur=0.12[f{i}]")
        labels += f"[f{i}]"
    n = len(p["falas"])
    fc.append(f"{labels}concat=n={n}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=7,"
              f"adelay={int(p.get('voz_inicio', 0.4) * 1000)}:all=1[voz]")
    voz_wav = None
    cmd_v = cmd + ["-filter_complex", ";".join(fc), "-map", "[voz]", "-ar", "48000", "-ac", "2", os.path.join(WK, "voz.wav")]
    run(cmd_v)
    voz_wav = os.path.join(WK, "voz.wav")
    fim_voz = dur(voz_wav)
    v0, v1 = p.get("musica_sob_voz", 0.12), p.get("musica_depois", 0.45)
    vol = f"{v0}+{v1 - v0:.3f}*clip((t-{fim_voz - 0.2:.3f})/1.0,0,1)"
    mix = os.path.join(WK, "mix.wav")
    run(["ffmpeg", "-y", "-i", voz_wav, "-stream_loop", "-1", "-i", p["musica"], "-filter_complex",
         f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total:.3f},volume='{vol}':eval=frame,"
         f"afade=t=in:d=0.4,afade=t=out:st={total - 1.6:.3f}:d=1.6[m];"
         f"[0:a]apad=whole_dur={total:.3f}[v];[v][m]amix=inputs=2:normalize=0:duration=longest,"
         f"loudnorm=I=-14:TP=-1.5:LRA=11[a]", "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", mix])

    # 4. final
    run(["ffmpeg", "-y", "-i", video, "-i", png, "-i", mix, "-filter_complex",
         f"[0:v][1:v]overlay=0:{p.get('texto_y', 255)},format=yuv420p[v]", "-map", "[v]", "-map", "2:a",
         "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", saida])
    print(f"OK {saida} duracao={total:.1f}s voz ate {fim_voz:.1f}s")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
