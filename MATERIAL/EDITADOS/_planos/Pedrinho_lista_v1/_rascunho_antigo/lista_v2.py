"""Versao 2 do estilo "A lista", modelada nos criativos de doacao mais escalados da Biblioteca
(Florisbela 96x, Ampara Brasil 57x, Lar Leao de Juda 40x, UniAngola 22x):
video cru em tela cheia, texto nativo de TikTok (frase fixa no topo em caixa amarela,
legenda curta palavra a palavra com contorno, etiqueta branca de R$ 5), cortes curtos,
sem moldura e sem filtro. Nenhum texto pode ficar em cima de rosto: cada elemento
escolhe a posicao livre a partir da deteccao de rostos de cada cena.

Uso: python lista_v2.py   (reaproveita os audios de lista.py; audio_br tem prioridade)
"""
import json
import os
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

import lista as L  # caminhos, audios (apath/make_audio), dur(), run()

P, BANK, RAW = L.P, L.BANK, L.RAW
OUT = L.ROOT + "/EDITADOS/Pedrinho_lista_v2.mp4"
W, H, FPS = 1080, 1920, 30
F = "C:/Windows/Fonts/"
BOLD, BLACK, EMOJI = F + "segoeuib.ttf", F + "seguibl.ttf", F + "seguiemj.ttf"
YEL = (255, 214, 0)

# Chamada fixa (base real: o Pedrinho pede "seja um anjo na minha vida"; doacoes compram os curativos)
HEADLINE = ["SEJA O ANJO DO PEDRINHO 👼", "DOE R$ 10 PRO CURATIVO DELE 💔"]
OLD_HEADLINE = "A LISTA DO PEDRINHO ESTÁ ACABANDO 💔"  # so para manter o resto do layout igual
# Zona segura do Reels/TikTok/Stories: fora dos 14% de cima e dos 35% de baixo, longe das bordas
SAFE_TOP, SAFE_BOTTOM, SAFE_W = 290, 1250, 860
PIP_K = 0.66  # tamanho do video nos closes em que o rosto ocupa a zona segura
PILL = "R$ 5 já ajuda ❤️"
KEY = {"ATADURA", "GAZE", "POMADA", "SORO", "FISIOLÓGICO", "ESPARADRAPO", "IMPERMEÁVEL", "ÓLEO",
       "GIRASSOL", "DUAS", "VEZES", "CINCO", "HORAS", "BOLHAS", "SANGUE", "ACABANDO", "DORMIR",
       "DOIS", "REAIS", "DOAR", "AGORA", "PELE", "BORBOLETA", "EPIDERMÓLISE", "BOLHOSA"}
os.makedirs(P + "/v2", exist_ok=True)


# ---------- texto com emoji ----------
def is_emoji(ch):
    o = ord(ch)
    return o >= 0x1F000 or 0x2600 <= o <= 0x27BF or o == 0xFE0F


def runs(text):
    out, cur, emo = [], "", None
    for ch in text:
        e = is_emoji(ch)
        if emo is None or e == emo:
            cur += ch
        else:
            out.append((cur, emo))
            cur = ch
        emo = e
    if cur:
        out.append((cur, emo))
    return out


def text_w(d, text, f, fe):
    return sum(d.textlength(t, font=fe if e else f) for t, e in runs(text))


