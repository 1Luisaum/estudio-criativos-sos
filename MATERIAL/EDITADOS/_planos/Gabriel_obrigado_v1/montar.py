"""Video do "obrigado" do Gabriel no estilo da referencia "mudar gancho.mp4" (SOS, entrevistas de rua).

Estilo: legenda pequena branca (Poppins Bold) no meio da tela, 1 a 3 palavras por vez; palavras-chave gigantes
(Poppins Black, verde neon com brilho ou branca), algumas com o video escurecido; sem caixas; tela cheia.
Fonte: a (17).MOV (transcricao ../../../.. scratchpad copiada em tx_a17.json). Musica: Orderly Chaos (Magnific).
Uso: python -I montar.py
"""
import glob, json, os, shutil, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\EDITING_SECTOR\Desktop\TODAS AS PASTAS\TUDO\VLOGS\GABRIEL\a (17).MOV"
SAIDA_DIR = r"C:\Users\EDITING_SECTOR\Desktop\TODAS AS PASTAS\TUDO\VLOGS\GABRIEL\EDITADOS"
SAIDA = os.path.join(SAIDA_DIR, "Gabriel_obrigado_v1.mp4")
FONTES = os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Windows", "Fonts")
MARCA = os.path.expanduser(r"~\.claude\skills\criativo-lettering-ong\scripts")
W, H, FPS = 1080, 1920, 30
MUS_VOL = 0.13
A6 = r"C:\Users\EDITING_SECTOR\Desktop\TODAS AS PASTAS\TUDO\VLOGS\GABRIEL\TRANSFORMAÇÃO GABRIEL\a (6).MOV"
# no trecho F a camera aponta para o chao: a imagem vem do estadio (a voz continua a do a (17))
COBRE = {"F": [(A6, 55.0), (A6, 119.0)]}
# cenas com o Gabriel em close: legenda e palavra gigante descem para o peito (y da legenda, y da palavra)
ALTURA = {"H": (1590, 1420), "G": (1590, 1420), "A1b": (1085, 1260)}
VERDE = "&H0014FF39&"   # #39FF14 em BGR
BRANCO = "&H00FFFFFF&"

