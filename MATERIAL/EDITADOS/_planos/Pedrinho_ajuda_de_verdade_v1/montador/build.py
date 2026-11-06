"""Monta o criativo vertical 9:16 a partir de um plano JSON (ver references/plano.md).

Os valores padrao deste arquivo (tamanhos, cores, posicoes, volumes) sao os do video aprovado
Pedrinho_5horas_v1 (25/10/2026). O plano so traz o que muda de um video para outro.

Passe 1: cada trecho de fala do bruto vira um segmento (zoom no bruto ou b-roll por cima, audio do bruto).
Passe 2: legendas ASS; audio (voz + musica) mixado num passe separado; video final; checagem de buracos no audio.

Uso: python -I build.py <plano.json> [--out outro.mp4]
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
from comum import foto_em_pe  # noqa: E402

FPS = 30
W, H = 1080, 1920
STILL_EXT = (".jpg", ".jpeg", ".png", ".webp")
AUDIO_CHAIN = "aresample=48000,aformat=sample_fmts=s16:channel_layouts=stereo"
VOICE_FX = "highpass=f=80,afftdn=nr=10:nf=-42,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2"
ZOOM_CYCLE = ["Z2", "Z3", "ZF", "Z1"]

PINK, WHITE, YELLOW, RED_C, BLACK = "&H00631EE9&", "&H00FFFFFF&", "&H0000E6FF&", "&H002A2AFF&", "&H00000000&"
RED_BOX, DARK_RED = "&H002904D9&", "&H0010036E&"  # caixa do gancho e faixa de doacao (#D90429), aprovado 26/10/2026
HEART = r"{\fnSegoe UI Symbol}♥{\fnArial Black}"


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(" ".join(cmd)); print(r.stderr[-3000:]); sys.exit(1)
    return r


def fr(t):
    return round(t * FPS)


def source_size(path):
    s = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:stream_side_data=rotation", "-of", "json", path]).stdout)["streams"][0]
    w, h = s["width"], s["height"]
    rot = next((sd["rotation"] for sd in s.get("side_data_list", []) if "rotation" in sd), 0)
    return (h, w) if abs(int(rot)) % 180 == 90 else (w, h)


def zoom_crop(spec, sw, sh):
    """spec = {"z": fator, "face": [x, y]} (rosto a 25% da altura) ou {"z": fator, "center": [x, y]}."""
    z = spec["z"]
    w, h = round(sw / z / 2) * 2, round(sh / z / 2) * 2
    if "center" in spec:
        x, y = spec["center"][0] - w / 2, spec["center"][1] - h / 2
    else:
        x, y = spec["face"][0] - w / 2, spec["face"][1] - h * 0.25
    return w, h, int(min(max(x, 0), sw - w)), int(min(max(y, 0), sh - h))


def piece_chain(idx, dur, label, still=False):
    """Peca de b-roll em tela cheia. Foto ganha aproximacao lenta e suave (parada parecia travada)."""
    if still:
        nf = max(1, fr(dur))
        return (f"[{idx}:v]scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
                f"zoompan=z='1+0.05*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
                f"setsar=1,trim=duration={dur:.4f},setpts=PTS-STARTPTS[{label}]")
    return (f"[{idx}:v]fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
            f"setsar=1,trim=duration={dur:.4f},setpts=PTS-STARTPTS[{label}]")


def piece_input(src, start, dur):
    if src.lower().endswith(STILL_EXT):
        src = foto_em_pe(src)
        return ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur + 0.1:.4f}", "-i", src]
    return ["-ss", f"{start:.3f}", "-t", f"{dur + 0.1:.4f}", "-an", "-i", src]


def broll_frames(items, t_in, nf):
    """Itens com "until" (tempo do bruto) terminam ali; os sem "until" dividem igualmente o que sobra."""
    ends = [fr(it["until"] - t_in) if "until" in it else None for it in items]
    ends[-1] = nf
    i, prev = 0, 0
    while i < len(ends):
        j = i
        while ends[j] is None:
            j += 1
        n = j - i + 1
        base, rest = divmod(ends[j] - prev, n)
        acc = prev
        for k in range(i, j + 1):
            acc += base + (1 if k - i < rest else 0)
            ends[k] = acc
        prev, i = ends[j], j + 1
    return [e - s for s, e in zip([0] + ends[:-1], ends)]


class Builder:
    def __init__(self, plan, plan_dir, out):
        self.p = plan
        self.plan_dir = plan_dir
        self.out = out
        self.bank = plan.get("bank", "")
        self.work = os.path.join(tempfile.gettempdir(), "edicao-criativo", plan.get("nome", "video"))
        os.makedirs(os.path.join(self.work, "segs"), exist_ok=True)
        os.makedirs(os.path.join(self.work, "fonts"), exist_ok=True)
        for f in ("ariblk.ttf", "arialbd.ttf", "seguisym.ttf", "impact.ttf"):
            shutil.copy(os.path.join(r"C:\Windows\Fonts", f), os.path.join(self.work, "fonts", f))
        # fontes proprias (tarja fixa e legenda), copiadas para o libass achar
        for src in [(plan.get("chamada") or {}).get("fonte"), plan.get("caption_font")]:
            if not src:
                continue
            dst = os.path.join(self.work, "fonts", os.path.basename(src))
            if os.path.exists(dst):  # a copia herda o "somente leitura" da fonte instalada
                os.chmod(dst, 0o666); os.remove(dst)
            shutil.copyfile(src, dst)
        self.raw = plan["raw"]
        sw, sh = source_size(self.raw)
        face = plan.get("face", [sw / 2, sh * 0.2])
        zooms = {"Z1": {"z": 1.0, "face": face}, "Z2": {"z": 1.3, "face": face},
                 "Z3": {"z": 1.7, "face": face}, "ZF": {"z": 2.0, "face": face}}
        for k, v in plan.get("zooms", {}).items():
            zooms[k] = {**v, "face": v.get("face", face)} if "center" not in v else v
        self.crops = {k: zoom_crop(v, sw, sh) for k, v in zooms.items()}

    def src(self, path):
        return path if os.path.isabs(path) else os.path.join(self.bank, path)

    # ------------------------------------------------------------ passe 1
    def segment(self, k, seg, zoom, path):
        t_in, t_out = seg["in"], seg["out"]
        nf = fr(t_out - t_in)
        d = nf / FPS
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{t_in:.3f}", "-t", f"{d:.4f}", "-i", self.raw]
        a = f"[0:a]{AUDIO_CHAIN},afade=t=in:d=0.012,afade=t=out:st={d - 0.015:.4f}:d=0.015[a]"
        items = seg.get("broll")
        if not items:
            w, h, x, y = self.crops[zoom]
            fc = f"[0:v]fps={FPS},crop={w}:{h}:{x}:{y},scale={W}:{H}:flags=lanczos,setsar=1[v];" + a
        else:
            chains, labels = [], ""
            for i, (it, n) in enumerate(zip(items, broll_frames(items, t_in, nf)), start=1):
                cmd += piece_input(self.src(it["src"]), it.get("start", 0.0), n / FPS)
                chains.append(piece_chain(i, n / FPS, f"p{i}", still=it["src"].lower().endswith(STILL_EXT)))
                labels += f"[p{i}]"
            fc = ";".join(chains) + f";{labels}concat=n={len(items)}:v=1:a=0[v];" + a
        run(cmd + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{d:.4f}",
                   "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", "-r", str(FPS),
                   "-c:a", "pcm_s16le", path])
        return d

    def endcard(self, path):
        e = self.p["endcard"]
        d = fr(e.get("dur", 3.4)) / FPS
        run(["ffmpeg", "-v", "error", "-y"] + piece_input(self.src(e["src"]), e.get("start", 0.0), d) +
            ["-f", "lavfi", "-t", f"{d:.4f}", "-i", "anullsrc=r=48000:cl=stereo",
             "-filter_complex", piece_chain(0, d, "v") + f";[1:a]{AUDIO_CHAIN}[a]",
             "-map", "[v]", "-map", "[a]", "-t", f"{d:.4f}",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", "-r", str(FPS),
             "-c:a", "pcm_s16le", path])
        return d

    # ------------------------------------------------------------ legendas
    def build_ass(self, words, total, end_start, path):
        p = self.p
        cap_y, hook_y = p.get("caption_y", 1010), p.get("hook_y", 1290)
        head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{p.get("caption_font_nome", "Arial Black")},{p.get("caption_fs", 100)},&H00FFFFFF,&H000000FF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,4,5,0,0,0,1
Style: Box,Arial,20,&H00631EE9,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Hook,Arial Black,84,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Cta,Arial Black,62,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,5,3,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        ev = []
        badge = p.get("badge")  # sem selo no canto desde 26/10/2026; o plano pode pedir um
        if badge:
            bw = int(text_w(badge + " O", 46) + 100)
            ev += [f"Dialogue: 3,{ts(0)},{ts(total)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\1c{BLACK}\\1a&H20&\\p1}}{rrect(48, 236, bw, 82, 20)}{{\\p0}}",
                   f"Dialogue: 4,{ts(0)},{ts(total)},Hook,,0,0,0,,{{\\an5\\pos({48 + bw // 2},277)\\fs46}}{badge} {HEART}"]
        for h in p.get("hook", []):
            ev += box_block(h["t0"], h["t1"], h["lines"], h.get("y", hook_y), h.get("fs", 92), fade=(0, 0))
        if p.get("chamada"):
            ch_end = total if p["chamada"].get("ate_o_fim") else end_start
            if not p["chamada"].get("imagem"):  # com imagem pronta, a tarja entra como overlay no passe final
                ev += chamada_block(max([h["t1"] for h in p.get("hook", [])] + [0.0]), ch_end, p["chamada"])
        ev += captions(words, end_start, cap_y, set(p.get("red", ["CURATIVO", "CURATIVOS"])))
        e = p.get("endcard")
        if e:
            ev.append(f"Dialogue: 0,{ts(end_start)},{ts(total)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\fad(250,0)\\1c{BLACK}\\1a&H70&\\p1}}m 0 0 l {W} 0 {W} {H} 0 {H}{{\\p0}}")
            if e.get("lines"):
                ev += box_block(end_start + 0.15, total, e["lines"], e.get("y", 860), e.get("fs", 76), fade=(200, 0))
            if e.get("cta"):
                ev.append(f"Dialogue: 2,{ts(end_start + 0.5)},{ts(total)},Cta,,0,0,0,,{{\\an5\\pos(540,{e.get('y', 860) + 220})\\fad(200,0)}}"
                          f"{e['cta']} {{\\fnSegoe UI Symbol\\1c{RED_C}}}♥")
        with open(path, "w", encoding="utf-8-sig") as fh:
            fh.write(head + "\n".join(ev) + "\n")

    # ------------------------------------------------------------ principal
    def build(self):
        p = self.p
        tx_path = p["transcript"] if os.path.isabs(p["transcript"]) else os.path.join(self.plan_dir, p["transcript"])
        raw_words = [w for w in json.load(open(tx_path, encoding="utf-8"))["words"] if w["type"] == "word"]
        fix = {k.upper(): v for k, v in p.get("fix", {}).items()}
        seg_paths, words, timeline, T, cyc = [], [], [], 0.0, 0
        for k, seg in enumerate(p["segments"]):
            zoom = seg.get("zoom")
            if not zoom and not seg.get("broll"):
                zoom = ZOOM_CYCLE[cyc % len(ZOOM_CYCLE)]; cyc += 1
            path = os.path.join(self.work, "segs", f"s{k:02d}.mkv")
            d = self.segment(k, seg, zoom, path)
            seg_fix = {**fix, **{a.upper(): b for a, b in seg.get("fix", {}).items()}}
            for w in raw_words:
                if seg["in"] <= (w["start"] + w["end"]) / 2 <= seg["out"]:
                    txt = w["text"].strip()
                    clean = txt.strip(",.!?…").upper()
                    words.append((T + w["start"] - seg["in"], T + min(w["end"], seg["out"]) - seg["in"],
                                  seg_fix.get(clean, clean), txt[-1:] in ",.!?…"))
            timeline.append({"seg": k, "bruto": [seg["in"], seg["out"]], "t0": round(T, 3), "dur": round(d, 3),
                             "visual": "broll" if seg.get("broll") else zoom})
            seg_paths.append(path)
            T += d
            print(f"seg {k:02d} ok  t={T:6.2f}")
        end_start = T
        if p.get("endcard"):
            path = os.path.join(self.work, "segs", "s99_end.mkv")
            T += self.endcard(path)
            seg_paths.append(path)
        total = T

        concat = os.path.join(self.work, "concat.txt")
        with open(concat, "w", encoding="utf-8") as fh:
            fh.writelines(f"file '{sp}'\n" for sp in seg_paths)
        aroll = os.path.join(self.work, "aroll.mkv")
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", concat, "-c", "copy", aroll])
        ass = os.path.join(self.work, "legendas.ass")
        self.build_ass(words, total, end_start, ass)

        # audio num passe separado: loudnorm no mesmo grafo do video abriu um buraco de 5,6 s no audio
        # do primeiro video; a voz leva um ganho fixo medido antes (alvo -15 LUFS)
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", aroll, "-vn", "-af", f"{VOICE_FX},ebur128", "-f", "null", "-"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        voice_i = float([l for l in r.stderr.splitlines() if l.strip().startswith("I:")][-1].split()[1])
        gain = p.get("voice_lufs", -15.0) - voice_i
        mix = os.path.join(self.work, "mix.wav")
        if p.get("music"):
            v0, v1 = p.get("music_vol", 0.12), p.get("music_end_vol", 0.32)
            vol = f"{v0}+{v1 - v0:.3f}*clip((t-{end_start - 0.3:.3f})/0.8,0,1)"
            ms = ["-ss", f"{p.get('music_start', 0.0):.2f}"] if p.get("music_start") else []
            fa = (f"[0:a]{VOICE_FX},volume={gain:.2f}dB[voz];"
                  f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume='{vol}':eval=frame,"
                  f"afade=t=in:d=0.4,afade=t=out:st={total - 1.3:.3f}:d=1.3[mus];"
                  "[voz][mus]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]")
            run(["ffmpeg", "-v", "error", "-y", "-i", aroll] + ms + ["-i", p["music"], "-filter_complex", fa,
                 "-map", "[a]", "-t", f"{total:.4f}", "-c:a", "pcm_s16le", mix])
        else:
            run(["ffmpeg", "-v", "error", "-y", "-i", aroll, "-af", f"{VOICE_FX},volume={gain:.2f}dB,alimiter=limit=0.89",
                 "-t", f"{total:.4f}", "-c:a", "pcm_s16le", mix])
        sat = p.get("saturation", 0.70)
        vf = f"[0:v]eq=saturation={sat}:contrast=1.04,subtitles=legendas.ass:fontsdir=fonts"
        img_in = []
        ch = p.get("chamada") or {}
        if ch.get("imagem"):
            # lettering pronto do usuario (26/10/2026): parado o video todo, por cima de tudo e sem a saturacao do video
            iw = ch.get("largura", 760)
            img_in = ["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.4f}", "-i", ch["imagem"]]
            vf += (f"[base];[2:v]scale={iw}:-2:flags=lanczos,format=rgba[let];"
                   f"[base][let]overlay=x=(W-w)/2:y={ch.get('y', 1290)}-h/2:shortest=1")
            print(f"lettering: {os.path.basename(ch['imagem'])} com {iw} px de largura, centro em y={ch.get('y', 1290)}")
        run(["ffmpeg", "-v", "error", "-y", "-i", aroll, "-i", mix] + img_in + ["-filter_complex",
             vf + ",format=yuv420p[v]",
             "-map", "[v]", "-map", "1:a", "-t", f"{total:.4f}",
             "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-profile:v", "high", "-pix_fmt", "yuv420p",
             "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", self.out], cwd=self.work)

        # guarda legendas e linha do tempo junto do plano, para conferir e refazer ajustes depois
        shutil.copy(ass, os.path.join(self.plan_dir, "legendas.ass"))
        json.dump({"total": total, "tela_final": end_start, "segmentos": timeline},
                  open(os.path.join(self.plan_dir, "linha_do_tempo.json"), "w", encoding="utf-8"), indent=1)

        r = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "packet=pts_time,duration_time",
                 "-of", "csv=p=0", self.out])
        pk = [tuple(map(float, l.split(",")[:2])) for l in r.stdout.split() if l]
        holes = [(round(a[0], 2), round(b[0], 2)) for a, b in zip(pk, pk[1:]) if b[0] - a[0] - a[1] > 0.02]
        print(f"audio: {pk[-1][0] + pk[-1][1]:.2f}s  buracos={holes or 'nenhum'}  ganho voz={gain:+.1f}dB")
        print(f"OK {self.out}  duracao={total:.2f}s  tela_final={end_start:.2f}s")
        if holes:
            sys.exit("ATENCAO: o audio do arquivo final tem buracos")


# ---------------------------------------------------------------- ASS

def ts(t):
    cs = int(round(max(0.0, t) * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


# larguras aproximadas da Arial Black (em) para dimensionar as caixas
ADV = {**{c: 0.778 for c in "ABCDRVXY"}, **{c: 0.833 for c in "GHKNOQU"}, **{c: 0.722 for c in "EPSTZ"},
       **{c: 0.667 for c in "FJL0123456789$"}, "M": 0.944, "W": 1.0, "I": 0.389, " ": 0.333}
ACC = str.maketrans("ÁÀÂÃÉÊÍÓÔÕÚÇ", "AAAAEEIOOOUC")


def text_w(s, fs):
    return sum(ADV.get(c, 0.75) for c in s.upper().translate(ACC)) * fs / 1.41


def rrect(x, y, w, h, r):
    X, Y = x + w, y + h
    return (f"m {x + r} {y} l {X - r} {y} b {X} {y} {X} {y} {X} {y + r} l {X} {Y - r} b {X} {Y} {X} {Y} {X - r} {Y} "
            f"l {x + r} {Y} b {x} {Y} {x} {Y} {x} {Y - r} l {x} {y + r} b {x} {y} {x} {y} {x + r} {y}")


IMPACT = r"C:\Windows\Fonts\impact.ttf"


def impact_w(s, fs):
    from PIL import ImageFont
    return ImageFont.truetype(IMPACT, fs).getlength(s)


def faixa(t0, t1, linhas, cy, fade=(150, 0), layer=5):
    """Faixa de anuncio de doacao (referencia aprovada em 26/10/2026): vermelha de ponta a ponta, com degrade
    do vermelho claro em cima para o escuro embaixo, texto branco Impact em maiusculas, linhas juntas, sombra
    escura e nenhum risco por cima. linhas = [(texto, tamanho)]; a fonte diminui se nao couber em 1000 px."""
    # versao de teste (pedido de 26/10/2026, so neste plano): retangulo vermelho chapado com sobra nos cantos,
    # texto branco seco, sem degrade e sem sombra
    SX = 1.04
    linhas = [(t.replace("*", "").upper(), fs) for t, fs in linhas]
    k = min(840 / max(impact_w(t, fs) * SX, 1) for t, fs in linhas)  # a linha mais longa ocupa ~840 px
    linhas = [(t, int(min(fs * k, 160))) for t, fs in linhas]
    lh = [fs * 0.96 for _, fs in linhas]
    fmax = max(fs for _, fs in linhas)
    pad_y, pad_x = int(fmax * 0.16), int(fmax * 0.34)
    bw = min(int(max(impact_w(t, fs) * SX for t, fs in linhas) + 2 * pad_x), W - 120)  # >= 60 px de sobra
    h = int(sum(lh) + 2 * pad_y)
    x0, y0 = (W - bw) // 2, int(cy - h / 2)
    ev = [f"Dialogue: {layer},{ts(t0)},{ts(t1)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\fad({fade[0]},{fade[1]})"
          f"\\1c&H001A0EC4&\\p1}}m {x0} {y0} l {x0 + bw} {y0} {x0 + bw} {y0 + h} {x0} {y0 + h}{{\\p0}}"]
    y = y0 + pad_y
    for (t, fs), l in zip(linhas, lh):
        yc = y + l / 2
        ev.append(f"Dialogue: {layer + 2},{ts(t0)},{ts(t1)},Hook,,0,0,0,,{{\\an5\\pos(540,{yc:.0f})\\fnImpact"
                  f"\\fs{fs}\\fscx{SX * 100:.0f}\\bord0\\shad0\\1c{WHITE}\\fad({fade[0]},{fade[1]})}}{t}")
        y += l
    return ev


ARIBLK = r"C:\Windows\Fonts\ariblk.ttf"


def tarja_fixa(t0, t1, linhas, cy, larg=760, fonte=ARIBLK, fonte_nome="Arial Black", vao=0.24):
    """Tarja de teste (referencias R$ 5,00 do usuario, 26/10/2026): caixa vermelha chapada com sobra nos cantos,
    valor gigante na 1a linha e 3 linhas menores centralizadas, tudo branco, sem sombra.
    Proporcoes medidas na referencia: valor ocupa 83% da largura da caixa e as linhas de baixo 67%;
    margem de cima 18% e de baixo 12,5% da altura; vao entre o valor e as linhas = 24% da altura do valor;
    entre as linhas pequenas, 22% da altura delas."""
    from PIL import ImageFont
    big, small = linhas[0].upper(), [l.upper() for l in linhas[1:]]

    def med(fs):  # (largura de cada linha, altura da maiuscula, subida, descida) em px a fs (PIL)
        f = ImageFont.truetype(fonte, fs)
        asc, desc = f.getmetrics()
        bb = f.getbbox("H")
        return f, bb[3] - bb[1], asc, desc

    f100, cap100, asc100, desc100 = med(100)
    eb = larg * 0.83 * 100 / f100.getlength(big)
    es = larg * 0.67 * 100 / max(f100.getlength(l) for l in small) if small else 0
    cb, cs = cap100 * eb / 100, cap100 * es / 100
    texto = cb + (vao * cb if small else 0) + len(small) * cs + max(len(small) - 1, 0) * 0.22 * cs
    h = texto / (1 - 0.18 - 0.125)
    x0, y0 = (W - larg) // 2, int(cy - h / 2)
    ev = [f"Dialogue: 5,{ts(t0)},{ts(t1)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\1c&H000202C3&\\p1}}"
          f"m {x0} {y0} l {x0 + larg} {y0} {x0 + larg} {y0 + h:.0f} {x0} {y0 + h:.0f}{{\\p0}}"]
    y = y0 + 0.18 * h  # topo da maiuscula da linha atual
    for i, (t, em, cap) in enumerate(zip([big] + small, [eb] + [es] * len(small), [cb] + [cs] * len(small))):
        k = em / 100
        # \an5 centra a caixa (subida + descida); a maiuscula fica deslocada (subida - descida - maiuscula) / 2
        off = ((asc100 - desc100) / 2 - cap100 / 2) * k
        ev.append(f"Dialogue: 7,{ts(t0)},{ts(t1)},Hook,,0,0,0,,{{\\an5\\pos(540,{y + cap / 2 - off:.0f})"
                  f"\\fn{fonte_nome}\\fs{(asc100 + desc100) * k:.0f}\\bord0\\shad0\\1c{WHITE}}}{t}")
        y += cap + (vao * cb if i == 0 else 0.22 * cs)
    print(f"tarja: caixa {larg}x{h:.0f} em y={y0}-{y0 + h:.0f}, maiusculas {cb:.0f}/{cs:.0f} px, fonte {fonte_nome}")
    return ev


def chamada_block(t0, t1, ch):
    """Faixa de doacao depois do gancho ate a tela final.
    ch = {"linhas": [["APENAS R$ 5", 124], ["PODEM MUDAR A VIDA DO", 64], ["PEDRINHO GUERREIRO!", 84]], "y": 1300}
    Com "fixa": true, ch["linhas"] e uma lista de textos (o 1o e o valor) e a tarja fica parada."""
    if ch.get("fixa"):
        return tarja_fixa(t0, t1, ch["linhas"], ch.get("y", 1310), ch.get("largura", 760),
                          ch.get("fonte", ARIBLK), ch.get("fonte_nome", "Arial Black"), ch.get("vao", 0.24))
    return faixa(t0, t1, [(t, fs) for t, fs in ch["linhas"]], ch.get("y", 1300), fade=(180, 0))


def box_block(t0, t1, lines, cy, fs, color=None, pad_x=None, pad_y=None, fade=(90, 0)):
    """Gancho e tela final no mesmo visual da faixa de doacao (era caixa arredondada ate 26/10/2026)."""
    return faixa(t0, t1, [(l, fs) for l in lines], cy, fade=fade, layer=0)


def captions(words, limit, cap_y, red):
    """Palavra por palavra: blocos de ate 3 palavras / 15 letras; as proximas ficam invisiveis para nao pular."""
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) == 3 or len(" ".join(x[2] for x in cur + [w])) > 15 or cur[-1][3]
                    or w[0] - cur[-1][1] > 0.45):
            chunks.append(cur); cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    ev = []
    for ci, ch in enumerate(chunks):
        nxt = chunks[ci + 1][0][0] if ci + 1 < len(chunks) else ch[-1][1] + 0.6
        chunk_end = nxt if nxt - ch[-1][1] < 0.7 else ch[-1][1] + 0.35
        for wi, w in enumerate(ch):
            t0 = w[0]
            t1 = min(ch[wi + 1][0] if wi + 1 < len(ch) else chunk_end, limit)
            if t1 <= t0:
                continue
            parts = []
            for j, x in enumerate(ch):
                col = RED_C if x[2] in red else WHITE
                al = "&H00&" if j <= wi else "&HFF&"
                parts.append(f"{{\\1c{col}\\3a{al}\\1a{al}\\4a{'&H64&' if j <= wi else '&HFF&'}}}{x[2]}")
            pop = r"\fscx90\fscy90\t(0,90,\fscx100\fscy100)" if wi == 0 else ""
            ev.append(f"Dialogue: 2,{ts(t0)},{ts(t1)},Cap,,0,0,0,,{{\\an5\\pos(540,{cap_y}){pop}}}" + " ".join(parts))
    return ev


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    plan_path = os.path.abspath(a.plan)
    plan = json.load(open(plan_path, encoding="utf-8"))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
    import comum as C
    out = os.path.abspath(a.out) if a.out else C.destino(plan_path, plan, "cortes", chave="out")
    Builder(plan, os.path.dirname(plan_path), out).build()
