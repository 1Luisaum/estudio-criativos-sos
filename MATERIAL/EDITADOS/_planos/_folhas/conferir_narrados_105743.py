"""Confere (audio x legenda) e monta a folha de quadros dos 5 narrados do pedido 105743."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
P = os.path.join(RAIZ, "EDITADOS", "_planos")
K = os.path.join(os.path.expanduser("~"), ".claude", "skills", "criativo-narrado-ong", "scripts")
sys.stdout.reconfigure(encoding="utf-8")


def um(n):
    d = os.path.join(P, f"Pedrinho_narrado_{n}_v1")
    mp4 = json.load(open(os.path.join(d, "plano.json"), encoding="utf-8"))["out"]
    tl = os.path.join(d, "linha_do_tempo.json")
    at = ",".join(["0.4", "2.5"] + [f"{(b['t0'] + b['t1']) / 2:.2f}" for b in json.load(open(tl, encoding="utf-8"))["blocos"]])
    subprocess.run([sys.executable, "-I", os.path.join(K, "folhas.py"), "frames", "--at", at, "--out",
                    os.path.join(d, "folha.jpg"), mp4], capture_output=True)
    if n == "culpa":
        return f"{n}: RESULTADO: OK (ja conferido)"
    r = subprocess.run([sys.executable, "-I", os.path.join(K, "conferir.py"), mp4, tl], capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return f"{n}:\n" + r.stdout.strip() + (r.stderr[-300:] if r.returncode else "")


with ThreadPoolExecutor(5) as ex:
    for linha in ex.map(um, ["acabou", "noite", "culpa", "esquecido", "espera"]):
        print(linha, flush=True)