# (nome, inicio, fim, zoom): trechos do bruto, na ordem do video
CORTES = [
 ("H", 521.15, 526.65, 1.0),
 ("A1", 6.16, 6.72, 1.0), ("A1b", 7.50, 9.75, 1.12), ("A2", 11.90, 14.25, 1.0), ("A3", 15.74, 17.25, 1.12),
 ("B1", 159.98, 162.98, 1.0), ("B2", 175.06, 177.12, 1.12),
 ("C1", 251.95, 255.90, 1.0), ("C2", 263.60, 268.10, 1.12),
 ("D1", 76.54, 78.95, 1.0), ("D2", 91.22, 93.75, 1.12),
 ("E1", 289.78, 295.62, 1.0), ("E2", 298.10, 301.02, 1.12), ("E3", 301.28, 302.75, 1.0), ("E4", 306.06, 307.72, 1.12),
 ("F", 326.30, 331.75, 1.0),
 ("G", 530.43, 533.40, 1.0),
]
# palavras-chave: (corte, palavras faladas, texto gigante, cor, escurece o video)
CHAVES = [
 ("H", ["quarenta", "mil"], "40 MIL", VERDE, False),
 ("H", ["sessenta", "toneladas"], "60 TONELADAS", VERDE, True),
 ("A1b", ["obrigado,"], "OBRIGADO", VERDE, False),
 ("E1", ["agradecido."], "AGRADECIDO", VERDE, False),
 ("F", ["fome", "por"], "FOME", VERDE, False),
 ("F", ["você"], "VOCÊ", BRANCO, True),
 ("G", ["muito", "obrigado."], "MUITO OBRIGADO", VERDE, True),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(" ".join(cmd[:12])); print(r.stderr[-2000:]); sys.exit(1)
    return r


def ts(t):
    c = int(round(max(0, t) * 100))
    return f"{c // 360000}:{c // 6000 % 60:02d}:{c // 100 % 60:02d}.{c % 100:02d}"


def main():
    work = os.path.join(AQUI, "render")
    os.makedirs(os.path.join(work, "fonts"), exist_ok=True)
    for f in ("Poppins-Black.ttf", "Poppins-Bold.ttf"):
        dst = os.path.join(work, "fonts", f)
        if os.path.exists(dst):
            os.chmod(dst, 0o666); os.remove(dst)
        shutil.copyfile(os.path.join(FONTES, f), dst)
    nv = subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=256x256:d=0.2", "-c:v", "h264_nvenc",
                         "-f", "null", "-"], capture_output=True).returncode == 0
    ENC = ["-c:v", "h264_nvenc", "-preset", "p5", "-cq", "17", "-b:v", "0"] if nv else ["-c:v", "libx264", "-preset", "fast", "-crf", "17"]
    words = [w for w in json.load(open(os.path.join(AQUI, "tx_a17.json"), encoding="utf-8"))["words"] if w["type"] == "word"]

    segs, tl, T = [], [], 0.0
    pos = {}
    for nome, a, b, z in CORTES:
        nf = round((b - a) * FPS); d = nf / FPS
        p = os.path.join(work, nome + ".mkv")
        vf = f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
        if z != 1.0:
            vf += f",crop=iw/{z}:ih/{z}:(iw-iw/{z})/2:(ih-ih/{z})*0.35,scale={W}:{H}:flags=lanczos"
        ent = ["-ss", f"{a:.3f}", "-t", f"{d:.4f}", "-i", SRC]
        mapa = ["-vf", vf + ",setsar=1"]
        if nome in COBRE:  # imagem de outro video, audio deste
            pecas = COBRE[nome]
            cada = d / len(pecas)
            fc = ""
            for i, (arq, ini) in enumerate(pecas, start=1):
                ent += ["-ss", f"{ini:.2f}", "-t", f"{cada + 0.1:.3f}", "-an", "-i", arq]
                fc += f"[{i}:v]{vf},setsar=1,trim=duration={cada:.4f},setpts=PTS-STARTPTS[p{i}];"
            fc += "".join(f"[p{i}]" for i in range(1, len(pecas) + 1)) + f"concat=n={len(pecas)}:v=1:a=0[v]"
            mapa = ["-filter_complex", fc, "-map", "[v]", "-map", "0:a"]
        run(["ffmpeg", "-v", "error", "-y"] + ent + mapa + ENC +
            ["-pix_fmt", "yuv420p", "-r", str(FPS), "-t", f"{d:.4f}",
             "-af", f"aresample=48000,aformat=channel_layouts=stereo,highpass=f=90,afftdn=nf=-28,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,"
                    f"loudnorm=I=-16:TP=-1.5:LRA=9,aresample=48000,afade=t=in:d=0.015,afade=t=out:st={d - 0.02:.3f}:d=0.02",
             "-c:a", "pcm_s16le", p])
        segs.append(p)
        pos[nome] = len(tl)
        for w in words:
            if a <= (w["start"] + w["end"]) / 2 <= b:
                tl.append({"c": nome, "t0": T + max(0, w["start"] - a), "t1": T + min(w["end"], b) - a, "x": w["text"]})
        T += d
        print(f"{nome} ok t={T:.2f}", flush=True)
    total = T

    # palavras-chave: acha a sequencia no corte e guarda o intervalo
    grandes, cobertos = [], set()
    for corte, seq, texto, cor, dim in CHAVES:
        idx = [i for i, w in enumerate(tl) if w["c"] == corte]
        k = next((i for i in idx if [tl[j]["x"].lower() for j in range(i, min(i + len(seq), len(tl)))] == [s.lower() for s in seq]), None)
        if k is None:
            sys.exit(f"chave nao achada: {corte} {seq}")
        n = len(seq) - (1 if seq[-1] == "por" else 0)  # "fome por": a segunda palavra so localiza
        t0, t1 = tl[k]["t0"], max(tl[k + n - 1]["t1"] + 0.25, tl[k]["t0"] + 0.7)
        grandes.append((t0, t1, texto, cor, dim, ALTURA.get(corte, (1085, 960))[1]))
        cobertos.update(range(k, k + n))

    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins,66,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,0,3,5,0,0,0,1
