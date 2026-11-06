"""Copia um modelo aprovado para uma pasta de plano nova, pronta para trocar falas, b-roll, textos e musica.
Uso: python -I novo_plano.py <modelo> <nome da pasta> [--crianca Adrielly]
  <modelo>: id de modelos\\ (ex.: peb212_l1_esqueceram) ou so o numero do PEB de exemplo (ex.: 212)
  <nome da pasta>: ex.: Pedrinho_bib_esqueceram_v2 (fica em EDITADOS\\_planos\\)
Depois: edite o plano.json e monte com  python -I bib.py "<pasta>\\plano.json"."""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import comum as C  # noqa: E402

args = sys.argv[1:]
if len(args) < 2:
    sys.exit(__doc__)
mod, nome = args[0], args[1]
achados = glob.glob(os.path.join(AQUI, "..", "modelos", (f"peb{mod}_*" if mod.isdigit() else mod) + ".json"))
if not achados:
    sys.exit("Modelo nao encontrado. Veja references\\modelos.md")
p = json.load(open(achados[0], encoding="utf-8"))
if "--crianca" in args:
    p["crianca"] = args[args.index("--crianca") + 1]
pasta = os.path.join(C.raiz(), "EDITADOS", "_planos", nome)
if os.path.exists(os.path.join(pasta, "plano.json")):
    sys.exit(f"Ja existe {pasta}\\plano.json (nao sobrescrevo). Use outro nome.")
os.makedirs(os.path.join(pasta, "render"), exist_ok=True)
json.dump(p, open(os.path.join(pasta, "plano.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("plano:", os.path.join(pasta, "plano.json"))
print("modelo:", p["modelo"]["id"], "-", p["modelo"]["descricao"][:160])
