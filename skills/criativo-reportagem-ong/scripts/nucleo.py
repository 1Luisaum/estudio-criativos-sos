"""Monta um criativo no estilo "Lista narrada" (nativo TikTok) a partir de um plano.json.

Uso:  python -I lista.py "<pasta do plano>\\plano.json"

O que sai (igual ao aprovado Pedrinho_lista_v2):
- so narracao do ElevenLabs + b-roll; os brutos entram SEM o audio deles;
- video cru em tela cheia, sem moldura e sem filtro;
- chamada fixa em caixa amarela SEMPRE na zona segura (y 290-1250) e nunca em cima de rosto;
- legenda curta (ate 3 palavras), branca com contorno, palavras-chave em amarelo;
- etiqueta branca de valor nos blocos marcados; foto de produto inteira com fundo desfocado;
- SEMPRE tela cheia (video e foto); close em que o rosto ocupa a zona segura: a chamada some so
  naquela cena (nunca diminuir o video nem desfocar o fundo).

A chave do ElevenLabs vem de ELEVENLABS_API_KEY (variavel de usuario do Windows).
Audios em <plano>/audio_br/<CHAVE>.mp3 (narrador brasileiro gerado no site) tem prioridade.
"""
import json
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
import comum as C  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402
from comum import enc_antes_da_logo  # noqa: E402  passada antes da logo: rapida e quase sem perda (27/10/2026)

W, H, FPS = 1080, 1920, 30
F = "C:/Windows/Fonts/"
BOLD, BLACK, EMOJI = F + "segoeuib.ttf", F + "seguibl.ttf", F + "seguiemj.ttf"
YEL = (255, 214, 0)
SAFE_TOP, SAFE_BOTTOM, SAFE_W = 290, 1250, 860   # zona segura do Reels/TikTok/Stories
TOPO_MAX = 470   # a chamada fica so no alto da tela (y 290 a 470); nunca no meio
LAYOUT_HL_H = 180  # altura de referencia usada para posicionar legenda/etiqueta (como no aprovado)
CAP_H = 230
PB = ",hue=s=0,eq=contrast=1.12:brightness=-0.02"  # preto e branco para imagem forte (gancho, ferida, close)
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS)]


# ---------- utilidades ----------
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stderr[-2500:])
        sys.exit("ffmpeg falhou: " + " ".join(cmd[:6]))


def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip())


def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def push(d, amount=0.03, h=H):
    """Aproximacao lenta (3%), como nos videos nativos."""
    return (f"scale=w='trunc({W}*(1+{amount}*t/{d:.3f})/2)*2':h=-2:eval=frame,"
            f"crop={W}:{h},setsar=1,fps={FPS}")


# ---------- audio ----------
def apath(P, k):
    br = f"{P}/audio_br/{k}.mp3"
    return br if os.path.exists(br) else f"{P}/audio/{k}.mp3"


def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key:
        return key
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as reg:
            return winreg.QueryValueEx(reg, "ELEVENLABS_API_KEY")[0]
    except OSError:
        sys.exit("Falta a variavel ELEVENLABS_API_KEY (ou coloque os mp3 em audio_br).")


def make_audio(P, plano):
    """Gera so as falas que faltam, pela API REST (o SDK do Python do sistema esta quebrado).
    A fala crua fica em audio/raw; a usada no video (audio/<k>.mp3) sai sem respiros e sem silencios."""
    import shutil
    import urllib.error
    import urllib.request
    os.makedirs(P + "/audio/raw", exist_ok=True)
    voz = plano.get("voz", {})
    vid = voz.get("voice_id", "XrExE9yKIg1WjnnlVkGX")
    for k, texto in plano.get("narracao", {}).items():
        if os.path.exists(f"{P}/audio_br/{k}.mp3"):
            continue
        raw, out = f"{P}/audio/raw/{k}.mp3", f"{P}/audio/{k}.mp3"
        if not os.path.exists(raw):
            if os.path.exists(out):  # fala antiga, gerada antes de tirar o respiro
                shutil.move(out, raw)
            else:
                body = json.dumps({"text": C.para_voz(texto),
                                   "model_id": voz.get("model_id", "eleven_multilingual_v2"),
                                   "voice_settings": {"stability": 0.55, "similarity_boost": 0.75, "style": 0.25,
                                                      "use_speaker_boost": True}}).encode("utf-8")
                req = urllib.request.Request(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128", data=body,
                    headers={"xi-api-key": api_key(), "Content-Type": "application/json", "Accept": "audio/mpeg"})
                try:
                    with urllib.request.urlopen(req, timeout=120) as r:
                        open(raw, "wb").write(r.read())
                except urllib.error.HTTPError as e:
                    sys.exit(f"ElevenLabs recusou {k}: {e.code} {e.read()[:300]!r}")
                print("narracao", k)
        if not os.path.exists(out):
            C.sem_respiro(raw, out)


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


