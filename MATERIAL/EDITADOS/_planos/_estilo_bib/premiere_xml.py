"""Monta um plano do estilo Bibliotecas (bib.py) como sequencia editavel do Premiere (XML do Final Cut Pro 7,
que o Premiere importa em Arquivo > Importar). Pedido do usuario em 05/11/2026.

Trilhas de video (de baixo para cima):
  V1 base (os takes em sequencia, cortados)   V2 b-roll por cima   V3 textos   V4 legenda (uma imagem por palavra)
  V5 cartela final   V6 marca (@juntospelaadrielly ou @soshumanhelppt, parada, 55% de opacidade)
Trilhas de audio: A1 falas reais (som dos takes)   A2 narracao   A3 musica (nivel ja medido como no bib.py)

O enquadramento e o do bib.py: cada take preenche 1080x1920 (escala "cobrir", centralizado) vezes o zoom do plano.
Fica de fora o que so existe no render: P&B, zoom lento das fotos, fades e o movimento da marca.

Uso: python -I premiere_xml.py <pasta do plano> [<pasta do plano> ...] --saida <pasta> [--marca juntos|sos]
"""
import json
import os
import re
import subprocess
import sys
import urllib.parse
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
SK = os.path.expanduser(r"~\.claude\skills\criativo-bibliotecas-ong\scripts")
BIB = os.path.join(SK, "bib.py")
PL = os.path.join(os.path.expanduser("~"), "Desktop", "EDIÇÃO COM CLAUDE", "EDITADOS", "_planos")
FPS, W, H = 30, 1080, 1920
MARCAS = {"juntos": os.path.join(os.path.dirname(os.path.abspath(__file__)), "marca_juntospelaadrielly.png"),
          "sos": os.path.join(SK, "marca_soshumanhelppt.png")}


def salvar(im, f):
    """Salva a imagem; se o Premiere estiver com ela aberta, mantem a que ja existe (o conteudo e o mesmo)."""
    try:
        im.save(f)
    except PermissionError:
        if not os.path.exists(f):
            raise


def fr(t):
    return int(round(t * FPS))


def probe(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "stream=codec_type,width,height:stream_side_data=rotation:stream_tags=rotate:format=duration",
                        "-of", "json", f], capture_output=True, text=True, encoding="utf-8", errors="replace")
    d = json.loads(r.stdout or "{}")
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    rot = abs(int(float((v.get("tags") or {}).get("rotate", 0) or 0)))
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = abs(int(float(sd["rotation"])))
    w, h = v.get("width", W), v.get("height", H)
    if rot in (90, 270):
        w, h = h, w
    dur = float((d.get("format") or {}).get("duration", 0) or 0)
    audio = any(s.get("codec_type") == "audio" for s in d.get("streams", []))
    return w, h, dur, audio


COMPAT = os.path.join(os.path.expanduser("~"), "Desktop", "EDIÇÃO COM CLAUDE", "EDITADOS", "PREMIERE", "_midia_h264")


def compat(f):
    """Video em HEVC (iPhone) aparece preto no Premiere sem a extensao HEVC: usa uma copia em H.264 (girada, com som)."""
    if not f.lower().endswith((".mov", ".mp4", ".m4v")):
        return f
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name",
                        "-of", "csv=p=0", f], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.stdout.strip().strip(",").split(",")[0] not in ("hevc", "h265"):
        return f
    os.makedirs(COMPAT, exist_ok=True)
    out = os.path.join(COMPAT, os.path.splitext(os.path.basename(f))[0] + "_h264.mp4")
    if not os.path.exists(out):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-map", "0:v:0", "-map", "0:a:0?", "-c:v", "libx264",
                        "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                        "-movflags", "+faststart", out], check=True)
        print("  copia H.264:", os.path.basename(out))
    return out


def lufs(f, ini=0.0, dur=90.0):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-ss", str(ini), "-t", str(dur), "-i", f, "-vn",
                        "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else -70.0


def url(f):
    return "file://localhost/" + urllib.parse.quote(os.path.abspath(f).replace("\\", "/"), safe="/:()[],'!$&*+=;@-_.~")


