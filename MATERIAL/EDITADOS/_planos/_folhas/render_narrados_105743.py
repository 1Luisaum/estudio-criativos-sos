"""Gera a narracao, monta e confere os 5 narrados do pedido 105743, um depois do outro."""
import os, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
P = os.path.join(RAIZ, "EDITADOS", "_planos")
K = os.path.join(os.path.expanduser("~"), ".claude", "skills", "criativo-narrado-ong", "scripts")
NOMES = sys.argv[1:] or ["acabou", "noite", "culpa", "esquecido", "espera"]
sys.stdout.reconfigure(encoding="utf-8")


def rodar(args, log):
    r = subprocess.run([sys.executable, "-I", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    log.write(r.stdout + r.stderr)
    return r.returncode, r.stdout + r.stderr


for n in NOMES:
    d = os.path.join(P, f"Pedrinho_narrado_{n}_v1")
    with open(os.path.join(d, "render_log.txt"), "w", encoding="utf-8") as log:
        code, out = rodar([os.path.join(K, "gerar_audio.py"), os.path.join(d, "roteiro_audio.json"), os.path.join(d, "audio")], log)
        if code:
            print(n, "ERRO audio", out[-400:], flush=True)
            continue
        code, out = rodar([os.path.join(K, "narrado.py"), os.path.join(d, "plano.json")], log)
        ok = [l for l in out.splitlines() if l.startswith(("OK", "audio:", "saida:"))]
        if code:
            print(n, "ERRO render", out[-600:], flush=True)
            continue
        mp4 = [l for l in ok if l.startswith("OK")][0].split()[1:]
        mp4 = " ".join(mp4).split("  duracao")[0]
        code, out2 = rodar([os.path.join(K, "conferir.py"), mp4, os.path.join(d, "linha_do_tempo.json")], log)
        res = [l for l in out2.splitlines() if "RESULTADO" in l]
        print(n, "|", " | ".join(ok), "|", res, flush=True)
