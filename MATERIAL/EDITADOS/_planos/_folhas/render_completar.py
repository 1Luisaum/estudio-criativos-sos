"""Renderiza os 16 planos de completar as LEVAs, um por vez. Resultado em _folhas/render_completar_log.txt."""
import json, os, subprocess, sys

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(os.path.expanduser("~"), ".claude", "skills")
LOG = os.path.join(P, "_folhas", "render_completar_log.txt")
os.environ.pop("ELEVENLABS_API_KEY", None)  # le a chave nova do Windows


def py(*a):
    return subprocess.run([sys.executable, "-I", *a], capture_output=True, text=True, encoding="utf-8", errors="replace")


for nome, d in json.load(open(os.path.join(P, "_folhas", "planos_completar.json"), encoding="utf-8")).items():
    pl = os.path.join(d, "plano.json")
    if "narrado" in nome:
        r = py(os.path.join(S, "criativo-narrado-ong", "scripts", "gerar_audio.py"), os.path.join(d, "roteiro_audio.json"), os.path.join(d, "audio"))
        if r.returncode == 0:
            r = py(os.path.join(S, "criativo-narrado-ong", "scripts", "narrado.py"), pl)
    elif "reportagem" in nome:
        r = py(os.path.join(S, "criativo-reportagem-ong", "scripts", "reportagem.py"), pl)
    elif "lista" in nome:
        r = py(os.path.join(S, "criativo-lista-ong", "scripts", "lista.py"), pl)
    elif "vsl" in nome:
        r = py(os.path.join(S, "criativo-vsl-voz-ong", "scripts", "vsl.py"), pl)
    else:
        r = py(os.path.join(S, "edicao-criativo-ong", "scripts", "build.py"), pl)
    open(os.path.join(d, "render_log.txt"), "w", encoding="utf-8").write(r.stdout + r.stderr)
    fim = [l for l in r.stdout.splitlines() if l.startswith("OK")]
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{nome}: {'OK ' + fim[-1] if r.returncode == 0 and fim else 'ERRO ' + (r.stdout + r.stderr)[-400:]}\n")
