"""5 Cortes com lettering com os brutos de 02/11/2026 (pedido de 03/11/2026). Uso: python -I gerar_lettering_0211.py
Cortes: do inicio da 1a palavra -0,03 s ao fim da ultima +0,06 s (tempos da transcricao em transcricoes\\pedrinho_0211)."""
import copy
import json
import os

H = os.path.expanduser("~")
RAIZ = os.path.join(H, "Desktop", "EDIÇÃO COM CLAUDE")
PL = os.path.join(RAIZ, "EDITADOS", "_planos")
D = os.path.join(RAIZ, "VÍDEOS PARA EDITAR", "PEDRINHO 02-11-2026")
LT = os.path.join(RAIZ, "lettings")
TX = os.path.join(H, ".claude", "estudio-ong", "CONHECIMENTO", "transcricoes", "pedrinho_0211")
CL = os.path.join(RAIZ, "banco de vídeos do pedrinho", "_clipes_bib")
EX = json.load(open(os.path.join(H, ".claude", "skills", "criativo-lettering-ong", "references",
                                 "exemplo-plano-pedrinho-ajuda-de-verdade.json"), encoding="utf-8"))
A, B = "20261102_144645", "lv_0_20261102155438"
K = {n: os.path.join(D, f"20261102_{x}.mp4") for n, x in
     (("K1", "104706"), ("K2", "104943"), ("K3", "113535"), ("K4", "113735"), ("K5", "113918"), ("K6", "114148"))}
BN1, BN2, BN3 = (os.path.join(CL, x) for x in ("bn1_curativos_cama_20s.mp4", "bn2_1760826007_92s.mp4",
                                                "bn3_1792347808_155s.mp4"))


def lt(nome):
    return os.path.join(LT, nome)


# frases de cada bruto: (inicio, fim, texto)
FA = {1: (1.57, 2.92, "Eu deito pra dormir"), 2: (3.49, 5.12, "e meu corpo todo dói."), 3: (5.73, 7.04, "E dói muito mesmo."),
      4: (10.39, 12.84, "E eu tenho uma doença rara"), 5: (13.29, 14.16, "e minha pele"), 6: (14.45, 15.56, "é toda cheia"),
      7: (15.97, 16.92, "de feridas."), 8: (19.03, 20.24, "Então, por favor,"), 9: (20.75, 22.36, "me ajude no tratamento"),
      10: (22.73, 23.70, "dessa semana,"), 11: (26.95, 28.64, "dois ou cinco reais."),
      12: (31.77, 34.54, "Cinco reais pode parecer pouco pra você,"), 13: (34.93, 35.72, "mas pra mim"),
      14: (36.27, 38.20, "é sempre mais um dia sem dor"), 15: (38.73, 40.58, "e mais um dia de vida."),
      16: (41.01, 41.58, "Então,"), 17: (42.07, 42.98, "muito obrigado.")}
FB = {1: (1.71, 3.20, "Eu tenho uma doença rara,"), 2: (3.59, 4.98, "que faz surgir bolhas"),
      3: (4.99, 6.16, "por todo o meu corpo."), 4: (7.61, 8.96, "E o meu tratamento"), 5: (9.33, 9.92, "é caro,"),
      6: (10.53, 11.34, "mas é ele"), 7: (11.77, 13.16, "que faz amenizar"), 8: (13.17, 14.50, "todas as minhas dores."),
      9: (15.31, 16.48, "Eu tenho sentido"), 10: (16.53, 18.40, "muita, muita dor mesmo,"), 11: (23.73, 24.36, "Por favor,"),
      12: (24.97, 26.60, "ajude no tratamento"), 13: (26.97, 27.92, "dessa semana,"),
      14: (28.45, 30.62, "seja com dois ou cinco reais,"), 15: (32.29, 34.26, "assim já vai ajudar muito mesmo."),
      16: (34.79, 36.26, "E o meu muito obrigado,"), 17: (36.53, 37.34, "de coração.")}

