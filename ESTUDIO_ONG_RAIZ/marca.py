"""Marca d'agua da SOS Human Help em todo video: o texto @soshumanhelppt (regra do usuario de 29/10/2026,
no lugar da logo da SOS de 26/10/2026).

A marca (marca_soshumanhelppt.png, ao lado deste arquivo, com o texto @soshumanhelppt) entra com opacidade baixa e anda devagar pela tela o video
inteiro, batendo nas bordas (como o logo de DVD), entre y=200 e y=1500. O audio e copiado sem mudar.

REGRA OBRIGATORIA (pedido do usuario, 26/10/2026): todo video de todo modelo e skill sai com a logo.
Nao existe opcao para desligar. Se a logo faltar, o montador PARA com erro (nunca entrega video sem logo).

Os montadores das skills chamam no_fim(plano, <mp4 final>) no fim. Para aplicar num video ja pronto:
    python -I marca.py "<video.mp4>"
Nao rode duas vezes no mesmo arquivo (a logo entraria duas vezes); para refazer, rode o montador de novo.
"""
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(AQUI, "marca_soshumanhelppt.png")  # @soshumanhelppt (29/10/2026)
OPACIDADE, LARGURA = 0.55, 405
VX, VY = 70, 45          # pixels por segundo (anda devagar)
TOPO, FUNDO = 200, 1500  # faixa vertical por onde a logo passa


def aplicar(mp4, opacidade=OPACIDADE, largura=LARGURA):
    if not os.path.exists(LOGO):
        sys.exit(f"ERRO: falta a logo obrigatoria {LOGO}. Copie marca_soshumanhelppt.png para a pasta de scripts da skill.")
    tmp = mp4 + ".marca.mp4"
    hx = f"(W-w)"
    hy = f"({FUNDO}-{TOPO}-h)"
    fc = (f"[1:v]scale={largura}:-1,format=rgba,colorchannelmixer=aa={opacidade}[lg];"
          f"[0:v][lg]overlay=x='abs(mod(t*{VX},2*{hx})-{hx})':"
          f"y='{TOPO}+abs(mod(t*{VY}+{hy}/2,2*{hy})-{hy})':shortest=1:eval=frame,format=yuv420p[v]")
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp4, "-loop", "1", "-i", LOGO, "-filter_complex", fc,
                        "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-preset", "slow", "-crf", "19",
                        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", tmp],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(r.stderr[-1500:])
        sys.exit("ffmpeg falhou ao aplicar a marca")
    shutil.move(tmp, mp4)
    print("marca: @soshumanhelppt aplicado")
    return mp4


def no_fim(plano, mp4):
    """Chamada pelos montadores no fim de todo video. Obrigatoria: ignora qualquer pedido de plano para tirar a logo."""
    if (plano or {}).get("sem_marca"):
        print("marca: 'sem_marca' ignorado - a logo e obrigatoria em todo video")
    return aplicar(mp4)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for f in sys.argv[1:]:
        aplicar(os.path.abspath(f))
