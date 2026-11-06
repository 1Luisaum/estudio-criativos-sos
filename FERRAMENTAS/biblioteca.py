"""Biblioteca de falas reais (27/10/2026): todas as frases dos brutos transcritos, com bruto, tempo e quem
fala, e em quais planos cada uma ja entrou. Substitui ler as transcricoes e os planos inteiros a cada video:
o roteirista consulta aqui o que existe e o que ainda nao foi usado.

Uso:
  python -I biblioteca.py atualizar            # refaz a partir de CONHECIMENTO/transcricoes e EDITADOS/_planos
  python -I biblioteca.py buscar atadura gaze  # frases com essas palavras (com o uso)
  python -I biblioteca.py livres [--bruto 001530] [--max-usos 0]   # frases pouco usadas
Arquivo: ~/.claude/estudio-ong/biblioteca_falas.json
"""
import argparse, glob, json, os, re, sys, unicodedata

H = os.path.expanduser("~")
TX = os.path.join(H, ".claude", "estudio-ong", "CONHECIMENTO", "transcricoes")
BIB = os.path.join(H, ".claude", "estudio-ong", "biblioteca_falas.json")
CONFIG = os.path.join(H, ".claude", "estudio-ong.json")


def raiz():
    try:
        return json.load(open(CONFIG, encoding="utf-8-sig"))["raiz"]
    except (OSError, ValueError, KeyError):
        return glob.glob(os.path.join(H, "Desktop", "EDI*CLAUDE"))[0]


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", s).split()


def brutos_do_leiame():
    """{arquivo de transcricao: (bruto, quem fala)} a partir da tabela do LEIA-ME."""
    out = {}
    try:
        for l in open(os.path.join(TX, "LEIA-ME.md"), encoding="utf-8"):
            m = re.match(r"\|\s*`([^`]+\.json)`.*?\|\s*(.+?)\s*\|\s*(.+?)\s*\|", l)
            if m:
                out[m.group(1)] = (m.group(2).strip("` "), m.group(3))
    except OSError:
        pass
    return out


def frases(words):
    """Quebra nas pontuacoes de fim de frase ou em pausas de 0,7 s; guarda inicio, fim e falante."""
    ws = [w for w in words if w.get("type", "word") == "word"]
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        fim = w["text"].strip()[-1:] in ".!?…"
        pausa = i + 1 < len(ws) and ws[i + 1]["start"] - w["end"] > 0.7
        if fim or pausa or i == len(ws) - 1:
            txt = " ".join(x["text"].strip() for x in cur)
            if len(cur) >= 3:
                out.append({"texto": txt, "inicio": round(cur[0]["start"], 2), "fim": round(cur[-1]["end"], 2),
                            "falante": cur[0].get("speaker_id", "")})
            cur = []
    return out


def textos_dos_planos():
    """{nome do plano: texto normalizado de tudo o que o plano escreve (cortes, falas, narracao, caixas)}."""
    out = {}
    for pd in glob.glob(os.path.join(raiz(), "EDITADOS", "_planos", "*")):
        acc = []
        for f in ("plano.json", "roteiro_audio.json"):
            try:
                d = json.load(open(os.path.join(pd, f), encoding="utf-8-sig"))
            except (OSError, ValueError):
                continue

            def walk(x):
                if isinstance(x, dict):
                    for k, v in x.items():
                        if k not in ("raw", "transcript", "bank", "music", "saida", "out", "src", "caminho"):
                            walk(v)
                elif isinstance(x, list):
                    for v in x:
                        walk(v)
                elif isinstance(x, str) and " " in x:
                    acc.append(x)
            walk(d)
        if acc:
            out[os.path.basename(pd)] = " " + " ".join(norm(" ".join(acc))) + " "
    return out


def cortes_dos_planos():
    """{nome do bruto (casefold): [(plano, inicio, fim)]} dos planos que cortam o bruto com tempo (raw + segments)."""
    out = {}
    for pd in glob.glob(os.path.join(raiz(), "EDITADOS", "_planos", "*")):
        try:
            p = json.load(open(os.path.join(pd, "plano.json"), encoding="utf-8-sig"))
        except (OSError, ValueError):
            continue
        raw = os.path.basename(p.get("raw") or "").casefold()
        for s in p.get("segments", []) if raw else []:
            if isinstance(s, dict) and "in" in s and "out" in s:
                out.setdefault(raw, []).append((os.path.basename(pd), s["in"], s["out"]))
    return out


