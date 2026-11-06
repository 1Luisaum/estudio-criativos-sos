"""Renderiza planos com os scripts de teste (scripts_v3). Uso: python -I render_v3.py Pedrinho_lista_v3 ...  (ou 'todos')
Resultado de cada um em <plano>/render_log.txt e uma linha em _folhas/render_v3_log.txt."""
import glob, os, subprocess, sys

F = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(F)
V3 = os.path.join(F, "scripts_v3")
LOG = os.path.join(F, "render_v3_log.txt")
os.environ.pop("ELEVENLABS_API_KEY", None)  # le a chave nova do Windows
sys.stdout.reconfigure(encoding="utf-8")


def py(*a):
    return subprocess.run([sys.executable, "-I", *a], capture_output=True, text=True, encoding="utf-8", errors="replace")


nomes = sys.argv[1:]
if nomes == ["todos"]:
    nomes = sorted(os.path.basename(d) for d in glob.glob(os.path.join(P, "Pedrinho_*")) if os.path.exists(os.path.join(d, "plano.json")))
for nome in nomes:
    d = os.path.join(P, nome)
    pl = os.path.join(d, "plano.json")
    if "_narrado_" in nome or nome == "Pedrinho_narrado_v1":
        r = py(os.path.join(V3, "criativo-narrado-ong", "gerar_audio.py"), os.path.join(d, "roteiro_audio.json"), os.path.join(d, "audio"))
        if r.returncode == 0:
            r2 = py(os.path.join(V3, "criativo-narrado-ong", "narrado.py"), pl)
            r = subprocess.CompletedProcess(r2.args, r2.returncode, r.stdout + r2.stdout, r.stderr + r2.stderr)
    elif "_reportagem_" in nome:
        r = py(os.path.join(V3, "criativo-reportagem-ong", "reportagem.py"), pl)
    elif "_lista_" in nome:
        r = py(os.path.join(V3, "criativo-lista-ong", "lista.py"), pl)
    elif "_vsl_" in nome:
        r = py(os.path.join(V3, "criativo-vsl-voz-ong", "vsl.py"), pl)
    else:
        r = py(os.path.join(V3, "edicao-criativo-ong", "build.py"), pl)
    open(os.path.join(d, "render_log.txt"), "w", encoding="utf-8").write(r.stdout + r.stderr)
    fim = [l for l in r.stdout.splitlines() if l.startswith("OK")]
    linha = f"{nome}: " + (fim[-1] if r.returncode == 0 and fim else "ERRO " + (r.stdout + r.stderr)[-500:])
    open(LOG, "a", encoding="utf-8").write(linha + "\n")
    print(linha, flush=True)
