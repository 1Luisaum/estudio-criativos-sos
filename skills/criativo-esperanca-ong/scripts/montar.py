"""Estilo "Da dor a esperanca" (criado em 27/10/2026): comeca muito impactante, desenvolve e acaba feliz.

Ato 1 - IMPACTO: cartela em P&B com batida de coracao e palavras gigantes entrando uma a uma; fala real de dor.
Ato 2 - DESENVOLVE: narrador + falas reais, ainda em P&B, musica tensa.
Virada: clarao branco + whoosh, a imagem ganha cor e a musica troca para uma esperancosa.
Ato 3 - ESPERANCA: momentos felizes em cor, fala de forca da crianca, pedido e tela final calorosa.

Blocos do plano: cartela | real | narr | vo | fim  (ver o plano de exemplo).
Uso: python -I montar.py plano.json
"""
import json
import os
import shutil
import subprocess
import sys

from PIL import ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
from comum import enc_antes_da_logo  # noqa: E402  passada antes da logo: rapida e quase sem perda (27/10/2026)

W, H, FPS = 1080, 1920, 30
F = "C:/Windows/Fonts/"
STILL = (".jpg", ".jpeg", ".png", ".webp")
AUD = "aresample=48000,aformat=sample_fmts=s16:channel_layouts=stereo"
VOZ_FX = "highpass=f=80,afftdn=nr=10:nf=-42,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2"
LOOK = {"pb": "hue=s=0,eq=contrast=1.16:brightness=-0.03,vignette=angle=PI/4.5",
        "cor": "eq=saturation=1.08:contrast=1.04,colorbalance=rm=0.04:bm=-0.03"}
WHITE, YELLOW, RED = "&H00FFFFFF&", "&H0000D4FF&", "&H002A2AFF&"
CAP_Y = 1150


def run(cmd, cwd=None):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd)
    if r.returncode:
        print(" ".join(cmd[:8])); print(r.stderr[-2500:])
        sys.exit("ffmpeg falhou")
    return r


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout)


def loud(args):
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


