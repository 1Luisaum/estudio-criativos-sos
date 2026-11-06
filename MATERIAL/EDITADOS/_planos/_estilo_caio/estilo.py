"""Desenho dos textos copiados dos anuncios do Caio (CP 54 e CP 1027), medidos nos quadros 1080x1920."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
FD = os.path.join(os.environ["LOCALAPPDATA"], r"Microsoft\Windows\Fonts")
BOLD = os.path.join(FD, "Poppins-Bold.ttf")
RED, WHITE, BLK, YEL = (237, 0, 0), (255, 255, 255), (0, 0, 0), (255, 237, 0)
W = 1080
TR = 0.03  # a letra do Caio e um pouco mais espacada


def _f(size):
    return ImageFont.truetype(BOLD, size)


def larg(f, t):
    return sum(f.getlength(c) for c in t) + TR * f.size * max(0, len(t) - 1)


def escreve(d, x, y, t, f, cor):
    for c in t:
        d.text((x, y), c, font=f, fill=cor, anchor="lm")
        x += f.getlength(c) + TR * f.size
    return x


def quebra(palavras, f, maxw):
    linhas, cur = [], []
    for w in palavras:
        if cur and larg(f, " ".join(cur + [w])) > maxw:
            linhas.append(cur)
            cur = [w]
        else:
            cur.append(w)
    return linhas + [cur]


def caixa_texto(palavras, size, fg, bg, maxw=900, padx=26, pady=14, raio=0, lh=1.06, cores=None, linhas=None):
    """Caixa cheia com texto centralizado (gancho, faixa do alto, CTA, legenda do CP 1027).
    cores: cor por palavra (karaoke do CP 1027); linhas: quebra fixa (lista de listas de palavras)."""
    f = _f(size)
    linhas = linhas or quebra(palavras, f, maxw)
    h = int(size * lh)
    sp = f.getlength(" ") + TR * size
    tw = max(larg(f, " ".join(l)) for l in linhas)
    im = Image.new("RGBA", (int(tw + padx * 2), h * len(linhas) + pady * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=raio, fill=bg)
    k = 0
    for i, l in enumerate(linhas):
        x = (im.width - larg(f, " ".join(l))) / 2
        y = pady + h * (i + 0.5)
        for w in l:
            x = escreve(d, x, y, w, f, cores[k] if cores else fg) + sp
            k += 1
    return im


def texto_seco(linhas, size=84, cor=WHITE, destaque=None, cor_destaque=RED):
    """Texto sem caixa: letra grossa com sombra escura suave; palavras em `destaque` em outra cor (29/10/2026)."""
    f = _f(size)
    h = int(size * 1.12)
    sp = f.getlength(" ") + TR * size
    H = h * len(linhas) + 40
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for camada, d, dx, dy in ((sh, ds, 3, 5), (im, None, 0, 0)):
        d = d or ImageDraw.Draw(camada)
        for i, l in enumerate(linhas):
            ws = l.split()
            x = (W - larg(f, l)) / 2 + dx
            y = 20 + h * (i + 0.5) + dy
            for w in ws:
                c = (0, 0, 0, 230) if camada is sh else (cor_destaque if destaque and w.strip(".,?!").upper() in destaque else cor)
                x = escreve(d, x, y, w, f, c) + sp
    base = Image.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)), sh.filter(ImageFilter.GaussianBlur(7)))
    base = Image.alpha_composite(base, sh.filter(ImageFilter.GaussianBlur(2)))
    return Image.alpha_composite(base, im)


def legenda_salto(palavras, j, size=72, maxw=900):
    """Legenda do CP 54 com a caixa vermelha pulando para a palavra que esta sendo falada (indice j)."""
    f = _f(size)
    sp = f.getlength(" ") + TR * size
    ls = quebra(palavras, f, maxw)
    h = int(size * 1.18)
    H = h * len(ls) + 30
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds, d = ImageDraw.Draw(sh), ImageDraw.Draw(im)
    k, pos = 0, []
    for i, l in enumerate(ls):
        x = (W - larg(f, " ".join(l))) / 2
        y = 15 + h * (i + 0.5)
        for w in l:
            pos.append((x, y, larg(f, w), w))
            x += larg(f, w) + sp
            k += 1
    for q, (x, y, lw, w) in enumerate(pos):
        if q == j:
            ds.rounded_rectangle([x - 12, y - size * 0.56 + 4, x + lw + 14, y + size * 0.62 + 4], radius=12, fill=(0, 0, 0, 120))
        else:
            escreve(ds, x + 3, y + 4, w, f, (0, 0, 0, 200))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(5)))
    d = ImageDraw.Draw(im)
    for q, (x, y, lw, w) in enumerate(pos):
        if q == j:
            d.rounded_rectangle([x - 14, y - size * 0.58, x + lw + 14, y + size * 0.62], radius=12, fill=RED)
        escreve(d, x, y, w, f, WHITE)
    return im


def legenda_cp54(palavras, size=72):
    """CP 54: branco com sombra escura; a ultima palavra fica sozinha na 2a linha numa caixa vermelha arredondada."""
    f = _f(size)
    l1, l2 = " ".join(palavras[:-1]), palavras[-1]
    w1, w2 = (larg(f, l1) if l1 else 0), larg(f, l2)
    H = int(size * 2.5)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    y1, y2 = int(size * 0.62), int(size * 1.6)
    bx = [(W - w2) / 2 - 14, y2 - size * 0.58, (W + w2) / 2 + 14, y2 + size * 0.62]
    if l1:
        escreve(ds, (W - w1) / 2 + 3, y1 + 4, l1, f, (0, 0, 0, 200))
    ds.rounded_rectangle([bx[0] + 2, bx[1] + 4, bx[2] + 2, bx[3] + 4], radius=12, fill=(0, 0, 0, 120))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(5)))
    d = ImageDraw.Draw(im)
    if l1:
        escreve(d, (W - w1) / 2, y1, l1, f, WHITE)
    d.rounded_rectangle(bx, radius=12, fill=RED)
    escreve(d, (W - w2) / 2, y2, l2, f, WHITE)
    return im
