"""Estilo "narrado": narrador (ElevenLabs) alternando com falas reais, b-roll P&B, cartelas de impacto.

Blocos do plano (na ordem):
  real  - fala real (crianca/mae) em cor, varios cortes do mesmo bruto, etiqueta com quem fala
  narr  - narracao em cima de b-roll (P&B ou cor), imagens trocam em palavras da narracao
  card  - tela preta com numero gigante + boom
  end   - tela final com chamada e botao "SAIBA MAIS" (o botao do anuncio e "Saiba mais")

Uso: python -I narrado.py <plano.json> [--out x.mp4]
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
from comum import foto_em_pe  # noqa: E402
from comum import enc_antes_da_logo  # noqa: E402  passada antes da logo: rapida e quase sem perda (27/10/2026)

FPS, W, H = 30, 1080, 1920
STILL = (".jpg", ".jpeg", ".png", ".webp")
AUDIO = "aresample=48000,aformat=sample_fmts=s16:channel_layouts=stereo"
VOICE_FX = "highpass=f=80,afftdn=nr=10:nf=-42,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2"
NARR_FX = "highpass=f=60,acompressor=threshold=-18dB:ratio=2:attack=5:release=120"
LOOK = {"pb": "hue=s=0,eq=contrast=1.18:brightness=-0.02,vignette=angle=PI/4.5",
        "cor": "eq=saturation=1.05:contrast=1.05"}
WHITE, YELLOW, RED, BLACK = "&H00FFFFFF&", "&H0000D4FF&", "&H002904D9&", "&H00000000&"
CAP_Y, TAG_Y = 1150, 1035


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(" ".join(cmd)); print(r.stderr[-3000:]); sys.exit(1)
    return r


def fr(t):
    return round(t * FPS)


def loudness(args):
    r = subprocess.run(["ffmpeg", "-hide_banner"] + args + ["-f", "null", "-"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return float([l for l in r.stderr.splitlines() if l.strip().startswith("I:")][-1].split()[1])


def src_size(p):
    s = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:stream_side_data=rotation", "-of", "json", p]).stdout)["streams"][0]
    rot = next((d["rotation"] for d in s.get("side_data_list", []) if "rotation" in d), 0)
    return (s["height"], s["width"]) if abs(int(rot)) % 180 == 90 else (s["width"], s["height"])


def crop(spec, sw, sh):
    z = spec.get("z", 1.0)
    w, h = round(sw / z / 2) * 2, round(sh / z / 2) * 2
    cx, cy = spec.get("center", [sw / 2, sh / 2])
    return w, h, int(min(max(cx - w / 2, 0), sw - w)), int(min(max(cy - h / 2, 0), sh - h))


def resolve_cut(words, first, last):
    """Corte por palavras: [inicio da 1a palavra, inicio da ultima] -> (in, out, palavras)."""
    i = min(range(len(words)), key=lambda k: abs(words[k]["start"] - first))
    j = min(range(len(words)), key=lambda k: abs(words[k]["start"] - last))
    prev_end = words[i - 1]["end"] if i else 0.0
    next_start = words[j + 1]["start"] if j + 1 < len(words) else words[j]["end"] + 0.5
    t_in = max(words[i]["start"] - 0.07, prev_end + 0.02)
    t_out = min(words[j]["end"] + 0.10, next_start - 0.02)
    return t_in, t_out, words[i:j + 1]


def piece_frames(items, nf):
    """Itens com "until" (segundos dentro do bloco) acabam ali; os sem dividem o resto igualmente."""
    ends = [min(fr(it["until"]), nf) if "until" in it else None for it in items]
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
    # um "until" alem do fim do bloco (a narracao ficou mais curta sem os respiros) dava pedaco negativo e
    # a montagem caia (27/10/2026): limita cada fim ao bloco e garante pelo menos 1 quadro por imagem
    n = len(ends)
    for k in range(n):
        ends[k] = min(max(ends[k], (ends[k - 1] if k else 0) + 1), nf - (n - 1 - k))
    ends[-1] = nf
    return [e - s for s, e in zip([0] + ends[:-1], ends)]


class Build:
    def __init__(self, plan, plan_dir, out):
        self.p, self.dir, self.out = plan, plan_dir, out
        self.bank = plan.get("bank", "")
        self.work = os.path.join(tempfile.gettempdir(), "estilo-narrado", plan["nome"])
        shutil.rmtree(self.work, ignore_errors=True)
        os.makedirs(os.path.join(self.work, "fonts"))
        for f in ("ariblk.ttf", "arialbd.ttf", "seguisym.ttf"):
            shutil.copy(os.path.join(r"C:\Windows\Fonts", f), os.path.join(self.work, "fonts", f))
        self.n = 0
        self.segs, self.words, self.spans, self.T = [], [], [], 0.0

    def path(self, p):
        if os.path.isabs(p):
            return p
        for base in (self.dir, self.bank):
            if os.path.exists(os.path.join(base, p)):
                return os.path.join(base, p)
        sys.exit(f"arquivo nao encontrado: {p}")

    def encode(self, inputs, fc, d):
        out = os.path.join(self.work, f"s{self.n:03d}.mkv")
        self.n += 1
        run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]",
             "-t", f"{d:.4f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p",
             "-r", str(FPS), "-c:a", "pcm_s16le", out])
        self.segs.append(out)
        self.T += d

    def visual_chain(self, idx, it, nf, look, label):
        """Peca de b-roll: preenche 9:16, cor/P&B e aproximacao lenta (8%)."""
        kb = it.get("zoom", 0.08)
        return (f"[{idx}:v]fps={FPS},scale=1350:2400:force_original_aspect_ratio=increase,crop=1350:2400,"
                f"zoompan=z='1+{kb}*on/{max(nf, 1)}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
                f"{LOOK[look]},setsar=1,trim=end_frame={nf},setpts=PTS-STARTPTS[{label}]")

    def visual_input(self, it, nf):
        src, d = foto_em_pe(self.path(it["src"])), nf / FPS + 0.2
        if src.lower().endswith(STILL):
            return ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", src]
        return ["-ss", f"{it.get('start', 0.0):.3f}", "-t", f"{d:.3f}", "-an", "-i", src]

    # ---------------------------------------------------------------- blocos
    def real(self, b):
        src = self.path(b["src"])
        words = [w for w in json.load(open(self.path(b["tx"]), encoding="utf-8-sig"))["words"] if w["type"] == "word"]
        sw, sh = src_size(src)
        cuts = [resolve_cut(words, a, z) for a, z in b["cuts"]]
        gain = b.get("lufs", -16.0) - loudness(["-ss", f"{cuts[0][0]:.2f}", "-to", f"{cuts[-1][1]:.2f}", "-i", src,
                                                 "-vn", "-af", f"{VOICE_FX},ebur128"])
        t0 = self.T
        crops = b.get("crops", [{"z": 1.0}])
        for k, (a, z, ws) in enumerate(cuts):
            nf = fr(z - a); d = nf / FPS
            cw, ch, cx, cy = crop(crops[k % len(crops)], sw, sh)
            fc = (f"[0:v]fps={FPS},crop={cw}:{ch}:{cx}:{cy},scale={W}:{H}:flags=lanczos,{LOOK['cor']},setsar=1[v];"
                  f"[0:a]{AUDIO},{VOICE_FX},volume={gain:.2f}dB,afade=t=in:d=0.012,afade=t=out:st={d - 0.015:.4f}:d=0.015[a]")
            base = self.T
            self.encode(["-ss", f"{a:.3f}", "-t", f"{d:.4f}", "-i", src], fc, d)
            for w in ws:
                self.words.append([base + w["start"] - a, base + min(w["end"], z) - a, w["text"]])
        self.spans.append({"type": "real", "t0": t0, "t1": self.T, "tag": b.get("tag", "")})

    def narr(self, b):
        audio = self.path(b["audio"])
        al = json.load(open(os.path.splitext(audio)[0] + ".json", encoding="utf-8-sig"))
        adur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio]).stdout)
        nf = fr(adur + b.get("tail", 0.15)); d = nf / FPS
        gain = b.get("lufs", -16.0) - loudness(["-i", audio, "-af", f"{NARR_FX},ebur128"])
        items, look = b["broll"], b.get("look", "pb")
        inputs, chains, labels = [], [], ""
        for i, (it, n) in enumerate(zip(items, piece_frames(items, nf))):
            inputs += self.visual_input(it, n)
            chains.append(self.visual_chain(i, it, n, it.get("look", look), f"p{i}"))
            labels += f"[p{i}]"
        k = len(items)
        inputs += ["-i", audio]
        fc = (";".join(chains) + f";{labels}concat=n={k}:v=1:a=0[v];"
              f"[{k}:a]{AUDIO},{NARR_FX},volume={gain:.2f}dB,apad=whole_dur={d:.4f}[a]")
        base = self.T
        self.encode(inputs, fc, d)
        for w in al["words"]:
            self.words.append([base + w["start"], base + w["end"], b.get("fix", {}).get(w["text"], w["text"])])
        self.spans.append({"type": "narr", "t0": base, "t1": self.T, "look": look})

    def silent(self, kind, b, video_inputs, vfc):
        nf = fr(b.get("dur", 1.2)); d = nf / FPS
        base = self.T
        self.encode(video_inputs + ["-f", "lavfi", "-t", f"{d:.4f}", "-i", "anullsrc=r=48000:cl=stereo"],
                    vfc(nf) + f";[{len([x for x in video_inputs if x == '-i'])}:a]{AUDIO}[a]", d)
        self.spans.append({"type": kind, "t0": base, "t1": self.T, **{k: v for k, v in b.items() if k != "type"}})

    def card(self, b):
        self.silent("card", b, ["-f", "lavfi", "-t", f"{b.get('dur', 1.2) + 0.2:.3f}", "-i", f"color=c=black:s={W}x{H}:r={FPS}"],
                    lambda nf: f"[0:v]trim=end_frame={nf},setsar=1[v]")

    def end(self, b):
        it = b["broll"]
        nf = fr(b.get("dur", 3.5))
        self.silent("end", b, self.visual_input(it, nf),
                    lambda n: self.visual_chain(0, it, n, it.get("look", "cor"), "v"))

    # ---------------------------------------------------------------- legendas
    def ass(self, total):
        p = self.p
        fixes = {k.upper(): v for k, v in p.get("caption_fix", {}).items()}
        red = set(p.get("red", []))
        L = []
        # gancho: faixa vermelha de telejornal que entra deslizando
        hk = p.get("hook")
        if hk:
            # linhas: {"text", "fs"}; *trecho* em amarelo e pulsando. Etiqueta piscando em cima da faixa.
            t0, t1 = hk.get("t0", 0.0), hk["t1"]
            lines = [l if isinstance(l, dict) else {"text": l, "fs": 64} for l in hk["lines"]]
            pad = 26
            hh = 2 * pad + sum(int(l["fs"] * 1.02) for l in lines)
            y0 = hk.get("y", 1235)
            bar = f"m 0 {y0} l {W} {y0} {W} {y0 + hh} 0 {y0 + hh}"
            L.append(f"Dialogue: 5,{ts(t0)},{ts(t1)},Box,,0,0,0,,{{\\an7\\move(-1080,0,0,0,0,180)\\1c{RED}\\p1}}{bar}{{\\p0}}")
            for yy in (y0, y0 + hh - 8):
                L.append(f"Dialogue: 6,{ts(t0)},{ts(t1)},Box,,0,0,0,,{{\\an7\\move(1080,0,0,0,0,220)\\1c{YELLOW}\\p1}}"
                         f"m 0 {yy} l {W} {yy} {W} {yy + 8} 0 {yy + 8}{{\\p0}}")
            y = y0 + pad
            for i, l in enumerate(lines):
                fs = l["fs"]
                cy = y + fs * 0.51
                y += int(fs * 1.02)
                pulse = "".join(f"\\t({400 + k * 700},{750 + k * 700},\\fscx112\\fscy112)\\t({750 + k * 700},{1100 + k * 700},\\fscx100\\fscy100)"
                                for k in range(int((t1 - t0) / 0.7)))
                styled = re.sub(r"\*([^*]+)\*", lambda m: f"{{\\1c{YELLOW}{pulse}}}{m.group(1)}{{\\1c{WHITE}\\fscx100\\fscy100}}", l["text"])
                pop = r"\fscx140\fscy140\t(150,330,\fscx100\fscy100)" if i == 0 else r"\fad(250,0)"
                L.append(f"Dialogue: 7,{ts(t0)},{ts(t1)},Txt,,0,0,0,,{{\\an5\\pos(540,{cy:.0f}){pop}\\fs{fs}}}{styled}")
            label = hk.get("label")
            if label:
                lw = int(len(label) * 37 + 70)
                k, t = 0, t0
                while t < t1:   # pisca: 0,45 s acesa, 0,2 s apagada
                    te = min(t + 0.45, t1)
                    L.append(f"Dialogue: 8,{ts(t)},{ts(te)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\1c{WHITE}\\p1}}"
                             f"{rrect((W - lw) // 2, y0 - 36, lw, 72, 14)}{{\\p0}}")
                    L.append(f"Dialogue: 9,{ts(t)},{ts(te)},Txt,,0,0,0,,{{\\an5\\pos(540,{y0})\\fs52\\1c{RED}\\4a&HFF&}}{label}")
                    t, k = te + 0.2, k + 1
        # clarao branco na troca de bloco. Etiqueta de quem fala so com "etiquetas": true no plano:
        # o usuario pediu (25/10/2026) para tirar "PEDRINHO" / "MAE DO PEDRINHO" da tela
        prev = None
        for s in self.spans:
            if p.get("etiquetas", False) and s["type"] == "real" and s.get("tag"):
                w = int(len(s["tag"]) * 31 + 70)
                L.append(f"Dialogue: 3,{ts(s['t0'])},{ts(s['t1'])},Box,,0,0,0,,{{\\an7\\pos(0,0)\\fad(120,0)\\1c{RED}\\p1}}"
                         f"{rrect((W - w) // 2, TAG_Y - 34, w, 68, 16)}{{\\p0}}")
                L.append(f"Dialogue: 4,{ts(s['t0'])},{ts(s['t1'])},Txt,,0,0,0,,{{\\an5\\pos(540,{TAG_Y})\\fs44\\fad(120,0)}}{s['tag']}")
            if prev and prev["type"] != s["type"]:
                L.append(f"Dialogue: 9,{ts(s['t0'])},{ts(s['t0'] + 0.16)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\fad(0,130)\\1c{WHITE}\\1a&H30&\\p1}}"
                         f"m 0 0 l {W} 0 {W} {H} 0 {H}{{\\p0}}")
            if s["type"] == "card":
                big, small = s["lines"][0], s["lines"][1] if len(s["lines"]) > 1 else ""
                pop = r"\fscx135\fscy135\t(0,160,\fscx100\fscy100)"
                L.append(f"Dialogue: 6,{ts(s['t0'])},{ts(s['t1'])},Txt,,0,0,0,,{{\\an5\\pos(540,{900 if small else 960}){pop}\\fs{s.get('fs', 230)}\\1c{RED}}}{big}")
                if small:
                    L.append(f"Dialogue: 6,{ts(s['t0'] + 0.12)},{ts(s['t1'])},Txt,,0,0,0,,{{\\an5\\pos(540,1110)\\fad(120,0)\\fs96}}{small}")
            if s["type"] == "end":
                L.append(f"Dialogue: 2,{ts(s['t0'])},{ts(s['t1'])},Box,,0,0,0,,{{\\an7\\pos(0,0)\\fad(250,0)\\1c{BLACK}\\1a&H60&\\p1}}"
                         f"m 0 0 l {W} 0 {W} {H} 0 {H}{{\\p0}}")
                for i, line in enumerate(s["lines"]):
                    styled = re.sub(r"\*([^*]+)\*", lambda m: f"{{\\1c{YELLOW}}}{m.group(1)}{{\\1c{WHITE}}}", line)
                    L.append(f"Dialogue: 6,{ts(s['t0'] + 0.1 * i)},{ts(s['t1'])},Txt,,0,0,0,,{{\\an5\\pos(540,{760 + 120 * i})\\fad(200,0)\\fs104}}{styled}")
                by = 760 + 120 * len(s["lines"]) + 90
                pulse = "".join(f"\\t({k * 700},{k * 700 + 350},\\fscx106\\fscy106)\\t({k * 700 + 350},{k * 700 + 700},\\fscx100\\fscy100)" for k in range(6))
                # desenho em coordenada absoluta (\an7 + \pos(0,0)); \org no centro do botao para o pulso
                L.append(f"Dialogue: 6,{ts(s['t0'] + 0.4)},{ts(s['t1'])},Box,,0,0,0,,{{\\an7\\pos(0,0)\\org(540,{by})\\fad(150,0){pulse}\\1c{RED}\\p1}}"
                         f"{rrect(210, by - 62, 660, 124, 62)}{{\\p0}}")
                L.append(f"Dialogue: 7,{ts(s['t0'] + 0.4)},{ts(s['t1'])},Txt,,0,0,0,,{{\\an5\\pos(540,{by})\\fad(150,0){pulse}\\fs64}}"
                         f"{s.get('button', 'SAIBA MAIS')} {{\\fnSegoe UI Symbol}}♥")
            prev = s
        # legenda: bloco inteiro na tela, palavra falada em amarelo e um pouco maior
        chunks, cur = [], []
        for w in self.words:
            txt = w[2].strip(",.!?…\"")
            t = fixes.get(txt.upper(), txt.upper())
            item = (w[0], w[1], t, w[2][-1:] in ",.!?…")
            if cur and (len(cur) == 3 or len(" ".join(x[2] for x in cur + [item])) > 16 or cur[-1][3] or item[0] - cur[-1][1] > 0.45):
                chunks.append(cur); cur = []
            cur.append(item)
        if cur:
            chunks.append(cur)
        blocked = [(s["t0"], s["t1"]) for s in self.spans if s["type"] in ("card", "end")]
        for ci, ch in enumerate(chunks):
            nxt = chunks[ci + 1][0][0] if ci + 1 < len(chunks) else ch[-1][1] + 0.4
            end = nxt if nxt - ch[-1][1] < 0.6 else ch[-1][1] + 0.3
            for wi, w in enumerate(ch):
                t0, t1 = w[0], (ch[wi + 1][0] if wi + 1 < len(ch) else end)
                for b0, b1 in blocked:
                    if t0 < b0 < t1:
                        t1 = b0
                if t1 <= t0:
                    continue
                parts = []
                for j, x in enumerate(ch):
                    if j == wi:
                        parts.append(f"{{\\1c{YELLOW}\\fscx112\\fscy112}}{x[2]}{{\\fscx100\\fscy100}}")
                    else:
                        parts.append(f"{{\\1c{RED if x[2] in red else WHITE}}}{x[2]}")
                L.append(f"Dialogue: 2,{ts(t0)},{ts(t1)},Cap,,0,0,0,,{{\\an5\\pos(540,{CAP_Y})}}" + " ".join(parts))
        head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Arial Black,84,&H00FFFFFF,&H000000FF,&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,6,4,5,0,0,0,1
Style: Box,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Txt,Arial Black,60,&H00FFFFFF,&H000000FF,&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,0,3,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        path = os.path.join(self.work, "legendas.ass")
        open(path, "w", encoding="utf-8-sig").write(head + "\n".join(L) + "\n")
        return path

    # ---------------------------------------------------------------- principal
    def build(self):
        for b in self.p["blocks"]:
            getattr(self, b["type"])(b)
            print(f"{b['type']:5} ok  t={self.T:6.2f}")
        total = self.T
        concat = os.path.join(self.work, "concat.txt")
        open(concat, "w", encoding="utf-8").writelines(f"file '{s}'\n" for s in self.segs)
        aroll = os.path.join(self.work, "aroll.mkv")
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", concat, "-c", "copy", aroll])
        ass = self.ass(total)

        # audio em passe separado (loudnorm/filtros longos no grafo do video ja abriram buraco no audio)
        p = self.p
        lifts = [s for s in self.spans if s["type"] in ("card", "end")]
        lift = "+".join(f"between(t,{s['t0']:.2f},{s['t1']:.2f})" for s in lifts) or "0"
        mv, mh = p.get("music_vol", 0.10), p.get("music_lift", 0.14)
        fx_in, fx_chain, k = [], [], 2
        for s in self.spans:
            hits = []
            if s["type"] == "narr":
                hits.append(("whoosh", s["t0"] - 0.25, 0.45))
            if s["type"] == "card":
                hits.append(("boom", s["t0"], 0.9))
            for name, t, vol in hits:
                fx = os.path.join(self.dir, "audio", f"fx_{name}.mp3")
                if os.path.exists(fx) and t >= 0:
                    fx_in += ["-i", fx]
                    fx_chain.append(f"[{k}:a]{AUDIO},volume={vol},adelay={int(t * 1000)}|{int(t * 1000)},apad[f{k}]")
                    k += 1
        fx_labels = "".join(f"[f{i}]" for i in range(2, k))
        fa = (f"[0:a]anull[voz];[1:a]{AUDIO},volume='{mv}+{mh}*({lift})':eval=frame,afade=t=in:d=0.5,"
              f"afade=t=out:st={total - 1.5:.2f}:d=1.5[mus];" + "".join(c + ";" for c in fx_chain) +
              f"[voz][mus]{fx_labels}amix=inputs={2 + len(fx_chain)}:duration=first:normalize=0,alimiter=limit=0.89[a]")
        mix = os.path.join(self.work, "mix.wav")
        ms = ["-ss", f"{p.get('music_start', 0.0):.2f}"]
        run(["ffmpeg", "-v", "error", "-y", "-i", aroll] + ms + ["-i", p["music"]] + fx_in +
            ["-filter_complex", fa, "-map", "[a]", "-t", f"{total:.4f}", "-c:a", "pcm_s16le", mix])
        run(["ffmpeg", "-v", "error", "-y", "-i", aroll, "-i", mix, "-filter_complex",
             "[0:v]subtitles=legendas.ass:fontsdir=fonts,format=yuv420p[v]", "-map", "[v]", "-map", "1:a",
             "-t", f"{total:.4f}", *enc_antes_da_logo(), "-profile:v", "high",
             "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
             self.out], cwd=self.work)
        shutil.copy(ass, os.path.join(self.dir, "legendas.ass"))
        json.dump({"total": total, "blocos": self.spans, "palavras": self.words},
                  open(os.path.join(self.dir, "linha_do_tempo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        r = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "packet=pts_time,duration_time",
                 "-of", "csv=p=0", self.out])
        pk = [tuple(map(float, l.split(",")[:2])) for l in r.stdout.split() if l]
        holes = [(round(a[0], 2), round(b[0], 2)) for a, b in zip(pk, pk[1:]) if b[0] - a[0] - a[1] > 0.02]
        print(f"audio: {pk[-1][0] + pk[-1][1]:.2f}s  buracos={holes or 'nenhum'}")
        import marca  # logo SOS andando pela tela, opacidade baixa (26/10/2026)
        marca.no_fim(self.p, self.out)
        print(f"OK {self.out}  duracao={total:.2f}s")


def ts(t):
    cs = int(round(max(0.0, t) * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def rrect(x, y, w, h, r):
    X, Y = x + w, y + h
    return (f"m {x + r} {y} l {X - r} {y} b {X} {y} {X} {y} {X} {y + r} l {X} {Y - r} b {X} {Y} {X} {Y} {X - r} {Y} "
            f"l {x + r} {Y} b {x} {Y} {x} {Y} {x} {Y - r} l {x} {y + r} b {x} {y} {x} {y} {x + r} {y}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    pp = os.path.abspath(a.plan)
    plan = json.load(open(pp, encoding="utf-8-sig"))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
    import comum as C
    out = os.path.abspath(a.out) if a.out else C.destino(pp, plan, "narrado", chave="out")
    Build(plan, os.path.dirname(pp), out).build()
