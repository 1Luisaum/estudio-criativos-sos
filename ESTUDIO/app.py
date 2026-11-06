"""Estudio de criativos: servidor local (so na sua maquina) para escolher o estilo e a pasta do material.

Abre em http://127.0.0.1:8765. Cria pedidos em EDITADOS/_pedidos/<id>.json, que o Claude executa
com a skill do estilo escolhido.

Funciona em qualquer computador: a pasta raiz e a pasta onde o ESTUDIO esta. Ao abrir, ele grava essa
pasta em ~/.claude/estudio-ong.json (as skills leem dali) e cria EDITADOS/RENDERIZADOS/LEVA 26 se faltar.
Desde 27/10/2026 todos os estilos salvam juntos em EDITADOS/RENDERIZADOS/LEVA NN (5 por leva, a partir da 26),
com o nome "PEB <n> - <ESTILO>.mp4" a partir do PEB 111 (a regra fica no comum.py das skills).
"""
import glob, hashlib, json, mimetypes, os, re, subprocess, sys, tempfile, threading, time, urllib.parse, webbrowser
from datetime import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # a pasta do material (a que tem ESTUDIO e EDITADOS)
EDITADOS = os.path.join(ROOT, "EDITADOS")
PEDIDOS = os.path.join(EDITADOS, "_pedidos")
EXEMPLOS = os.path.join(HERE, "exemplos")
CONFIG = os.path.join(os.path.expanduser("~"), ".claude", "estudio-ong.json")
THUMBS = os.path.join(tempfile.gettempdir(), "estudio_thumbs")
LEVA_RE = re.compile(r"^LEVA\s*0*(\d+)$", re.I)
POR_LEVA = 5
RENDER = os.path.join(EDITADOS, "RENDERIZADOS")   # pasta unica de todos os estilos (27/10/2026)
LEVA_INICIAL, PEB_INICIAL = 26, 111
PEB_RE = re.compile(r"^(PEB|AEB)\s*-?\s*(\d+)\b", re.I)
# numeracao por crianca (27/10/2026): prefixo, primeiro numero, primeira LEVA
CRIANCAS = {"Pedrinho": ("PEB", 111, 26), "Adrielly": ("AEB", 34, 41)}
PASTAS_LIBERADAS = set()                           # pastas escolhidas nesta sessao (miniaturas e players)
PORT = int(os.environ.get("ESTUDIO_PORTA", "8765"))   # troque se a porta estiver ocupada
VIDEO = (".mp4", ".mov", ".m4v", ".mkv", ".avi", ".webm")
PHOTO = (".jpg", ".jpeg", ".png", ".webp")
AUDIO = (".mp3", ".wav", ".m4a", ".aac", ".ogg")

