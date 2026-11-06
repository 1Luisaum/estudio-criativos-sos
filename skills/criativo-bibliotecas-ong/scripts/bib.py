"""Skill criativo-bibliotecas-ong. Montador dos criativos modelados nas bibliotecas de anuncios (Lar Maos Amigas, Lar Mae Ritinha, Movimento de Amor,
Florisbela, Leao de Juda), para os brutos do Pedrinho de 02/11/2026 (pedido do usuario, 03/11/2026).
Uso: python -I bib.py "<pasta do plano>\\plano.json"
Plano:
  base    [{arq, ini, fim, som?, pb?, zoom?, topo?}]  pedacos em sequencia (a fala sem pausas, ou b-roll mudo)
  broll   [[t0, t1, arq, ini, {pb?, zoom?}]]           por cima da base, o som da base continua
  textos  [{de, ate, linhas, estilo caixa|seco, fg, bg, size, y, alinha centro|esq, raio, pad, destaque, fonte}]
  legenda {estilo palavra|amarelo|pequena|unicef|nenhuma, y, size}  palavras dos pedacos com som (transcricao do bruto)
  musica, musica_volume, musica_ini;  fim {de, linhas, cor, setas}  (cartela por cima do fim da base)
Marca @soshumanhelppt no fim (marca.py da skill)."""
import glob
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # comum.py e marca.py desta skill
import comum as C  # noqa: E402
import marca  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402

PP = os.path.abspath(sys.argv[1])
P = os.path.dirname(PP)
R = os.path.join(P, "render")
os.makedirs(R, exist_ok=True)
p = json.load(open(PP, encoding="utf-8"))
SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _resolve(x):
    """Os modelos guardam caminhos com {RAIZ} (pasta do material) e {SKILL} (esta skill): valem em qualquer PC."""
    if isinstance(x, str):
        return x.replace("{RAIZ}", C.raiz(PP)).replace("{SKILL}", SKILL)
    if isinstance(x, list):
        return [_resolve(v) for v in x]
    if isinstance(x, dict):
        return {k: _resolve(v) for k, v in x.items()}
    return x


p = _resolve(p)
W, H, FPS = 1080, 1920, 30
TX = os.path.expanduser(r"~\.claude\estudio-ong\CONHECIMENTO\transcricoes")
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontes")  # Poppins vai junto (outro PC pode nao ter)
if not os.path.exists(os.path.join(FD, "Poppins-Bold.ttf")):
    FD = os.path.join(os.environ["LOCALAPPDATA"], r"Microsoft\Windows\Fonts")
FONTES = {"bold": os.path.join(FD, "Poppins-Bold.ttf"), "black": os.path.join(FD, "Poppins-Black.ttf"),
          "medium": os.path.join(FD, "Poppins-Medium.ttf"), "regular": os.path.join(FD, "Poppins-Regular.ttf"),
          "impact": r"C:\Windows\Fonts\impact.ttf", "italico": r"C:\Windows\Fonts\arialbi.ttf",
          "serif": r"C:\Windows\Fonts\times.ttf", "serif_bold": r"C:\Windows\Fonts\timesbd.ttf",
          "arial": r"C:\Windows\Fonts\arialbd.ttf"}
EMOJI = r"C:\Windows\Fonts\seguiemj.ttf"
COR = {"branco": (255, 255, 255), "preto": (0, 0, 0), "amarelo": (255, 222, 0), "vermelho": (226, 18, 28),
       "verde": (24, 200, 60), "azul": (20, 45, 90)}


def cor(c):
    return tuple(c) if isinstance(c, list) else COR[c]


def fonte(nome, size):
    f = FONTES.get(nome, FONTES["bold"])
    if not os.path.exists(f):
        f = FONTES["bold"] if os.path.exists(FONTES["bold"]) else r"C:\Windows\Fonts\arialbd.ttf"
    return ImageFont.truetype(f, size)


def _emo(ch):
    return ord(ch) > 0x2500 and ch not in "•–—’“”"


