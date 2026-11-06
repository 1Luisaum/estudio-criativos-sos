"""Instala o Estudio de Criativos (SOS Human Help) neste computador, sem perguntas, e abre o Estudio.
O Claude do editor roda isto depois de garantir o Python 3.12 (veja CLAUDE.md).

Uso: python -I instalar.py [--pasta "<pasta do material>"] [--escolher] [--sem-atalho] [--nao-abrir]
  sem --pasta: usa a pasta da instalacao anterior ou "Area de Trabalho\\EDIÇÃO COM CLAUDE";
  --escolher: abre uma janela para o editor escolher a pasta.
Pode rodar de novo para atualizar: troca as skills e o ESTUDIO e nunca mexe em EDITADOS.
"""
import glob, json, os, shutil, subprocess, sys

PACOTE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
SKILLS = os.path.join(HOME, ".claude", "skills")
CONFIG = os.path.join(HOME, ".claude", "estudio-ong.json")
PYDIR = os.path.dirname(sys.executable)
ESTILOS = ["CORTES COM GANCHO", "NARRADO DE IMPACTO", "LISTA NARRADA", "VSL COM VOZ DA CRIANÇA", "REPORTAGEM"]


def passo(t):
    print(f"\n== {t}", flush=True)


def desktop():
    r = subprocess.run(["powershell", "-NoProfile", "-Command", "[Environment]::GetFolderPath('Desktop')"],
                       capture_output=True, text=True)
    return r.stdout.strip() or os.path.join(HOME, "Desktop")


def achar_ffmpeg():
    """Pasta do ffmpeg.exe: no PATH desta janela, no PATH salvo no Windows ou onde o winget instala."""
    if shutil.which("ffmpeg") and shutil.which("ffprobe"):
        return os.path.dirname(shutil.which("ffmpeg"))
    import winreg
    pastas = []
    for raiz, chave in ((winreg.HKEY_CURRENT_USER, "Environment"),
                        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")):
        try:
            with winreg.OpenKey(raiz, chave) as k:
                pastas += os.path.expandvars(winreg.QueryValueEx(k, "Path")[0]).split(";")
        except OSError:
            pass
    pastas += glob.glob(os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages",
                                     "Gyan.FFmpeg*", "*", "bin"))
    return next((p for p in pastas if p and os.path.isfile(os.path.join(p, "ffmpeg.exe"))
                 and os.path.isfile(os.path.join(p, "ffprobe.exe"))), None)


def ligar_ffmpeg(pasta):
    """Poe ffmpeg e ffprobe ao lado do python.exe (link, sem ocupar espaco). O Windows procura ali primeiro,
    entao os scripts e o Estudio acham o FFmpeg mesmo antes de o Claude ser reaberto com o PATH novo."""
    for exe in ("ffmpeg.exe", "ffprobe.exe"):
        src, dst = os.path.join(pasta, exe), os.path.join(PYDIR, exe)
        if os.path.normcase(src) == os.path.normcase(dst):
            continue
        if os.path.exists(dst):
            os.remove(dst)
        try:
            os.link(src, dst)
        except OSError:
            shutil.copy2(src, dst)


def escolher_pasta(padrao):
    import tkinter as tk
    from tkinter import filedialog
    r = tk.Tk()
    r.withdraw()
    r.attributes("-topmost", True)
    p = filedialog.askdirectory(initialdir=os.path.dirname(padrao), mustexist=False,
                                title="Escolha (ou crie) a pasta do seu material. Cancelar = " + padrao)
    r.destroy()
    return os.path.normpath(p) if p else padrao