Style: Big,Poppins Black,136,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Box,Arial,20,&H00000000,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    # legenda pequena: ate 3 palavras / 18 letras, quebra em pontuacao, some nas palavras gigantes
    ch, cur = [], []
    for i, w in enumerate(tl):
        if i in cobertos:
            if cur:
                ch.append(cur); cur = []
            continue
        if cur and (len(cur) == 3 or len(" ".join(x["x"] for x in cur + [w])) > 18 or cur[-1]["x"][-1] in ",.?!" or w["t0"] - cur[-1]["t1"] > 0.4):
            ch.append(cur); cur = []
        cur.append(w)
    if cur:
        ch.append(cur)
    for i, g in enumerate(ch):
        fim = min(g[-1]["t1"] + 0.25, ch[i + 1][0]["t0"] if i + 1 < len(ch) else total)
        ev.append(f"Dialogue: 2,{ts(g[0]['t0'])},{ts(fim)},Cap,,0,0,0,,{{\\an5\\pos(540,{ALTURA.get(g[0]['c'], (1085, 960))[0]})}}" + " ".join(x["x"] for x in g))
    # palavras gigantes com pop; verde ganha brilho
    from PIL import ImageFont
    for t0, t1, texto, cor, dim, gy in grandes:
        if dim:
            ev.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\fad(70,70)\\1a&H30&\\p1}}m 0 0 l {W} 0 {W} {H} 0 {H}{{\\p0}}")
        em = ImageFont.truetype(os.path.join(FONTES, "Poppins-Black.ttf"), 100)
        asc, desc = em.getmetrics()
        alvo = min(150.0, 780 / (em.getlength(texto) / 100))  # letra de ~150 px; frase longa encolhe para caber na tela
        fs = int(alvo * (asc + desc) / 100 * 1.33)  # o libass desenha a Poppins a 75% do tamanho calculado
        pop = r"\fscx125\fscy125\t(0,90,\fscx100\fscy100)"
        if cor == VERDE:
            ev.append(f"Dialogue: 4,{ts(t0)},{ts(t1)},Big,,0,0,0,,{{\\an5\\pos(540,{gy}){pop}\\fs{fs}\\1c{cor}\\3c{cor}\\bord10\\blur14\\1a&H60&\\3a&H60&}}{texto}")
        ev.append(f"Dialogue: 5,{ts(t0)},{ts(t1)},Big,,0,0,0,,{{\\an5\\pos(540,{gy}){pop}\\fs{fs}\\1c{cor}}}{texto}")
    ass = os.path.join(work, "legendas.ass")
    open(ass, "w", encoding="utf-8-sig").write(head + "\n".join(ev) + "\n")

    lst = os.path.join(work, "lista.txt")
    open(lst, "w", encoding="utf-8").writelines(f"file '{p}'\n" for p in segs)
    aroll = os.path.join(work, "aroll.mkv")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", aroll])
    # audio em passe separado: voz + musica; a musica sobe um pouco nos ultimos 3 s
    mix = os.path.join(work, "mix.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", aroll, "-stream_loop", "-1", "-i", os.path.join(AQUI, "Orderly_Chaos.mp3"), "-filter_complex",
         f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total:.3f},volume='{MUS_VOL}+0.10*clip((t-{total - 3:.2f})/1,0,1)':eval=frame,"
         f"afade=t=in:d=0.3,afade=t=out:st={total - 1.2:.3f}:d=1.2[m];[0:a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]",
         "-map", "[a]", "-t", f"{total:.4f}", "-c:a", "pcm_s16le", mix])
    os.makedirs(SAIDA_DIR, exist_ok=True)
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "render/aroll.mkv", "-i", "render/mix.wav", "-filter_complex",
                        "[0:v]subtitles=render/legendas.ass:fontsdir=render/fonts,format=yuv420p[v]", "-map", "[v]", "-map", "1:a",
                        "-t", f"{total:.4f}"] + ENC[:4] + ["-cq", "19", "-b:v", "0"] +
                       ["-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", SAIDA],
                       cwd=AQUI, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(r.stderr[-2000:]); sys.exit(1)
    sys.path.insert(0, MARCA)
    import marca
    marca.aplicar(SAIDA)
    json.dump({"total": total, "cortes": CORTES, "grandes": [g[:3] for g in grandes]},
              open(os.path.join(AQUI, "linha_do_tempo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK {SAIDA} duracao={total:.2f}s")


main()