def larg(f, t):
    return sum((f.size * 1.15 if _emo(c) else f.getlength(c)) for c in t)


def escreve(d, x, y, t, f, fill, stroke=0, stroke_fill=(0, 0, 0)):
    for c in t:
        if _emo(c):
            try:
                fe = ImageFont.truetype(EMOJI, int(f.size * 0.9))
                d.text((x, y), c, font=fe, anchor="lm", embedded_color=True)
            except OSError:
                pass
            x += f.size * 1.15
        else:
            d.text((x, y), c, font=f, fill=fill, anchor="lm", stroke_width=stroke, stroke_fill=stroke_fill)
            x += f.getlength(c)
    return x


def png(nome, im):
    f = os.path.join(R, nome + ".png")
    im.save(f)
    return f


def texto_img(t):
    """Caixa cheia (fundo de cor) ou texto seco com contorno/sombra; palavras em 'destaque' trocam de cor."""
    f = fonte(t.get("fonte", "bold"), t.get("size", 52))
    linhas = t["linhas"]
    lh = int(f.size * t.get("lh", 1.18))
    padx, pady = t.get("pad", [26, 14])
    fg = cor(t.get("fg", "branco"))
    dest = {w.strip(".,!?:\"'").upper() for w in t.get("destaque", [])}
    cd = cor(t.get("cor_destaque", "amarelo"))
    tw = max(larg(f, l) for l in linhas)
    caixa = t.get("estilo", "caixa") == "caixa"
    bw = int(tw + padx * 2) if caixa else W
    bh = lh * len(linhas) + pady * 2 + 20
    im = Image.new("RGBA", (W, bh), (0, 0, 0, 0))
    esq = t.get("alinha") == "esq"
    x0 = t.get("x", 40) if esq else (W - bw) // 2
    if caixa and t.get("por_linha"):  # uma faixa por linha, do tamanho da linha (Maos Amigas, Leao de Juda)
        d = ImageDraw.Draw(im)
        for i, l in enumerate(linhas):
            lw = larg(f, l) + padx * 2
            bx = t.get("x", 40) if esq else (W - lw) / 2
            yc = 10 + pady + lh * (i + 0.5)
            d.rectangle([bx, yc - lh * 0.44, bx + lw, yc + lh * 0.46], fill=cor(t.get("bg", "branco")))
        if t.get("barra"):  # barra preta vertical a esquerda do bloco (Leao de Juda "Urgente!!")
            d.rectangle([t.get("x", 40) - 16, 10 + pady, t.get("x", 40) - 6, 10 + pady + lh * len(linhas)],
                        fill=cor(t.get("cor_barra", "preto")))
    elif caixa:
        d = ImageDraw.Draw(im)
        if t.get("sombra_caixa"):
            sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(sh).rounded_rectangle([x0 + 4, 14, x0 + bw + 4, 14 + bh - 20], radius=t.get("raio", 0),
                                                 fill=(0, 0, 0, 110))
            im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(6)))
            d = ImageDraw.Draw(im)
        d.rounded_rectangle([x0, 10, x0 + bw, 10 + bh - 20], radius=t.get("raio", 0), fill=cor(t.get("bg", "branco")))
    else:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ds = ImageDraw.Draw(sh)
        for i, l in enumerate(linhas):
            x = (x0 + padx) if esq else (W - larg(f, l)) / 2
            escreve(ds, x + 3, 10 + pady + lh * (i + 0.5) + 4, l, f, (0, 0, 0, 220))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(5)))
    d = ImageDraw.Draw(im)
    st = t.get("contorno", 0 if caixa else 3)
    sf = cor(t.get("cor_contorno", "preto"))
    for i, l in enumerate(linhas):
        x = (x0 + padx) if esq else (W - larg(f, l)) / 2
        y = 10 + pady + lh * (i + 0.5)
        for w in l.split(" "):
            c = cd if w.strip(".,!?:\"'").upper() in dest else fg
            x = escreve(d, x, y, w, f, c, st, sf) + f.getlength(" ")
    return im