def usado_em(fr, planos, cortes):
    """Planos onde a frase entrou, mesmo que em parte: pelo tempo do corte no bruto ou por 3 trios de palavras
    seguidas no texto do plano (os planos guardam a fala limpa, sem os "e" e com plural corrigido)."""
    ws = norm(fr["texto"])
    tri = [" " + " ".join(ws[i:i + 3]) + " " for i in range(max(1, len(ws) - 2))]
    ok = {n for n, t in planos.items() if sum(x in t for x in tri) >= min(3, len(tri))}
    for plano, a, b in cortes.get(fr["bruto"].casefold(), []):
        if a < fr["fim"] - 0.2 and b > fr["inicio"] + 0.2:
            ok.add(plano)
    return sorted(ok)


def atualizar():
    leia = brutos_do_leiame()
    planos = textos_dos_planos()
    cortes = cortes_dos_planos()
    bib = []
    # Adrielly (27/10/2026): transcricoes/adrielly/<nome>.json + indice.json {caminho do bruto: nome}
    adri = {}
    try:
        adri = {v: k for k, v in json.load(open(os.path.join(TX, "adrielly", "indice.json"), encoding="utf-8")).items()}
    except (OSError, ValueError):
        pass
    arquivos = sorted(glob.glob(os.path.join(TX, "*.json"))) + \
        sorted(f for f in glob.glob(os.path.join(TX, "adrielly", "*.json")) if not f.endswith("indice.json"))
    for f in arquivos:
        try:
            d = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if os.path.basename(os.path.dirname(f)) == "adrielly":
            rel = adri.get(os.path.basename(f), os.path.basename(f))
            leia[os.path.basename(f)] = (os.path.basename(rel), f"Adrielly ({os.path.dirname(rel) or 'raiz dos brutos'})")
        bruto, quem = leia.get(os.path.basename(f), ("?", "?"))
        bruto = re.split(r"(?<=\.mp4)", bruto, 1)[0].strip("` ")  # "roteiro 7.mp4` (VIDEOS..." -> "roteiro 7.mp4"
        for fr in frases(d.get("words", [])):
            fr.update({"transcricao": os.path.basename(f), "bruto": bruto, "quem_fala": quem})
            fr["usado_em"] = usado_em(fr, planos, cortes)
            bib.append(fr)
    json.dump({"frases": bib}, open(BIB, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    usadas = sum(1 for b in bib if b["usado_em"])
    print(f"biblioteca: {len(bib)} frases de {len({b['transcricao'] for b in bib})} brutos; "
          f"{usadas} já usadas, {len(bib) - usadas} nunca usadas -> {BIB}")


def mostrar(b):
    u = f"usada {len(b['usado_em'])}x ({', '.join(b['usado_em'][:3])}{'…' if len(b['usado_em']) > 3 else ''})" \
        if b["usado_em"] else "NUNCA USADA"
    print(f"[{b['bruto']} {b['inicio']:.2f}-{b['fim']:.2f} {b['falante']}] {b['texto']}  · {u}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("atualizar")
    b = sp.add_parser("buscar"); b.add_argument("palavras", nargs="+")
    l = sp.add_parser("livres"); l.add_argument("--bruto", default=""); l.add_argument("--max-usos", type=int, default=0)
    a = ap.parse_args()
    if a.cmd == "atualizar":
        atualizar()
        sys.exit()
    bib = json.load(open(BIB, encoding="utf-8"))["frases"]
    if a.cmd == "buscar":
        q = [norm(p)[0] for p in a.palavras if norm(p)]
        for x in bib:
            if all(w in norm(x["texto"]) for w in q):
                mostrar(x)
    else:
        for x in bib:
            if len(x["usado_em"]) <= a.max_usos and a.bruto.lower() in (x["bruto"] + x["transcricao"]).lower():
                mostrar(x)
