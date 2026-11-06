"""Pedrinho_atadura_v1 (27/10/2026): gancho de ~8 s modelado no anuncio 1669162520799709 (UNICEF Brasil,
"Isso pode parecer um simples sache...") + cortes com lettering bem simples.

Gancho: foto de produto parada (crepe) com narrador (Kaique) -> mae fazendo o curativo -> close do Pedrinho;
legenda pequena em 2 linhas no meio da tela, branca, com a palavra falada numa caixinha (vermelha, no lugar
do azul da UNICEF). Sem lettering no gancho, como na referencia; o lettering entra com os cortes.
Cortes: build_cortes.py (copia do build da skill criativo-lettering-ong, sem a logo), sem musica;
a musica (piano) entra aqui, continua do gancho ate o fim, e a logo SOS (obrigatoria) vai no video inteiro.

Uso: python -I montar.py plano.json
"""
import json, os, subprocess, sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import comum  # noqa: E402
import marca  # noqa: E402  logo SOS obrigatoria em todo video (26/10/2026)

FPS, W, H = 30, 1080, 1920
FONTE = r"C:\Windows\Fonts\seguibl.ttf"
VOICE_FX = "highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2"


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        print(" ".join(cmd)); print(r.stderr[-3000:]); sys.exit(1)
    return r


def cobrir(img):
    """recorta a imagem (BGR) para 9:16 pelo centro e escala para 2x a tela (zoom suave sem travar)."""
    h, w = img.shape[:2]
    if w / h > W / H:
        nw = int(h * W / H); x = (w - nw) // 2; img = img[:, x:x + nw]
    else:
        nh = int(w * H / W); y = (h - nh) // 2; img = img[y:y + nh]
    return cv2.resize(img, (W * 2, H * 2), interpolation=cv2.INTER_LANCZOS4)


def quadro_zoom(big, z):
    """zoom z (>=1) no centro, com subpixel (warpAffine) para nao dar degrau."""
    s = z / 2.0
    M = np.float32([[s, 0, W / 2 - s * W], [0, s, H / 2 - s * H]])
    return cv2.warpAffine(big, M, (W, H), flags=cv2.INTER_LINEAR)


def frames_video(src, start, dur):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{start}", "-i", src, "-t", f"{dur}",
                        "-vf", f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                        "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    return a.reshape(-1, H, W, 3)


