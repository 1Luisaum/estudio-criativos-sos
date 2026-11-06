"""Copia os scripts das skills para _folhas/scripts_v3 e aplica as correcoes pedidas em 26/10/2026 (sem mexer nas skills):
travadinha, produtos sem panoramica, "gaze" falado "gáze", foto deitada, respiro do narrador, chamada so no alto,
legenda e etiqueta dentro da zona segura. Quando o usuario mandar salvar, estes arquivos voltam para as skills."""
import os, re, shutil, sys

S = os.path.join(os.path.expanduser("~"), ".claude", "skills")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts_v3")
SKILLS = ["criativo-lista-ong", "criativo-vsl-voz-ong", "criativo-reportagem-ong", "criativo-narrado-ong", "edicao-criativo-ong"]
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
for s in SKILLS:
    shutil.copytree(os.path.join(S, s, "scripts"), os.path.join(OUT, s), ignore=shutil.ignore_patterns("__pycache__"))


def troca(path, pares):
    txt = open(path, encoding="utf-8").read()
    for old, new, n in pares:
        c = len(re.findall(old, txt, flags=re.S)) if n < 0 else txt.count(old)
        if c != abs(n):
            sys.exit(f"{path}: esperava {abs(n)}x, achei {c}x: {old[:80]}")
        txt = re.sub(old, lambda m: new, txt, flags=re.S) if n < 0 else txt.replace(old, new)
    open(path, "w", encoding="utf-8", newline="\n").write(txt)


# ------------------------------------------------------------------ comum.py (igual em todas)
COMUM_EXTRA = r'''

# ---------- pronuncia ----------
GAZE_RE = re.compile(r"\b(g)aze(s?)\b", re.I)


def _voz_extra(texto):
    """'gaze' se le 'gáze' (nao 'gueize'); a legenda continua escrita 'gaze'."""
    return GAZE_RE.sub(lambda m: m.group(1) + "áze" + m.group(2), texto)


# ---------- respiro do narrador ----------
def respiros(mp3, limiar=-40, minimo=0.12):
    """Trechos sem fala (respiro e silencio) maiores que `minimo` segundos: [(inicio, fim)]."""
    import subprocess
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp3, "-af", f"silencedetect=n={limiar}dB:d={minimo}",
                        "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    ini = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", r.stderr)]
    fim = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    dur = _duracao(mp3)
    return [(max(0.0, a), fim[i] if i < len(fim) else dur) for i, a in enumerate(ini)]


def _duracao(mp3):
    import subprocess
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def sem_respiro(src, dst, words=None, deixa=0.05):
    """Tira respiros e silencios da fala gerada (deixa `deixa` s em cada emenda; corta tudo no inicio e no fim).
    Com `words` (tempo por palavra), devolve as palavras com o tempo reajustado."""
    import subprocess
    dur = _duracao(src)
    cortes = []
    for a, b in respiros(src):
        if a <= 0.01:
            cortes.append((0.0, b))
        elif b >= dur - 0.01:
            cortes.append((a, dur))
        elif b - a > deixa:
            cortes.append((a + deixa / 2, b - deixa / 2))
    keep, t = [], 0.0
    for a, b in cortes:
        if a > t:
            keep.append((t, a))
        t = max(t, b)
    if t < dur:
        keep.append((t, dur))
    if not keep:
        keep = [(0.0, dur)]
    fc = ";".join(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS[k{i}]" for i, (a, b) in enumerate(keep))
    fc += ";" + "".join(f"[k{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[a]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", fc, "-map", "[a]",
                    "-c:a", "libmp3lame", "-b:a", "192k", dst], check=True)
    if words is None:
        return None

    def novo(t):
        tirado = 0.0
        for a, b in cortes:
            if t >= b:
                tirado += b - a
            elif t > a:
                return a - tirado
        return t - tirado
    return [{**w, "start": round(novo(w["start"]), 3), "end": round(max(novo(w["end"]), novo(w["start"]) + 0.05), 3)}
            for w in words]


# ---------- foto deitada ----------
def foto_em_pe(path):
    """Foto com rotacao gravada pela camera (EXIF) vira uma copia em pe; as outras voltam como estao."""
    import hashlib, tempfile
    if not path.lower().endswith((".jpg", ".jpeg")):
        return path
    from PIL import Image, ImageOps
    with Image.open(path) as im:
        if im.getexif().get(0x0112, 1) in (1, None):
            return path
        pasta = os.path.join(tempfile.gettempdir(), "fotos_em_pe")
        os.makedirs(pasta, exist_ok=True)
        out = os.path.join(pasta, hashlib.md5(os.path.abspath(path).encode()).hexdigest() + ".png")
        if not os.path.exists(out):
            ImageOps.exif_transpose(im).convert("RGB").save(out)
    return out
'''
for s in SKILLS:
    f = os.path.join(OUT, s, "comum.py")
    troca(f, [('    return SOS_RE.sub(SOS_FALADO, texto)\n', '    return _voz_extra(SOS_RE.sub(SOS_FALADO, texto))\n', 1)])
    open(f, "a", encoding="utf-8").write(COMUM_EXTRA)

