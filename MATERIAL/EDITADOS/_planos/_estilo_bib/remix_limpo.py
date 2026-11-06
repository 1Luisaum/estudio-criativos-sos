"""Refaz o audio de um video do bib.py sem o loudnorm dinamico (que sobe o chiado das pausas e dos agudos em 11-14 dB)
e troca no MP4, sem mexer na imagem. Pedido do usuario de 06/11/2026 ("cheia de chuvisco").
Cada pedaco recebe ganho FIXO medido: falas reais e narracao a -16 LUFS, musica a -27 LUFS (-15 sem fala);
no fim so um limitador leve.
Uso: python -I remix_limpo.py <pasta do plano> [<mp4>]"""
import json
import os
import re
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
PL = os.path.join(os.path.expanduser("~"), "Desktop", "EDIÇÃO COM CLAUDE", "EDITADOS", "_planos")
RAIZ = os.path.join(os.path.expanduser("~"), "Desktop", "EDIÇÃO COM CLAUDE")
FALA, MUS_SOB, MUS_SO = -16.0, -27.0, -15.0


def r(x):
    return x.replace("{RAIZ}", RAIZ) if isinstance(x, str) else x


def lufs(args):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-nostats"] + args + ["-vn", "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", o)
    return float(m[-1]) if m else -70.0


def ganho(alvo, med, teto=12.0):
    return 10 ** (max(min(alvo - med, teto), -20) / 20)


def main():
    pasta = sys.argv[1]
    p = json.load(open(os.path.join(PL, pasta, "plano.json"), encoding="utf-8-sig"))
    mp4 = sys.argv[2] if len(sys.argv) > 2 else r(p["saida"])
    base = p["base"]
    total = sum(b["fim"] - b["ini"] for b in base)
    cmd, fc, lab, t, k = ["ffmpeg", "-v", "error", "-y"], [], [], 0.0, 0
    tem_fala = bool(p.get("voz"))
    for b in base:
        d = b["fim"] - b["ini"]
        if b.get("som"):
            tem_fala = True
            arq = r(b["arq"])
            g = ganho(FALA, lufs(["-ss", str(b["ini"]), "-t", f"{d:.3f}", "-i", arq]))
            cmd += ["-ss", f"{b['ini']:.3f}", "-t", f"{d:.3f}", "-i", arq]
            ms = int(round(t * 1000))
            fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.4f},afade=t=in:d=0.03,"
                      f"afade=t=out:st={max(d - 0.04, 0):.3f}:d=0.04,adelay={ms}|{ms}[s{k}]")
            lab.append(f"[s{k}]")
            k += 1
        t += d
    vz = p.get("voz")
    if vz:
        arq = r(vz["arq"])
        g = ganho(FALA, lufs(["-i", arq]))
        ms = int(round(vz.get("de", 0) * 1000))
        cmd += ["-i", arq]
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.4f},adelay={ms}|{ms}[s{k}]")
        lab.append(f"[s{k}]")
        k += 1
    if p.get("musica"):
        m = r(p["musica"])
        alvo = p.get("musica_lufs", MUS_SOB if tem_fala else MUS_SO)
        g = ganho(alvo, lufs(["-t", "90", "-i", m]), teto=20)
        cmd += ["-ss", str(p.get("musica_ini", 0)), "-stream_loop", "-1", "-i", m]
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
                  f"volume={g:.4f},afade=t=in:d=0.4,afade=t=out:st={total - 1.5:.3f}:d=1.5[s{k}]")
        lab.append(f"[s{k}]")
        k += 1
    fc.append("".join(lab) + f"amix=inputs={len(lab)}:normalize=0:duration=longest,apad,atrim=0:{total:.3f},"
              "alimiter=limit=0.93:attack=3:release=60:level=disabled[a]")
    wav = mp4 + ".limpo.wav"
    subprocess.run(cmd + ["-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s16le", wav], check=True)
    tmp = mp4 + ".novo.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-shortest", tmp], check=True)
    shutil.move(tmp, mp4)
    os.remove(wav)
    print("audio limpo:", os.path.basename(mp4), f"{total:.1f}s, {len(lab)} faixas")


main()
