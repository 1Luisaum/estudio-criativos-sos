"""Estilo "A LISTA": monta o criativo so com narracao do ElevenLabs + b-roll.

Uso: python lista.py            (gera audios que faltam e renderiza)
A chave do ElevenLabs vem da variavel de ambiente ELEVENLABS_API_KEY.
"""
import json
import math
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = "C:/Users/EDITING_SECTOR/Desktop/EDIÇÃO COM CLAUDE"
BANK = ROOT + "/banco de vídeos do pedrinho"
RAW = ROOT + "/VÍDEOS PARA EDITAR"
P = ROOT + "/EDITADOS/_planos/Pedrinho_lista_v1"
OUT = ROOT + "/EDITADOS/Pedrinho_lista_v1.mp4"
MUSIC = ROOT + "/MÚSICAS/alex-morgan-sad-piano-emotional-rain-story-575883.mp3"
W, H, FPS = 1080, 1920, 30

F = "C:/Windows/Fonts/"
HAND, HAND_B = F + "segoepr.ttf", F + "segoeprb.ttf"
ARIAL_B, IMPACT, BLACK = F + "arialbd.ttf", F + "impact.ttf", F + "seguibl.ttf"
INK, RED, PAPER = (24, 46, 122), (214, 38, 46), (255, 249, 232)

ITEMS = ["Atadura", "Gaze", "Pomada", "Soro fisiológico", "Esparadrapo impermeável", "Óleo de girassol"]
ITEM_IMG = ["crepe bandagem.png", "GAZE.png", "Pomada.png", "soro fisiológico.png",
            "esparadrapo impermeável.png", "OLeo de girassol.png"]

ROT = json.load(open(P + "/roteiro.json", encoding="utf-8"))
os.makedirs(P + "/audio", exist_ok=True)
os.makedirs(P + "/ov", exist_ok=True)
os.makedirs(P + "/seg", exist_ok=True)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stderr[-2500:])
        sys.exit("ffmpeg falhou: " + " ".join(cmd[:6]))


def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip())


# ---------- audio (ElevenLabs) ----------
def apath(k):
    """Usa o audio da pasta audio_br (narrador brasileiro gerado no site) quando existir."""
    br = f"{P}/audio_br/{k}.mp3"
    return br if os.path.exists(br) else f"{P}/audio/{k}.mp3"


def make_audio():
    need = [k for k in ROT["narracao"] if not os.path.exists(apath(k))]
    need_fx = [k for k in ROT["efeitos"] if not os.path.exists(f"{P}/audio/fx_{k}.mp3")]
    if not need and not need_fx:
        return
    from elevenlabs import VoiceSettings
    from elevenlabs.client import ElevenLabs
    c = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    for k in need:
        audio = c.text_to_speech.convert(
            voice_id=ROT["voice_id"], model_id="eleven_multilingual_v2",
            text=ROT["narracao"][k], output_format="mp3_44100_128",
            voice_settings=VoiceSettings(stability=0.55, similarity_boost=0.75, style=0.25,
                                         use_speaker_boost=True))
        with open(f"{P}/audio/{k}.mp3", "wb") as f:
            for ch in audio:
                f.write(ch)
        print("narracao", k)
    for k in need_fx:
        fx = ROT["efeitos"][k]
        audio = c.text_to_sound_effects.convert(text=fx["text"], duration_seconds=fx["dur"])
        with open(f"{P}/audio/fx_{k}.mp3", "wb") as f:
            for ch in audio:
                f.write(ch)
        print("efeito", k)


# ---------- desenho (Pillow) ----------
def font(path, size):
    return ImageFont.truetype(path, size)


def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def blur_bg(path):
    img = cover(Image.open(path).convert("RGB"), W, H)
    img = img.filter(ImageFilter.GaussianBlur(38))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.blend(img, dark, 0.45).convert("RGBA")


def shadowed(layer, angle, blur=18, alpha=150):
    """Gira a camada e devolve (imagem com sombra, deslocamento)."""
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    pad = blur * 3
    sh = Image.new("RGBA", (layer.width + pad * 2, layer.height + pad * 2), (0, 0, 0, 0))
    mask = layer.split()[3].point(lambda a: alpha if a > 0 else 0)
    sh.paste((0, 0, 0, 255), (pad + 8, pad + 14), mask)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    sh.alpha_composite(layer, (pad, pad))
    return sh, pad