class Seq:
    def __init__(self, nome):
        self.nome, self.files, self.n = nome, {}, 0
        self.v, self.a = {}, {}

    def fileref(self, f, still=False):
        f = compat(f)
        if f in self.files:
            return f'<file id="{self.files[f][0]}"/>'
        fid = f"file-{len(self.files) + 1}"
        w, h, dur, audio = (Image.open(f).size + (0, False)) if still else probe(f)
        self.files[f] = (fid, w, h, dur, audio)
        d = fr(dur) if dur else fr(3600)
        so_audio = (not still) and os.path.splitext(f)[1].lower() in (".mp3", ".wav", ".m4a", ".aac")
        media = "" if so_audio else (f"<video><samplecharacteristics><width>{w}</width><height>{h}</height>"
                                     "</samplecharacteristics></video>")
        if audio:
            media += ("<audio><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics>"
                      "<channelcount>2</channelcount></audio>")
        return (f'<file id="{fid}"><name>{escape(os.path.basename(f))}</name><pathurl>{escape(url(f))}</pathurl>'
                f"<rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate><duration>{d}</duration>"
                f"<media>{media}</media></file>")

    def clip(self, trilha, f, t0, t1, ini=0.0, escala=None, opac=None, still=False, tipo="v", nivel=None):
        self.n += 1
        f = compat(f)
        ref = self.fileref(f, still)
        _, w, h, _, _ = self.files[f]
        s, e = fr(t0), fr(t1)
        if e <= s:
            return
        i0 = fr(ini)
        fx = ""
        if tipo == "v":
            sc = escala if escala is not None else max(W / w, H / h) * 100
            fx += ("<filter><effect><name>Basic Motion</name><effectid>basic</effectid><effectcategory>motion"
                   "</effectcategory><effecttype>motion</effecttype><mediatype>video</mediatype>"
                   f"<parameter><parameterid>scale</parameterid><name>Scale</name><value>{sc:.2f}</value></parameter>"
                   "</effect></filter>")
            if opac is not None:
                fx += ("<filter><effect><name>Opacity</name><effectid>opacity</effectid><effectcategory>motion"
                       "</effectcategory><effecttype>motion</effecttype><mediatype>video</mediatype>"
                       f"<parameter><parameterid>opacity</parameterid><name>opacity</name><value>{opac}</value>"
                       "</parameter></effect></filter>")
        elif nivel is not None:
            fx += ("<filter><effect><name>Audio Levels</name><effectid>audiolevels</effectid><effectcategory>"
                   "audiolevels</effectcategory><effecttype>audiolevels</effecttype><mediatype>audio</mediatype>"
                   f"<parameter><parameterid>level</parameterid><name>Level</name><value>{min(nivel, 3.98):.4f}"
                   "</value></parameter></effect></filter>")
        st = "<stillframe>TRUE</stillframe>" if still else ""
        x = (f'<clipitem id="clip-{self.n}"><name>{escape(os.path.basename(f))}</name><enabled>TRUE</enabled>'
             f"<duration>{e - s + i0 + 1}</duration><rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate>"
             f"<start>{s}</start><end>{e}</end><in>{i0}</in><out>{i0 + e - s}</out>{st}{ref}"
             + (f"<sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack>" if tipo == "a" else "")
             + f"{fx}</clipitem>")
        (self.v if tipo == "v" else self.a).setdefault(trilha, []).append(x)

    def xml(self, total):
        def trilhas(d, n):
            return "".join(f"<track>{''.join(d.get(i, []))}</track>" for i in range(1, n + 1))
        nv = max(self.v) if self.v else 1
        na = max(self.a) if self.a else 1
        return ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4"><sequence id="seq-1">'
                f"<name>{escape(self.nome)}</name><duration>{fr(total)}</duration>"
                f"<rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate><media>"
                f"<video><format><samplecharacteristics><rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate>"
                f"<width>{W}</width><height>{H}</height><pixelaspectratio>square</pixelaspectratio>"
                f"</samplecharacteristics></format>{trilhas(self.v, nv)}</video>"
                f"<audio><numOutputChannels>2</numOutputChannels>{trilhas(self.a, na)}</audio>"
                "</media></sequence></xmeml>\n")


def carregar_bib(plano, pasta_png):
    """Executa o bib.py so ate as definicoes (texto_img, fontes, _resolve), sem montar o video."""
    src = open(BIB, encoding="utf-8").read().rsplit("\nmain()", 1)[0]
    ns = {"__file__": BIB, "__name__": "bibxml"}
    argv = sys.argv
    sys.argv = [BIB, plano]
    try:
        exec(compile(src, BIB, "exec"), ns)
    finally:
        sys.argv = argv
    ns["R"] = pasta_png
    return ns