V = {
    "Pedrinho_lettering_dia_sem_dor_v1": dict(
        raw=A, frases=FA, ordem=list(range(1, 18)), angulo="o corpo todo doi ate para dormir; 5 reais e mais um dia sem dor",
        broll={7: (K["K6"], 9), 9: (K["K4"], 5), 11: (K["K2"], 3), 14: (K["K1"], 2)},
        lettering=("Imagem do ChatGPT 26 de out. de 2026, 17_45_38.png", "R$ 5,00 PODEM AJUDAR O PEDRINHO HOJE"),
        fim=(BN2, 1.0)),
    "Pedrinho_lettering_bolhas_v1": dict(
        raw=B, frases=FB, ordem=list(range(1, 18)), angulo="doenca rara com bolhas; o tratamento caro ameniza as dores",
        broll={8: (K["K4"], 10), 10: (K["K6"], 3), 12: (K["K2"], 5), 14: (K["K3"], 6)},
        lettering=("Imagem do ChatGPT 26 de out. de 2026, 17_45_55.png", "R$ 5,00 PODEM LEVAR ALÍVIO PRO PEDRINHO"),
        fim=(BN3, 1.0)),
    "Pedrinho_lettering_pode_parecer_pouco_v1": dict(
        raw=A, frases=FA, ordem=[12, 13, 14, 15, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16, 17],
        angulo="abre com 'cinco reais pode parecer pouco pra voce, mas pra mim e mais um dia sem dor'",
        broll={2: (K["K6"], 15), 7: (K["K1"], 4), 9: (BN1, 1), 11: (K["K3"], 2)},
        lettering=("Imagem do ChatGPT 26 de out. de 2026, 17_46_14.png", "R$ 5,00 PODEM LEVAR CONFORTO PRO PEDRINHO"),
        fim=(BN3, 2.5)),
    "Pedrinho_lettering_muita_dor_v1": dict(
        raw=B, frases=FB, ordem=[9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16, 17],
        angulo="abre com 'eu tenho sentido muita, muita dor mesmo'",
        broll={5: (K["K2"], 8), 8: (K["K1"], 5), 12: (K["K5"], 2), 14: (BN1, 1)},
        lettering=("R$ 5,00 Podem Ajudar o Pedrinho (1).png", "R$ 5,00 PODEM AJUDAR O PEDRINHO HOJE"),
        fim=(BN2, 9.0)),
    "Pedrinho_lettering_tratamento_semana_v1": dict(
        raw=B, frases=FB, ordem=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17],
        angulo="sem citar valor na fala: o tratamento caro e o pedido de ajuda no tratamento dessa semana",
        broll={8: (K["K3"], 0), 10: (K["K5"], 5), 12: (K["K4"], 20)},
        lettering=("Imagem do ChatGPT 26 de out. de 2026, 17_53_18.png", "R$ 10,00 PODEM AJUDAR NO TRATAMENTO DO PEDRINHO"),
        fim=(BN2, 1.0)),
}
ZC = ["Z1", "Z2", "Z3", "ZF"]
for nome, v in V.items():
    p = copy.deepcopy(EX)
    for k in ("out", "saida"):
        p.pop(k, None)
    segs, zi = [], 0
    for n in v["ordem"]:
        a, b, txt = v["frases"][n]
        s = {"in": a, "out": b, "txt": txt}
        if n in v["broll"]:
            src, st = v["broll"][n]
            s["broll"] = [{"src": src, "start": st}]
        else:
            s["zoom"] = ZC[zi % 4]
            zi += 1
        segs.append(s)
    p.update(nome=nome, pedido="5 variacoes cortes com lettering com os brutos novos (03/11/2026)", angulo=v["angulo"],
             raw=os.path.join(D, v["raw"] + ".mp4"), transcript=os.path.join(TX, v["raw"] + ".json"),
             face=[540, 600], segments=segs, fix={"DOIS": "2", "CINCO": "5"},
             red=["DOR", "DÓI", "DORES", "FERIDAS", "BOLHAS", "TRATAMENTO", "CARO", "2", "5", "REAIS", "VIDA", "RARA"],
             chamada={"imagem": lt(v["lettering"][0]), "texto_do_lettering": v["lettering"][1]},
             fatos={"falas": f"Pedrinho, {v['raw']}.mp4 (gravado em 02/11/2026)",
                    "valor": "o lettering de R$10 vai so no video sem a fala do valor" if "10" in v["lettering"][1]
                    else "R$5: ele fala 'dois ou cinco reais'"})
    p["endcard"] = dict(p["endcard"], src=v["fim"][0], start=v["fim"][1])
    pasta = os.path.join(PL, nome)
    os.makedirs(pasta, exist_ok=True)
    f = os.path.join(pasta, "plano.json")
    if os.path.exists(f):
        old = json.load(open(f, encoding="utf-8"))
        if old.get("out"):
            p["out"] = old["out"]
    json.dump(p, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(nome, round(sum(s["out"] - s["in"] for s in segs), 1), "s de fala")
