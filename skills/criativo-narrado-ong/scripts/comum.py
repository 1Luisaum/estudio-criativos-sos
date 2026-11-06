"""Funcoes comuns as skills de criativo da ONG. O arquivo e IGUAL em todas as skills (o instalador copia).

- raiz(): pasta do material (a que tem EDITADOS). Vem do caminho do plano ou de ~/.claude/estudio-ong.json,
  que o Estudio grava ao abrir. Assim funciona em qualquer computador.
- destino(): onde salvar o video. Regra do usuario de 27/10/2026: uma pasta unica para todos os estilos,
  EDITADOS/RENDERIZADOS/LEVA NN, com 5 videos por leva, comecando na LEVA 26; o arquivo se chama
  "PEB <numero> - <ESTILO>.mp4", com numero seguido comecando no PEB 111. Se o plano ja tem um PEB na
  pasta (re-render), ele e substituido no mesmo lugar, com o mesmo numero.
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
    # o ".mp4.marca.mp4" e o temporario da logo sendo aplicada: contar ele fez LEVAs fecharem com 3 ou 4 (27/10/2026)
    return [f for f in os.listdir(pasta) if f.lower().endswith(VIDEO) and ".marca." not in f.lower()]


RENDER = "RENDERIZADOS"  # pasta unica de todos os estilos (27/10/2026)
LEVA_INICIAL = 26
PEB_INICIAL = 111
PEB_RE = re.compile(r"^(?:PEB|AEB)\s*-?\s*(\d+)\b", re.I)  # qualquer video numerado (Pedrinho ou Adrielly)
# numeracao por crianca (regra do usuario, 27/10/2026): Pedrinho "PEB <n>" a partir do 111;
# Adrielly "AEB <n>" a partir do 34
PREFIXOS = {"Pedrinho": ("PEB", 111), "Adrielly": ("AEB", 34)}
# cada crianca tem as suas LEVAs: Pedrinho a partir da 26, Adrielly a partir da 41 (regra do usuario, 27/10/2026)
LEVAS_INICIAIS = {"PEB": 26, "AEB": 41}


def _achar_em_render(pr, nome):
    """Caminho atual de um video ja numerado, em qualquer subpasta de RENDERIZADOS (ou None)."""
    for cur, _, fs in os.walk(pr):
        if nome in fs:
            return os.path.join(cur, nome)
    return None


def levas_da_crianca(pr, prefixo, reservados=None):
    """[(numero, caminho)] das LEVAs de uma crianca, em qualquer subpasta de RENDERIZADOS: as que tem video ou
    reserva com o prefixo dela (PEB/AEB). LEVA vazia nao e de ninguem."""
    reservados = reservados or {}
    rx = re.compile(rf"^{prefixo}\s*-?\s*\d+", re.I)
    out = []
    for cur, ds, _ in os.walk(pr):
        for d in ds:
            m = LEVA_RE.match(d)
            p = os.path.join(cur, d)
            if m and any(rx.match(x) for x in set(videos_em(p)) | reservados.get(p.casefold(), set())):
                out.append((int(m.group(1)), p))
    return sorted(out)


def crianca_do_plano(plano_path, plano):
    """Pedrinho ou Adrielly: pelo campo "crianca" do plano, senao pelo nome da pasta do plano ou pelo bruto."""
    c = (plano.get("crianca") or "").lower()
    if c:
        return "Adrielly" if c.startswith("adri") else "Pedrinho"
    pistas = [os.path.basename(os.path.dirname(os.path.abspath(plano_path))), plano.get("raw") or "",
              plano.get("bank") or "", plano.get("banco") or ""]
    return "Adrielly" if any("adriel" in x.lower() for x in pistas) else "Pedrinho"


def rotulo(estilo):
    """Nome do estilo no arquivo: o nome da pasta antiga dele, em maiusculas (ex.: 'CORTES COM LETTERING')."""
    return PASTAS.get(estilo, estilo).upper()


def pasta_render(editados):
    return os.path.join(editados, RENDER)


def numeros_usados(editados, prefixo="PEB"):
    """Numeros ja usados com o prefixo (PEB ou AEB): arquivos na pasta de render (em qualquer subpasta) e
    saidas ja gravadas nos planos (reservadas)."""
    usados = set()
    rx = re.compile(rf"^{prefixo}\s*-?\s*(\d+)\b", re.I)
    for cur, _, fs in os.walk(pasta_render(editados)):
        usados |= {int(m.group(1)) for f in fs if f.lower().endswith(VIDEO) and ".marca." not in f.lower()
                   and (m := rx.match(f))}
    pl = os.path.join(editados, "_planos")
    if os.path.isdir(pl):
        for n in os.listdir(pl):
            f = os.path.join(pl, n, "plano.json")
            try:
                p = json.load(open(f, encoding="utf-8-sig"))
            except (OSError, ValueError):
                continue
            for k in ("saida", "out"):
                s = p.get(k) or ""
                if RENDER.casefold() in s.casefold() and (m := rx.match(os.path.basename(s))):
                    usados.add(int(m.group(1)))
    return usados


def destino(plano_path, plano, estilo, chave="saida"):
    """Caminho final do video: EDITADOS/RENDERIZADOS/LEVA NN/PEB <n> - <ESTILO>.mp4. Grava o caminho no plano.json.

    Com "saida_fixa": true no plano, usa o caminho do plano sem mexer (para um teste fora das levas).
    """
    atual = plano.get(chave) or ""
    if plano.get("saida_fixa") and atual:
        os.makedirs(os.path.dirname(os.path.abspath(atual)), exist_ok=True)
        return atual
    editados = os.path.join(raiz(plano_path), "EDITADOS")
    pr = pasta_render(editados)
    os.makedirs(pr, exist_ok=True)
    trava = _travar(os.path.join(pr, ".reserva_peb.lock"))  # dois videos montando juntos nao pegam o mesmo PEB
    try:
        prefixo, inicial = PREFIXOS[crianca_do_plano(plano_path, plano)]
        movido = _achar_em_render(pr, os.path.basename(atual)) if atual and PEB_RE.match(os.path.basename(atual)) \
            else None
        if movido:
            alvo = movido  # re-render: mesmo numero, onde o video esta hoje (o usuario pode ter movido a LEVA)
        else:
            n = max(numeros_usados(editados, prefixo) | {inicial - 1}) + 1
            reservados = _reservados_por_leva(editados)
            lv = levas_da_crianca(pr, prefixo, reservados)
            # toda LEVA tem que fechar com 5 (regra do usuario, 27/10/2026): o video novo vai para a LEVA
            # incompleta mais antiga da crianca; so abre uma nova quando todas estao cheias
            livre = next((d for _, d in lv
                          if len(set(videos_em(d)) | reservados.get(d.casefold(), set())) < POR_LEVA), None)
            if livre:
                pasta = livre
            else:
                # a LEVA nova fica junto das outras da mesma crianca (ex.: RENDERIZADOS\TUDO BALBINO)
                base = os.path.dirname(lv[-1][1]) if lv else pr
                pasta = os.path.join(base, f"LEVA {(lv[-1][0] + 1) if lv else LEVAS_INICIAIS[prefixo]:02d}")
            alvo = os.path.join(pasta, f"{prefixo} {n} - {rotulo(estilo)}.mp4")
        os.makedirs(os.path.dirname(alvo), exist_ok=True)
        if atual != alvo:
            plano[chave] = alvo
            d = json.load(open(plano_path, encoding="utf-8-sig"))
            d[chave] = alvo
            json.dump(d, open(plano_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    finally:
        _soltar(trava)
    print("saida:", alvo)
    return alvo


# ---------- codificacao do video final (27/10/2026) ----------
# Na placa de video NVIDIA (h264_nvenc) a passada final fica ~4x mais rapida com a mesma qualidade
# (teste no PEB 140: 8,8 s contra 33,8 s, SSIM 0,9944 contra 0,9948). Sem NVIDIA, ou com ESTUDIO_CPU=1,
# volta para o x264 de antes.
_NVENC = {}


def tem_nvenc():
    if "ok" not in _NVENC:
        if os.environ.get("ESTUDIO_CPU") == "1":
            _NVENC["ok"] = False
        else:
            import subprocess
            r = subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=s=320x240:d=0.2", "-c:v",
                                "h264_nvenc", "-f", "null", "-"], capture_output=True)
            _NVENC["ok"] = r.returncode == 0
    return _NVENC["ok"]


def enc_final():
    """Argumentos de video da passada final (e da logo): NVENC se houver, senao x264 slow."""
    if tem_nvenc():
        return ["-c:v", "h264_nvenc", "-preset", "p5", "-tune", "hq", "-rc", "vbr", "-cq", "21", "-b:v", "0",
                "-profile:v", "high", "-pix_fmt", "yuv420p"]
    return ["-c:v", "libx264", "-preset", "slow", "-crf", "19", "-profile:v", "high", "-pix_fmt", "yuv420p"]


def enc_antes_da_logo():
    """Passada final dos montadores. Como o marca.py sempre recodifica o video para por a logo (com enc_final),
    esta passada e so intermediaria: rapida e quase sem perda. Assim a codificacao de qualidade acontece uma vez."""
    if tem_nvenc():
        return ["-c:v", "h264_nvenc", "-preset", "p1", "-rc", "constqp", "-qp", "14", "-pix_fmt", "yuv420p"]
    return ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "12", "-pix_fmt", "yuv420p"]


def inicio_do_som(path, limiar_db=-45, minimo=0.2):
    """Segundo em que a trilha comeca a soar (pula o silencio do inicio do arquivo). Pedido do usuario
    (27/10/2026): a musica tem que comecar ja no primeiro segundo do video; a 'sleep' tinha 1,1 s de silencio."""
    import subprocess
    r = subprocess.run(["ffmpeg", "-hide_banner", "-t", "15", "-i", path, "-af",
                        f"silencedetect=n={limiar_db}dB:d={minimo}", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    ini = fim = None
    for l in r.stderr.splitlines():
        if "silence_start:" in l and ini is None:
            ini = float(l.split("silence_start:")[1].split()[0])
        if "silence_end:" in l and fim is None:
            fim = float(l.split("silence_end:")[1].split()[0])
    return round(fim, 2) if ini is not None and ini < 0.05 and fim else 0.0


def chave_de(itens, arquivos=()):
    """Impressao digital de uma parte: o que a gera (comando, trecho do plano) + data e tamanho dos arquivos."""
    import hashlib
    marcas = [(f, os.path.getmtime(f), os.path.getsize(f)) if os.path.isfile(f) else (f, 0, 0) for f in arquivos]
    return hashlib.md5(json.dumps([itens, marcas], ensure_ascii=False, default=str).encode("utf-8")).hexdigest()


def ja_pronta(path, chave):
    """True se a parte em `path` foi feita com a mesma impressao digital (correcao: reaproveita o que nao mudou)."""
    try:
        return os.path.isfile(path) and open(path + ".chave", encoding="utf-8").read() == chave
    except OSError:
        return False


def marcar_pronta(path, chave):
    open(path + ".chave", "w", encoding="utf-8").write(chave)


def ffmpeg_cache(cmd, path, runner):
    """Roda o comando ffmpeg que gera `path` so se algo mudou desde a ultima vez (27/10/2026).
    Devolve True se reaproveitou. `runner` e a funcao run() do montador."""
    entradas = [cmd[i + 1] for i, a in enumerate(cmd[:-1]) if a == "-i"]
    chave = chave_de([c for c in cmd if c != path], entradas)
    if ja_pronta(path, chave):
        return True
    runner(cmd)
    marcar_pronta(path, chave)
    return False


def _reservados_por_leva(editados):
    """{pasta da LEVA (casefold): {arquivos}} das saidas ja gravadas nos planos, mesmo sem o MP4 pronto ainda."""
    out = {}
    pl = os.path.join(editados, "_planos")
    for n in os.listdir(pl) if os.path.isdir(pl) else []:
        try:
            p = json.load(open(os.path.join(pl, n, "plano.json"), encoding="utf-8-sig"))
        except (OSError, ValueError):
            continue
        for k in ("saida", "out"):
            s = p.get(k) or ""
            if RENDER.casefold() in s.casefold() and PEB_RE.match(os.path.basename(s)):
                out.setdefault(os.path.dirname(os.path.abspath(s)).casefold(), set()).add(os.path.basename(s))
    return out


def _travar(path, espera=120):
    import time
    t0 = time.time()
    while True:
        try:
            return os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY), path
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(path) > 60:  # trava esquecida por um script que caiu
                    os.remove(path)
                    continue
            except OSError:
                pass
            if time.time() - t0 > espera:
                raise SystemExit("A reserva do numero PEB esta travada: apague " + path)
            time.sleep(0.2)


def _soltar(trava):
    fd, path = trava
    os.close(fd)
    try:
        os.remove(path)
    except OSError:
        pass


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
