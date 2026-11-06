"""Folha com quadros (com grade de 108x192 px reais) dos brutos do pedido 105743, nos tempos das falas."""
import glob, os, subprocess, sys, tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BR = os.path.join(RAIZ, "VÍDEOS PARA EDITAR")
OUT = os.path.join(RAIZ, "EDITADOS", "_planos", "_folhas")
VIDS = {"20260917_000819": [2, 12, 31, 45, 57, 67], "20260916_235338": [1, 13, 30, 36, 43, 52],
        "20260917_001530": [5, 15, 30, 44, 80, 91], "Nenhuma mãe": [2, 10, 20, 36, 46, 52],
        "absurdo de caro": [3, 18, 35, 54, 56, 59], "peço perdão": [1, 12, 30, 40, 64, 72],
        "roteiro 8": [3, 20, 33, 55, 70, 93], "roteiro 9": [2, 22, 45, 49, 56, 80],
        "roteiro 7": [3, 16, 24, 120, 130, 140]}
tmp = tempfile.mkdtemp()
for chave, ts in VIDS.items():
    src = next(p for p in glob.glob(os.path.join(BR, "*.mp4")) if chave in os.path.basename(p))
    frames = []
    for i, t in enumerate(ts):
        f = os.path.join(tmp, f"{i}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", src, "-frames:v", "1", "-vf",
                        "scale=360:640,drawgrid=w=36:h=64:t=1:c=yellow@0.35,"
                        f"drawtext=fontfile=C\\\\:/Windows/Fonts/arialbd.ttf:text='{t}s':x=8:y=8:fontsize=28:"
                        "fontcolor=white:box=1:boxcolor=black", f], check=True)
        frames.append(f)
    out = os.path.join(OUT, "grade_" + chave.replace(" ", "_").replace("ã", "a").replace("ç", "c") + ".jpg")
    inputs = sum([["-i", f] for f in frames], [])
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
                    "".join(f"[{i}:v]" for i in range(len(frames))) + f"hstack=inputs={len(frames)}", out], check=True)
    print(out)
