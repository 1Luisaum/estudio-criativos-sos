"""Transcreve (com quem fala) os brutos do pedido 2026-10-26_105743 que ainda nao tem transcricao."""
import glob, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BR = os.path.join(RAIZ, "VÍDEOS PARA EDITAR")
OUT = os.path.join(RAIZ, "EDITADOS", "_planos", "_tx_brutos")
K = os.path.join(os.path.expanduser("~"), ".claude", "skills", "criativo-narrado-ong", "scripts", "transcrever.py")
ALVOS = {"20260916_235338.mp4": "t_235338", "20260917_000819.mp4": "t_000819", "20260917_001530.mp4": "t_001530",
         "roteiro 7.mp4": "t_roteiro7b", "roteiro 8.mp4": "t_roteiro8", "roteiro 9.mp4": "t_roteiro9",
         "Nenhuma mãe": "t_nenhuma_mae", "absurdo de caro": "t_absurdo_caro", "peço perdão": "t_peco_perdao",
         "Um Vídeo Novo": "t_video_novo"}
os.makedirs(OUT, exist_ok=True)


def achar(chave):
    return next(p for p in glob.glob(os.path.join(BR, "*.mp4")) if chave in os.path.basename(p))


def um(item):
    chave, nome = item
    out = os.path.join(OUT, nome + ".json")
    if not os.path.exists(out):
        r = subprocess.run([sys.executable, "-I", K, achar(chave), out, "--diarize"], capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        if r.returncode:
            return f"ERRO {nome}: {r.stderr[-300:]}"
    d = json.load(open(out, encoding="utf-8"))
    return f"ok {nome}: {d.get('text', '')[:90]}"


sys.stdout.reconfigure(encoding="utf-8")
json.dump({n: achar(c) for c, n in ALVOS.items()}, open(os.path.join(OUT, "_fontes.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
with ThreadPoolExecutor(4) as ex:
    for linha in ex.map(um, ALVOS.items()):
        print(linha, flush=True)