# ------------------------------------------------------------------ nucleo (lista.py, vsl/nucleo.py, reportagem/nucleo.py)
MAKE_AUDIO = '''def make_audio(P, plano):
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
            C.sem_respiro(raw, out)'''

PHOTO_INPUT = '''def photo_input(WK, b, d, card):
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
    return png, chain, [(a - x0, b_, c - x0, e) for a, b_, c, e in fb]'''

for rel in ("criativo-lista-ong/lista.py", "criativo-vsl-voz-ong/nucleo.py", "criativo-reportagem-ong/nucleo.py"):
    troca(os.path.join(OUT, rel), [
        (r"def make_audio\(P, plano\):.*?(?=\n\n\n# ---------- texto com emoji)", MAKE_AUDIO, -1),
        (r"def photo_input\(WK, b, d, card\):.*?(?=\n\n\ndef render_block)", PHOTO_INPUT, -1),
        ("SAFE_TOP, SAFE_BOTTOM, SAFE_W = 290, 1250, 860   # zona segura do Reels/TikTok/Stories\n",
         "SAFE_TOP, SAFE_BOTTOM, SAFE_W = 290, 1250, 860   # zona segura do Reels/TikTok/Stories\n"
         "TOPO_MAX = 470   # a chamada fica so no alto da tela (y 290 a 470); nunca no meio\n", 1),
        ('    hl_c = list(range(200, 460, 40)) + list(range(1700, 1300, -40))\n'
         '    cap_c = sorted(range(420, 1720, 40), key=lambda y: abs(y - 1180))\n'
         '    pl_c = list(range(1720, 1380, -40)) + list(range(380, 700, 40))\n',
         '    hl_c = list(range(SAFE_TOP, TOPO_MAX + 1, 20))  # chamada so no alto\n'
         '    cap_c = sorted(range(480, SAFE_BOTTOM - CAP_H + 1, 20), key=lambda y: abs(y - 1000))  # legenda na zona segura\n'
         '    pl_c = list(range(SAFE_BOTTOM - 100, 880, -10)) + list(range(480, 800, 20))  # etiqueta na zona segura\n', 1),
        ('        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", png]\n        fc.append(chain)\n',
         '        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", png]\n        fc.append(chain)\n', 1),
        ('f"{push(each)}{PB if is_pb(b, scene) else \'\'},trim=duration={each:.3f}',
         'f"setsar=1,fps={FPS}{PB if is_pb(b, scene) else \'\'},trim=duration={each:.3f}', 1),
        ('y = place(cand.height, list(range(SAFE_TOP, SAFE_BOTTOM - cand.height + 1, 10)), taken, xr)',
         'y = place(cand.height, list(range(SAFE_TOP, TOPO_MAX + 1, 10)), taken, xr)', 1),
    ])