def hexcor(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def gancho(p, work):
    g, bank = p["gancho"], p["bank"]
    fim = g["fim"]; n = round(fim * FPS)
    # palavras com tempo (narracao do ElevenLabs, alinhamento de cada N)
    pal = []
    for nar in g["narracao"]:
        d = json.load(open(os.path.join(AQUI, "audio", nar["id"] + ".json"), encoding="utf-8"))
        pal += [(nar["t"] + w["start"], nar["t"] + w["end"]) for w in d["words"]]
    blocos, k = [], 0
    for linhas in g["blocos"]:
        ws = [w for l in linhas for w in l.split()]
        blocos.append((linhas, pal[k:k + len(ws)])); k += len(ws)
    assert k == len(pal), f"blocos tem {k} palavras e a narracao {len(pal)}"
    inicio = [b[1][0][0] for b in blocos]

    fonte = ImageFont.truetype(FONTE, g["legenda_fs"])
    caixa = hexcor(g["destaque"])

    def legenda(t):
        bi = max([i for i, t0 in enumerate(inicio) if t0 <= t + 1e-6] or [None]) if t >= inicio[0] - 0.05 else None
        if bi is None:
            return None
        linhas, tempos = blocos[bi]
        prox = [i for i, (a, _) in enumerate(tempos) if a <= t + 1e-6]
        ativo = prox[-1] if prox else 0
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
        lh = int(g["legenda_fs"] * 1.22); y = g["legenda_y"] - lh * len(linhas) / 2
        idx = 0
        esp = fonte.getlength(" ")
        for linha in linhas:
            ws = linha.split()
            larg = sum(fonte.getlength(w) for w in ws) + esp * (len(ws) - 1)
            x = (W - larg) / 2
            for w in ws:
                lw = fonte.getlength(w)
                if idx == ativo:
                    b = fonte.getbbox("ÁH")
                    dr.rounded_rectangle([x - 9, y + b[1] - 6, x + lw + 9, y + b[3] + 8], radius=10, fill=caixa + (255,))
                    dr.text((x, y), w, font=fonte, fill=(255, 255, 255, 255))
                else:  # contorno escuro: a foto do crepe e clara
                    dr.text((x + 2, y + 3), w, font=fonte, fill=(0, 0, 0, 140), stroke_width=4, stroke_fill=(0, 0, 0, 140))
                    dr.text((x, y), w, font=fonte, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(20, 20, 20, 255))
                x += lw + esp; idx += 1
            y += lh
        return im

    # fundos
    cenas = []
    for c in g["cenas"]:
        src = os.path.join(bank, c["src"])
        nf = round(c["t1"] * FPS) - round(c["t0"] * FPS)
        if src.lower().endswith((".png", ".jpg", ".jpeg")):
            img = cv2.imdecode(np.fromfile(src, np.uint8), cv2.IMREAD_COLOR)
            cenas.append(("foto", cobrir(img), nf, c["zoom"]))
        else:
            fr = frames_video(src, c["start"], nf / FPS + 0.2)
            cenas.append(("video", fr, nf, c["zoom"]))
    saida = os.path.join(work, "gancho_v.mp4")
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
                           "-pix_fmt", "yuv420p", saida], stdin=subprocess.PIPE)
    cache = {}
    f = 0
    for tipo, dado, nf, (z0, z1) in cenas:
        for i in range(nf):
            u = i / max(nf - 1, 1); z = z0 + (z1 - z0) * u  # linear: a curva suave parava nas pontas (freezedetect)
            if tipo == "foto":
                q = quadro_zoom(dado, z)
            else:
                q = dado[min(i, len(dado) - 1)]
            rgb = Image.fromarray(cv2.cvtColor(q, cv2.COLOR_BGR2RGB)).convert("RGBA")
            t = f / FPS
            chave = None
            lg = legenda(t)
            if lg is not None:
                rgb.alpha_composite(lg)
            ff.stdin.write(rgb.convert("RGB").tobytes())
            f += 1
    ff.stdin.close(); ff.wait()
    assert f == n, (f, n)

    # voz do gancho (narracoes nos tempos do plano), mesmo alvo de volume dos cortes (-15 LUFS)
    ins, fc, labs = [], [], ""
    for i, nar in enumerate(g["narracao"]):
        ins += ["-i", os.path.join(AQUI, "audio", nar["id"] + ".mp3")]
        ms = int(nar["t"] * 1000)
        fc.append(f"[{i}:a]aresample=48000,aformat=sample_fmts=s16:channel_layouts=stereo,adelay={ms}|{ms}[n{i}]")
        labs += f"[n{i}]"
    voz0 = os.path.join(work, "gancho_voz0.wav")
    run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fc) +
         f";{labs}amix=inputs={len(ins) // 2}:normalize=0,apad,atrim=0:{fim}[a]", "-map", "[a]", "-c:a", "pcm_s16le", voz0])
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", voz0, "-af", f"{VOICE_FX},ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    vi = float([l for l in r.stderr.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    voz = os.path.join(work, "gancho_voz.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", voz0, "-af", f"{VOICE_FX},volume={-15.0 - vi:.2f}dB,alimiter=limit=0.89",
         "-c:a", "pcm_s16le", voz])
    print(f"gancho: {fim:.2f}s, {len(pal)} palavras, voz {vi:.1f} LUFS -> -15")
    return saida, voz


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    plano_path = os.path.abspath(sys.argv[1])
    p = json.load(open(plano_path, encoding="utf-8"))
    work = os.path.join(AQUI, "render"); os.makedirs(work, exist_ok=True)
    hv, ha = gancho(p, work)
    fim = p["gancho"]["fim"]

    # cortes com lettering, sem musica e sem logo (os dois entram no video inteiro aqui)
    pc = {k: v for k, v in p.items() if k not in ("music", "gancho", "saida")}
    pc_path = os.path.join(AQUI, "plano_cortes.json")
    json.dump(pc, open(pc_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cortes = os.path.join(work, "cortes.mp4")
    r = subprocess.run([sys.executable, "-I", os.path.join(AQUI, "build_cortes.py"), pc_path, "--out", cortes],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("\n".join(l for l in r.stdout.splitlines() if l.startswith(("lettering", "audio", "OK"))))
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)
    lt = json.load(open(os.path.join(AQUI, "linha_do_tempo.json"), encoding="utf-8"))
    total = fim + lt["total"]; tela = fim + lt["tela_final"]

    saida = comum.destino(plano_path, p, "CORTES COM LETTERING")
    v0, v1 = p.get("music_vol", 0.12), p.get("music_end_vol", 0.32)
    vol = f"{v0}+{v1 - v0:.3f}*clip((t-{tela - 0.3:.3f})/0.8,0,1)"
    fc = (f"[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v];"
          f"[2:a][1:a]concat=n=2:v=0:a=1[voz];"
          f"[3:a]aresample=48000,aformat=channel_layouts=stereo,volume='{vol}':eval=frame,"
          f"afade=t=in:d=0.4,afade=t=out:st={total - 1.3:.3f}:d=1.3[mus];"
          f"[voz][mus]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]")
    run(["ffmpeg", "-v", "error", "-y", "-i", hv, "-i", cortes, "-i", ha, "-i", p["music"], "-filter_complex", fc,
         "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "19",
         "-profile:v", "high", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida])
    marca.no_fim(p, saida)
    print(f"OK {saida} duracao={total:.2f}s gancho={fim:.2f}s tela_final={tela:.2f}s")


if __name__ == "__main__":
    main()