def legenda_unicef(p, ns, pasta_png, y_padrao=1190):
    sys.path.insert(0, SK)
    import leg_unicef as L
    ws = L.palavras(p)
    limite = p.get("fim", {}).get("de", 1e9)
    ws = [w for w in ws if w[0] < limite]
    if not ws:
        return []
    Y = (p.get("legenda") or {}).get("y", y_padrao)
    bl = L.blocos(ws)
    fonte = ImageFont.truetype(L.FONTE, L.FS)
    esp = fonte.getlength(" ")
    out = []
    for bi, b in enumerate(bl):
        pal = [w for l in b for w in l]
        nxt = bl[bi + 1][0][0][0] if bi + 1 < len(bl) else min(limite, pal[-1][1] + 0.4)
        for ativo, w0 in enumerate(pal):
            t1 = pal[ativo + 1][0] if ativo + 1 < len(pal) else min(nxt, limite)
            im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            dr = ImageDraw.Draw(im)
            lh = int(L.FS * 1.22)
            y = Y - lh * len(b) / 2
            idx = 0
            for linha in b:
                larg = sum(fonte.getlength(w[2]) for w in linha) + esp * (len(linha) - 1)
                x = (W - larg) / 2
                for w in linha:
                    lw = fonte.getlength(w[2])
                    if idx == ativo:
                        bb = fonte.getbbox("ÁH")
                        dr.rounded_rectangle([x - 9, y + bb[1] - 6, x + lw + 9, y + bb[3] + 8], radius=10,
                                             fill=L.CAIXA + (255,))
                        dr.text((x, y), w[2], font=fonte, fill=(255, 255, 255, 255))
                    else:
                        dr.text((x + 2, y + 3), w[2], font=fonte, fill=(0, 0, 0, 140), stroke_width=4,
                                stroke_fill=(0, 0, 0, 140))
                        dr.text((x, y), w[2], font=fonte, fill=(255, 255, 255, 255), stroke_width=3,
                                stroke_fill=(20, 20, 20, 255))
                    x += lw + esp
                    idx += 1
                y += lh
            f = os.path.join(pasta_png, f"legenda_{bi:03d}_{ativo:02d}.png")
            salvar(im, f)
            out.append((f, w0[0] if ativo else max(w0[0] - 0.03, 0), t1))
    return out


