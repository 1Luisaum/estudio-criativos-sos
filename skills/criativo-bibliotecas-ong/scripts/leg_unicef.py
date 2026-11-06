"""Legenda no estilo da skill criativo-unicef-ong (2 linhas no meio, branca com contorno, palavra falada numa
caixinha vermelha), queimada por cima de um video ja montado pelo bib.py (que nao tem esse estilo).
Pedido do usuario (05/11/2026, AEB 100): legenda no estilo UNICEF em todos os videos que tem fala.
Usa a narracao do plano (voz.tx + voz.de) e as falas reais dos pedacos com som da base; para quando entra a
cartela final (fim.de). O bib.py chama por_legenda() quando o plano tem "legenda": {"estilo": "unicef"}.
Uso: por_legenda(mp4, plano_dict)"""
import glob
import json
import os
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FONTE = r"C:\Windows\Fonts\seguibl.ttf"
FS, Y, CAIXA, MAXC = 56, 1190, (217, 4, 41), 22


def blocos(ws):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        txt = " ".join(x[2] for x in cur)
        fim_frase = w[2][-1:] in ".!?"
        if len(txt) > 2 * MAXC - 6 or (fim_frase and len(cur) >= 3):
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    res = []
    for b in out:
        l1, l2 = [], []
        for w in b:
            (l1 if not l2 and len(" ".join(x[2] for x in l1 + [w])) <= MAXC else l2).append(w)
        res.append([l for l in (l1, l2) if l])
    return res


RAIZ = os.path.join(os.path.expanduser("~"), "Desktop", "EDIÇÃO COM CLAUDE")
TX = os.path.join(os.path.expanduser("~"), ".claude", "estudio-ong", "CONHECIMENTO", "transcricoes")


def _r(a):
    return a.replace("{RAIZ}", RAIZ)


def _tx(arq):
    nome = os.path.splitext(os.path.basename(arq))[0] + ".json"
    for c in [os.path.join(os.path.dirname(arq), nome)] + glob.glob(os.path.join(TX, "**", nome), recursive=True):
        if os.path.exists(c):
            return c
    return None


def palavras(p):
    ws, acc = [], 0.0
    for pc in p.get("base", []):
        if pc.get("som") and pc.get("legenda", True):
            tx = pc.get("tx") or _tx(_r(pc["arq"]))
            for w in (json.load(open(_r(tx), encoding="utf-8"))["words"] if tx else []):
                if w.get("type", "word") == "word" and pc["ini"] - 0.05 <= w["start"] < pc["fim"] - 0.05:
                    ws.append((acc + w["start"] - pc["ini"], acc + min(w["end"], pc["fim"]) - pc["ini"], w["text"]))
        acc += pc["fim"] - pc["ini"]
    vz = p.get("voz")
    if vz:
        ws += [(w["start"] + vz.get("de", 0), w["end"] + vz.get("de", 0), w["text"])
               for w in json.load(open(_r(vz["tx"]), encoding="utf-8"))["words"] if w.get("type", "word") == "word"]
    return sorted(ws)


def por_legenda(mp4, p):
    global Y
    Y = (p.get("legenda") or {}).get("y", 1190)  # meio da tela; o plano pode mudar se houver texto ali
    ws = palavras(p)
    if not ws:
        print("legenda unicef: sem fala, nada a fazer")
        return
    limite = p.get("fim", {}).get("de", 1e9)
    ws = [w for w in ws if w[0] < limite]
    bl = blocos(ws)
    fonte = ImageFont.truetype(FONTE, FS)
    esp = fonte.getlength(" ")
    cache = {}

    def img(bi, ativo):
        if (bi, ativo) in cache:
            return cache[(bi, ativo)]
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
        linhas = bl[bi]; lh = int(FS * 1.22); y = Y - lh * len(linhas) / 2; idx = 0
        for linha in linhas:
            larg = sum(fonte.getlength(w[2]) for w in linha) + esp * (len(linha) - 1)
            x = (W - larg) / 2
            for w in linha:
                lw = fonte.getlength(w[2])
                if idx == ativo:
                    b = fonte.getbbox("ÁH")
                    dr.rounded_rectangle([x - 9, y + b[1] - 6, x + lw + 9, y + b[3] + 8], radius=10, fill=CAIXA + (255,))
                    dr.text((x, y), w[2], font=fonte, fill=(255, 255, 255, 255))
                else:
                    dr.text((x + 2, y + 3), w[2], font=fonte, fill=(0, 0, 0, 140), stroke_width=4, stroke_fill=(0, 0, 0, 140))
                    dr.text((x, y), w[2], font=fonte, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(20, 20, 20, 255))
                x += lw + esp; idx += 1
            y += lh
        cache[(bi, ativo)] = im
        return im

    tempos = []  # (inicio do bloco, fim do bloco, [inicio de cada palavra])
    for i, b in enumerate(bl):
        pal = [w for l in b for w in l]
        nxt = bl[i + 1][0][0][0] if i + 1 < len(bl) else min(limite, pal[-1][1] + 0.4)
        tempos.append((pal[0][0], min(nxt, limite), [w[0] for w in pal]))

    def legenda(t):
        for bi, (a, z, ini) in enumerate(tempos):
            if a - 0.03 <= t < z:
                ativo = max([k for k, s in enumerate(ini) if s <= t + 1e-6] or [0])
                return img(bi, ativo)
        return None

    tmp = mp4 + ".leg.mp4"
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", mp4, "-f", "rawvideo", "-pix_fmt", "rgb24", "-r", str(FPS), "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", mp4, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264",
                            "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "copy", tmp],
                           stdin=subprocess.PIPE)
    n, f = W * H * 3, 0
    while True:
        buf = dec.stdout.read(n)
        if len(buf) < n:
            break
        lg = legenda(f / FPS)
        if lg is not None:
            fr = Image.frombytes("RGB", (W, H), buf).convert("RGBA")
            fr.alpha_composite(lg)
            buf = fr.convert("RGB").tobytes()
        enc.stdin.write(buf); f += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    if enc.returncode:
        raise SystemExit("ffmpeg falhou na legenda unicef")
    shutil.move(tmp, mp4)
    print(f"legenda unicef: {len(bl)} blocos, {f} quadros")
