"""Conferencia automatica de um MP4 final, sem mandar imagem para o Claude (27/10/2026).

Checa: duracao, travadinha (freezedetect), buracos no audio, logo SOS (marca gravada pelo marca.py) e
rosto em cima das faixas de texto do estilo (deteccao OpenCV a cada 0,5 s). So gera uma folha de quadros
pequena quando acha algo, para o Claude olhar so o que precisa.

Uso: python -I conferir_auto.py <mp4> [--estilo "CORTES COM LETTERING"] [--zonas 890-1010,1076-1504]
                                [--desde 10.5] [--json saida.json]
O estilo sai do nome "PEB <n> - <ESTILO>.mp4" se nao for passado. Saida: 0 = tudo ok, 2 = ver avisos.
"""
import argparse, json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
import rostos  # noqa: E402

# faixas de texto fixas de cada estilo (y0, y1) na tela 1080x1920, tiradas dos SKILL.md; "desde" = a partir de
# quantos segundos a faixa vale (o gancho do UNICEF nao tem lettering). Duracao (min, max) em segundos.
ESTILOS = {
    "CORTES COM LETTERING": {"zonas": [(890, 1010), (1076, 1504)], "dur": (25, 50)},
    "UNICEF": {"zonas": [(890, 1010), (1076, 1504)], "desde_gancho": True, "dur": (35, 50)},
    "CORTES COM GANCHO": {"zonas": [(950, 1070)], "dur": (20, 50)},
    "CAIXAS PEDIDO DE TEMPO": {"zonas": [(200, 470), (1220, 1480)], "dur": (25, 40)},
    "CAIXAS ASPAS": {"zonas": [(200, 470), (1220, 1480)], "dur": (25, 40)},
    "CAIXAS URGENTE": {"zonas": [(200, 470), (1220, 1480)], "dur": (25, 40)},
    "MÃE DESESPERADA": {"zonas": [(1344, 1580)], "dur": (25, 40)},
    "SALVA VIDA": {"zonas": [(180, 420)], "dur": (24, 34)},
    "CORRENTE DO BEM": {"zonas": [(240, 500)], "dur": (24, 34)},
    "DA DOR À ESPERANÇA": {"zonas": [(1100, 1200)], "dur": (35, 50)},
    "NARRADO DE IMPACTO": {"zonas": [(1180, 1340)], "dur": (55, 80)},
    "REPORTAGEM": {"zonas": [(290, 470), (1080, 1250)], "dur": (45, 65)},
}


def run(c):
    return subprocess.run(c, capture_output=True, text=True, encoding="utf-8", errors="replace")