def leg_img(ws, j, est, size, lg=None):
    """Legenda: 'palavra' (uma por vez, branca), 'amarelo' (2-3 palavras, a falada em amarelo),
    'pequena' (frase curta, branca com sombra)."""
    lg = lg or {}
    if est == "palavra":
        return texto_img({"linhas": [ws[j].lower()], "estilo": "seco", "size": size, "contorno": lg.get("contorno", 3),
                          "fonte": lg.get("fonte", "bold")})
    if est == "amarelo":
        alta = lg.get("caixa_alta", True)
        l = " ".join(w.upper() if alta else w for w in ws)
        return texto_img({"linhas": [l], "estilo": "seco", "size": size, "fonte": lg.get("fonte", "impact"),
                          "contorno": lg.get("contorno", 4), "destaque": [ws[j].upper()],
                          "cor_destaque": lg.get("cor", "amarelo")})
    f = fonte("bold", size)
    linhas, cur = [], []
    for w in ws:
        if cur and larg(f, " ".join(cur + [w])) > 700:
            linhas.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    linhas.append(" ".join(cur))
    return texto_img({"linhas": linhas, "estilo": "seco", "size": size, "contorno": lg.get("contorno", 2), "lh": 1.1})


def limpa(w):
    return w.replace("já––", "já").strip()


def achar_tx(arq):
    """Transcricao do bruto (mesmo nome, .json) em CONHECIMENTO\\transcricoes ou ao lado do bruto."""
    nome = os.path.splitext(os.path.basename(arq))[0] + ".json"
    for c in [os.path.join(os.path.dirname(arq), nome)] + glob.glob(os.path.join(TX, "**", nome), recursive=True):
        if os.path.exists(c):
            return c
    sys.exit(f"Falta a transcricao de {arq}: rode transcrever.py e salve em {TX}\\<pasta>\\{nome}")


def palavras(pedacos):
    out, acc = [], 0.0
    for pc in pedacos:
        dur = pc["fim"] - pc["ini"]
        if pc.get("som") and pc.get("legenda", True):
            tx = pc.get("tx") or achar_tx(pc["arq"])
            for w in json.load(open(tx, encoding="utf-8"))["words"]:
                if w.get("type", "word") == "word" and pc["ini"] - 0.05 <= w["start"] < pc["fim"] - 0.05:
                    out.append((acc + w["start"] - pc["ini"], acc + min(w["end"], pc["fim"]) - pc["ini"],
                                limpa(w["text"])))
        acc += dur
    return out


def grupos(ws, maxp):
    out, cur = [], []
    for w in ws:
        if cur and (len(cur) >= maxp or w[0] - cur[-1][1] > 0.6):
            out.append(cur)
            cur = []
        cur.append(w)
        if re.search(r"[.,?!]$", w[2]):
            out.append(cur)
            cur = []
    return out + ([cur] if cur else [])


def entrada(arq, ini, dur):
    """Video com -ss/-t; imagem parada (.png/.jpg) em loop pelo tempo do pedaco."""
    if arq.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        return ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", arq]
    return ["-ss", f"{ini:.3f}", "-t", f"{dur:.3f}", "-i", arq]


def vchain(k, pc, dur, t0=None):
    z = pc.get("zoom", 1.0)
    zz = ""
    if z > 1:
        y = "0" if pc.get("topo") else f"(ih-{H})/2"
        zz = f",scale={round(W * z / 2) * 2}:{round(H * z / 2) * 2},crop={W}:{H}:(iw-{W})/2:{y}"
    pb = ",hue=s=0" if pc.get("pb") else ""
    luz = f",eq=brightness={pc['luz']}" if pc.get("luz") else ""
    if pc.get("kb"):  # zoom lento nas imagens paradas
        luz += f",scale={W * 2}:{H * 2},zoompan=z='min(1+0.0009*on,1.12)':d=1:s={W}x{H}:fps={FPS}"
    pts = f"setpts=PTS-STARTPTS+{t0}/TB" if t0 is not None else "setpts=PTS-STARTPTS"
    return (f"[{k}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}{zz},fps={FPS},setsar=1{pb}{luz},"
            f"format=yuv420p,trim=0:{dur:.3f},{pts}")


