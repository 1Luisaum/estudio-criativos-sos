"""Copia da edicao do anuncio 1428626718623984 da Causas do Bem (Kaue), pedida pelo usuario em 26/10/2026.

- gancho: a mae falando para a camera (selfie com a crianca), com o proprio audio, em jump cuts;
- depois: a voz da crianca (e o "que Deus abencoe" da mae) por cima de b-roll curto, e no fim so musica;
- o video todo: caixa vermelha parada com 3 linhas brancas e, embaixo, a chamada em branco com contorno.

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
VERMELHO = (226, 18, 28)
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS)]
VOZ = "highpass=f=80,afftdn=nf=-25"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(r.stderr[-2500:])
        sys.exit("ffmpeg falhou")
    return r


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout)


def fonte(size, var="Bold Condensed"):
    f = ImageFont.truetype(F + "bahnschrift.ttf", size)
    f.set_variation_by_name(var)
    return f


def emoji_split(s):
    """[(texto, eh_emoji)]"""
    out, cur, emo = [], "", None
    for ch in s:
        e = ord(ch) >= 0x1F000 or 0x2600 <= ord(ch) <= 0x27BF
        if emo is None or e == emo:
            cur += ch
        else:
            out.append((cur, emo)); cur = ch
        emo = e
    if cur:
        out.append((cur, emo))
    return out


def largura(d, s, f, fe):
    return sum(d.textlength(t, font=fe if e else f) for t, e in emoji_split(s))


def escreve(d, x, y, s, f, fe, **kw):
    for t, e in emoji_split(s):
        if e:
            d.text((x, y + f.size * 0.05), t, font=fe, embedded_color=True)
            x += d.textlength(t, font=fe)
        else:
            d.text((x, y), t, font=f, **kw)
            x += d.textlength(t, font=f)


def caixa_png(linhas, cta, path, size=46):
    """Caixa vermelha unica com as linhas brancas centralizadas; embaixo a chamada branca com contorno preto."""
    f, fe = fonte(size), ImageFont.truetype(F + "seguiemj.ttf", int(size * 0.8))
    fc, fce = fonte(46, "Bold"), ImageFont.truetype(F + "seguiemj.ttf", 38)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = max(largura(tmp, ln, f, fe) for ln in linhas)
    lh = int(size * 1.1)
    bw, bh = int(tw + 40), lh * len(linhas) + 16
    im = Image.new("RGBA", (W, bh + 90), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0 = (W - bw) // 2
    d.rectangle([x0, 0, x0 + bw, bh], fill=VERMELHO)
    for i, ln in enumerate(linhas):
        escreve(d, (W - largura(d, ln, f, fe)) / 2, 6 + i * lh, ln, f, fe, fill="white")
    if cta:
        escreve(d, (W - largura(d, cta, fc, fce)) / 2, bh + 16, cta, fc, fce, fill="white",
                stroke_width=4, stroke_fill="black")
    im.save(path)
    return im.height


def cena(WK, i, c, d):
    foto = c["src"].lower().endswith((".jpg", ".jpeg", ".png"))
    nf = round(d * FPS)
    vf = (f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
          f"zoompan=z='1+0.06*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}"
          if foto else f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}")
    inp = (["-loop", "1", "-framerate", str(FPS), "-t", f"{d + 0.2:.3f}", "-i", c["src"]] if foto
           else ["-ss", f"{c['start']:.3f}", "-t", f"{d + 0.2:.3f}", "-an", "-i", c["src"]])
    out = os.path.join(WK, f"b{i:02d}.mp4")
    # format=yuv420p: a foto .jpg vem em yuvj420p (faixa cheia) e a juncao com o gancho parava ali (27/10/2026)
    run(["ffmpeg", "-y"] + inp + ["-vf", vf + f",setsar=1,format=yuv420p,trim=duration={d:.3f}", "-an", *ENC, out])
    return out


def main():
    pp = os.path.abspath(sys.argv[1])
    P = os.path.dirname(pp)
    p = json.load(open(pp, encoding="utf-8"))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
    import comum as C
    saida = C.destino(pp, p, p.get("pasta_saida", "MÃE DESESPERADA"))
    WK = os.path.join(P, "render")
    os.makedirs(WK, exist_ok=True)

    # 1. gancho: a mae falando, video e audio do mesmo trecho (a boca bate com a voz)
    partes, audios, t = [], [], 0.0
    for i, (a, b) in enumerate(p["gancho"]["cortes"]):
        d = round((b - a) * FPS) / FPS
        v = os.path.join(WK, f"g{i:02d}.mkv")
        zoom = p["gancho"].get("zooms", [1.0])[i % len(p["gancho"].get("zooms", [1.0]))]
        crop = f",crop=iw/{zoom}:ih/{zoom}" if zoom != 1.0 else ""
        run(["ffmpeg", "-y", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", p["gancho"]["fonte"], "-filter_complex",
             f"[0:v]fps={FPS}{crop},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1[v];"
             f"[0:a]aresample=48000,aformat=channel_layouts=mono,{VOZ},afade=t=in:d=0.015,afade=t=out:st={d - 0.03:.3f}:d=0.03[a]",
             "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
             "-r", str(FPS), "-c:a", "pcm_s16le", v])
        partes.append(v); t += d
    fim_gancho = t

    # 2. voz por cima do b-roll (falas reais coladas, com respiro curto)
    cmd, fc, lab = ["ffmpeg", "-y"], [], ""
    for i, f in enumerate(p["voz_off"]):
        a, b = f["corte"]
        cmd += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", f["fonte"]]
        fc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=mono,{VOZ},afade=t=in:d=0.02,"
                  f"afade=t=out:st={b - a - 0.04:.3f}:d=0.04,apad=pad_dur={f.get('respiro', 0.12)}[f{i}]")
        lab += f"[f{i}]"
    off = os.path.join(WK, "off.wav")
    run(cmd + ["-filter_complex", ";".join(fc) + f";{lab}concat=n={len(p['voz_off'])}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=7[o]",
               "-map", "[o]", "-ar", "48000", "-ac", "1", off])

    # 3. b-roll ate o fim
    broll = [cena(WK, i, c, c["dur"]) for i, c in enumerate(p["cenas"])]
    bvid = os.path.join(WK, "broll.mp4")
    # junta recodificando: com "-c copy", cena de foto (zoompan) e cena de video tinham escalas de tempo diferentes
    ins = sum([["-i", x] for x in broll], [])
    run(["ffmpeg", "-y"] + ins + ["-filter_complex", "".join(f"[{i}:v]" for i in range(len(broll))) +
                                  f"concat=n={len(broll)}:v=1:a=0[v]", "-map", "[v]", *ENC, bvid])

    # gancho (com som) + b-roll (sem som) num video so
    glst = os.path.join(WK, "lista_g.txt")
    open(glst, "w", encoding="utf-8").writelines(f"file '{x}'\n" for x in partes)
    gvid = os.path.join(WK, "gancho.mkv")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", glst, "-c", "copy", gvid])
    video = os.path.join(WK, "video.mp4")
    run(["ffmpeg", "-y", "-i", gvid, "-i", bvid, "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]",
         "-map", "[v]", *ENC, video])
    total = dur(video)

    # 4. audio: voz da mae (gancho) + voz em off + musica que sobe no fim
    off_d = dur(off)
    ini_off = fim_gancho + p.get("pausa_off", 0.15)
    v0, v1 = p.get("musica_sob_voz", 0.10), p.get("musica_depois", 0.40)
    sobe = ini_off + off_d
    vol = f"{v0}+{v1 - v0:.3f}*clip((t-{sobe - 0.2:.3f})/1.0,0,1)"
    mix = os.path.join(WK, "mix.wav")
    run(["ffmpeg", "-y", "-i", gvid, "-i", off, "-stream_loop", "-1", "-i", p["musica"], "-filter_complex",
         f"[0:a]loudnorm=I=-16:TP=-1.5:LRA=7,aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={total:.3f}[g];"
         f"[1:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(ini_off * 1000)}:all=1,apad=whole_dur={total:.3f}[o];"
         f"[2:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total:.3f},volume='{vol}':eval=frame,"
         f"afade=t=in:d=0.4,afade=t=out:st={total - 1.6:.3f}:d=1.6[m];"
         f"[g][o][m]amix=inputs=3:normalize=0:duration=longest,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
         "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", mix])

    # 5. caixa parada o video todo
    png = os.path.join(WK, "caixa.png")
    caixa_png(p["caixa"], p.get("cta", ""), png)
    run(["ffmpeg", "-y", "-i", video, "-i", png, "-i", mix, "-filter_complex",
         f"[0:v][1:v]overlay=0:{p.get('caixa_y', 1344)},format=yuv420p[v]", "-map", "[v]", "-map", "2:a",
         "-t", f"{total:.3f}", *enc_antes_da_logo(), "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", saida])
    json.dump({"total": total, "fim_gancho": fim_gancho, "off": [ini_off, ini_off + off_d]},
              open(os.path.join(P, "linha_do_tempo.json"), "w", encoding="utf-8"), indent=1)
    import marca  # logo SOS andando pela tela, opacidade baixa (26/10/2026)
    marca.no_fim(p, saida)
    print(f"OK {saida} duracao={total:.1f}s gancho ate {fim_gancho:.1f}s voz em off {ini_off:.1f}-{ini_off + off_d:.1f}s")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
