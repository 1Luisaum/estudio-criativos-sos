"""Catalogo de rostos do banco e dos brutos (27/10/2026): onde fica o rosto em cada foto e em cada segundo de
video, ja na tela 1080x1920 (recorte 9:16 pelo centro, como os montadores fazem). Feito uma vez; depois so
atualiza o que mudou. Serve para escolher foto/trecho ANTES de montar, sem olhar imagem nenhuma.

Uso:
  python -I catalogo.py atualizar                    # varre banco de videos do <crianca> e VIDEOS PARA EDITAR
  python -I catalogo.py livres --zona 1076-1504 [--zona 890-1010] [--tipo foto|video] [--de banco|brutos]
        [--crianca Adrielly]
        lista o que tem rosto e nenhum rosto nas faixas (fotos e trechos de video de 2 s ou mais)
  python -I catalogo.py ver "<arquivo>" [--t 12]     # rostos daquele arquivo (ou daquele segundo)
Arquivo: ~/.claude/estudio-ong/catalogo_rostos.json
"""
import argparse, glob, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
import rostos  # noqa: E402

CAT = os.path.join(os.path.expanduser("~"), ".claude", "estudio-ong", "catalogo_rostos.json")
CONFIG = os.path.join(os.path.expanduser("~"), ".claude", "estudio-ong.json")
VIDEO = (".mp4", ".mov", ".m4v", ".mkv")


def raiz():
    try:
        return json.load(open(CONFIG, encoding="utf-8-sig"))["raiz"]
    except (OSError, ValueError, KeyError):
        return glob.glob(os.path.join(os.path.expanduser("~"), "Desktop", "EDI*CLAUDE"))[0]


def carregar():
    try:
        return json.load(open(CAT, encoding="utf-8"))
    except (OSError, ValueError):
        return {"arquivos": {}}


def salvar(c):
    import time
    tmp = CAT + ".tmp"
    json.dump(c, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    for _ in range(50):  # no Windows, outro processo lendo o catalogo bloqueia a troca por um instante
        try:
            os.replace(tmp, CAT)
            return
        except PermissionError:
            time.sleep(0.2)
    os.replace(tmp, CAT)


def crianca_de(path):
    """Pedrinho ou Adrielly pelo caminho (a pasta da Adrielly fica em <raiz>\\adrielly, desde 27/10/2026)."""
    return "Adrielly" if "adriel" in path.lower() else "Pedrinho"


def fontes():
    """[(grupo, caminho)] do banco e dos brutos das duas criancas. As versoes _tratadas (P&B/borrado) entram no
    banco; os originais fortes ficam de fora das sugestoes (fortes.json)."""
    r = raiz()
    pastas = [(p, "banco") for p in glob.glob(os.path.join(r, "banco de v*"))]
    pastas += [(os.path.join(r, "VÍDEOS PARA EDITAR"), "brutos")]
    for b in glob.glob(os.path.join(r, "adrielly", "BANCO*")):
        pastas += [(b, "banco"), (os.path.join(b, "_jpg_do_heic"), "banco"), (os.path.join(b, "_tratadas"), "banco")]
    pastas += [(d, "brutos") for d in glob.glob(os.path.join(r, "adrielly", "BRUTOS*", "**"), recursive=True)
               if os.path.isdir(d)]
    out = []
    for pasta, grupo in pastas:
        if not os.path.isdir(pasta):
            continue
        for f in sorted(os.listdir(pasta)):
            p = os.path.join(pasta, f)
            if os.path.isfile(p) and f.lower().endswith(rostos.FOTO + VIDEO) and "(1)" not in f:
                out.append((grupo, p))
    return out


def atualizar():
    c = carregar()
    for grupo, p in fontes():
        chave = os.path.basename(p)
        mt = os.path.getmtime(p)
        if c["arquivos"].get(chave, {}).get("mtime") == mt:
            continue
        if p.lower().endswith(rostos.FOTO):
            q = rostos.ler_foto(p)
            item = {"tipo": "foto", "rostos": rostos.no_quadro(q) if q is not None else []}
        else:
            item = {"tipo": "video", "por_segundo": {str(t): rostos.no_quadro(q)
                                                     for t, q in rostos.quadros_video(p, passo=1.0)}}
        c["arquivos"][chave] = {"grupo": grupo, "crianca": crianca_de(p), "caminho": p, "mtime": mt, **item}
        salvar(c)
        n = len(item.get("por_segundo", {})) or 1
        print(f"  {grupo:6s} {chave[:60]:60s} {n} quadro(s)", flush=True)
    print("catalogo:", CAT, len(c["arquivos"]), "arquivos")


def _livre(rs, zonas):
    rs = [r for r in rs if r[3] - r[1] >= 70]
    return bool(rs) and not any(rostos.cruza(r, z, folga=-40) for r in rs for z in zonas)


def evitar():
    """{arquivo: motivo} dos que nunca entram em video (evitar.json, ao lado)."""
    try:
        return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "evitar.json"),
                              encoding="utf-8"))["arquivos"]
    except (OSError, ValueError, KeyError):
        return {}


def fortes():
    """{arquivo original: "pb"|"borrado"} das imagens muito fortes (fortes.json, ao lado)."""
    try:
        return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fortes.json"),
                              encoding="utf-8"))["arquivos"]
    except (OSError, ValueError, KeyError):
        return {}


def livres(zonas, tipo=None, de=None, crianca=None):
    c = carregar()["arquivos"]
    ev, fo = evitar(), fortes()
    for nome, a in sorted(c.items()):
        if nome in ev or nome in fo or (tipo and a["tipo"] != tipo) or (de and a["grupo"] != de) or                 (crianca and a.get("crianca", crianca_de(a["caminho"])).lower() != crianca.lower()):
            continue
        if a["tipo"] == "foto":
            if _livre(a["rostos"], zonas):
                print(f"foto   {nome}  rosto y={[(r[1], r[3]) for r in a['rostos']]}")
        else:
            ts = sorted((float(t), rs) for t, rs in a["por_segundo"].items())
            ini = None
            trechos = []
            for t, rs in ts + [(1e9, [])]:
                if _livre(rs, zonas):
                    ini = t if ini is None else ini
                else:
                    if ini is not None and t - ini >= 2:
                        trechos.append((ini, t if t < 1e9 else ts[-1][0] + 1))
                    ini = None
            if trechos:
                print(f"video  {nome}  " + ", ".join(f"{a_:.0f}-{b_:.0f}s" for a_, b_ in trechos[:12]))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("atualizar")
    l = sp.add_parser("livres"); l.add_argument("--zona", action="append", required=True)
    l.add_argument("--tipo", choices=["foto", "video"]); l.add_argument("--de", choices=["banco", "brutos"])
    l.add_argument("--crianca", help="Pedrinho ou Adrielly")
    v = sp.add_parser("ver"); v.add_argument("arquivo"); v.add_argument("--t", type=float)
    a = ap.parse_args()
    if a.cmd == "atualizar":
        atualizar()
    elif a.cmd == "livres":
        livres([tuple(map(int, z.split("-"))) for z in a.zona], a.tipo, a.de, a.crianca)
    else:
        it = carregar()["arquivos"].get(os.path.basename(a.arquivo))
        if not it:
            sys.exit("nao esta no catalogo (rode: catalogo.py atualizar)")
        if it["tipo"] == "foto":
            print(it["rostos"])
        else:
            ps = it["por_segundo"]
            print(ps.get(str(float(int(a.t)))) if a.t is not None else {k: v for k, v in list(ps.items())[:30]})