VOZ_LUFS, MUS_SOB_FALA, MUS_SOZINHA = -16.0, -27.0, -15.0
_LUFS = {}


def _ebur(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else -70.0


def nivel(args):
    """(LUFS integrado, pico real dBTP) de um trecho de audio."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats"] + args + ["-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    tp = re.findall(r"Peak:\s+(-?[\d.inf]+) dBFS", r.stderr)
    try:
        return (float(i[-1]) if i else -70.0), (float(tp[-1]) if tp else -70.0)
    except ValueError:
        return -70.0, -70.0


def enc_audio():
    """06/11/2026: o AAC padrao do ffmpeg (192k, com preenchimento de ruido) acrescentava chiado nos agudos da voz
    (-14 dB em 12-20 kHz). O AAC do Windows (aac_mf) ou o do ffmpeg sem PNS a 256k ficam em -29/-30 dB."""
    global _ENC_AUDIO
    try:
        return _ENC_AUDIO
    except NameError:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True, errors="replace")
        _ENC_AUDIO = (["-c:a", "aac_mf", "-b:a", "256k"] if " aac_mf " in r.stdout
                      else ["-c:a", "aac", "-b:a", "256k", "-aac_coder", "twoloop", "-aac_pns", "0"])
        return _ENC_AUDIO


def ganho_seguro(args, alvo=-16.0, teto=-2.0):
    """Ganho fixo (dB) que leva a fala a `alvo` LUFS sem passar o pico de `teto` dBTP. 06/11/2026: subir a voz e
    cortar o pico no limitador (3-5 dB) fazia a narracao 'chiar'; com ganho seguro o limitador nao trabalha."""
    lv, tp = nivel(args)
    if lv < -60:
        return 0.0
    return max(min(alvo - lv, teto - tp, 12.0), -20.0)


def lufs_arquivo(f):
    if f not in _LUFS:
        _LUFS[f] = _ebur(["ffmpeg", "-hide_banner", "-nostats", "-t", "90", "-i", f, "-af", "ebur128", "-f", "null", "-"])
    return _LUFS[f]


def lufs_do_grafo(cmd, fa, rotulo):
    """Mede o volume (LUFS) da fala ja montada, sem o video, para aplicar um ganho fixo."""
    g = ";".join(fa) + f";[{rotulo}]ebur128[med]"
    return _ebur([c for c in cmd if c != "-v" and c != "error"] + ["-filter_complex", g, "-map", "[med]", "-f", "null", "-"])


def main():
    base = p["base"]
    total = sum(pc["fim"] - pc["ini"] for pc in base)
    cmd, fc, fa = ["ffmpeg", "-y", "-v", "error"], [], []  # fa: so o audio (medido antes, sem loudnorm)
    for i, pc in enumerate(base):
        cmd += entrada(pc["arq"], pc["ini"], pc["fim"] - pc["ini"] + 0.1)
    k = len(base)
    cat = []
    for i, pc in enumerate(base):
        dur = pc["fim"] - pc["ini"]
        fc.append(vchain(i, pc, dur) + f"[v{i}]")
        if pc.get("som"):
            g = ganho_seguro(["-ss", f"{pc['ini']:.3f}", "-t", f"{dur:.3f}", "-i", pc["arq"]])
            fa.append(f"[{i}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,aresample=48000,volume={g:.2f}dB,"
                      f"aformat=channel_layouts=stereo,afade=t=in:d=0.03,afade=t=out:st={dur - 0.04:.3f}:d=0.04[a{i}]")
        else:
            fa.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{dur:.3f}[a{i}]")
        cat.append(f"[v{i}]")
    fc.append("".join(cat) + f"concat=n={len(base)}:v=1:a=0[base]")
    fa.append("".join(f"[a{i}]" for i in range(len(base))) + f"concat=n={len(base)}:v=0:a=1[voz0]")
    acc = "base"
    for j, (t0, t1, arq, ini, *op) in enumerate(p.get("broll", [])):
        op = op[0] if op else {}
        cmd += entrada(arq, ini, t1 - t0 + 0.2)
        fc.append(vchain(k, op, t1 - t0 + 0.2, t0) + f"[b{j}]")
        fc.append(f"[{acc}][b{j}]overlay=0:0:eof_action=pass:enable='between(t,{t0},{t1})'[ob{j}]")
        acc, k = f"ob{j}", k + 1
    ovs = []
    for i, t in enumerate(p.get("textos", [])):
        im = texto_img(t)
        ovs.append((png(f"txt{i}", im), 0, t["y"] - im.height // 2, t["de"], t.get("ate", total)))
    lg = p.get("legenda", {"estilo": "nenhuma"})
    vz = p.get("voz")
    if lg["estilo"] not in ("nenhuma", "unicef"):  # "unicef" entra depois, por cima do video pronto
        ws = palavras(base)
        if vz:
            ws += [(w["start"] + vz.get("de", 0), w["end"] + vz.get("de", 0), limpa(w["text"]))
                   for w in json.load(open(vz["tx"], encoding="utf-8"))["words"] if w.get("type", "word") == "word"]
            ws.sort()
        maxp = {"palavra": 1, "amarelo": 3, "pequena": 6}[lg["estilo"]]
        size = lg.get("size", {"palavra": 62, "amarelo": 74, "pequena": 44}[lg["estilo"]])
        for gi, gr in enumerate(grupos(ws, maxp)):
            nxt = ws.index(gr[-1]) + 1
            fim = min(gr[-1][1] + 0.35, ws[nxt][0] if nxt < len(ws) else total)
            if lg["estilo"] == "pequena":
                im = leg_img([w[2] for w in gr], 0, "pequena", size, lg)
                ovs.append((png(f"leg{gi:03d}", im), 0, lg["y"] - im.height // 2, gr[0][0], fim))
                continue
            for jj, w in enumerate(gr):
                b = gr[jj + 1][0] if jj + 1 < len(gr) else fim
                im = leg_img([x[2] for x in gr], jj, lg["estilo"], size, lg)
                ovs.append((png(f"leg{gi:03d}_{jj}", im), 0, lg["y"] - im.height // 2, w[0], b))
    if p.get("fim"):
        fm = p["fim"]
        im = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * fm.get("escuro", 0.6))))
        box = texto_img({"linhas": fm["linhas"], "estilo": "caixa", "bg": fm.get("cor", "verde"), "fg": "branco",
                         "size": fm.get("size", 66), "fonte": "black", "raio": 18, "pad": [34, 22],
                         "sombra_caixa": True})
        im.alpha_composite(box, (0, fm.get("y", 900) - box.height // 2))
        if fm.get("sub"):
            sb = texto_img({"linhas": fm["sub"], "estilo": "seco", "size": fm.get("size_sub", 50), "contorno": 0,
                            "fg": fm.get("cor_sub", "branco"), "fonte": fm.get("fonte_sub", "bold")})
            im.alpha_composite(sb, (0, fm.get("y", 900) + box.height // 2 + fm.get("gap_sub", 20)))
        if fm.get("setas"):
            d = ImageDraw.Draw(im)
            y = fm.get("y_setas") or fm.get("y", 900) + box.height // 2 + (200 if fm.get("sub") else 70)
            for q in range(2):
                yy = y + q * 46
                d.line([(W / 2 - 60, yy), (W / 2, yy + 50), (W / 2 + 60, yy)], fill=(255, 255, 255), width=18,
                       joint="curve")
        ovs.append((png("fim", im), 0, 0, fm["de"], total))
    n = k
    for j, (f, x, y, t0, t1) in enumerate(ovs):
        cmd += ["-loop", "1", "-t", f"{total + 1:.2f}", "-i", f]
        fc.append(f"[{acc}][{n + j}:v]overlay={x}:{y}:enable='between(t,{t0:.2f},{t1:.2f})'[x{j}]")
        acc = f"x{j}"
    fc.append(f"[{acc}]trim=0:{total:.3f},setpts=PTS-STARTPTS,format=yuv420p[v]")
    tem_voz = any(pc.get("som") for pc in base) or bool(vz)
    extra = 0
    if vz:  # narracao do ElevenLabs por cima da base
        cmd += ["-i", vz["arq"]]
        ms = int(vz.get("de", 0) * 1000)
        gn = ganho_seguro(["-i", vz["arq"]])
        fa.append(f"[{n + len(ovs)}:a]aresample=48000,volume={gn:.2f}dB,aformat=channel_layouts=stereo,adelay={ms}|{ms},"
                  f"apad,atrim=0:{total:.3f}[nar]")
        fa.append("[voz0][nar]amix=inputs=2:normalize=0[voz1]")
        extra = 1
    fa.append("[%s]atrim=0:%.3f,asetpts=PTS-STARTPTS[vozc]" % ("voz1" if vz else "voz0", total))
    # fala: loudnorm (como antes). A musica e que tem o nivel medido e fixo (03/11/2026).
    # So narracao (sem fala dos brutos): ganho fixo medido. O loudnorm dinamico subia ~4 dB os primeiros
    # segundos e estourava o comeco (PEB 227, 03/11/2026).
    # 06/11/2026: sem loudnorm dinamico (subia o chiado) e sem ganho global (estourava e o limitador distorcia):
    # cada fala e a narracao ja vem com ganho seguro (-16 LUFS, pico ate -2 dBTP)
    fa.append("[vozc]anull[voz]")
    if p.get("musica"):
        cmd += ["-ss", str(p.get("musica_ini", 0)), "-stream_loop", "-1", "-i", p["musica"]]
        if p.get("musica_volume_fixo"):  # volume escrito no plano, sem medir
            v1 = p.get("musica_volume", 0.10 if tem_voz else 0.9)
            v2 = (p.get("musica_depois") or [0, v1])[1]
        else:  # a musica fica sempre no mesmo nivel: por baixo da fala ou sozinha
            lm = lufs_arquivo(p["musica"])
            alvo = p.get("musica_lufs", MUS_SOB_FALA if tem_voz else MUS_SOZINHA)
            v1 = 10 ** ((alvo - lm) / 20)
            v2 = 10 ** ((MUS_SOZINHA - lm) / 20)
        vol = f"{v1:.4f}"
        if p.get("musica_depois"):  # a musica sobe quando a fala acaba (Florisbela "sinal")
            vol = f"'if(lt(t,{p['musica_depois'][0]}),{v1:.4f},{v2:.4f})':eval=frame"
        fa.append(f"[{n + len(ovs) + extra}:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume={vol},"
                  f"afade=t=in:d=0.4,afade=t=out:st={total - 1.5:.3f}:d=1.5[m]")
        fa.append("[voz][m]amix=inputs=2:normalize=0,alimiter=limit=0.95:attack=10:release=80:level=disabled[a]")
    else:
        fa.append("[voz]alimiter=limit=0.95:attack=10:release=80:level=disabled[a]")
    fc += fa
    saida = C.destino(PP, p, p["estilo"])
    r = subprocess.run(cmd + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-r", str(FPS),
                              *C.enc_final(), *enc_audio(), "-ar", "48000", "-movflags", "+faststart",
                              saida], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(r.stderr[-2500:])
        sys.exit("ffmpeg falhou")
    if lg["estilo"] == "unicef":  # legenda do estilo UNICEF (pedido de 05/11/2026, AEB 100)
        import leg_unicef
        leg_unicef.por_legenda(saida, p)
    marca.no_fim(p, saida)
    print(f"OK {saida} planejado={total:.2f}s")


main()