def draw_text(d, x, y, text, f, fe, fill, stroke=0, stroke_fill="black"):
    for t, e in runs(text):
        if e:
            d.text((x, y + f.size * 0.08), t, font=fe, embedded_color=True)
            x += d.textlength(t, font=fe)
        else:
            d.text((x, y), t, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
            x += d.textlength(t, font=f)


def wrap(d, text, f, fe, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if text_w(d, t, f, fe) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


# ---------- elementos (cada um devolve imagem RGBA recortada + altura) ----------
def headline_img(text, maxw=900):
    """Caixa amarela com texto preto, como o texto nativo do TikTok.
    text pode ser uma lista de linhas (fonte diminui ate caber em maxw)."""
    size = 60
    f, fe = ImageFont.truetype(BOLD, size), ImageFont.truetype(EMOJI, int(size * 0.83))
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    if isinstance(text, list):
        lines = text
        while max(text_w(tmp, ln, f, fe) for ln in lines) > maxw:
            size -= 2
            f, fe = ImageFont.truetype(BOLD, size), ImageFont.truetype(EMOJI, int(size * 0.83))
    else:
        lines = wrap(tmp, text, f, fe, maxw)
    lh = int(size * 1.34)
    im = Image.new("RGBA", (W, lh * len(lines) + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        tw = text_w(d, ln, f, fe)
        x0 = (W - tw) / 2
        d.rounded_rectangle([x0 - 22, i * lh + 4, x0 + tw + 22, i * lh + lh + 8], radius=14, fill=YEL)
    for i, ln in enumerate(lines):
        tw = text_w(d, ln, f, fe)
        draw_text(d, (W - tw) / 2, i * lh + 6 * size / 60, ln, f, fe, "black")
    return im


def pill_img(text):
    """Etiqueta branca com texto preto (como a da Ampara Brasil)."""
    f, fe = ImageFont.truetype(BOLD, 54), ImageFont.truetype(EMOJI, 44)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = text_w(tmp, text, f, fe)
    im = Image.new("RGBA", (W, 100), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0 = (W - tw) / 2
    d.rounded_rectangle([x0 - 30, 6, x0 + tw + 30, 94], radius=44, fill=(255, 255, 255, 245))
    draw_text(d, x0, 14, text, f, fe, "black")
    return im


def caption_img(words, size=84):
    """Legenda curta: branco com contorno preto, palavra-chave em amarelo."""
    f = ImageFont.truetype(BLACK, size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    text = " ".join(words)
    lines = [text] if tmp.textlength(text, font=f) <= 960 else [" ".join(words[:len(words) // 2]),
                                                                 " ".join(words[len(words) // 2:])]
    lh = size + 18
    im = Image.new("RGBA", (W, lh * len(lines) + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        x = (W - d.textlength(ln, font=f)) / 2
        for w in ln.split():
            clean = w.strip(".,:!?…").upper()
            w = w.rstrip(".,:")
            d.text((x, 10 + i * lh), w, font=f, fill=YEL if clean in KEY else "white",
                   stroke_width=9, stroke_fill="black")
            x += d.textlength(w + " ", font=f)
    return im


# ---------- rostos ----------
def faces(src, start, length, tag):
    """Caixas de rosto (x0,y0,x1,y1) no quadro final 1080x1920, com margem.
    So conta rosto confirmado em pelo menos 2 dos 5 momentos da cena (evita falso positivo)."""
    import cv2
    import numpy as np
    cas = [cv2.CascadeClassifier(cv2.data.haarcascades + n) for n in
           ("haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt2.xml")]
    prof = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
    per = []
    for k in range(5):
        t = start + length * (k + 0.5) / 5
        png = f"{P}/v2/face_{tag}_{k}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1",
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", png])
        if not os.path.exists(png):
            continue
        g = cv2.imdecode(np.fromfile(png, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
        found = []
        for cc in cas:
            found += [tuple(b) for b in cc.detectMultiScale(g, 1.1, 6, minSize=(55, 55))]
        found += [tuple(b) for b in prof.detectMultiScale(g, 1.1, 9, minSize=(70, 70))]
        per.append(found)

    def iou(a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        ix = max(0, min(ax + aw, bx + bw) - max(ax, bx))
        iy = max(0, min(ay + ah, by + bh) - max(ay, by))
        inter = ix * iy
        return inter / float(aw * ah + bw * bh - inter + 1e-6)

    boxes = []
    for i, found in enumerate(per):
        for b in found:
            seen = sum(1 for j, other in enumerate(per) if j != i and any(iou(b, o) > 0.2 for o in other))
            if seen >= 1:
                x, y, w, h = b
                boxes.append((x - w * 0.25, y - h * 0.45, x + w * 1.25, y + h * 1.35))
    return boxes


def place(height, cands, busy):
    """Primeira posicao vertical candidata que nao bate em rosto nem em outro texto."""
    best, best_hit = cands[0], None
    for y in cands:
        hit = sum(max(0, min(y + height, b[3]) - max(y, b[1])) for b in busy)
        if hit == 0:
            return y
        if best_hit is None or hit < best_hit:
            best, best_hit = y, hit
    return best


# ---------- render ----------
ENC = L.ENC


# Areas protegidas marcadas a mao (rostos pequenos que o detector nao pega).
# chave: (nome do arquivo, inicio do trecho) -> caixas no quadro final 1080x1920
MANUAL = {
    ("Roteiro_ esse calor tá acabando com a pele do meu filho.mp4", 6.0): [(660, 960, 1080, 1400)],
    ("Roteiro_ esse calor tá acabando com a pele do meu filho.mp4", 20.0): [(660, 960, 1080, 1400)],
}


def hits(y, h, boxes):
    return sum(max(0, min(y + h, b[3]) - max(y, b[1])) for b in boxes)


def layout(busy, hl_h, pl_h, show_pill, cap_h=230):
    """Escolhe topo / etiqueta / legenda sem tocar rosto nem um ao outro."""
    hl_c = list(range(200, 460, 40)) + list(range(1700, 1300, -40))
    cap_c = sorted(range(420, 1720, 40), key=lambda y: abs(y - 1180))
    pl_c = list(range(1720, 1380, -40)) + list(range(380, 700, 40))
    for with_pill in ([True, False] if show_pill else [False]):
        taken = list(busy)
        y_hl = place(hl_h, hl_c, taken)
        taken.append((0, y_hl, W, y_hl + hl_h))
        y_pl = None
        if with_pill:
            y_pl = place(pl_h, pl_c, taken)
            taken.append((0, y_pl, W, y_pl + pl_h))
        y_cap = place(cap_h, cap_c, taken)
        if hits(y_cap, cap_h, taken) == 0:
            break
    return y_hl, y_pl, y_cap, hits(y_hl, hl_h, busy) + hits(y_cap, cap_h, busy)


def render(seg, shots, words_t, out, card=None, end=False, show_pill=True):
    """Video em tela cheia (ou foto inteira com fundo desfocado) + textos nativos.
    A posicao dos textos e escolhida cena por cena, longe dos rostos."""
    d = seg["d"]
    hl_old = headline_img("AJUDE A COMPLETAR A LISTA DO PEDRINHO 🙏" if end else OLD_HEADLINE)
    hl = headline_img(HEADLINE, SAFE_W)
    pl = pill_img("👇 Toque em DOAR AGORA" if end else PILL)
    cmd, fc = ["ffmpeg", "-y"], []
    windows = []  # (t0, t1, busy)
    if card:
        img = Image.open(card).convert("RGB")
        ph = int(img.height * W / img.width)
        top_photo = (H - ph) // 2 + (60 if end else 0)
        bg = L.cover(img, W, H).filter(ImageFilter.GaussianBlur(40))
        bg = Image.blend(bg, Image.new("RGB", (W, H)), 0.35)
        bg.paste(img.resize((W, ph), Image.LANCZOS), (0, top_photo))
        bg.save(f"{P}/v2/{seg['name']}_card.png")
        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", f"{P}/v2/{seg['name']}_card.png"]
        fc.append(f"[0:v]{L.push(d, 0.03)}[bg]")
        windows.append([0.0, d, [(0, top_photo, W, top_photo + ph)], 0])
        n_in = 1
    else:
        each = d / len(shots)
        labels = []
        for i, (src, st) in enumerate(shots):
            fb = faces(src, st, each, f"{seg['name']}_{i}") + MANUAL.get((os.path.basename(src), st), [])
            windows.append([i * each, (i + 1) * each, fb, 0])
        n_in = len(shots)

    # posicoes: resto igual ao aprovado; a chamada sempre na zona segura e longe de rosto.
    # Se o rosto ocupa a zona segura (close), o video desce e o topo vira a propria imagem desfocada.
    plans = []
    for win in windows:
        busy = win[2]
        shift = 0  # 0 = tela cheia; 1 = close reduzido e encaixado abaixo da chamada
        for attempt in range(2):
            if shift:
                k, ox, oy = PIP_K, (W - int(W * PIP_K)) // 2, SAFE_TOP + hl.height + 30
                moved = [(x0 * k + ox, y0 * k + oy, x1 * k + ox, y1 * k + oy) for (x0, y0, x1, y1) in busy]
            else:
                moved = list(busy)
            _, y_pl, y_cap, _ = layout(moved, hl_old.height, pl.height, show_pill)
            taken = moved + [(0, y_cap, W, y_cap + 230)]
            if y_pl is not None:
                taken.append((0, y_pl, W, y_pl + pl.height))
            y_hl = place(hl.height, list(range(SAFE_TOP, SAFE_BOTTOM - hl.height + 1, 10)), taken)
            bad = hits(y_hl, hl.height, taken)
            if bad == 0 or card or attempt == 1:
                break
            shift = 1
        win[3] = shift
        plans.append((y_hl, y_pl, y_cap, bad))
        print(f"  {seg['name']}: chamada={y_hl}-{y_hl + hl.height} legenda={y_cap} "
              f"etiqueta={y_pl} desce_video={shift} sobreposicao={bad:.0f}")
    if not card:
        labels = []
        for i, (src, st) in enumerate(shots):
            sh = windows[i][3]
            cmd += ["-ss", f"{st:.2f}", "-t", f"{each + 0.1:.3f}", "-i", src]
            chain = (f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                     f"{L.push(each, 0.03)},trim=duration={each:.3f},setpts=PTS-STARTPTS")
            if sh:
                pw, ph_ = int(W * PIP_K) // 2 * 2, int(H * PIP_K) // 2 * 2
                fc.append(chain + f",split[f{i}][g{i}]")
                fc.append(f"[g{i}]gblur=sigma=40,eq=brightness=-0.15[gb{i}]")
                fc.append(f"[f{i}]scale={pw}:{ph_}[fs{i}]")
                fc.append(f"[gb{i}][fs{i}]overlay={(W - pw) // 2}:{SAFE_TOP + hl.height + 30}[b{i}]")
            else:
                fc.append(chain + f"[b{i}]")
            labels.append(f"[b{i}]")
        fc.append("".join(labels) + f"concat=n={len(shots)}:v=1:a=0[bg]")

    last, k = "[bg]", n_in
    for wi, ((t0, t1, _, _), (y_hl, y_pl, y_cap, bad)) in enumerate(zip(windows, plans)):
        base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        base.alpha_composite(hl, (0, y_hl))
        if y_pl is not None:
            base.alpha_composite(pl, (0, y_pl))
        png = f"{P}/v2/{seg['name']}_base{wi}.png"
        base.save(png)
        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", png]
        fc.append(f"{last}[{k}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[o{k}]")
        last, k = f"[o{k}]", k + 1
        for j, (a, b, ws) in enumerate(words_t):
            a2, b2 = max(a, t0), min(b, t1)
            if b2 - a2 < 0.02:
                continue
            cp = f"{P}/v2/{seg['name']}_c{j}.png"
            if not os.path.exists(cp) or wi == 0:
                caption_img(ws).save(cp)
            cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", cp]
            fc.append(f"{last}[{k}:v]overlay=0:{y_cap}:enable='between(t,{a2:.3f},{b2:.3f})'[o{k}]")
            last, k = f"[o{k}]", k + 1
    L.run(cmd + ["-filter_complex", ";".join(fc), "-map", last, "-an", *ENC, out])


def chunks(text, t0, t1, size=3):
    """Divide a fala em blocos de ate 3 palavras, com tempo proporcional ao tamanho."""
    words = text.replace("...", "…").split()
    groups = [words[i:i + size] for i in range(0, len(words), size)]
    weights = [sum(len(w) + 2 for w in g) for g in groups]
    tot, out, t = sum(weights), [], t0
    for g, wt in zip(groups, weights):
        dt = (t1 - t0) * wt / tot
        out.append((t, t + dt, [w.upper() for w in g]))
        t += dt
    return out


def main():
    L.make_audio()
    N = L.ROT["narracao"]
    A = {k: L.dur(L.apath(k)) for k in N}
    BED = BANK + "/Vídeo Mostrando itens de curativos em cima da Cama  e  Finalizando os Curativos_.mp4"
    CINCO = RAW + "/20260916_234157.mp4"
    DORMIR = RAW + "/Roteiro_ Eu não aguento mais não conseguir dormir.mp4"
    CALOR = RAW + "/Roteiro_ esse calor tá acabando com a pele do meu filho.mp4"
    ACAB = RAW + "/Roteiro_ os meus curativos estão acabando e eu tô com medo seja um anjo na minha vida.mp4"
    plan = [  # nome, fala, pausa depois, b-roll | foto
        ("s01", "N01", 0.35, [(ACAB, 0.2), (BED, 205.0)], None),
        ("i1", "I1", 0.25, None, BANK + "/crepe bandagem.png"),
        ("i2", "I2", 0.25, None, BANK + "/GAZE.png"),
        ("i3", "I3", 0.25, None, BANK + "/Pomada.png"),
        ("i4", "I4", 0.25, None, BANK + "/soro fisiológico.png"),
        ("i5", "I5", 0.25, None, BANK + "/esparadrapo impermeável.png"),
        ("i6", "I6", 0.25, None, BANK + "/OLeo de girassol.png"),
        ("s03", "N03", 0.4, None, BANK + "/Curativos 2 x ao Dia.png"),
        ("s04", "N04", 0.35, [(BED, 160.0), (BED, 232.0), (BED, 290.0)], None),
        ("s05", "N05", 0.4, [(CINCO, 27.5), (CINCO, 40.0)], None),
        ("s06", "N06", 0.35, [(CALOR, 6.0), (DORMIR, 4.0)], None),
        ("s07", "N07", 0.5, [(ACAB, 9.0), (BED, 300.0)], None),
        ("s08", "N08", 0.35, [(CALOR, 20.0), (BED, 250.0)], None),
        ("s09", "N09", 1.6, None, BANK + "/Ana e Pedro sorrindo.png"),
    ]
    segs = []
    for name, key, pad, shots, card in plan:
        seg = {"name": name, "key": key, "d": A[key] + pad, "fx": None, "fx_at": 0.0}
        speech_end = max(0.4, A[key] - 0.1)
        words_t = chunks(N[key], 0.12, 0.12 + speech_end)
        render(seg, shots, words_t, f"{P}/v2/{name}.mp4", card=card, end=(name == "s09"),
               show_pill=name in ("s07", "s08", "s09"))
        segs.append(seg)
        print("ok", name)

    with open(P + "/v2/lista.txt", "w", encoding="utf-8") as f:
        for s in segs:
            f.write(f"file '{P}/v2/{s['name']}.mp4'\n")
    L.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", P + "/v2/lista.txt", "-c", "copy",
           P + "/v2/video.mp4"])

    cmd, parts, t = ["ffmpeg", "-y"], [], 0.0
    for i, s in enumerate(segs):
        cmd += ["-i", L.apath(s["key"])]
        parts.append(f"[{i}:a]adelay={int((t + 0.12) * 1000)}:all=1[a{i}]")
        t += s["d"]
    total, n = t, len(segs)
    cmd += ["-stream_loop", "-1", "-i", L.MUSIC]
    parts.append(f"[{n}:a]atrim=0:{total:.3f},volume=0.12,afade=t=out:st={total - 1.8:.3f}:d=1.8[m]")
    parts.append("".join(f"[a{i}]" for i in range(n)) +
                 f"[m]amix=inputs={n + 1}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    L.run(cmd + ["-filter_complex", ";".join(parts), "-map", "[aout]", "-t", f"{total:.3f}",
                 "-c:a", "pcm_s16le", P + "/v2/audio.wav"])
    L.run(["ffmpeg", "-y", "-i", P + "/v2/video.mp4", "-i", P + "/v2/audio.wav", "-map", "0:v",
           "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
           "-movflags", "+faststart", OUT])
    json.dump({"total": total, "segs": segs}, open(P + "/v2/linha_do_tempo.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"OK {OUT} ({total:.1f}s)")


if __name__ == "__main__":
    main()
