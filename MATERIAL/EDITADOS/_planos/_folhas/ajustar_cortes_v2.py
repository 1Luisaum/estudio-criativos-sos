"""Aplica nos 5 planos de Cortes com gancho: sem selo, faixa de doacao e CTA 'Saiba mais'."""
import glob, json, os

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BR = os.path.join(os.path.dirname(os.path.dirname(P)), "VÍDEOS PARA EDITAR")
VALOR = {"Pedrinho_5horas_v1": "R$ 5", "Pedrinho_curativos_acabando_v1": "R$ 5", "Pedrinho_noite_v1": "R$ 12",
         "Pedrinho_espera_v1": "R$ 5", "Pedrinho_esquecido_v1": "R$ 3"}
for nome, valor in VALOR.items():
    f = os.path.join(P, nome, "plano.json")
    p = json.load(open(f, encoding="utf-8-sig"))
    p["badge"] = None
    p["chamada"] = {"linhas": [[f"APENAS {valor}", 124], ["PODEM MUDAR A VIDA DO", 64], ["PEDRINHO GUERREIRO!", 84]], "y": 1300}
    if p.get("endcard"):
        p["endcard"]["cta"] = "TOQUE EM SAIBA MAIS"
    if not os.path.exists(p["raw"]):  # bruto renomeado (ganhou "_" no fim)
        base = os.path.splitext(os.path.basename(p["raw"]))[0]
        p["raw"] = next(x for x in glob.glob(os.path.join(BR, "*.mp4")) if os.path.basename(x).startswith(base)).replace("\\", "/")
    json.dump(p, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok", nome, valor, os.path.exists(p["raw"]))