def draw_text(d, x, y, text, f, fe, fill):
    for t, e in runs(text):
        if e:
            d.text((x, y + f.size * 0.08), t, font=fe, embedded_color=True)
            x += d.textlength(t, font=fe)
        else:
            d.text((x, y), t, font=f, fill=fill)
            x += d.textlength(t, font=f)


# ---------- elementos ----------
def headline_img(lines, maxw=SAFE_W):
    """Caixa amarela com texto preto (texto nativo do TikTok); a fonte diminui ate caber."""
    size = 60
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while True:
        f, fe = ImageFont.truetype(BOLD, size), ImageFont.truetype(EMOJI, int(size * 0.83))
        if max(text_w(tmp, ln, f, fe) for ln in lines) <= maxw or size <= 30:
            break
        size -= 2
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
    """Etiqueta branca com texto preto."""
    f, fe = ImageFont.truetype(BOLD, 54), ImageFont.truetype(EMOJI, 44)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = text_w(tmp, text, f, fe)
    im = Image.new("RGBA", (W, 100), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0 = (W - tw) / 2
    d.rounded_rectangle([x0 - 30, 6, x0 + tw + 30, 94], radius=44, fill=(255, 255, 255, 245))
    draw_text(d, x0, 14, text, f, fe, "black")
    return im


def caption_img(words, key, size=84):
    """Legenda curta: branco com contorno preto, palavra-chave em amarelo, sem pontuacao final."""
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
            d.text((x, 10 + i * lh), w, font=f, fill=YEL if clean in key else "white",
                   stroke_width=9, stroke_fill="black")
            x += d.textlength(w + " ", font=f)
    return im


def chunks(text, t0, t1, size=3):
    """Blocos de ate 3 palavras, com tempo proporcional ao tamanho (funciona com qualquer voz)."""
    words = text.replace("...", "…").split()
    groups = [words[i:i + size] for i in range(0, len(words), size)]
    weights = [sum(len(w) + 2 for w in g) for g in groups]
    tot, out, t = sum(weights), [], t0
    for g, wt in zip(groups, weights):
        dt = (t1 - t0) * wt / tot
        out.append((t, t + dt, [w.upper() for w in g]))
        t += dt
    return out


# ---------- rostos ----------
def faces(WK, src, start, length, tag):
    """Caixas de rosto (x0,y0,x1,y1) no quadro 1080x1920, com margem.
    So conta rosto confirmado em pelo menos 2 dos 5 momentos da cena (evita falso positivo).
    Precisa do OpenCV 4 (o 5 nao tem CascadeClassifier)."""
    import cv2
    import numpy as np
    cas = [cv2.CascadeClassifier(cv2.data.haarcascades + n) for n in
           ("haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt2.xml")]
    prof = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
    per = []
    for k in range(5):
        t = start + length * (k + 0.5) / 5
        png = f"{WK}/face_{tag}_{k}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1",
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", png])
        if not os.path.exists(png):
            continue
        # imdecode porque o imread nao abre caminho com acento (EDIÇÃO)
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
            if any(iou(b, o) > 0.2 for j, other in enumerate(per) if j != i for o in other):
                x, y, w, h = b
                boxes.append((x - w * 0.25, y - h * 0.3, x + w * 1.25, y + h * 1.4))
    return boxes


def hits(y, h, boxes, xr=(0, W)):
    """Sobreposicao vertical com as caixas que tambem cruzam a faixa horizontal xr do elemento."""
    return sum(max(0, min(y + h, b[3]) - max(y, b[1])) for b in boxes
               if min(xr[1], b[2]) - max(xr[0], b[0]) > 0)


def xrange_of(img, pad=12):
    bb = img.getbbox() or (0, 0, W, 1)
    return (bb[0] - pad, bb[2] + pad)


def place(height, cands, busy, xr=(0, W)):
    """Primeira altura candidata que nao bate em rosto nem em outro texto."""
    best, best_hit = cands[0], None
    for y in cands:
        hit = hits(y, height, busy, xr)
        if hit == 0:
            return y
        if best_hit is None or hit < best_hit:
            best, best_hit = y, hit
    return best


def layout(busy, pl_h, show_pill):
    """Legenda e etiqueta (a chamada entra depois, na zona segura)."""
    hl_c = list(range(SAFE_TOP, TOPO_MAX + 1, 20))  # chamada so no alto
    cap_c = sorted(range(480, SAFE_BOTTOM - CAP_H + 1, 20), key=lambda y: abs(y - 1000))  # legenda na zona segura
    pl_c = list(range(SAFE_BOTTOM - 100, 880, -10)) + list(range(480, 800, 20))  # etiqueta na zona segura
    for with_pill in ([True, False] if show_pill else [False]):
        taken = list(busy)
        y_ref = place(LAYOUT_HL_H, hl_c, taken)
        taken.append((0, y_ref, W, y_ref + LAYOUT_HL_H))
        y_pl = None
        if with_pill:
            y_pl = place(pl_h, pl_c, taken)
            taken.append((0, y_pl, W, y_pl + pl_h))
        y_cap = place(CAP_H, cap_c, taken)
        if hits(y_cap, CAP_H, taken) == 0:
            break
    return y_pl, y_cap


# ---------- bloco (sempre tela cheia) ----------
def smaller(img, k):
    """Mesma arte em k% do tamanho, ainda centralizada numa faixa da largura do video."""
    im = img.resize((int(img.width * k), int(img.height * k)), Image.LANCZOS)
    out = Image.new("RGBA", (W, im.height), (0, 0, 0, 0))
    out.alpha_composite(im, ((W - im.width) // 2, 0))
    return out


def photo_faces(img):
    """Rostos numa foto (caixas no tamanho da propria imagem, com margem)."""
    import cv2
    import numpy as np
    g = cv2.cvtColor(np.array(img.convert("RGB")), cv2.COLOR_RGB2GRAY)
    found = []
    for n in ("haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt2.xml"):
        found += list(cv2.CascadeClassifier(cv2.data.haarcascades + n).detectMultiScale(g, 1.1, 6, minSize=(70, 70)))
    return [(x - w * 0.25, y - h * 0.3, x + w * 1.25, y + h * 1.4) for (x, y, w, h) in found]


def is_pb(b, scene=None):
    """Preto e branco: o bloco inteiro ("pb": true) ou so a cena ([video, inicio, "pb"])."""
    return bool(b.get("pb")) or (scene is not None and len(scene) > 2 and scene[2] == "pb")


def photo_input(WK, b, d, card):
    """Foto SEMPRE em tela cheia e em pe (rotacao da camera corrigida). Quadro parado, centrado nos rostos
    (ou no meio), com aproximacao lenta e suave (sem panoramica lateral e sem degraus de zoom)."""
    img = Image.open(C.foto_em_pe(card)).convert("RGB")
    s = max(W / img.width, H / img.height)
    big = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    oy = (big.height - H) // 2
    big = big.crop((0, oy, big.width, oy + H))
    fb = photo_faces(big)
    extra = big.width - W
    cx = (min(x0 for x0, _, _, _ in fb) + max(x1 for _, _, x1, _ in fb)) / 2 if fb else big.width / 2
    x0 = int(max(0, min(extra, cx - W / 2)))
    png = f"{WK}/{b['nome']}_foto.png"
    big.crop((x0, 0, x0 + W, H)).save(png)
    nf = max(1, round(d * FPS))
    chain = (f"[0:v]scale={W * 2}:{H * 2},zoompan=z='1+0.04*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
             f"d=1:s={W}x{H}:fps={FPS},setsar=1{PB if is_pb(b) else ''}[bg]")
    return png, chain, [(a - x0, b_, c - x0, e) for a, b_, c, e in fb]


def render_block(WK, plano, b, d, words_t, out, manual):
    """Video SEMPRE em tela cheia. A chamada fica na zona segura e nunca em cima de rosto:
    se o rosto ocupa a zona segura inteira (close), a chamada some so naquela cena."""
    hl = headline_img(plano["chamada"])
    hl_small = smaller(hl, 0.8)
    final = b.get("final", False)
    pl = pill_img(plano["etiqueta_final"] if final else plano["etiqueta"])
    show_pill = b.get("etiqueta", False) or final
    key = {w.upper() for w in plano.get("palavras_chave", [])}
    cmd, fc, windows = ["ffmpeg", "-y"], [], []
    card = b.get("foto")
    shots = b.get("cenas") or []
    if card:
        png, chain, fb = photo_input(WK, b, d, card)
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", png]
        fc.append(chain)
        windows.append([0.0, d, fb])
        n_in = 1
    else:
        each = d / len(shots)
        labels = []
        for i, scene in enumerate(shots):
            src, st = scene[0], scene[1]
            fb = faces(WK, src, st, each, f"{b['nome']}_{i}")
            fb += [tuple(z["caixa"]) for z in manual
                   if os.path.basename(z["arquivo"]) == os.path.basename(src) and abs(z["inicio"] - st) < 0.01]
            windows.append([i * each, (i + 1) * each, fb])
            cmd += ["-ss", f"{st:.2f}", "-t", f"{each + 0.1:.3f}", "-i", src]
            fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                      f"setsar=1,fps={FPS}{PB if is_pb(b, scene) else ''},trim=duration={each:.3f},setpts=PTS-STARTPTS[b{i}]")
            labels.append(f"[b{i}]")
        fc.append("".join(labels) + f"concat=n={len(shots)}:v=1:a=0[bg]")
        n_in = len(shots)

    plans = []
    for _, _, busy in windows:
        y_pl, y_cap = layout(busy, pl.height, show_pill)
        taken = list(busy) + [(0, y_cap, W, y_cap + CAP_H)]
        if y_pl is not None:
            taken.append((0, y_pl, W, y_pl + pl.height))
        y_hl, use = None, hl
        for cand in (hl, hl_small):  # tamanho normal; se nao couber, 80%; se ainda nao, some na cena
            xr = xrange_of(cand)
            y = place(cand.height, list(range(SAFE_TOP, TOPO_MAX + 1, 10)), taken, xr)
            if not hits(y, cand.height, taken, xr):
                y_hl, use = y, cand
                break
        plans.append((y_hl, y_pl, y_cap, use))
        print(f"  {b['nome']}: chamada={'ESCONDIDA (rosto ocupa a zona segura)' if y_hl is None else y_hl} "
              f"legenda={y_cap} etiqueta={y_pl}")

    last, k = "[bg]", n_in
    for wi, ((t0, t1, _), (y_hl, y_pl, y_cap, use)) in enumerate(zip(windows, plans)):
        base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if y_hl is not None:
            base.alpha_composite(use, (0, y_hl))
        if y_pl is not None:
            base.alpha_composite(pl, (0, y_pl))
        png = f"{WK}/{b['nome']}_base{wi}.png"
        base.save(png)
        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", png]
        fc.append(f"{last}[{k}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[o{k}]")
        last, k = f"[o{k}]", k + 1
        for j, (a, bb, ws) in enumerate(words_t):
            a2, b2 = max(a, t0), min(bb, t1)
            if b2 - a2 < 0.02:
                continue
            cp = f"{WK}/{b['nome']}_c{j}.png"
            caption_img(ws, key).save(cp)
            cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", cp]
            fc.append(f"{last}[{k}:v]overlay=0:{y_cap}:enable='between(t,{a2:.3f},{b2:.3f})'[o{k}]")
            last, k = f"[o{k}]", k + 1
    run(cmd + ["-filter_complex", ";".join(fc), "-map", last, "-an", *enc_antes_da_logo(), "-r", str(FPS), out])


def main():
    plano_path = os.path.abspath(sys.argv[1])
    P = os.path.dirname(plano_path).replace("\\", "/")
    plano = json.load(open(plano_path, encoding="utf-8-sig"))
    saida = C.destino(plano_path, plano, "lista")
    WK = P + "/render"
    os.makedirs(WK, exist_ok=True)
    make_audio(P, plano)
    N = {k: C.para_tela(v) for k, v in plano["narracao"].items()}
    manual = plano.get("zonas_protegidas", [])

    segs = []
    for b in plano["blocos"]:
        a = dur(apath(P, b["fala"]))
        d = a + b.get("pausa", 0.35)
        words_t = chunks(N[b["fala"]], 0.12, 0.12 + max(0.4, a - 0.1))
        render_block(WK, plano, b, d, words_t, f"{WK}/{b['nome']}.mp4", manual)
        segs.append({"nome": b["nome"], "fala": b["fala"], "d": d})

    with open(WK + "/lista.txt", "w", encoding="utf-8") as f:
        for s in segs:
            f.write(f"file '{WK}/{s['nome']}.mp4'\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", WK + "/lista.txt", "-c", "copy", WK + "/video.mp4"])

    cmd, parts, t = ["ffmpeg", "-y"], [], 0.0
    for i, s in enumerate(segs):
        cmd += ["-i", apath(P, s["fala"])]
        parts.append(f"[{i}:a]adelay={int((t + 0.12) * 1000)}:all=1[a{i}]")
        t += s["d"]
    total, n = t, len(segs)
    mix = "".join(f"[a{i}]" for i in range(n))
    if plano.get("musica"):
        cmd += ["-stream_loop", "-1", "-i", plano["musica"]]
        vol = plano.get("musica_volume", 0.12)
        parts.append(f"[{n}:a]atrim=0:{total:.3f},volume={vol},afade=t=out:st={total - 1.8:.3f}:d=1.8[m]")
        mix += "[m]"
        n += 1
    parts.append(f"{mix}amix=inputs={n}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    run(cmd + ["-filter_complex", ";".join(parts), "-map", "[aout]", "-t", f"{total:.3f}",
               "-c:a", "pcm_s16le", WK + "/audio.wav"])
    run(["ffmpeg", "-y", "-i", WK + "/video.mp4", "-i", WK + "/audio.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", saida])
    json.dump({"total": total, "blocos": segs}, open(P + "/linha_do_tempo.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"OK {saida} duracao={total:.1f}s")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
