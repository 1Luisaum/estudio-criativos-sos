"""Deteccao de rostos (OpenCV, sem internet) nas coordenadas da tela 1080x1920.

Usa o haarcascade_frontalface_alt2, que no teste de 27/10/2026 achou o rosto do Pedrinho na maioria dos
quadros (close deitado, cadeira de rodas, com a mae) e quase nao inventa rosto. Nao e perfeito: um rosto
muito de lado ou coberto pode passar. Por isso a conferencia avisa "nenhum rosto achado" em vez de garantir.
"""
import subprocess

import cv2
import numpy as np

W, H = 1080, 1920
_CASC = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
FOTO = (".jpg", ".jpeg", ".png", ".webp")


def no_quadro(bgr):
    """[(x0, y0, x1, y1)] dos rostos num quadro ja em 1080x1920 (ou na proporcao 9:16)."""
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    k = 540 / g.shape[1]
    g = cv2.equalizeHist(cv2.resize(g, (540, int(g.shape[0] * k))))
    out = []
    for (x, y, w, h) in _CASC.detectMultiScale(g, 1.08, 4, minSize=(36, 36)):
        s = W / 540
        out.append((int(x * s), int(y * s), int((x + w) * s), int((y + h) * s)))
    return out


def cobrir(bgr):
    """Recorta para 9:16 pelo centro e escala para 1080x1920 (como os montadores fazem)."""
    h, w = bgr.shape[:2]
    if w / h > W / H:
        nw = int(h * W / H); x = (w - nw) // 2; bgr = bgr[:, x:x + nw]
    else:
        nh = int(w * H / W); y = (h - nh) // 2; bgr = bgr[y:y + nh]
    return cv2.resize(bgr, (W, H), interpolation=cv2.INTER_AREA)


def ler_foto(path):
    im = cv2.imdecode(np.fromfile(path, np.uint8), cv2.IMREAD_COLOR)
    return None if im is None else cobrir(im)


def quadros_video(path, passo=1.0, inicio=0.0, dur=None, cobrir_tela=True):
    """[(t, quadro 1080x1920)] a cada `passo` segundos (ffmpeg ja gira o video pela rotacao gravada)."""
    vf = f"fps=1/{passo}," + ("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
                              if cobrir_tela else "scale=1080:1920")
    cmd = ["ffmpeg", "-v", "error", "-ss", str(inicio), "-i", path] + (["-t", str(dur)] if dur else []) + \
          ["-vf", vf, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    b = subprocess.run(cmd, capture_output=True).stdout
    n = len(b) // (W * H * 3)
    a = np.frombuffer(b[:n * W * H * 3], np.uint8).reshape(n, H, W, 3)
    return [(round(inicio + i * passo, 2), a[i]) for i in range(n)]


def cruza(rosto, zona, folga=0):
    """O rosto (x0, y0, x1, y1) encosta na faixa vertical zona=(y0, y1)?"""
    return rosto[1] < zona[1] + folga and rosto[3] > zona[0] - folga
