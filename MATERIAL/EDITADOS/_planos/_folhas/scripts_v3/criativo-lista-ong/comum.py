"""Funcoes comuns as skills de criativo da ONG. O arquivo e IGUAL em todas as skills (o instalador copia).

- raiz(): pasta do material (a que tem EDITADOS). Vem do caminho do plano ou de ~/.claude/estudio-ong.json,
  que o Estudio grava ao abrir. Assim funciona em qualquer computador.
- destino(): onde salvar o video. Fica em EDITADOS/<PASTA DO ESTILO>/LEVA NN, com 5 videos por leva;
  a 6a vai para a LEVA seguinte, que e criada na hora. Se o video ja existe numa leva (re-render),
  ele e substituido no mesmo lugar.
- para_voz() / para_tela(): a ONG e "S.O.S", lida "esse o esse". Na narracao vai "Ésse Ô Ésse";
  na legenda vai "SOS".
"""
import json
import os
import re

CONFIG = os.path.join(os.path.expanduser("~"), ".claude", "estudio-ong.json")
PASTAS = {"cortes": "CORTES COM GANCHO", "narrado": "NARRADO DE IMPACTO", "lista": "LISTA NARRADA",
          "vsl": "VSL COM VOZ DA CRIANÇA", "reportagem": "REPORTAGEM"}
POR_LEVA = 5
LEVA_RE = re.compile(r"^LEVA\s*0*(\d+)$", re.I)
VIDEO = (".mp4", ".mov")


def config():
    try:
        return json.load(open(CONFIG, encoding="utf-8-sig"))
    except (OSError, ValueError):
        return {}


def raiz(plano_path=None):
    """Pasta do material. Primeiro pelo caminho do plano (<raiz>/EDITADOS/_planos/<nome>/plano.json)."""
    if plano_path:
        p = os.path.abspath(plano_path)
        for _ in range(6):
            p = os.path.dirname(p)
            if os.path.basename(p).upper() == "EDITADOS":
                return os.path.dirname(p)
    r = config().get("raiz")
    if r and os.path.isdir(r):
        return r
    raise SystemExit("Nao achei a pasta do material. Abra o Estudio uma vez (ele grava a pasta em "
                     f"{CONFIG}) ou deixe o plano dentro de EDITADOS\\_planos.")


def pasta_estilo(editados, estilo):
    """EDITADOS/<PASTA DO ESTILO>. Aceita a pasta que ja existe com outra caixa (ex.: 'reportagem')."""
    alvo = PASTAS.get(estilo, estilo.upper())
    if os.path.isdir(editados):
        for d in os.listdir(editados):
            if d.casefold() == alvo.casefold() and os.path.isdir(os.path.join(editados, d)):
                return os.path.join(editados, d)
    return os.path.join(editados, alvo)


def levas(pasta):
    """[(numero, caminho)] das pastas LEVA, em ordem."""
    out = []
    if os.path.isdir(pasta):
        for d in os.listdir(pasta):
            m = LEVA_RE.match(d)
            if m and os.path.isdir(os.path.join(pasta, d)):
                out.append((int(m.group(1)), os.path.join(pasta, d)))
    return sorted(out)


def videos_em(pasta):
    return [f for f in os.listdir(pasta) if f.lower().endswith(VIDEO)]


def destino(plano_path, plano, estilo, chave="saida"):
    """Caminho final do video na LEVA certa. Grava o caminho escolhido de volta no plano.json.

    Com "saida_fixa": true no plano, usa o caminho do plano sem mexer (para um teste fora das levas).
    """
    atual = plano.get(chave) or ""
    if plano.get("saida_fixa") and atual:
        os.makedirs(os.path.dirname(os.path.abspath(atual)), exist_ok=True)
        return atual
    nome = os.path.basename(atual) or (plano.get("nome") or os.path.basename(os.path.dirname(
        os.path.abspath(plano_path)))) + ".mp4"
    pe = pasta_estilo(os.path.join(raiz(plano_path), "EDITADOS"), estilo)
    lv = levas(pe)
    alvo = next((os.path.join(d, nome) for _, d in lv if os.path.exists(os.path.join(d, nome))), None)
    if not alvo:
        if lv and len(videos_em(lv[-1][1])) < POR_LEVA:
            pasta = lv[-1][1]
        else:
            pasta = os.path.join(pe, f"LEVA {(lv[-1][0] + 1) if lv else 1:02d}")
        os.makedirs(pasta, exist_ok=True)
        alvo = os.path.join(pasta, nome)
    if atual != alvo:
        plano[chave] = alvo
        d = json.load(open(plano_path, encoding="utf-8-sig"))
        d[chave] = alvo
        json.dump(d, open(plano_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saida:", alvo)
    return alvo


# ---------- nome da ONG ----------
SOS_RE = re.compile(r"\bS\.?\s?O\.?\s?S\b\.?", re.I)
SOS_FALADO = "Ésse Ô Ésse"


def para_voz(texto):
    """Texto que vai para o ElevenLabs: 'Sos Human Help' -> 'Ésse Ô Ésse Human Help'."""
    return _voz_extra(SOS_RE.sub(SOS_FALADO, texto))


def para_tela(texto):
    """Texto da legenda: 'Sos Human Help' -> 'SOS Human Help'."""
    return SOS_RE.sub("SOS", texto)


def juntar_sos(words):
    """Palavras com tempo vindas do ElevenLabs: junta 'Ésse' 'Ô' 'Ésse' de volta em 'SOS'."""
    alvo = [w.casefold() for w in SOS_FALADO.split()]
    out, i = [], 0
    while i < len(words):
        trio = words[i:i + 3]
        if len(trio) == 3 and [re.sub(r"[^\wÀ-ÿ]", "", w["text"]).casefold() for w in trio] == alvo:
            fim = re.sub(r"^[\wÀ-ÿ]+", "", trio[2]["text"])  # pontuacao grudada na ultima
            out.append({**trio[0], "text": "SOS" + fim, "end": trio[2]["end"]})
            i += 3
        else:
            out.append(words[i])
            i += 1
    return out


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