def conferir(mp4, estilo=None, zonas=None, desde=0.0, folha_dir=None):
    nome = os.path.basename(mp4)
    if not estilo and " - " in nome:
        estilo = nome.split(" - ", 1)[1].rsplit(".", 1)[0].upper()
    cfg = ESTILOS.get(estilo or "", {})
    zonas = zonas or cfg.get("zonas", [])
    probe = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "format=duration:format_tags=comment",
                            "-of", "json", mp4]).stdout or "{}")
    dur = float(probe.get("format", {}).get("duration", 0))
    avisos, info = [], {"arquivo": mp4, "estilo": estilo, "duracao": round(dur, 2)}
    lo, hi = cfg.get("dur", (0, 1e9))
    if not lo <= dur <= hi:
        avisos.append(f"duração {dur:.1f} s fora da faixa do estilo ({lo}-{hi} s)")
    # logo
    tag = (probe.get("format", {}).get("tags", {}) or {}).get("comment", "")
    info["logo"] = "logo SOS" in tag
    if not info["logo"]:
        avisos.append("sem a marca da logo no arquivo (montado antes de 27/10 ou sem passar pelo marca.py)")
    # travadinha (0,2 s ou mais e erro; foto parada de proposito como tela final pode aparecer)
    fz = []
    st = None
    for l in run(["ffmpeg", "-hide_banner", "-i", mp4, "-vf", "freezedetect=n=0.002:d=0.12", "-map", "0:v",
                  "-f", "null", "-"]).stderr.splitlines():
        if "freeze_start:" in l:
            st = float(l.split("freeze_start:")[1])
        if "freeze_duration:" in l and st is not None:
            d = float(l.split("freeze_duration:")[1])
            if d >= 0.2:
                fz.append((round(st, 2), round(d, 2)))
    info["travadinhas"] = fz
    if fz:
        avisos.append(f"travadinha(s) de 0,2 s ou mais em {fz} (se for a tela final parada, ignore)")
    # buracos no audio
    pk = [tuple(map(float, l.split(",")[:2])) for l in run(["ffprobe", "-v", "error", "-select_streams", "a",
          "-show_entries", "packet=pts_time,duration_time", "-of", "csv=p=0", mp4]).stdout.split() if l]
    holes = [(round(a[0], 2), round(b[0], 2)) for a, b in zip(pk, pk[1:]) if b[0] - a[0] - a[1] > 0.02]
    info["buracos_audio"] = holes
    if not pk:
        avisos.append("sem áudio")
    elif holes:
        avisos.append(f"buracos no áudio em {holes}")
    # rosto x faixas de texto
    batidas = []
    if zonas:
        for t, q in rostos.quadros_video(mp4, passo=0.5, cobrir_tela=False):
            if t < desde:
                continue
            for r in rostos.no_quadro(q):
                if (r[3] - r[1]) < 70:  # muito pequeno: costuma ser engano do detector
                    continue
                for z in zonas:
                    if rostos.cruza(r, z, folga=-40):  # so conta se o rosto entra 40 px ou mais no texto
                        batidas.append({"t": t, "rosto_y": [r[1], r[3]], "faixa": list(z)})
    info["rosto_em_texto"] = batidas
    if batidas:
        ts = sorted({b["t"] for b in batidas})
        avisos.append(f"rosto encostando numa faixa de texto em {len(ts)} momento(s): {ts[:12]}")
    info["avisos"] = avisos
    # folha so dos momentos suspeitos
    if folha_dir and batidas:
        os.makedirs(folha_dir, exist_ok=True)
        ts = sorted({b["t"] for b in batidas})[:6]
        fs = []
        for i, t in enumerate(ts):
            f = os.path.join(folha_dir, f"_suspeito_{os.path.splitext(nome)[0]}_{i}.png")  # nome proprio: duas conferencias em paralelo
            run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", mp4, "-frames:v", "1", "-vf", "scale=240:-2", f])
            fs.append(f)
        folha = os.path.join(folha_dir, os.path.splitext(nome)[0] + "_suspeitos.jpg")
        ins = sum([["-i", f] for f in fs], [])
        run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex",
             "".join(f"[{i}]" for i in range(len(fs))) + f"hstack=inputs={len(fs)}" if len(fs) > 1 else "null", folha])
        for f in fs:
            os.remove(f)
        info["folha_suspeitos"] = folha
    return info


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4")
    ap.add_argument("--estilo")
    ap.add_argument("--zonas", help="faixas y0-y1 separadas por virgula")
    ap.add_argument("--desde", type=float, default=0.0)
    ap.add_argument("--json")
    ap.add_argument("--folha", help="pasta para a folha dos momentos suspeitos")
    a = ap.parse_args()
    z = [tuple(map(int, s.split("-"))) for s in a.zonas.split(",")] if a.zonas else None
    r = conferir(os.path.abspath(a.mp4), a.estilo and a.estilo.upper(), z, a.desde, a.folha)
    if a.json:
        json.dump(r, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{os.path.basename(a.mp4)}: {r['duracao']} s · logo {'ok' if r['logo'] else 'NÃO MARCADA'} · "
          f"{'OK' if not r['avisos'] else str(len(r['avisos'])) + ' aviso(s)'}")
    for x in r["avisos"]:
        print("  -", x)
    sys.exit(2 if r["avisos"] else 0)