ESTILOS = [
    {"id": "cortes", "skill": "edicao-criativo-ong", "nome": "Cortes com gancho", "pasta": "CORTES COM GANCHO",
     "resumo": "A criança falando, sem pausas nem vícios, com zoom a cada corte, caixa rosa de gancho e legenda palavra por palavra.",
     "exemplo": "Pedrinho_5horas_v1.mp4", "duracao": "20 a 45 s",
     "itens": ["Remove pausas e \"é\"", "Zoom a cada corte", "Gancho em caixa rosa", "Legenda com destaque vermelho",
               "B-roll do banco", "Selo SAIBA MAIS"],
     "precisa": "1 vídeo bruto da criança falando", "brutos": "um"},
    {"id": "lettering", "skill": "criativo-lettering-ong", "nome": "Cortes com lettering", "pasta": "CORTES COM LETTERING",
     "resumo": "A criança falando, sem pausas nem vícios, com zoom a cada corte e UM lettering da pasta \"lettings\" parado o vídeo todo.",
     "exemplo": "Pedrinho_ajuda_de_verdade_v1.mp4", "duracao": "30 a 45 s",
     "itens": ["Remove pausas e \"é\"", "Zoom a cada corte", "1 lettering pronto o vídeo todo",
               "Legenda em Poppins Black", "B-roll do banco", "CTA Saiba mais"],
     "precisa": "1 vídeo bruto da criança falando + imagens na pasta \"lettings\"", "brutos": "um"},
    {"id": "narrado", "skill": "criativo-narrado-ong", "nome": "Narrado de impacto", "pasta": "NARRADO DE IMPACTO",
     "resumo": "Narrador do ElevenLabs alternando com falas reais da criança e da mãe. Narração em preto e branco, pessoas reais em cor.",
     "exemplo": "Pedrinho_narrado_v1.mp4", "duracao": "60 a 75 s",
     "itens": ["Narração ElevenLabs", "P&B → cor na virada", "Manchete URGENTE", "Cartelas de número + boom",
               "Copy nova a cada vídeo", "Botão SAIBA MAIS"],
     "precisa": "vídeos com falas reais da criança e/ou da mãe", "brutos": "varios"},
    {"id": "reportagem", "skill": "criativo-reportagem-ong", "nome": "Reportagem", "pasta": "REPORTAGEM",
     "resumo": "Parece uma matéria jornalística: repórter em off sobre b-roll e sonoras da criança e da mãe com tarja de nome.",
     "exemplo": "Pedrinho_reportagem_v1.mp4", "duracao": "50 a 60 s",
     "itens": ["Off do repórter (ElevenLabs)", "Sonoras com voz real", "Tarja de nome (GC)",
               "Manchete no alto da tela", "Legenda de jornal", "CTA Saiba mais"],
     "precisa": "brutos com falas da criança e/ou da mãe + b-roll do banco", "brutos": "varios"},
    # estilo "caixas": edicao copiada dos anuncios validados da Causas do Bem (caso Kaue), 26/10/2026;
    # o corpo e o mesmo nos tres, so o gancho muda (para testar gancho)
    {"id": "caixas_pedido", "skill": "criativo-caixas-pedido-ong", "nome": "Caixas: pedido de tempo",
     "pasta": "CAIXAS PEDIDO DE TEMPO",
     "resumo": "A criança pede tempo para a câmera; depois a voz dela sobre b-roll curto, com caixa parada no alto e caixa de R$ 10,00 embaixo.",
     "exemplo": "Pedrinho_caixas_pedido_v1.mp4", "duracao": "30 a 35 s",
     "itens": ["Gancho: pedido de tempo", "Frase real em verde", "Voz real da criança",
               "Take dela falando (3-5 s)", "Caixa no alto + caixa de valor", "Verde ou vermelho"],
     "precisa": "brutos em que a criança fala + vídeos e fotos do banco", "brutos": "varios"},
    {"id": "caixas_aspas", "skill": "criativo-caixas-aspas-ong", "nome": "Caixas: aspas",
     "pasta": "CAIXAS ASPAS",
     "resumo": "Mãe e criança juntas na câmera com a citação \"Para muitos… Para ele, é uma luta\"; depois o mesmo corpo com as caixas paradas.",
     "exemplo": "Pedrinho_caixas_aspas_v1.mp4", "duracao": "30 a 35 s",
     "itens": ["Gancho: mãe e criança", "Citação em faixas brancas", "Voz real da criança",
               "Take dela falando (3-5 s)", "Caixa no alto + caixa de valor", "Verde ou vermelho"],
     "precisa": "vídeo da mãe com a criança + brutos em que a criança fala + banco", "brutos": "varios"},
    {"id": "caixas_urgente", "skill": "criativo-caixas-urgente-ong", "nome": "Caixas: urgente",
     "pasta": "CAIXAS URGENTE",
     "resumo": "Narrador em off por 3-4 s sobre um close real com a faixa URGENTE!!; depois o mesmo corpo com as caixas paradas. Sem apresentadora de IA.",
     "exemplo": "Pedrinho_caixas_urgente_v1.mp4", "duracao": "30 a 35 s",
     "itens": ["Gancho: URGENTE!!", "Narrador ElevenLabs (curto)", "Close real da criança",
               "Voz real da criança", "Caixa no alto + caixa de valor", "Verde ou vermelho"],
     "precisa": "brutos em que a criança fala + um close forte + banco", "brutos": "varios"},
    # copias de outros dois anuncios validados da Causas do Bem (26/10/2026)
    {"id": "corrente", "skill": "criativo-corrente-ong", "nome": "Corrente do bem",
     "pasta": "CORRENTE DO BEM",
     "resumo": "Um texto só, parado no alto, branco com trechos em amarelo; a voz da criança nos primeiros segundos e depois só música sobre o b-roll.",
     "exemplo": "Pedrinho_corrente_v1.mp4", "duracao": "28 a 32 s",
     "itens": ["Texto fixo com destaque amarelo", "Voz real da criança (6-8 s)", "Depois só música",
               "B-roll em cor", "Passagens pelo preto", "Sem caixa e sem legenda"],
     "precisa": "brutos com a criança pedindo ajuda + vídeos e fotos do banco", "brutos": "varios"},
    {"id": "mae_desesperada", "skill": "criativo-mae-desesperada-ong", "nome": "Mãe desesperada",
     "pasta": "MÃE DESESPERADA",
     "resumo": "A mãe falando para a câmera no gancho; depois a voz da criança sobre b-roll curto, com a caixa vermelha \"Essa mãe está desesperada…\" o vídeo todo.",
     "exemplo": "Pedrinho_mae_desesperada_v1.mp4", "duracao": "30 a 34 s",
     "itens": ["Gancho: a mãe falando", "Voz real da criança", "B-roll de ~2,6 s",
               "Caixa vermelha fixa (3 linhas)", "R$5,00 se torna vida", "Clique em Saiba mais"],
     "precisa": "vídeo da mãe falando + brutos em que a criança fala + banco", "brutos": "varios"},
    # copia do anuncio validado da Ampara Brasil (26/10/2026)
    {"id": "salva_vida", "skill": "criativo-salva-vida-ong", "nome": "Salva vida",
     "pasta": "SALVA VIDA",
     "resumo": "Sem fala, só música; o valor grande e a faixa \"Salva vida, ajude o…\" parados no alto, sobre cenas íntimas e lentas que se misturam.",
     "exemplo": "Pedrinho_salva_vida_v1.mp4", "duracao": "26 a 30 s",
     "itens": ["Sem fala, só música", "R$10,00 grande no alto", "Faixa branca com o pedido",
               "6 cenas lentas em cor", "Fusão entre as cenas", "Sem legenda e sem caixa"],
     "precisa": "vídeos do banco com a criança e a mãe (não precisa de fala)", "brutos": "varios"},
    # estilo criado em 27/10/2026: impacto -> desenvolve -> final feliz para doar
    {"id": "esperanca", "skill": "criativo-esperanca-ong", "nome": "Da dor à esperança",
     "pasta": "DA DOR À ESPERANÇA",
     "resumo": "Começa muito impactante em P&B (batida de coração, palavras gigantes, a fala mais dolorida), desenvolve e vira para cor com um final feliz e o pedido.",
     "exemplo": "Pedrinho_esperanca_v1.mp4", "duracao": "38 a 45 s",
     "itens": ["Impacto: coração + palavras gigantes", "Narrador + falas reais", "P&B → cor na virada",
               "Música tensa → esperançosa", "Final feliz com o pedido", "Legenda em uma linha"],
     "precisa": "brutos com falas da criança e da mãe + fotos e vídeos felizes do banco", "brutos": "varios"},
    {"id": "unicef", "skill": "criativo-unicef-ong", "nome": "UNICEF",
     "pasta": "UNICEF",
     "resumo": "Gancho de 8 s modelado no anúncio da UNICEF: \"Isso pode parecer uma simples atadura…\" sobre a foto do item, a mãe fazendo o curativo e a criança; depois cortes com lettering bem simples.",
     "exemplo": "Pedrinho_atadura_v1.mp4", "duracao": "40 a 45 s",
     "itens": ["Gancho \"pode parecer simples\"", "Narrador ElevenLabs (8 s)", "Foto do item de curativo",
               "Legenda com caixinha vermelha", "Cortes da criança falando", "1 lettering parado"],
     "precisa": "1 vídeo bruto da criança falando + fotos dos itens e cenas da mãe no banco + imagens na pasta \"lettings\"",
     "brutos": "um"},
]


