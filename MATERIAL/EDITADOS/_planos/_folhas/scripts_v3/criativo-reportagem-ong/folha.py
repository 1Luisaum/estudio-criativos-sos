"""Folha de conferencia: quadros do MP4 final com as linhas da zona segura (ciano).

Uso: python -I folha.py "<saida.mp4>" "<pasta do plano>\\linha_do_tempo.json" "<folha.png>" [quadros_por_bloco]
Mostra cada bloco (1 quadro nas fotos, 2 nos blocos de video) em miniatura 180x320.
"""
import json
import os
import subprocess
import sys

mp4, tl, out = sys.argv[1], sys.argv[2], sys.argv[3]
per = int(sys.argv[4]) if len(sys.argv) > 4 else 2
d = json.load(open(tl, encoding="utf-8"))
tmp = os.path.join(os.path.dirname(os.path.abspath(out)), "_folha")
os.makedirs(tmp, exist_ok=True)
for f in os.listdir(tmp):
    os.remove(os.path.join(tmp, f))
t, i = 0.0, 0
for b in d["blocos"]:
    n = 1 if b["nome"].startswith("i") else per
    for k in range(n):
        ts = t + b["d"] * (k + 0.5) / n
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ts:.2f}", "-i", mp4, "-frames:v", "1", "-vf",
                        "scale=180:320,drawbox=y=48:w=180:h=1:c=cyan,drawbox=y=208:w=180:h=1:c=cyan",
                        os.path.join(tmp, f"f{i:03d}.png")])
        i += 1
    t += b["d"]
cols = 6
rows = (i + cols - 1) // cols
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(tmp, "f%03d.png"),
                "-vf", f"tile={cols}x{rows}", "-frames:v", "1", out])
print(f"OK {out} ({i} quadros)")