def polaroid(path, width, border=18):
    img = Image.open(path).convert("RGB")
    h = int(img.height * width / img.width)
    img = img.resize((width, h), Image.LANCZOS)
    card = Image.new("RGBA", (width + border * 2, h + border * 2), (255, 255, 255, 255))
    card.paste(img, (border, border))
    return card


def note(n_items, highlight=None, extra_2x=False, width=920):
    lh, top = 92, 150
    h = top + lh * len(ITEMS) + 60
    im = Image.new("RGBA", (width, h), PAPER + (255,))
    d = ImageDraw.Draw(im)
    for i in range(len(ITEMS) + 1):
        y = top - 18 + i * lh
        d.line([(30, y), (width - 30, y)], fill=(170, 196, 230, 255), width=2)
    d.line([(110, 0), (110, h)], fill=(232, 120, 120, 255), width=3)
    d.text((140, 30), "Lista do Pedrinho", font=font(HAND_B, 66), fill=INK)
    for i in range(n_items):
        y = top + i * lh
        d.rounded_rectangle([140, y + 14, 182, y + 56], radius=6, outline=INK, width=4)
        size = 54
        f = font(HAND_B if i == highlight else HAND, size)
        while d.textlength(ITEMS[i], font=f) > width - 245:
            size -= 2
            f = font(HAND_B if i == highlight else HAND, size)
        d.text((205, y - 6 + (54 - size) // 2), ITEMS[i], font=f, fill=INK)
        if i == highlight:
            tw = d.textlength(ITEMS[i], font=f)
            d.line([(205, y + 66), (205 + tw, y + 62)], fill=RED, width=6)
    if extra_2x:
        f = font(HAND_B, 92)
        cx, cy = width - 170, top + 20
        d.text((cx - 120, cy - 60), "2x", font=f, fill=RED)
        d.text((cx - 150, cy + 50), "ao dia!", font=font(HAND_B, 56), fill=RED)
        d.ellipse([cx - 190, cy - 80, cx + 150, cy + 150], outline=RED, width=7)
    return im


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def caption(canvas, text, y=1420, size=66):
    d = ImageDraw.Draw(canvas)
    f = font(ARIAL_B, size)
    lines = wrap(d, text, f, 920)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        d.text(((W - tw) / 2, y + i * (size + 14)), ln, font=f, fill="white",
               stroke_width=7, stroke_fill="black")


def sticky(text1, text2, angle=5, color=(255, 226, 92)):
    im = Image.new("RGBA", (470, 330), color + (255,))
    d = ImageDraw.Draw(im)
    size = 112
    f1, f2 = font(HAND_B, size), font(HAND_B, 50)
    while d.textlength(text1, font=f1) > 420:
        size -= 4
        f1 = font(HAND_B, size)
    d.text(((470 - d.textlength(text1, font=f1)) / 2, 40 + (112 - size) // 2), text1, font=f1, fill=INK)
    d.text(((470 - d.textlength(text2, font=f2)) / 2, 200), text2, font=f2, fill=INK)
    return shadowed(im, angle, blur=12, alpha=120)


def stamp(text="ACABANDO"):
    f = font(IMPACT, 170)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = int(tmp.textlength(text, font=f))
    im = Image.new("RGBA", (tw + 100, 260), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([8, 8, tw + 92, 252], radius=24, outline=RED + (235,), width=14)
    d.text((50, 22), text, font=f, fill=RED + (235,))
    return im.rotate(-12, resample=Image.BICUBIC, expand=True)


def frame_list(card_path, n_items, highlight=None, extra_2x=False, card_angle=-2.0):
    cv = blur_bg(card_path)
    card, pad = shadowed(polaroid(card_path, 900), card_angle)
    cv.alpha_composite(card, ((W - card.width) // 2, 120 - pad))
    nt, pad = shadowed(note(n_items, highlight, extra_2x), 1.5)
    cv.alpha_composite(nt, ((W - nt.width) // 2, 900 - pad))
    return cv


def overlay_full(text=None, hook=False, sticky_args=None, sticky_y=1020):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if hook:
        im = Image.new("RGBA", (960, 430), PAPER + (255,))
        d = ImageDraw.Draw(im)
        f = font(HAND_B, 70)
        for i, ln in enumerate(wrap(d, text, f, 880)):
            d.text((40, 30 + i * 96), ln, font=f, fill=INK)
        d.line([(40, 400), (600, 396)], fill=RED, width=7)
        sh, pad = shadowed(im, -2.5)
        ov.alpha_composite(sh, ((W - sh.width) // 2, 170 - pad))
    else:
        d = ImageDraw.Draw(ov)
        d.text((60, 120), "Lista do Pedrinho", font=font(HAND_B, 50), fill="white",
               stroke_width=4, stroke_fill=INK)
        if text:
            caption(ov, text)
    if sticky_args:
        sh, pad = sticky(*sticky_args)
        ov.alpha_composite(sh, (W - sh.width - 30, sticky_y - pad))
    return ov


VH = 1340          # altura da janela de video nos blocos de b-roll
BAND = H - VH      # faixa de papel embaixo, onde ficam todos os textos


def band(text, hook=False, sticky_args=None):
    """Faixa de papel abaixo do video: nenhum texto fica em cima da imagem."""
    im = Image.new("RGBA", (W, BAND), PAPER + (255,))
    d = ImageDraw.Draw(im)
    for y in range(150, BAND, 86):
        d.line([(0, y), (W, y)], fill=(170, 196, 230, 255), width=2)
    d.line([(90, 0), (90, BAND)], fill=(232, 120, 120, 255), width=3)
    d.rectangle([0, 0, W, 10], fill=(0, 0, 0, 90))
    d.text((120, 40), "Lista do Pedrinho", font=font(HAND_B, 46), fill=RED)
    maxw = 500 if sticky_args else 900
    size = 64 if hook else 56
    f = font(HAND_B, size)
    lines = wrap(d, text, f, maxw)
    while len(lines) > 4:
        size -= 4
        f = font(HAND_B, size)
        lines = wrap(d, text, f, maxw)
    for i, ln in enumerate(lines):
        d.text((120, 128 + i * 86 + (86 - size) // 2 - 14), ln, font=f, fill=INK)
    if sticky_args:
        sh, pad = sticky(*sticky_args)
        k = 0.8
        sh = sh.resize((int(sh.width * k), int(sh.height * k)), Image.LANCZOS)
        pad = int(pad * k)
        im.alpha_composite(sh, (W - sh.width + pad - 30, 150 - pad))
    return im


def face_offset(src, start, length, tag):
    """Escolhe o recorte vertical da janela para manter os rostos inteiros dentro dela."""
    import cv2
    cas = [cv2.CascadeClassifier(cv2.data.haarcascades + n) for n in
           ("haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt2.xml",
            "haarcascade_profileface.xml")]
    tops, bots = [], []
    for k in range(5):
        t = start + length * (k + 0.5) / 5
        png = f"{P}/seg/face_{tag}_{k}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1",
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", png])
        if not os.path.exists(png):
            continue
        import numpy as np  # imread nao abre caminhos com acento (EDIÇÃO)
        g = cv2.imdecode(np.fromfile(png, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
        for cc in cas:
            for (x, y, w, h) in cc.detectMultiScale(g, 1.1, 5, minSize=(90, 90)):
                tops.append(y - h * 0.35)
                bots.append(y + h * 1.25)
    print(f"rostos {tag}: {len(tops)}")
    if not tops:
        return 180
    top, bot = min(tops), max(bots)
    if bot - top <= VH:
        oy = (top + bot) / 2 - VH / 2
    else:
        oy = top - 40
    return int(max(0, min(H - VH, oy)))


def frame_end():
    cv = blur_bg(BANK + "/Ana e Pedro sorrindo.png")
    card, pad = shadowed(polaroid(BANK + "/Ana e Pedro sorrindo.png", 900), 2)
    cv.alpha_composite(card, ((W - card.width) // 2, 200 - pad))
    d = ImageDraw.Draw(cv)
    f = font(HAND_B, 78)
    for i, ln in enumerate(["Ajude a completar", "a lista do Pedrinho"]):
        tw = d.textlength(ln, font=f)
        d.text(((W - tw) / 2, 1060 + i * 105), ln, font=f, fill="white",
               stroke_width=5, stroke_fill=INK)
    bw, bh, by = 760, 170, 1420
    d.rounded_rectangle([(W - bw) / 2, by, (W + bw) / 2, by + bh], radius=85, fill=RED)
    fb = font(BLACK, 86)
    t = "DOAR AGORA"
    d.text(((W - d.textlength(t, font=fb)) / 2, by + 26), t, font=fb, fill="white")
    return cv


# ---------- video (FFmpeg) ----------
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS)]
GRADE = "eq=saturation=0.88:contrast=1.05:brightness=-0.015,vignette=PI/5"


def push(d, amount=0.045, h=H):
    return (f"scale=w='trunc({W}*(1+{amount}*t/{d:.3f})/2)*2':h=-2:eval=frame,"
            f"crop={W}:{h},setsar=1,fps={FPS}")


def render_static(png, d, out, stamp_png=None, stamp_at=0.0):
    cmd = ["ffmpeg", "-y", "-loop", "1", "-t", f"{d:.3f}", "-i", png]
    fc = f"[0:v]{push(d, 0.035)}[v]"
    if stamp_png:
        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", stamp_png]
        fc += (f";[1:v]format=rgba,fade=in:st={stamp_at:.2f}:d=0.12:alpha=1[s];"
               f"[v][s]overlay=(W-w)/2:1380-h/2:shortest=1[v2]")
        out_label = "[v2]"
    else:
        out_label = "[v]"
    run(cmd + ["-filter_complex", fc, "-map", out_label, "-an", *ENC, out])


def render_full(shots, d, band_png, out, tag):
    """Video na janela de cima (recorte guiado pelos rostos) + faixa de papel embaixo."""
    cmd, fc, labels = ["ffmpeg", "-y"], [], []
    each = d / len(shots)
    for i, (src, start) in enumerate(shots):
        oy = face_offset(src, start, each, f"{tag}_{i}")
        cmd += ["-ss", f"{start:.2f}", "-t", f"{each + 0.1:.3f}", "-i", src]
        fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                  f"crop={W}:{VH}:0:{oy},{GRADE},{push(each, 0.03, VH)},"
                  f"trim=duration={each:.3f},setpts=PTS-STARTPTS[b{i}]")
        labels.append(f"[b{i}]")
    n = len(shots)
    cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", band_png]
    fc.append("".join(labels) + f"concat=n={n}:v=1:a=0,pad={W}:{H}:0:0:black[bg]")
    fc.append(f"[{n}:v]format=rgba[o]")
    fc.append(f"[bg][o]overlay=0:{VH}:shortest=1[v]")
    run(cmd + ["-filter_complex", ";".join(fc), "-map", "[v]", "-an", *ENC, out])


def main():
    make_audio()
    A = {k: dur(apath(k)) for k in ROT["narracao"]}
    BED = BANK + "/Vídeo Mostrando itens de curativos em cima da Cama  e  Finalizando os Curativos_.mp4"
    CINCO = RAW + "/20260916_234157.mp4"
    DORMIR = RAW + "/Roteiro_ Eu não aguento mais não conseguir dormir.mp4"
    CALOR = RAW + "/Roteiro_ esse calor tá acabando com a pele do meu filho.mp4"
    ACABANDO = RAW + "/Roteiro_ os meus curativos estão acabando e eu tô com medo seja um anjo na minha vida.mp4"

    segs = []  # (nome, audio_key, duracao, fx)
    ov = P + "/ov/"

    def add(name, key, pad, fx=None, fx_at=0.0, extra=0.0):
        segs.append({"name": name, "key": key, "d": A[key] + pad + extra, "fx": fx, "fx_at": fx_at})
        return segs[-1]["d"]

    # 1. gancho
    d = add("s01", "N01", 0.45)
    band(ROT["narracao"]["N01"], hook=True).save(ov + "s01.png")
    render_full([(ACABANDO, 0.2), (BED, 205.0)], d, ov + "s01.png", P + "/seg/s01.mp4", "s01")
    # 2. itens
    for i in range(6):
        d = add(f"i{i + 1}", f"I{i + 1}", 0.3, fx="caneta", fx_at=0.0)
        frame_list(BANK + "/" + ITEM_IMG[i], i + 1, highlight=i,
                   card_angle=-2 if i % 2 == 0 else 2).save(ov + f"i{i + 1}.png")
        render_static(ov + f"i{i + 1}.png", d, P + f"/seg/i{i + 1}.mp4")
    # 3. duas vezes por dia
    d = add("s03", "N03", 0.5, fx="caneta", fx_at=0.9)
    frame_list(BANK + "/Curativos 2 x ao Dia.png", 6, extra_2x=True).save(ov + "s03.png")
    render_static(ov + "s03.png", d, P + "/seg/s03.mp4")
    # 4. a doenca
    d = add("s04", "N04", 0.4)
    band(ROT["narracao"]["N04"]).save(ov + "s04.png")
    render_full([(BED, 160.0), (BED, 232.0), (BED, 290.0)], d, ov + "s04.png", P + "/seg/s04.mp4", "s04")
    # 5. cinco horas
    d = add("s05", "N05", 0.5)
    band(ROT["narracao"]["N05"], sticky_args=("5 horas", "de curativo")).save(ov + "s05.png")
    render_full([(CINCO, 27.5), (CINCO, 40.0)], d, ov + "s05.png", P + "/seg/s05.mp4", "s05")
    # 6. feridas e sono
    d = add("s06", "N06", 0.4)
    band(ROT["narracao"]["N06"]).save(ov + "s06.png")
    render_full([(CALOR, 6.0), (DORMIR, 4.0)], d, ov + "s06.png", P + "/seg/s06.mp4", "s06")
    # 7. acabando
    stamp_at = max(0.3, A["N07"] - 0.9)
    d = add("s07", "N07", 0.7, fx="carimbo", fx_at=stamp_at)
    frame_list(BANK + "/Remédios, Pomadas e Cremes.png", 6).save(ov + "s07.png")
    stamp().save(ov + "stamp.png")
    render_static(ov + "s07.png", d, P + "/seg/s07.mp4", ov + "stamp.png", stamp_at)
    # 8. dois, cinco reais
    d = add("s08", "N08", 0.4)
    band(ROT["narracao"]["N08"], sticky_args=("R$ 2 • R$ 5", "já ajuda demais", -4)).save(ov + "s08.png")
    render_full([(CALOR, 20.0), (BED, 300.0)], d, ov + "s08.png", P + "/seg/s08.mp4", "s08")
    # 9. final
    d = add("s09", "N09", 1.6)
    frame_end().save(ov + "s09.png")
    render_static(ov + "s09.png", d, P + "/seg/s09.mp4")

    # concatena o video
    with open(P + "/seg/lista.txt", "w", encoding="utf-8") as f:
        for s in segs:
            f.write(f"file '{P}/seg/{s['name']}.mp4'\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", P + "/seg/lista.txt", "-c", "copy",
         P + "/seg/video.mp4"])

    # monta o audio: narracao + efeitos + musica
    cmd, parts, t = ["ffmpeg", "-y"], [], 0.0
    idx = 0
    for s in segs:
        cmd += ["-i", apath(s["key"])]
        parts.append(f"[{idx}:a]adelay={int((t + 0.12) * 1000)}:all=1[a{idx}]")
        idx += 1
        if s["fx"]:
            cmd += ["-i", f"{P}/audio/fx_{s['fx']}.mp3"]
            vol = 0.5 if s["fx"] == "caneta" else 0.9
            parts.append(f"[{idx}:a]volume={vol},adelay={int((t + s['fx_at']) * 1000)}:all=1[a{idx}]")
            idx += 1
        t += s["d"]
    total = t
    cmd += ["-stream_loop", "-1", "-i", MUSIC]
    parts.append(f"[{idx}:a]atrim=0:{total:.3f},volume=0.13,afade=t=out:st={total - 1.8:.3f}:d=1.8[m]")
    mix_in = "".join(f"[a{i}]" for i in range(idx)) + "[m]"
    parts.append(f"{mix_in}amix=inputs={idx + 1}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    run(cmd + ["-filter_complex", ";".join(parts), "-map", "[aout]", "-t", f"{total:.3f}",
               "-c:a", "pcm_s16le", P + "/seg/audio.wav"])

    run(["ffmpeg", "-y", "-i", P + "/seg/video.mp4", "-i", P + "/seg/audio.wav",
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest", "-movflags", "+faststart", OUT])
    json.dump({"total": total, "segs": segs}, open(P + "/linha_do_tempo.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"OK {OUT} ({total:.1f}s)")


if __name__ == "__main__":
    main()