# estilo "Bibliotecas" (03/11/2026): um cartao por modelo da skill criativo-bibliotecas-ong (24 anuncios de outras
# ONGs copiados). Lidos da propria skill, entao um modelo novo em modelos\ aparece aqui sozinho.
BIB_ONG = {"maosamigas": "Lar Mãos Amigas", "maeritinha": "Lar Mãe Ritinha", "florisbela": "Florisbela",
           "leaodejuda": "Lar Leão de Judá", "movamor": "Movimento de Amor"}


def estilos_bibliotecas():
    out = []
    pasta = os.path.join(os.path.expanduser("~"), ".claude", "skills", "criativo-bibliotecas-ong", "modelos")
    for f in sorted(glob.glob(os.path.join(pasta, "*.json"))):
        try:
            p = json.load(open(f, encoding="utf-8"))
            m = p["modelo"]
        except (OSError, ValueError, KeyError):
            continue
        ong = BIB_ONG.get(os.path.basename(p.get("ref", "")).split("_")[0], "outra ONG")
        voz, fala = bool(p.get("voz")), any(x.get("som") for x in p.get("base", []))
        tipo = "Narração + imagem de IA" if voz else ("Fala real da criança" if fala else "Só música e texto")
        musica = os.path.splitext(os.path.basename(p.get("musica", "")))[0]
        tot = sum(x["fim"] - x["ini"] for x in p.get("base", []))
        resumo = re.sub(r"^\d+\.\s*", "", m.get("descricao", ""))
        resumo = re.sub(r"^[A-Za-zÀ-ú ]*\d{9,}:\s*", "", resumo)
        out.append({"id": "bib_" + m["id"], "skill": "criativo-bibliotecas-ong", "modelo": m["id"],
                    "nome": f"Biblioteca: {m.get('titulo', m['id'])}", "pasta": p.get("estilo", "BIB"),
                    "resumo": f"Copiado do anúncio do {ong}. " + resumo[:1].upper() + resumo[1:],
                    "exemplo": f"{m['exemplo']} - {p.get('estilo', '').upper()}.mp4", "duracao": f"{round(tot)} s",
                    "itens": [ong, tipo, "Música: " + musica[:40]],
                    "precisa": ("brutos com a criança falando" if fala else
                                "vídeos e fotos da criança e dos curativos (não precisa de fala)"),
                    "brutos": "varios"})
    return out


