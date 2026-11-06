"""Lista tudo o que ja foi usado nos videos narrados, para a copy nova nao repetir nada.

Le EDITADOS/_planos/*/plano.json e roteiro_audio.json e mostra, por video: manchete, falas reais
usadas (com o arquivo de origem), narracoes, cartelas e tela final.
Com --checar <roteiro_audio.json novo>, aponta frases da narracao nova parecidas com alguma ja usada.

Uso: python -I copias_usadas.py [--checar caminho\\roteiro_audio.json]
"""
import argparse, difflib, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
import comum as C  # noqa: E402

PLANOS = os.path.join(C.raiz(), "EDITADOS", "_planos")


def load(p):
    try:
        return json.load(open(p, encoding="utf-8-sig"))
    except Exception:
        return None


def frases(texto):
    return [f.strip() for f in re.split(r"(?<=[.!?…])\s+", texto) if len(f.strip()) > 3]


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower())


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--checar", default="")
    a = ap.parse_args()
    usadas = []          # (video, tipo, texto)
    aberturas = []       # 1o bloco de cada video
    proprio = os.path.normcase(os.path.dirname(os.path.abspath(a.checar))) if a.checar else ""
    for d in sorted(glob.glob(os.path.join(PLANOS, "*"))):
        if os.path.normcase(os.path.abspath(d)) == proprio:
            continue          # o proprio video em producao nao conta
        plano, rot = load(os.path.join(d, "plano.json")), load(os.path.join(d, "roteiro_audio.json"))
        if not plano or "blocks" not in plano:
            continue          # so videos do estilo narrado
        nome = os.path.basename(d)
        aberturas.append((nome, plano["blocks"][0].get("txt", "")))
        print(f"\n=== {nome}")
        hk = plano.get("hook")
        if hk:
            txt = " / ".join(l["text"] if isinstance(l, dict) else l for l in hk["lines"]).replace("*", "")
            print(f"  manchete: {txt}"); usadas.append((nome, "manchete", txt))
        for b in plano["blocks"]:
            t = b.get("type")
            if t == "real":
                print(f"  real [{b.get('tag', '')}] {os.path.basename(b['src'])} {b['cuts'][0][0]:.1f}s: {b.get('txt', '')}")
                usadas.append((nome, "real", b.get("txt", "")))
            elif t == "narr":
                key = os.path.splitext(os.path.basename(b["audio"]))[0]
                txt = (rot or {}).get("narracao", {}).get(key, b.get("txt", ""))
                print(f"  narr ({b.get('look', 'pb')}): {txt}")
                usadas += [(nome, "narr", f) for f in frases(txt)]
            elif t == "card":
                txt = " / ".join(b["lines"]); print(f"  cartela: {txt}"); usadas.append((nome, "cartela", txt))
            elif t == "end":
                txt = " / ".join(b["lines"]).replace("*", ""); print(f"  final: {txt}"); usadas.append((nome, "final", txt))
    if a.checar:
        novo = load(a.checar)
        print("\n=== checagem da narracao nova")
        ruins = 0
        for k, txt in novo["narracao"].items():
            for f in frases(txt):
                parecidas = [(v, t, u) for v, t, u in usadas if t in ("narr", "manchete", "cartela", "final")
                             and difflib.SequenceMatcher(None, norm(f), norm(u)).ratio() >= 0.6]
                for v, t, u in parecidas:
                    print(f"  REPETE  {k}: \"{f}\"  ~  {t} de {v}: \"{u}\"")
                ruins += len(parecidas)
        # plano novo (se ja existir na mesma pasta): manchete, cartelas e final tambem precisam ser novos;
        # falas reais repetidas e a mesma abertura viram aviso
        plano_novo = load(os.path.join(os.path.dirname(os.path.abspath(a.checar)), "plano.json"))
        avisos = 0
        if plano_novo and "blocks" in plano_novo:
            novos = []
            hk = plano_novo.get("hook")
            if hk:
                novos.append(("manchete", " / ".join(l["text"] if isinstance(l, dict) else l for l in hk["lines"]).replace("*", "")))
            for b in plano_novo["blocks"]:
                if b.get("type") == "card":
                    novos.append(("cartela", " / ".join(b["lines"])))
                elif b.get("type") == "end":
                    novos.append(("final", " / ".join(b["lines"]).replace("*", "")))
            for t, txt in novos:
                for v, tu, u in usadas:
                    if tu == t and difflib.SequenceMatcher(None, norm(txt), norm(u)).ratio() >= 0.6:
                        print(f"  REPETE  {t}: \"{txt}\"  ~  {v}: \"{u}\""); ruins += 1
            reais = [b.get("txt", "") for b in plano_novo["blocks"] if b.get("type") == "real"]
            for r in reais:
                for v, tu, u in usadas:
                    if tu == "real" and difflib.SequenceMatcher(None, norm(r), norm(u)).ratio() >= 0.7:
                        print(f"  aviso   fala real repetida: \"{r}\" (ja usada em {v})"); avisos += 1
            primeiro = plano_novo["blocks"][0].get("txt", "")
            for v, ab in aberturas:
                if difflib.SequenceMatcher(None, norm(primeiro), norm(ab)).ratio() >= 0.7:
                    print(f"  REPETE  abertura igual a de {v}: \"{ab}\""); ruins += 1
        print("RESULTADO:", "copy toda nova" if not ruins else f"{ruins} repeticao(oes); reescreva",
              f"| {avisos} fala(s) real(is) repetida(s): use falas novas sempre que o material permitir" if avisos else "")


if __name__ == "__main__":
    main()
