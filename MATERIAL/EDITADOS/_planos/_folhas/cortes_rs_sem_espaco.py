"""Faixa de doacao dos cortes: 'APENAS R$ 5' -> 'APENAS R$5' (como na referencia) e renderiza com scripts_v3."""
import json, os, subprocess, sys

F = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(F)
B = os.path.join(F, "scripts_v3", "edicao-criativo-ong", "build.py")
sys.stdout.reconfigure(encoding="utf-8")
for n in ("Pedrinho_5horas_v1", "Pedrinho_curativos_acabando_v1", "Pedrinho_noite_v1", "Pedrinho_espera_v1", "Pedrinho_esquecido_v1"):
    f = os.path.join(P, n, "plano.json")
    p = json.load(open(f, encoding="utf-8-sig"))
    p["chamada"]["linhas"][0][0] = p["chamada"]["linhas"][0][0].replace("R$ ", "R$")
    json.dump(p, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, "-I", B, f], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(n, p["chamada"]["linhas"][0][0], "OK" if r.returncode == 0 else "ERRO " + r.stderr[-300:], flush=True)