ESTILOS += estilos_bibliotecas()
QTD_MAX = 5

# ---------------------------------------------------------------- envio para o Planejar (03/11/2026)
# Os prontos marcados vão para o dashboard de postagens (pasta "postador"), em Planejar. O postador grava
# o caminho dele em estudio-ong.json; o Claude escreve título, legenda e capa depois, sozinho.
PESSOA_DO_CODIGO = {"PEB": "pedrinho", "AEB": "adrielly"}


def pasta_postador():
    try:
        p = json.load(open(CONFIG, encoding="utf-8-sig")).get("postador", "")
    except (OSError, ValueError):
        p = ""
    p = p or os.path.join(os.path.expanduser("~"), "Desktop", "tiktok", "postador")
    return p if os.path.isfile(os.path.join(p, "registrar.py")) else ""


def no_planejar():
    """{caminho do vídeo do Estúdio: status do post} dos que já foram para o postador."""
    pp = pasta_postador()
    out = {}
    for f in glob.glob(os.path.join(pp, "fila", "*", "post.json")) if pp else []:
        try:
            p = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if p.get("origem"):
            out[os.path.normcase(p["origem"])] = p.get("status", "")
    return out


def enviar_planejar(paths):
    pp = pasta_postador()
    if not pp:
        return [{"path": p, "erro": "não achei a pasta do postador"} for p in paths]
    res = []
    render = os.path.normcase(os.path.abspath(RENDER)) + os.sep
    for p in paths:
        m = PEB_RE.match(os.path.basename(p))
        if not os.path.isfile(p) or not os.path.normcase(os.path.abspath(p)).startswith(render) or not m:
            res.append({"path": p, "erro": "só vídeos prontos de RENDERIZADOS"})
            continue
        r = subprocess.run([sys.executable, os.path.join(pp, "registrar.py"), "importar",
                            PESSOA_DO_CODIGO[m.group(1).upper()], p], cwd=pp, capture_output=True, timeout=600,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        saida = r.stdout.decode("utf-8", "replace").strip()
        if r.returncode == 0:
            # capa provisoria e copia de envio (leva alguns minutos): roda aqui, sem segurar a pagina
            pid = json.loads(saida.splitlines()[-1])["id"]
            threading.Thread(target=subprocess.run, daemon=True, args=(
                [sys.executable, os.path.join(pp, "registrar.py"), "preparar", pid],),
                kwargs={"cwd": pp, "capture_output": True,
                        "creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0)}).start()
        res.append({"path": p, "ok": r.returncode == 0,
                    "erro": "" if r.returncode == 0 else (r.stderr.decode("utf-8", "replace")[-300:] or saida)})
    return res


def pasta_estilo(est):
    """EDITADOS/<PASTA DO ESTILO>, aceitando a que ja existe com outra caixa (ex.: 'reportagem')."""
    if os.path.isdir(EDITADOS):
        for d in os.listdir(EDITADOS):
            if d.casefold() == est["pasta"].casefold() and os.path.isdir(os.path.join(EDITADOS, d)):
                return os.path.join(EDITADOS, d)
    return os.path.join(EDITADOS, est["pasta"])


def _pronto(f):
    """Video numerado pronto (PEB/AEB), sem o temporario da logo ".mp4.marca.mp4"."""
    return bool(PEB_RE.match(f)) and f.lower().endswith(".mp4") and f.lower().count(".mp4") == 1


def leva_atual(crianca="Pedrinho"):
    """(LEVA atual relativa a RENDERIZADOS, videos nela, proximo codigo) da crianca. Cada uma tem a sua numeracao
    (Pedrinho PEB/LEVA 26+, Adrielly AEB 34/LEVA 41+) e as LEVAs podem estar em subpastas (ex.: TUDO BALBINO).
    A regra e aplicada pelas skills (comum.destino) na hora de salvar; aqui e so para mostrar."""
    prefixo, inicial, leva_ini = CRIANCAS[crianca]
    rx = re.compile(rf"^{prefixo}\s*-?\s*(\d+)\b", re.I)
    lv, usados = [], set()
    for cur, ds, _ in os.walk(RENDER):
        for d in ds:
            if (m := LEVA_RE.match(d)):
                p = os.path.join(cur, d)
                nums = [int(x.group(1)) for f in os.listdir(p) if _pronto(f) and (x := rx.match(f))]
                if nums:
                    lv.append((int(m.group(1)), p, len(nums))); usados |= set(nums)
    prox = f"{prefixo} {max(usados | {inicial - 1}) + 1}"
    lv.sort()
    for num, p, n in lv:
        if n < POR_LEVA:  # a LEVA incompleta mais antiga recebe o proximo video
            return os.path.relpath(p, RENDER), n, prox
    base = os.path.dirname(lv[-1][1]) if lv else RENDER
    return os.path.relpath(os.path.join(base, f"LEVA {(lv[-1][0] + 1) if lv else leva_ini:02d}"), RENDER), 0, prox


def preparar():
    """Grava a pasta raiz para as skills e cria as pastas que faltam (_pedidos, _planos, RENDERIZADOS/LEVA 26)."""
    os.makedirs(os.path.dirname(CONFIG), exist_ok=True)
    try:
        cfg = json.load(open(CONFIG, encoding="utf-8-sig"))
    except (OSError, ValueError):
        cfg = {}
    cfg.update({"raiz": ROOT, "estudio": HERE})
    json.dump(cfg, open(CONFIG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for p in (PEDIDOS, os.path.join(EDITADOS, "_planos")):
        os.makedirs(p, exist_ok=True)
    if not any(LEVA_RE.match(d) for _, ds, _ in os.walk(RENDER) for d in ds):
        os.makedirs(os.path.join(RENDER, f"LEVA {LEVA_INICIAL:02d}"), exist_ok=True)


def achar_video(nome):
    """Video de exemplo pelo nome: em ESTUDIO/exemplos ou em qualquer LEVA de EDITADOS."""
    for base in (EXEMPLOS, EDITADOS):
        for cur, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if not d.startswith("_")]
            if nome in files:
                return os.path.join(cur, nome)
    return ""


def ffprobe(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                              "format=duration:stream=width,height:stream_side_data=rotation", "-of", "json", path],
                             capture_output=True, text=True, timeout=20).stdout
        d = json.loads(out)
        s = (d.get("streams") or [{}])[0]
        rot = next((x["rotation"] for x in s.get("side_data_list", []) if "rotation" in x), 0)
        w, h = s.get("width", 0), s.get("height", 0)
        if abs(int(rot)) % 180 == 90:
            w, h = h, w
        return {"dur": round(float(d["format"].get("duration", 0)), 1), "w": w, "h": h}
    except Exception:
        return {"dur": 0, "w": 0, "h": 0}


def scan(folder):
    """Arquivos da pasta e das subpastas (ate 2 niveis), agrupados por subpasta."""
    groups = {}
    base_depth = folder.rstrip("\\/").count(os.sep)
    for cur, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if not d.startswith((".", "_")) and d not in ("ESTUDIO", "EDITADOS")]
        if cur.count(os.sep) - base_depth >= 2:
            dirs[:] = []
        rel = os.path.relpath(cur, folder)
        for f in sorted(files):
            p = os.path.join(cur, f)
            ext = os.path.splitext(f)[1].lower()
            kind = "video" if ext in VIDEO else "foto" if ext in PHOTO else "audio" if ext in AUDIO else None
            if not kind or "(1)" in f:
                continue
            item = {"nome": f, "path": p, "tipo": kind}
            if kind == "video":
                item.update(ffprobe(p))
            groups.setdefault("." if rel == "." else rel, []).append(item)
    return [{"pasta": k, "arquivos": v} for k, v in groups.items()]


def thumb(path, t):
    os.makedirs(THUMBS, exist_ok=True)
    key = hashlib.md5(f"{path}|{t}|{os.path.getmtime(path)}".encode()).hexdigest()
    out = os.path.join(THUMBS, key + ".jpg")
    if not os.path.exists(out):
        cmd = ["ffmpeg", "-v", "error", "-y"]
        if not path.lower().endswith(PHOTO):
            cmd += ["-ss", str(t)]
        subprocess.run(cmd + ["-i", path, "-frames:v", "1", "-vf", "scale=270:-2", "-q:v", "4", out],
                       capture_output=True, timeout=60)
    return out


def pick_folder(initial):
    """Janela nativa do Windows para escolher pasta (processo separado, sempre na frente)."""
    code = ("import tkinter as tk, sys\nfrom tkinter import filedialog\nr=tk.Tk();r.withdraw();r.attributes('-topmost',True)\n"
            f"p=filedialog.askdirectory(initialdir={initial!r},title='Escolha a pasta com o material e o bruto')\n"
            "sys.stdout.buffer.write((p or '').encode('utf-8'))")
    r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, timeout=600)
    return os.path.normpath(r.stdout.decode("utf-8")) if r.stdout else ""


# ---------------------------------------------------------------- producao ao vivo (27/10/2026)
# O Claude grava EDITADOS/_demanda_atual.json quando comeca uma demanda (titulo, inicio, total, grupos).
# O progresso de cada video vem das etapas reais: processos do Windows (montador, narracao, transcricao,
# com o caminho do plano na linha de comando), arquivos do plano e o MP4 em RENDERIZADOS.
DEMANDA = os.path.join(EDITADOS, "_demanda_atual.json")
PLANOS_DIR = os.path.join(EDITADOS, "_planos")
# tempo tipico de montagem por estilo (s), so para estimar a % enquanto o montador roda
TIPICO = [("unicef", 260), ("lettering", 200), ("narrado", 320), ("reportagem", 320), ("esperanca", 260),
          ("caixas", 220), ("corrente", 140), ("mae", 170), ("salva", 140), ("lista", 240), ("vsl", 240)]
_PROC = {"t": 0, "lista": []}


def processos():
    """[(nome, inicio_epoch, linha de comando)] de python/ffmpeg. Uma thread atualiza a lista a cada ~4 s
    (o PowerShell leva alguns segundos); a pagina sempre recebe a ultima lista na hora."""
    if not _PROC.get("thread"):
        _PROC["thread"] = threading.Thread(target=_loop_processos, daemon=True)
        _PROC["thread"].start()
        for _ in range(100):  # a primeira leitura, para a primeira pagina ja vir certa
            if _PROC["t"]:
                break
            time.sleep(0.1)
    return _PROC["lista"]


def _loop_processos():
    while True:
        _ler_processos()
        time.sleep(4)


def _ler_processos():
    ps = ("[Console]::OutputEncoding=[Text.Encoding]::UTF8; Get-CimInstance Win32_Process -Filter "
          "\"name='python.exe' or name='ffmpeg.exe'\" | % { [pscustomobject]@{n=$_.Name;"
          "t=[int64](($_.CreationDate.ToUniversalTime()-[datetime]'1970-01-01').TotalSeconds);c=$_.CommandLine} } "
          "| ConvertTo-Json -Compress")
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, timeout=20,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        d = json.loads(r.stdout.decode("utf-8", "replace") or "[]")
        d = d if isinstance(d, list) else [d]
        _PROC["lista"] = [(x.get("n", ""), x.get("t", 0), x.get("c") or "") for x in d]
    except Exception:
        _PROC["lista"] = []
    _PROC["t"] = time.time()
    return _PROC["lista"]


def demanda():
    try:
        return json.load(open(DEMANDA, encoding="utf-8-sig"))
    except (OSError, ValueError):
        return None


def rotulo_peb(f):
    return f.split(" - ", 1)[-1].rsplit(".", 1)[0].upper() if " - " in f else ""


def etapa_plano(pd, procs, agora):
    """(%, etapa, ativo) de um plano a partir dos processos e dos arquivos."""
    nome = os.path.basename(pd)
    try:
        p = json.load(open(os.path.join(pd, "plano.json"), encoding="utf-8-sig"))
    except (OSError, ValueError):
        p = None
    s = (p or {}).get("saida") or (p or {}).get("out") or ""
    saida = s if "RENDERIZADOS" in s.upper() else ""
    meus = [(n, t, c) for n, t, c in procs if ("\\" + nome + "\\") in c.replace("/", "\\")
            or (saida and os.path.basename(saida) in c)]
    mont = [t for n, t, c in meus if n == "python.exe" and re.search(r"(montar|build|build_cortes|caixas|narrado|"
                                                                      r"reportagem|lista|vsl)\.py", c)]
    narr = any("gerar_audio" in c for n, t, c in meus)
    trans = any(re.search(r"transcre|transcribe", c) for n, t, c in meus)
    fila = any("rodar.py" in c and nome in c for n, t, c in procs)
    existe = bool(saida) and os.path.isfile(saida)
    if mont:
        el = agora - min(mont)
        tip = next((v for k, v in TIPICO if k in nome.lower()), 240)
        if existe and agora - os.path.getmtime(saida) < 120:
            return 96, "aplicando a logo e finalizando", True
        return int(50 + 44 * min(1.0, el / tip)), f"montando ({int(el // 60)}:{int(el % 60):02d} min)", True
    if existe:
        return 100, ("pronto · conferindo" if trans or any("freezedetect" in c and os.path.basename(saida) in c
                                                             for _, _, c in procs) else "pronto"), trans
    if narr:
        return 30, "gerando a narração", True
    if trans:
        return 20, "transcrevendo as falas", True
    if p is None:
        return 5, "criando o plano", True
    audio = os.path.join(pd, "audio")
    tem_audio = os.path.isdir(audio) and any(f.endswith(".mp3") for f in os.listdir(audio))
    mex = max([os.path.getmtime(os.path.join(a, b)) for a, _, fs in os.walk(pd) for b in fs] or [0])
    ativo = agora - mex < 180
    if tem_audio:
        return 40, "narração pronta · " + ("na fila da montagem" if fila else "aguardando a montagem"), ativo or fila
    return 15, "plano escrito · " + ("na fila da montagem" if fila else "preparando"), ativo or fila


def producao():
    agora = time.time()
    dm = demanda()
    inicio = 0
    if dm and dm.get("inicio"):
        try:
            inicio = datetime.fromisoformat(dm["inicio"]).timestamp()
        except ValueError:
            inicio = 0
    procs = processos()
    # videos prontos em RENDERIZADOS
    feitos = []
    for cur, _, fs in os.walk(RENDER):  # em qualquer subpasta (ex.: TUDO BALBINO)
        for f in fs:
            # ".mp4.marca.mp4" e o arquivo temporario da logo sendo aplicada: nao e video pronto
            if _pronto(f):
                m = PEB_RE.match(f); fp = os.path.join(cur, f)
                feitos.append({"arquivo": f, "codigo": f"{m.group(1).upper()} {int(m.group(2))}",
                               "leva": os.path.relpath(cur, RENDER), "path": fp,
                               "hora": os.path.getmtime(fp), "estilo": rotulo_peb(f)})
    # planos da demanda (ou mexidos nas ultimas 2 h, sem demanda)
    corte = inicio or agora - 7200
    videos = []
    for pd in glob.glob(os.path.join(PLANOS_DIR, "*")):
        if not os.path.isdir(pd) or os.path.basename(pd).startswith("_"):
            continue
        if os.path.getctime(pd) < corte and os.path.getmtime(pd) < corte:
            continue
        pct, etapa, ativo = etapa_plano(pd, procs, agora)
        try:
            p = json.load(open(os.path.join(pd, "plano.json"), encoding="utf-8-sig"))
        except (OSError, ValueError):
            p = {}
        s = p.get("saida") or p.get("out") or ""
        peb = os.path.basename(s) if "RENDERIZADOS" in s.upper() else ""
        videos.append({"plano": os.path.basename(pd), "pct": pct, "etapa": etapa, "ativo": ativo,
                       "peb": peb, "estilo": rotulo_peb(peb) if peb else "", "criado": os.path.getctime(pd)})
    finalizando = {v["peb"] for v in videos if v["pct"] < 100 and v["peb"]}
    feitos = [f for f in feitos if f["arquivo"] not in finalizando and agora - f["hora"] > 10]  # so os terminados
    da_demanda = [f for f in feitos if f["hora"] >= inicio] if inicio else []
    enviados = no_planejar()
    for f in feitos:
        f["plano"] = next((v["plano"] for v in videos if v["peb"] == f["arquivo"]), "")
        f["planejar"] = enviados.get(os.path.normcase(f["path"]), "")
    n = len(da_demanda) if dm else 0
    total = (dm or {}).get("total") or 0
    # previsao pelo ritmo real entre os videos prontos (o comeco gasta tempo lendo e planejando): so com 3 ou mais
    horas = sorted(f["hora"] for f in da_demanda)
    eta = None
    if dm and total and n >= 3 and n < total:
        eta = agora + (total - n) * (horas[-1] - horas[0]) / (n - 1)
    grupos = []
    for g in (dm or {}).get("grupos", []):
        grupos.append({"nome": g.get("nome", ""), "estilos": [
            {"estilo": e, "meta": m, "feitos": sum(f["estilo"] == e.upper() for f in da_demanda)}
            for e, m in g.get("estilos", {}).items()]})
    andamento = sorted([v for v in videos if v["pct"] < 100], key=lambda v: (-v["ativo"], -v["pct"], v["plano"]))
    return {"agora": agora, "demanda": dm, "inicio": inicio, "total": total, "feitos_demanda": n, "eta": eta,
            "grupos": grupos, "andamento": andamento,
            "ativos": sum(1 for v in andamento if v["ativo"]),
            "prontos": sorted(feitos, key=lambda f: -f["hora"])[:40]}


def list_pedidos():
    os.makedirs(PEDIDOS, exist_ok=True)
    out = []
    for f in sorted(os.listdir(PEDIDOS), reverse=True):
        if f.endswith(".json"):
            try:
                p = json.load(open(os.path.join(PEDIDOS, f), encoding="utf-8-sig"))
            except Exception:
                continue
            saidas = p.get("saidas") or ([p["saida"]] if p.get("saida") else [])
            if saidas and all(os.path.exists(s) for s in saidas):
                p["status"] = "concluido"
            out.append(p)
    return out


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send_json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def send_file(self, path, ctype=None):
        size = os.path.getsize(path)
        ctype = ctype or mimetypes.guess_type(path)[0] or "application/octet-stream"
        rng = self.headers.get("Range")
        start, end = 0, size - 1
        if rng and rng.startswith("bytes="):
            a, _, b = rng[6:].partition("-")
            start = int(a) if a else max(0, size - int(b))
            end = int(b) if a and b else size - 1
            self.send_response(206)
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        else:
            self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        with open(path, "rb") as fh:
            fh.seek(start)
            left = end - start + 1
            try:
                while left > 0:
                    chunk = fh.read(min(1 << 20, left))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    left -= len(chunk)
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                pass

    def allowed(self, p):
        """So arquivos da pasta do usuario, da raiz do material ou de uma pasta escolhida no Estudio."""
        p = os.path.normcase(os.path.abspath(p))
        bases = {os.path.expanduser("~"), ROOT, *PASTAS_LIBERADAS}
        return os.path.isfile(p) and any(p.startswith(os.path.normcase(os.path.abspath(b)) + os.sep) for b in bases)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
        if u.path == "/":
            return self.send_file(os.path.join(HERE, "index.html"), "text/html; charset=utf-8")
        if u.path == "/api/estilos":
            estilos = []
            for e in ESTILOS:
                txt = []
                for cr in CRIANCAS:
                    leva, n, prox = leva_atual(cr)
                    txt.append(f"{cr}: {leva} ({n} de {POR_LEVA}) · próximo {prox} - {e['pasta']}")
                estilos.append({**e, "leva": " | ".join(txt)})
            return self.send_json({"estilos": estilos, "raiz": ROOT})
        if u.path == "/api/escolher-pasta":
            return self.send_json({"pasta": pick_folder(q.get("inicio", ROOT))})
        if u.path == "/api/pasta":
            p = q.get("path", "")
            if not os.path.isdir(p):
                return self.send_json({"erro": "pasta não encontrada"}, 404)
            PASTAS_LIBERADAS.add(p)
            return self.send_json({"pasta": p, "grupos": scan(p)})
        if u.path == "/api/pedidos":
            return self.send_json({"pedidos": list_pedidos()})
        if u.path == "/api/producao":
            return self.send_json(producao())
        if u.path == "/thumb":
            p = q.get("path", "")
            if not self.allowed(p):
                return self.send_json({"erro": "arquivo fora da pasta do usuário"}, 403)
            return self.send_file(thumb(p, float(q.get("t", 2))), "image/jpeg")
        if u.path == "/media":
            p = q.get("path", "")
            if not os.path.isabs(p):
                p = achar_video(os.path.basename(p))
                if not p:
                    return self.send_json({"erro": "exemplo não encontrado"}, 404)
            if not self.allowed(p):
                return self.send_json({"erro": "arquivo fora da pasta do usuário"}, 403)
            return self.send_file(p)
        self.send_json({"erro": "não encontrado"}, 404)

    def do_POST(self):
        if self.path not in ("/api/pedido", "/api/planejar"):
            return self.send_json({"erro": "não encontrado"}, 404)
        # So a propria pagina do Estudio pode criar pedidos ou mandar videos para o Planejar.
        if self.headers.get("Origin") not in (None, f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}"):
            return self.send_json({"erro": "proibido"}, 403)
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8"))
        if self.path == "/api/planejar":
            return self.send_json({"resultados": enviar_planejar(body.get("paths", [])[:40])})
        est = next((e for e in ESTILOS if e["id"] == body.get("estilo")), None)
        if not est or not body.get("pasta") or not body.get("brutos"):
            return self.send_json({"erro": "escolha o estilo, a pasta e pelo menos um bruto"}, 400)
        os.makedirs(PEDIDOS, exist_ok=True)
        pid = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        path = os.path.join(PEDIDOS, pid + ".json")
        leva, n, prox = leva_atual("Adrielly" if str(body.get("crianca", "")).lower().startswith("adri") else "Pedrinho")
        pedido = {"id": pid, "criado": datetime.now().isoformat(timespec="seconds"), "status": "pendente",
                  "estilo": est["id"], "estilo_nome": est["nome"], "skill": est["skill"],
                  "raiz": ROOT, "arquivo": path, "pasta_saida": os.path.join(RENDER, leva),
                  "crianca": body.get("crianca", ""), "pasta": body["pasta"], "brutos": body["brutos"],
                  "banco": body.get("banco", []), "musica": body.get("musica", ""),
                  "observacoes": body.get("observacoes", ""), "saida": None, "saidas": []}
        try:
            qtd = max(1, min(QTD_MAX, int(body.get("quantidade", 1))))
        except (TypeError, ValueError):
            qtd = 1
        pedido["quantidade"] = qtd
        if est.get("modelo"):
            pedido["modelo"] = est["modelo"]
        msg = (f"Executa o pedido do Estúdio {pid} (arquivo {path}) com a skill {est['skill']}"
               + (f", modelo {est['modelo']}." if est.get("modelo") else "."))
        if qtd > 1:
            msg += (f" Gere {qtd} criativos diferentes entre si (gancho, copy, chamada e cenas diferentes em cada um)"
                    f" e coloque todos em \"saidas\".")
        pedido["mensagem"] = msg
        json.dump(pedido, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        self.send_json({"pedido": pedido, "mensagem": msg})


def main():
    preparar()
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    url = f"http://127.0.0.1:{PORT}"
    print(f"Estúdio aberto em {url}  (feche esta janela para desligar)")
    if "--sem-navegador" not in sys.argv:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    srv.serve_forever()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