def montar(pasta, saida, marca):
    plano = os.path.join(PL, pasta, "plano.json")
    p0 = json.load(open(plano, encoding="utf-8-sig"))
    alvo = p0.get("saida") or ""
    nome = os.path.splitext(os.path.basename(alvo))[0] or pasta
    dst = os.path.join(saida, nome)
    png = os.path.join(dst, "imagens")
    os.makedirs(png, exist_ok=True)
    ns = carregar_bib(plano, png)
    p = ns["p"]
    s = Seq(nome)
    base = p["base"]
    total = sum(pc["fim"] - pc["ini"] for pc in base)
    t, fala = 0.0, False
    for pc in base:
        d = pc["fim"] - pc["ini"]
        still = pc["arq"].lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
        z = pc.get("zoom", 1.0)
        if still:  # vira PNG de verdade em 1080x1920 (as imagens da Magnific sao JPG com nome .png e o Premiere recusa)
            from PIL import ImageOps
            im = ImageOps.exif_transpose(Image.open(pc["arq"])).convert("RGB")
            k = max(W * z / im.width, H * z / im.height)
            im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
            y0 = 0 if pc.get("topo") else (im.height - H) // 2
            im = im.crop(((im.width - W) // 2, y0, (im.width - W) // 2 + W, y0 + H))
            foto = os.path.join(png, f"foto_{t:06.2f}.png")
            salvar(im, foto)
            s.clip(1, foto, t, t + d, 0, escala=100, still=True)
        else:
            w, h, _, _ = probe(pc["arq"])
            s.clip(1, pc["arq"], t, t + d, pc["ini"], escala=max(W / w, H / h) * 100 * z)
        if pc.get("som"):
            fala = True
            g = -15.0 - lufs(pc["arq"], pc["ini"], d)
            s.clip(1, pc["arq"], t, t + d, pc["ini"], tipo="a", nivel=10 ** (max(min(g, 12), -20) / 20))
        t += d
    for t0, t1, arq, ini, *op in p.get("broll", []):
        op = op[0] if op else {}
        w, h, _, _ = probe(arq)
        s.clip(2, arq, t0, t1, ini, escala=max(W / w, H / h) * 100 * op.get("zoom", 1.0))
    for i, tx in enumerate(p.get("textos", [])):
        im = ns["texto_img"](tx)
        tela = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tela.alpha_composite(im, (0, max(0, tx["y"] - im.height // 2)))
        f = os.path.join(png, f"texto_{i}.png")
        salvar(tela, f)
        s.clip(3, f, tx.get("de", 0), tx.get("ate", total), escala=100, still=True)
    lg = p.get("legenda") or {}
    if lg.get("estilo") == "unicef":
        for f, a, b in legenda_unicef(p, ns, png):
            s.clip(4, f, a, b, escala=100, still=True)
    elif lg.get("estilo") not in (None, "nenhuma"):
        print(f"  {nome}: legenda '{lg.get('estilo')}' fica so no MP4 (o XML so leva a UNICEF)")
    if p.get("fim"):
        fm = p["fim"]
        im = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * fm.get("escuro", 0.6))))
        box = ns["texto_img"]({"linhas": fm["linhas"], "estilo": "caixa", "bg": fm.get("cor", "verde"), "fg": "branco",
                               "size": fm.get("size", 66), "fonte": "black", "raio": 18, "pad": [34, 22],
                               "sombra_caixa": True})
        im.alpha_composite(box, (0, fm.get("y", 900) - box.height // 2))
        f = os.path.join(png, "cartela_final.png")
        salvar(im, f)
        s.clip(5, f, fm["de"], total, escala=100, still=True)
    mk = MARCAS[marca]
    if os.path.exists(mk):
        lg_ = Image.open(mk).convert("RGBA")
        lg_ = lg_.resize((540 if marca == "juntos" else 405, round(lg_.height * (540 if marca == "juntos" else 405) / lg_.width)))
        tela = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tela.alpha_composite(lg_, ((W - lg_.width) // 2, 640))
        f = os.path.join(png, "marca.png")
        salvar(tela, f)
        s.clip(6, f, 0, total, escala=100, opac=55, still=True)
    vz = p.get("voz")
    if p.get("voz_partes"):  # cada trecho original do ElevenLabs no seu lugar, sem ganho (para analisar o arquivo cru)
        for vp in p["voz_partes"]:
            s.clip(2, vp["arq"], vp["de"], min(total, vp["de"] + probe(vp["arq"])[2]), tipo="a", nivel=1.0)
        fala = True
    elif vz:
        g = -15.0 - lufs(vz["arq"])
        s.clip(2, vz["arq"], vz.get("de", 0), min(total, vz.get("de", 0) + probe(vz["arq"])[2]), tipo="a",
               nivel=10 ** (max(min(g, 12), -20) / 20))
        fala = True
    if p.get("musica"):
        m = p["musica"]
        if p.get("musica_volume_fixo"):
            nv = p.get("musica_volume", 0.10 if fala else 0.9)
        else:
            nv = 10 ** (((-27.0 if fala else -15.0) - lufs(m)) / 20)
        md = probe(m)[2]
        ini = float(p.get("musica_ini", 0))
        t = 0.0
        while t < total - 0.05:  # a musica volta do comeco se o video for mais longo que ela
            d = min(md - ini, total - t)
            s.clip(3, m, t, t + d, ini, tipo="a", nivel=nv)
            t += d
            ini = 0.0
    f = os.path.join(dst, nome + ".xml")
    open(f, "w", encoding="utf-8").write(s.xml(total))
    print(f"ok {nome}: {total:.1f}s, {s.n} clipes -> {f}")
    return f


if __name__ == "__main__":
    args = sys.argv[1:]
    saida = args[args.index("--saida") + 1]
    marca = args[args.index("--marca") + 1] if "--marca" in args else "juntos"
    pastas = [a for i, a in enumerate(args) if not a.startswith("--") and args[i - 1] not in ("--saida", "--marca")]
    for pa in pastas:
        montar(pa, saida, marca)