def tem_chave():
    if os.environ.get("ELEVENLABS_API_KEY"):
        return True
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return bool(winreg.QueryValueEx(k, "ELEVENLABS_API_KEY")[0])
    except OSError:
        return False


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]

    passo("1/6 FFmpeg")
    ff = achar_ffmpeg()
    if not ff:
        print("instalando pelo winget...", flush=True)
        subprocess.run(["winget", "install", "-e", "--id", "Gyan.FFmpeg",
                        "--accept-package-agreements", "--accept-source-agreements"])
        ff = achar_ffmpeg()
    if not ff:
        sys.exit("Nao consegui instalar o FFmpeg. Instale pelo gyan.dev e rode de novo.")
    ligar_ffmpeg(ff)
    print("ok:", ff)

    passo("2/6 Bibliotecas do Python (Pillow, NumPy, OpenCV 4)")
    r = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "--disable-pip-version-check", "-q",
                        "pillow", "numpy", "opencv-python-headless<5"])
    if r.returncode:
        sys.exit("O pip falhou. Veja a mensagem acima.")
    print("ok")

    passo("3/6 Skills do Claude")
    os.makedirs(SKILLS, exist_ok=True)
    for s in sorted(os.listdir(os.path.join(PACOTE, "skills"))):
        dest = os.path.join(SKILLS, s)
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        shutil.copytree(os.path.join(PACOTE, "skills", s), dest)
        print("  ", s)

    conh = os.path.join(HOME, ".claude", "estudio-ong", "CONHECIMENTO")
    if os.path.isdir(conh):
        shutil.rmtree(conh)
    shutil.copytree(os.path.join(PACOTE, "CONHECIMENTO"), conh)
    print("   conhecimento (regras, falas reais, transcricoes):", conh)

    # ferramentas do lote (27/10/2026): fila de montagem, conferencia automatica, catalogo de rostos,
    # biblioteca de falas; e os agentes roteirista e revisor
    ferr = os.path.join(HOME, ".claude", "estudio-ong", "ferramentas")
    if os.path.isdir(os.path.join(PACOTE, "FERRAMENTAS")):
        if os.path.isdir(ferr):
            shutil.rmtree(ferr)
        shutil.copytree(os.path.join(PACOTE, "FERRAMENTAS"), ferr)
        print("   ferramentas do lote:", ferr)
    ag_dir = os.path.join(HOME, ".claude", "agents")
    if os.path.isdir(os.path.join(PACOTE, "AGENTES")):
        os.makedirs(ag_dir, exist_ok=True)
        for f in os.listdir(os.path.join(PACOTE, "AGENTES")):
            shutil.copy2(os.path.join(PACOTE, "AGENTES", f), os.path.join(ag_dir, f))
            print("   agente:", f)

    passo("4/6 Pasta do material")
    try:
        atual = json.load(open(CONFIG, encoding="utf-8-sig")).get("raiz")
    except (OSError, ValueError):
        atual = None
    padrao = atual or os.path.join(desktop(), "EDIÇÃO COM CLAUDE")
    if "--pasta" in args:
        raiz = args[args.index("--pasta") + 1]
    elif "--escolher" in args:
        raiz = escolher_pasta(padrao)
    else:
        raiz = padrao
    os.makedirs(raiz, exist_ok=True)
    estudio = os.path.join(raiz, "ESTUDIO")
    if os.path.isdir(estudio):
        shutil.rmtree(estudio)
    shutil.copytree(os.path.join(PACOTE, "ESTUDIO"), estudio)
    for p in ("VÍDEOS PARA EDITAR", "MÚSICAS", os.path.join("EDITADOS", "_pedidos"), os.path.join("EDITADOS", "_planos")):
        os.makedirs(os.path.join(raiz, p), exist_ok=True)
    # pasta unica de todos os estilos (27/10/2026): EDITADOS\RENDERIZADOS\LEVA 26, 5 por leva, "PEB 111 - <ESTILO>"
    pe = os.path.join(raiz, "EDITADOS", "RENDERIZADOS")
    os.makedirs(pe, exist_ok=True)
    if not any(d.upper().startswith("LEVA") for d in os.listdir(pe)):
        os.makedirs(os.path.join(pe, "LEVA 26"))
    mus = os.path.join(PACOTE, "MÚSICAS")
    for f in os.listdir(mus) if os.path.isdir(mus) else []:
        d = os.path.join(raiz, "MÚSICAS", f)
        if not os.path.exists(d):
            shutil.copy2(os.path.join(mus, f), d)
    try:
        cfg = json.load(open(CONFIG, encoding="utf-8-sig"))
    except (OSError, ValueError):
        cfg = {}
    cfg.update({"raiz": raiz, "estudio": estudio})
    json.dump(cfg, open(CONFIG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # material pronto (03/11/2026): brutos novos do Pedrinho, musicas tristes da Magnific, referencias das
    # bibliotecas de anuncios, trechos do banco e o montador do estilo "Bibliotecas". Junta com o que o editor
    # ja tem: nunca apaga nem troca video ou musica dele; so os scripts do estilo sao atualizados.
    mat = os.path.join(PACOTE, "MATERIAL")
    novos = 0
    for base, _, arqs in os.walk(mat):
        rel = os.path.relpath(base, mat)
        for f in arqs:
            src, dst = os.path.join(base, f), os.path.join(raiz, rel, f)
            script = os.path.basename(base) in ("_estilo_bib", "fontes")
            if script or not os.path.exists(dst):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                novos += 1
    if os.path.isdir(mat):
        for g in ("gerar_planos.py", "gerar_planos2.py"):  # planos com os caminhos deste PC
            subprocess.run([sys.executable, "-I", os.path.join(raiz, "EDITADOS", "_planos", "_estilo_bib", g)],
                           capture_output=True)
        print(f"   material e estilo Bibliotecas: {novos} arquivos")
    print("ok:", raiz)

    passo("5/6 Atalho na área de trabalho")
    bat = os.path.join(estudio, "ABRIR ESTUDIO.bat")
    if "--sem-atalho" in args:
        print("pulado")
    else:
        lnk = os.path.join(desktop(), "Estudio de Criativos.lnk")
        ps = (f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{lnk}');"
              f"$s.TargetPath='{bat}';$s.WorkingDirectory='{estudio}';$s.Save()")
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
        print("ok:", lnk)

    passo("6/6 Conferência")
    teste = ("import cv2, PIL, subprocess; assert int(cv2.__version__.split('.')[0]) == 4, cv2.__version__;"
             "assert hasattr(cv2, 'CascadeClassifier');"
             "[subprocess.run([x, '-version'], capture_output=True, check=True) for x in ('ffmpeg', 'ffprobe')];"
             "print('OpenCV', cv2.__version__, '| Pillow', PIL.__version__, '| FFmpeg ok')")
    env = dict(os.environ, PATH=os.environ.get("SystemRoot", r"C:\Windows") + r"\System32")  # como um PATH antigo
    r = subprocess.run([sys.executable, "-I", "-c", teste], env=env, capture_output=True, text=True)
    if r.returncode:
        sys.exit("Falhou a conferência:\n" + r.stderr[-800:])
    print(r.stdout.strip())
    chave = tem_chave()
    print("Chave do ElevenLabs:", "configurada" if chave else "FALTA (o editor coloca; veja o COMECE AQUI)")

    if "--nao-abrir" not in args:
        os.startfile(bat)
        print("\nEstúdio aberto (janela preta + navegador em http://127.0.0.1:8765).")
    print("\nPRONTO" + ("" if chave else " (falta só a chave do ElevenLabs para narração e transcrição)"))


if __name__ == "__main__":
    main()