class Montador:
    def __init__(self, pp):
        self.pp = pp
        self.P = os.path.dirname(pp)
        self.p = json.load(open(pp, encoding="utf-8"))
        self.WK = os.path.join(self.P, "render")
        shutil.rmtree(self.WK, ignore_errors=True)
        os.makedirs(os.path.join(self.WK, "fonts"))
        for f in ("ariblk.ttf", "seguiemj.ttf", "seguisym.ttf"):
            shutil.copy(F + f, os.path.join(self.WK, "fonts", f))
        self.n, self.T = 0, 0.0
        self.segs, self.words, self.spans, self.fx = [], [], [], []

    def path(self, p):
        if os.path.isabs(p):
            return p
        for base in (self.P, self.p.get("banco", "")):
            if os.path.exists(os.path.join(base, p)):
                return os.path.join(base, p)
        sys.exit(f"arquivo nao encontrado: {p}")

    def encode(self, inputs, fc, d):
        out = os.path.join(self.WK, f"s{self.n:03d}.mkv")
        self.n += 1
        run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]",
             "-t", f"{d:.4f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-pix_fmt", "yuv420p",
             "-r", str(FPS), "-c:a", "pcm_s16le", out])
        self.segs.append(out)
        self.T += d

    # -------- pecas visuais
    def visual(self, idx, it, nf, look, label, kb=0.06):
        src = self.path(it["src"])
        if src.lower().endswith(STILL):
            inp = ["-loop", "1", "-framerate", str(FPS), "-t", f"{nf / FPS + 0.2:.3f}", "-i", src]
            ch = (f"[{idx}:v]scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
                  f"zoompan=z='1+{it.get('zoom', kb)}*on/{max(nf, 1)}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                  f"d=1:s={W}x{H}:fps={FPS},{LOOK[look]},setsar=1,trim=end_frame={nf},setpts=PTS-STARTPTS[{label}]")
        else:
            inp = ["-ss", f"{it.get('start', 0):.3f}", "-t", f"{nf / FPS + 0.2:.3f}", "-an", "-i", src]
            ch = (f"[{idx}:v]fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                  f"{LOOK[look]},setsar=1,trim=end_frame={nf},setpts=PTS-STARTPTS[{label}]")
        return inp, ch

    def broll(self, items, d, look):
        nf = round(d * FPS)
        ends = [round(it["ate"] * FPS) if "ate" in it else None for it in items]
        ends[-1] = nf
        # itens sem "ate" dividem igualmente o que sobra
        i, prev, frames = 0, 0, []
        while i < len(ends):
            j = i
            while ends[j] is None:
                j += 1
            k = j - i + 1
            base, rest = divmod(ends[j] - prev, k)
            for q in range(k):
                frames.append(base + (1 if q < rest else 0))
            prev, i = ends[j], j + 1
        inputs, chains, labels = [], [], ""
        for q, (it, f) in enumerate(zip(items, frames)):
            inp, ch = self.visual(q, it, f, it.get("look", look), f"p{q}")
            inputs += inp; chains.append(ch); labels += f"[p{q}]"
        return inputs, ";".join(chains) + f";{labels}concat=n={len(items)}:v=1:a=0[v]", len(items)

    def gain(self, args, alvo=-16.0):
        return alvo - loud(args)

    # -------- blocos
    def cartela(self, b):
        d = b["dur"]
        inp, ch = self.visual(0, {"src": b["foto"], "zoom": b.get("zoom", 0.18)}, round(d * FPS), b.get("look", "pb"), "v")
        t0 = self.T
        if b.get("audio"):  # narracao no hook, entrando em audio_inicio
            audio = self.path(os.path.join("audio", b["audio"] + ".mp3"))
            g = self.gain(["-i", audio, "-af", "ebur128"])
            ms = int(b.get("audio_inicio", 0.0) * 1000)
            self.encode(inp + ["-i", audio], ch + f";[1:a]{AUD},volume={g:.2f}dB,adelay={ms}:all=1,apad=whole_dur={d:.4f}[a]", d)
        else:
            self.encode(inp + ["-f", "lavfi", "-t", f"{d:.3f}", "-i", "anullsrc=r=48000:cl=stereo"],
                        ch + f";[1:a]{AUD}[a]", d)
        self.spans.append({"tipo": "cartela", "t0": t0, "t1": self.T, "palavras": b["palavras"], "y": b.get("palavras_y", 1350)})
        for nome, t in b.get("fx", []):
            self.fx.append((nome, t0 + t))

    def real(self, b):
        src = self.path(b["src"])
        words = [w for w in json.load(open(self.path(b["tx"]), encoding="utf-8-sig"))["words"] if w["type"] == "word"]
        sw, sh = src_size(src)
        g = self.gain(["-ss", f"{b['cortes'][0][0]:.2f}", "-to", f"{b['cortes'][-1][1]:.2f}", "-i", src, "-vn",
                       "-af", f"{VOZ_FX},ebur128"])
        crops = b.get("crops", [{"z": 1.0}])
        t_ini = self.T
        for k, (a, z) in enumerate(b["cortes"]):
            d = round((z - a) * FPS) / FPS
            cw, chh, cx, cy = crop(crops[k % len(crops)], sw, sh)
            fc = (f"[0:v]fps={FPS},crop={cw}:{chh}:{cx}:{cy},scale={W}:{H}:flags=lanczos,{LOOK[b.get('look', 'cor')]},setsar=1[v];"
                  f"[0:a]{AUD},{VOZ_FX},volume={g:.2f}dB,afade=t=in:d=0.012,afade=t=out:st={d - 0.02:.4f}:d=0.02[a]")
            base = self.T
            self.encode(["-ss", f"{a:.3f}", "-t", f"{d:.4f}", "-i", src], fc, d)
            for w in words:
                if a <= (w["start"] + w["end"]) / 2 <= z:
                    self.words.append([base + w["start"] - a, base + min(w["end"], z) - a, w["text"]])
        self.spans.append({"tipo": "real", "t0": t_ini, "t1": self.T})

    def narr(self, b):
        audio = self.path(os.path.join("audio", b["audio"] + ".mp3"))
        al = json.load(open(audio[:-4] + ".json", encoding="utf-8-sig"))
        d = round((dur(audio) + b.get("folga", 0.2)) * FPS) / FPS
        g = self.gain(["-i", audio, "-af", "ebur128"])
        inputs, fc, k = self.broll(b["broll"], d, b.get("look", "pb"))
        base = self.T
        self.encode(inputs + ["-i", audio], fc + f";[{k}:a]{AUD},volume={g:.2f}dB,apad=whole_dur={d:.4f}[a]", d)
        for w in al["words"]:
            self.words.append([base + w["start"], base + w["end"], b.get("fix", {}).get(w["text"], w["text"])])
        self.spans.append({"tipo": "narr", "t0": base, "t1": self.T, "look": b.get("look", "pb")})
        for nome, t in b.get("fx", []):
            self.fx.append((nome, base + t))

    def vo(self, b):
        """Fala real (so o audio) por cima de b-roll."""
        src = self.path(b["src"])
        words = [w for w in json.load(open(self.path(b["tx"]), encoding="utf-8-sig"))["words"] if w["type"] == "word"]
        g = self.gain(["-ss", f"{b['cortes'][0][0]:.2f}", "-to", f"{b['cortes'][-1][1]:.2f}", "-i", src, "-vn",
                       "-af", f"{VOZ_FX},ebur128"])
        wav = os.path.join(self.WK, f"vo{self.n:03d}.wav")
        parts, labels, acc, timed = [], "", 0.0, []
        cmd = ["ffmpeg", "-v", "error", "-y"]
        for k, (a, z) in enumerate(b["cortes"]):
            cmd += ["-ss", f"{a:.3f}", "-t", f"{z - a:.3f}", "-i", src]
            parts.append(f"[{k}:a]{AUD},{VOZ_FX},volume={g:.2f}dB,afade=t=in:d=0.015,afade=t=out:st={z - a - 0.03:.3f}:d=0.03[c{k}]")
            labels += f"[c{k}]"
            for w in words:
                if a <= (w["start"] + w["end"]) / 2 <= z:
                    timed.append([acc + w["start"] - a, acc + min(w["end"], z) - a, w["text"]])
            acc += z - a
        run(cmd + ["-filter_complex", ";".join(parts) + f";{labels}concat=n={len(b['cortes'])}:v=0:a=1[a]",
                   "-map", "[a]", "-c:a", "pcm_s16le", wav])
        d = round((acc + b.get("folga", 0.25)) * FPS) / FPS
        inputs, fc, k = self.broll(b["broll"], d, b.get("look", "cor"))
        base = self.T
        self.encode(inputs + ["-i", wav], fc + f";[{k}:a]{AUD},apad=whole_dur={d:.4f}[a]", d)
        self.words += [[base + a, base + z, t] for a, z, t in timed]
        self.spans.append({"tipo": "vo", "t0": base, "t1": self.T})

    def fim(self, b):
        d = b["dur"]
        inp, ch = self.visual(0, {"src": b["foto"], "zoom": 0.06}, round(d * FPS), "cor", "v")
        t0 = self.T
        self.encode(inp + ["-f", "lavfi", "-t", f"{d:.3f}", "-i", "anullsrc=r=48000:cl=stereo"],
                    ch + f";[1:a]{AUD}[a]", d)
        self.spans.append({"tipo": "fim", "t0": t0, "t1": self.T, "linhas": b["linhas"], "cta": b.get("cta", "")})

    # -------- legendas e graficos (ASS)
    def ass(self, total):
        p = self.p
        L = []
        virada = p.get("virada_bloco")
        for i, s in enumerate(self.spans):
            if s["tipo"] == "cartela":
                ps = s["palavras"]
                for k, (txt, t, cor, fs) in enumerate(ps):
                    a = s["t0"] + t
                    z = s["t0"] + ps[k + 1][1] if k + 1 < len(ps) else s["t1"]
                    c = RED if cor == "vermelho" else WHITE
                    L.append(f"Dialogue: 6,{ts(a)},{ts(z)},Big,,0,0,0,,{{\\an5\\pos(540,{s['y']})\\fs{fs}\\1c{c}"
                             f"\\fscx160\\fscy160\\t(0,140,\\fscx100\\fscy100)}}{txt}")
            if s["tipo"] == "fim":
                L.append(f"Dialogue: 2,{ts(s['t0'])},{ts(s['t1'])},Box,,0,0,0,,{{\\an7\\pos(0,0)\\fad(300,0)\\1c&H000000&\\1a&H70&\\p1}}"
                         f"m 0 0 l {W} 0 {W} {H} 0 {H}{{\\p0}}")
                for k, ln in enumerate(s["linhas"]):
                    txt = ln.replace("*", "")
                    st = f"{{\\1c{YELLOW}}}" if ln.startswith("*") else ""
                    L.append(f"Dialogue: 6,{ts(s['t0'] + 0.15 * k)},{ts(s['t1'])},Big,,0,0,0,,{{\\an5\\pos(540,{1180 + 120 * k})"
                             f"\\fad(250,0)\\fs100}}{st}{txt}")
                if s["cta"]:
                    L.append(f"Dialogue: 6,{ts(s['t0'] + 0.5)},{ts(s['t1'])},Cta,,0,0,0,,{{\\an5\\pos(540,{1180 + 120 * len(s['linhas']) + 40})"
                             f"\\fad(200,0)}}{s['cta']} {{\\fnSegoe UI Symbol\\1c{RED}}}♥")
            if virada is not None and i == virada:
                L.append(f"Dialogue: 9,{ts(s['t0'])},{ts(s['t0'] + 0.28)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\fad(0,220)\\1c{WHITE}\\p1}}"
                         f"m 0 0 l {W} 0 {W} {H} 0 {H}{{\\p0}}")
        # legenda em UMA linha: blocos de ate 3 palavras, palavra falada em amarelo
        fonte = ImageFont.truetype(F + "ariblk.ttf", 100)
        chunks, cur = [], []
        for w in self.words:
            t = w[2].strip(",.!?…\"").upper()
            if not t:
                continue
            item = (w[0], w[1], t, w[2][-1:] in ",.!?…")
            if cur and (len(cur) == 3 or cur[-1][3] or item[0] - cur[-1][1] > 0.45):
                chunks.append(cur); cur = []
            cur.append(item)
        if cur:
            chunks.append(cur)
        bloqueado = [(s["t0"], s["t1"]) for s in self.spans if s["tipo"] in ("cartela", "fim")]
        for ci, ch in enumerate(chunks):
            texto = " ".join(x[2] for x in ch)
            largura84 = fonte.getlength(texto) * (84 / 1.41) / 100  # no ASS, \fs e a altura da linha (1,41 em)
            fs = min(84, int(84 * 980 / max(largura84, 1)))  # sempre UMA linha: a letra diminui ate caber
            nxt = chunks[ci + 1][0][0] if ci + 1 < len(chunks) else ch[-1][1] + 0.4
            fimc = nxt if nxt - ch[-1][1] < 0.6 else ch[-1][1] + 0.3
            for wi, w in enumerate(ch):
                a, z = w[0], (ch[wi + 1][0] if wi + 1 < len(ch) else fimc)
                for b0, b1 in bloqueado:
                    if a < b0 < z:
                        z = b0
                if z <= a:
                    continue
                parts = [f"{{\\1c{YELLOW}}}{x[2]}" if j == wi else f"{{\\1c{WHITE}}}{x[2]}" for j, x in enumerate(ch)]
                L.append(f"Dialogue: 3,{ts(a)},{ts(z)},Cap,,0,0,0,,{{\\an5\\pos(540,{CAP_Y})\\fs{fs}}}" + " ".join(parts))
        head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Arial Black,84,&H00FFFFFF,&H000000FF,&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,6,4,5,0,0,0,1
Style: Big,Arial Black,150,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,7,6,5,0,0,0,1
Style: Cta,Arial Black,60,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,3,5,0,0,0,1
Style: Box,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        path = os.path.join(self.WK, "legendas.ass")
        open(path, "w", encoding="utf-8-sig").write(head + "\n".join(L) + "\n")
        return path

    # -------- principal
    def fecha_frase(self):
        """A legenda nunca junta o fim de um bloco com o comeco do proximo."""
        if self.words and self.words[-1][2][-1:] not in ",.!?…":
            self.words[-1][2] += "."

    def montar(self):
        p = self.p
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import comum as C
        saida = C.destino(self.pp, p, p.get("pasta_saida", "DA DOR À ESPERANÇA"))
        for b in p["blocos"]:
            getattr(self, b["tipo"])(b)
            self.fecha_frase()
            print(f"{b['tipo']:7} ok  t={self.T:6.2f}")
        total = self.T
        virada_t = self.spans[p["virada_bloco"]]["t0"]
        concat = os.path.join(self.WK, "concat.txt")
        open(concat, "w", encoding="utf-8").writelines(f"file '{s}'\n" for s in self.segs)
        aroll = os.path.join(self.WK, "aroll.mkv")
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", concat, "-c", "copy", aroll])
        self.ass(total)

        # audio: voz + musica tensa ate a virada + musica esperancosa depois + efeitos
        fim_t = next(s["t0"] for s in self.spans if s["tipo"] == "fim")
        mt, me = p["musica_tensa"], p["musica_esperanca"]
        v_t, v_e, v_fim = p.get("vol_tensa", 0.12), p.get("vol_esperanca", 0.13), p.get("vol_fim", 0.42)
        ins = ["-i", aroll, "-ss", f"{p.get('tensa_inicio', 0):.2f}", "-i", mt, "-ss", f"{p.get('esperanca_inicio', 0):.2f}", "-i", me]
        fc = [f"[0:a]anull[voz]",
              f"[1:a]{AUD},atrim=0:{virada_t + 0.6:.3f},volume={v_t},afade=t=in:d=0.3,afade=t=out:st={virada_t - 0.2:.3f}:d=0.8[mt]",
              f"[2:a]{AUD},atrim=0:{total - virada_t:.3f},volume='{v_e}+{v_fim - v_e:.3f}*clip((t-{fim_t - virada_t - 0.3:.3f})/0.8,0,1)':eval=frame,"
              f"afade=t=in:d=0.8,afade=t=out:st={total - virada_t - 1.5:.3f}:d=1.5,adelay={int(virada_t * 1000)}:all=1[me]"]
        labels, k = "[voz][mt][me]", 3
        vols = {"coracao": 0.9, "boom": 0.8, "whoosh": 0.6}
        for nome, t in self.fx:
            f = os.path.join(self.P, "audio", f"fx_{nome}.mp3")
            if os.path.exists(f) and t >= 0:
                ins += ["-i", f]
                fc.append(f"[{k}:a]{AUD},volume={vols.get(nome, 0.7)},adelay={int(t * 1000)}:all=1[f{k}]")
                labels += f"[f{k}]"; k += 1
        fc.append(f"{labels}amix=inputs={k}:duration=first:normalize=0,alimiter=limit=0.89[a]")
        mix = os.path.join(self.WK, "mix.wav")
        run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fc), "-map", "[a]",
             "-t", f"{total:.4f}", "-c:a", "pcm_s16le", mix])
        run(["ffmpeg", "-v", "error", "-y", "-i", aroll, "-i", mix, "-filter_complex",
             "[0:v]subtitles=legendas.ass:fontsdir=fonts,format=yuv420p[v]", "-map", "[v]", "-map", "1:a",
             "-t", f"{total:.4f}", *enc_antes_da_logo(), "-pix_fmt", "yuv420p",
             "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida], cwd=self.WK)
        shutil.copy(os.path.join(self.WK, "legendas.ass"), os.path.join(self.P, "legendas.ass"))
        json.dump({"total": total, "virada": virada_t, "blocos": self.spans, "palavras": self.words},
                  open(os.path.join(self.P, "linha_do_tempo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        import marca  # logo SOS obrigatoria em todo video (26/10/2026); nao ha excecao na skill
        marca.no_fim(p, saida)
        print(f"OK {saida} duracao={total:.1f}s virada={virada_t:.1f}s")


def ts(t):
    cs = int(round(max(0.0, t) * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    Montador(os.path.abspath(sys.argv[1])).montar()