# ------------------------------------------------------------------ reportagem.py
troca(os.path.join(OUT, "criativo-reportagem-ong", "reportagem.py"), [
    ('        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", png]\n        fc.append(chain)\n',
     '        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", png]\n        fc.append(chain)\n', 1),
    ('f"{N.push(each, 0.02)}{N.PB', 'f"setsar=1,fps={FPS}{N.PB', 1),
    ('            y_pl = N.place(pl.height, list(range(1720, 1380, -40)), taken)',
     '            y_pl = N.place(pl.height, list(range(N.SAFE_BOTTOM - pl.height, 860, -10)), taken)  # zona segura', 1),
    ('        y_cap = N.place(cap_h, sorted(range(900, 1720, 20), key=lambda y: abs(y - 1300)), taken)',
     '        y_cap = N.place(cap_h, sorted(range(700, N.SAFE_BOTTOM - cap_h + 1, 10), key=lambda y: abs(y - 1060)), taken)', 1),
    ('            cands = sorted(range(N.SAFE_TOP, N.SAFE_BOTTOM - gc_h + 1, 10), key=lambda y: -y) + \\\n'
     '                list(range(N.SAFE_BOTTOM - gc_h + 10, 1560, 10))',
     '            cands = sorted(range(N.SAFE_TOP, N.SAFE_BOTTOM - gc_h + 1, 10), key=lambda y: -y)  # so na zona segura', 1),
    # a fala real segue rodando (sem som) ate a troca de cena, em vez de congelar o ultimo quadro
    ('        v = f"{WK}/{b[\'nome\']}_v{i}.mp4"\n'
     '        N.run(["ffmpeg", "-y", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", b["fonte"],',
     '        v = f"{WK}/{b[\'nome\']}_v{i}.mp4"\n'
     '        tv = t1 - t0 + (1.6 if i == len(b["cortes"]) - 1 else 0.0)\n'
     '        N.run(["ffmpeg", "-y", "-ss", f"{t0:.3f}", "-t", f"{tv:.3f}", "-i", b["fonte"],', 1),
])

# ------------------------------------------------------------------ narrado
troca(os.path.join(OUT, "criativo-narrado-ong", "narrado.py"), [
    ('import argparse, json, os, re, shutil, subprocess, sys, tempfile\n',
     'import argparse, json, os, re, shutil, subprocess, sys, tempfile\n\n'
     'sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path\n'
     'from comum import foto_em_pe  # noqa: E402\n', 1),
    ('        src, d = self.path(it["src"]), nf / FPS + 0.2\n', '        src, d = foto_em_pe(self.path(it["src"])), nf / FPS + 0.2\n', 1),
])
GERAR = '''    os.makedirs(os.path.join(out, "raw"), exist_ok=True)
    for name, text in cfg["narracao"].items():
        mp3, js = os.path.join(out, f"{name}.mp3"), os.path.join(out, f"{name}.json")
        raw_mp3, raw_js = os.path.join(out, "raw", f"{name}.mp3"), os.path.join(out, "raw", f"{name}.json")
        if not os.path.exists(raw_mp3):
            if os.path.exists(mp3) and os.path.exists(js):  # fala antiga, gerada antes de tirar o respiro
                os.replace(mp3, raw_mp3)
                os.replace(js, raw_js)
            else:
                r = json.loads(post(f"https://api.elevenlabs.io/v1/text-to-speech/{cfg['voice_id']}/with-timestamps"
                                    "?output_format=mp3_44100_128",
                                    {"text": C.para_voz(text), "model_id": cfg.get("model_id", "eleven_multilingual_v2"),
                                     "voice_settings": vs}))
                open(raw_mp3, "wb").write(base64.b64decode(r["audio_base64"]))
                json.dump({"text": C.para_tela(text), "words": C.juntar_sos(words_from_alignment(r["alignment"]))},
                          open(raw_js, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if not os.path.exists(mp3):  # versao usada no video: sem respiro, com o tempo das palavras reajustado
            words = C.sem_respiro(raw_mp3, mp3, json.load(open(raw_js, encoding="utf-8"))["words"])
            json.dump({"text": C.para_tela(text), "words": words}, open(js, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            print(f"{name}: {words[-1]['end']:.2f}s  {text}")
'''
troca(os.path.join(OUT, "criativo-narrado-ong", "gerar_audio.py"), [
    (r"    for name, text in cfg\[\"narracao\"\]\.items\(\):\n        mp3 = .*?(?=    for name, fx in cfg)", GERAR, -1)])

# ------------------------------------------------------------------ cortes (build.py)
troca(os.path.join(OUT, "edicao-criativo-ong", "build.py"), [
    ('import argparse, json, os, re, shutil, subprocess, sys, tempfile\n',
     'import argparse, json, os, re, shutil, subprocess, sys, tempfile\n\n'
     'sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path\n'
     'from comum import foto_em_pe  # noqa: E402\n', 1),
    ('    if src.lower().endswith(STILL_EXT):\n        return ["-loop"',
     '    if src.lower().endswith(STILL_EXT):\n        src = foto_em_pe(src)\n        return ["-loop"', 1),
])

import py_compile  # noqa: E402
for s in SKILLS:
    for f in os.listdir(os.path.join(OUT, s)):
        if f.endswith(".py"):
            py_compile.compile(os.path.join(OUT, s, f), doraise=True)
print("scripts_v3 ok:", OUT)
