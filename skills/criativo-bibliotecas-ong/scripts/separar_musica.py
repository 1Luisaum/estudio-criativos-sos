"""Tira a voz de um anuncio de referencia e deixa so a musica de fundo (Demucs htdemucs), para usar a mesma
musica dos criativos que deram certo (pedido do usuario, 03/11/2026).
Uso (com o Python do Demucs): ~/.claude/estudio-ong/sep/Scripts/python.exe separar_musica.py <entrada.mp4|wav> <saida.wav>"""
import subprocess
import sys
import tempfile
import os

import numpy as np
import soundfile as sf
import torch
from demucs.apply import apply_model
from demucs.pretrained import get_model

src, dst = sys.argv[1], sys.argv[2]
tmp = os.path.join(tempfile.mkdtemp(), "in.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "2", "-ar", "44100", tmp], check=True)
wav, sr = sf.read(tmp, dtype="float32")
x = torch.from_numpy(wav.T.copy())
ref = x.mean(0)
m = get_model("htdemucs")
m.eval()
with torch.no_grad():
    out = apply_model(m, ((x - ref.mean()) / ref.std())[None], device="cpu", progress=False)[0]
out = out * ref.std() + ref.mean()
musica = sum(out[i] for i, n in enumerate(m.sources) if n != "vocals")
sf.write(dst, musica.numpy().T.astype(np.float32), sr)
print("ok", dst)
