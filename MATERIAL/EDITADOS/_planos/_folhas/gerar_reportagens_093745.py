"""Gera os 5 planos do pedido 2026-10-26_093745 (Reportagem, 5 criativos diferentes)."""
import json
import os

R = "C:/Users/EDITING_SECTOR/Desktop/EDIÇÃO COM CLAUDE/"
BANK, RAW, PL = R + "banco de vídeos do pedrinho/", R + "VÍDEOS PARA EDITAR/", R + "EDITADOS/_planos/"
MUS = R + "MÚSICAS/"
TX = PL + "Pedrinho_narrado_calor_v1/tx/"
TXC = PL + "_tx_corrigidas/"
ACAB = RAW + "Roteiro_ os meus curativos estão acabando e eu tô com medo seja um anjo na minha vida.mp4"
CALOR = RAW + "Roteiro_ esse calor tá acabando com a pele do meu filho.mp4"
DORMIR = RAW + "Roteiro_ Eu não aguento mais não conseguir dormir.mp4"
CINCO = RAW + "20260916_234157.mp4"
BED = BANK + "Vídeo Mostrando itens de curativos em cima da Cama  e  Finalizando os Curativos_.mp4"
EVENTO = BANK + "20241110_104724.mp4"
CAMA_MAE = BANK + "20260824_182501.mp4"

# transcricao do "dormir" com a palavra corrigida (o Scribe ouviu "pelomenetes" no lugar de "ferimentos")
os.makedirs(TXC, exist_ok=True)
d = json.load(open(TX + "v2_dormir.json", encoding="utf-8"))
for w in d["words"]:
    if w["text"] == "pelomenetes":
        w["text"] = "ferimentos"
json.dump(d, open(TXC + "v2_dormir.json", "w", encoding="utf-8"), ensure_ascii=False)

S = {  # fontes das sonoras: (video, transcricao)
    "v1": (CINCO, TX + "v1_cinco_horas.json"),
    "v2": (DORMIR, TXC + "v2_dormir.json"),
    "v3": (CALOR, TX + "v3_mae_calor.json"),
    "v4": (ACAB, TX + "v4_curativos_acabando.json"),
}
GC_P = ["PEDRINHO GUERREIRO", "tem epidermólise bolhosa"]
GC_M = ["MÃE DO PEDRINHO", "cuida dos curativos todos os dias"]
FIM = "👇 Toque em SAIBA MAIS"
FATOS = {
    "epidermolise bolhosa / pele de borboleta": "Pedrinho em banco/Roteiro 7.mp4",
    "nao consegue dormir, feridas abertas e doloridas": "Pedrinho em Roteiro_ Eu nao aguento mais nao conseguir dormir.mp4",
    "curativo 2x por dia": "mae em Roteiro_ esse calor... (segundo curativo do dia) + foto 'Curativos 2 x ao Dia'",
    "ultimo curativo levou 5 horas; bolhas de sangue e de agua; feridas cada vez mais abertas": "Pedrinho em 20260916_234157.mp4",
    "cuidados passam de 40 mil por mes": "Pedrinho em banco/Roteiro 7; mae em Roteiro 2 e 4",
    "mae faz todos os curativos": "banco/Roteiro 4",
    "curativos acabando; precisa de atadura e pomada; 2 ou 5 reais ajudam": "Pedrinho (Roteiro_ os meus curativos...) e mae (Roteiro_ esse calor...)",
    "calor acabando com a pele": "mae em Roteiro_ esse calor...",
}
ZM = lambda ini: [  # noqa: E731  rosto da mae e Pedrinho ao fundo na selfie do calor
    {"arquivo": os.path.basename(CALOR), "inicio": ini, "caixa": [0, 80, 640, 1020], "quem": "rosto da mae (quem fala)"},
    {"arquivo": os.path.basename(CALOR), "inicio": ini, "caixa": [660, 960, 1080, 1400], "quem": "Pedrinho pequeno ao fundo"}]


def son(nome, src, cortes, gc=None, **kw):
    b = {"nome": nome, "tipo": "sonora", "fonte": S[src][0], "tx": S[src][1], "cortes": cortes}
    if gc:
        b["gc"] = gc
    b.update(kw)
    return b


def off(nome, fala, cenas=None, foto=None, **kw):
    b = {"nome": nome, "tipo": "off", "fala": fala}
    if cenas:
        b["cenas"] = cenas
    if foto:
        b["foto"] = BANK + foto
    b.update(kw)
    return b


def plano(n, musica, manchete, etiqueta, narr, blocos, zonas):
    return {"nome": f"Pedrinho_reportagem_v{n}", "pedido": "2026-10-26_093745",
            "saida": R + f"EDITADOS/Pedrinho_reportagem_v{n}.mp4",
            "voz": {"voice_id": "nPczCjzI2devNBz1zQrb", "model_id": "eleven_multilingual_v2",
                    "obs": "reporter provisorio (Brian); falta narrador brasileiro (audio_br)"},
            "musica": MUS + musica, "musica_volume": 0.07, "marca": "SOS HUMAN HELP",
            "manchete": manchete, "etiqueta": etiqueta, "etiqueta_final": FIM,
            "narracao": narr, "fatos": FATOS, "blocos": blocos, "zonas_protegidas": zonas}


P = []
# v2 — a noite sem dormir
P.append(plano(2, "echoes_of_lumen-sad-piano-591198.mp3",
    ["MENINO COM “PELE DE BORBOLETA”", "NÃO CONSEGUE DORMIR DE DOR"], "R$ 10 ajuda nos curativos ❤️",
    {"OFF1": "Para o Pedrinho, a noite é a pior hora do dia. A dor não deixa ele dormir.",
     "OFF2": "Ele tem epidermólise bolhosa, a pele de borboleta. Qualquer atrito pode virar ferida.",
     "OFF3": "O curativo é trocado duas vezes por dia. Da última vez, a troca levou cinco horas.",
     "OFF4": "A Sos Human Help está arrecadando doações para atadura, gaze e pomada. Com dez reais, você já ajuda.",
     "OFF5": "Toque em Saiba mais e ajude o Pedrinho a ter uma noite de sono."},
    [off("b01", "OFF1", foto="20260113_023031.jpg", pb=True),
     son("b02", "v2", [[3.22, 4.76], [5.60, 10.64]], GC_P),
     off("b03", "OFF2", cenas=[[BED, 165.0, "pb"], [BED, 232.0]]),
     son("b04", "v1", [[35.02, 36.22], [37.18, 39.20]]),
     off("b05", "OFF3", cenas=[[CINCO, 30.0, "pb"], [BED, 290.0]]),
     son("b06", "v3", [[3.90, 6.22], [8.12, 8.84]], GC_M),
     off("b07", "OFF4", foto="Remédios, Pomadas e Cremes.png", etiqueta=True),
     son("b08", "v2", [[13.72, 13.72], [14.86, 15.86]], etiqueta=True),
     off("b09", "OFF5", foto="20221127_220927.jpg", final=True)],
    ZM(3.90)))
# v3 — os curativos estao acabando
P.append(plano(3, "monument_music-wander-143535 (2).mp3",
    ["CURATIVOS DE MENINO COM", "DOENÇA RARA ESTÃO NO FIM"], "Doe R$ 10 para os curativos ❤️",
    {"OFF1": "O Pedrinho só tem os curativos que cabem nas mãos dele.",
     "OFF2": "Ele tem epidermólise bolhosa. A pele dele precisa de curativo todos os dias.",
     "OFF3": "Gaze, atadura, pomada e soro. Os cuidados com a pele dele passam de quarenta mil reais por mês.",
     "OFF4": "A Sos Human Help está arrecadando doações para repor os curativos do Pedrinho. Dez reais já fazem diferença.",
     "OFF5": "Toque em Saiba mais e ajude a repor os curativos do Pedrinho."},
    [off("b01", "OFF1", cenas=[[CINCO, 5.0, "pb"], [BED, 145.0, "pb"]]),
     son("b02", "v4", [[4.32, 6.06], [7.24, 7.82]], GC_P),
     off("b03", "OFF2", cenas=[[BED, 175.0, "pb"], [BED, 25.0]]),
     son("b04", "v3", [[10.50, 11.20], [11.88, 12.18], [15.62, 16.06], [17.42, 17.66], [18.90, 20.06]], GC_M),
     off("b05", "OFF3", foto="Curativos 2 x ao Dia.png"),
     son("b06", "v4", [[8.36, 9.40], [10.54, 11.46], [13.20, 13.48], [14.44, 14.98], [16.18, 16.40]]),
     off("b07", "OFF4", cenas=[[BED, 15.0]], etiqueta=True),
     son("b08", "v4", [[21.24, 24.04]], etiqueta=True),
     off("b09", "OFF5", foto="20260729_164523.jpg", final=True)],
    ZM(10.50)))
# v4 — cinco horas de curativo
P.append(plano(4, "alex-morgan-sad-piano-emotional-rain-story-575883.mp3",
    ["CURATIVO DE MENINO COM DOENÇA", "RARA CHEGOU A DURAR 5 HORAS"], "Doe R$ 10 pro curativo dele ❤️",
    {"OFF1": "Cinco horas. Foi quanto durou o último curativo do Pedrinho.",
     "OFF2": "Ele tem epidermólise bolhosa. A pele se solta com qualquer atrito, e todo dia aparecem bolhas novas.",
     "OFF3": "É a mãe quem faz cada curativo, duas vezes por dia.",
     "OFF4": "A Sos Human Help está arrecadando doações para os curativos. Com dez reais, você ajuda essa família.",
     "OFF5": "Toque em Saiba mais e seja o anjo do Pedrinho."},
    [off("b01", "OFF1", foto="20240426_144311.jpg", pb=True),
     son("b02", "v1", [[10.60, 11.70], [13.48, 15.90], [19.68, 21.16], [21.80, 22.54], [23.56, 24.64],
                       [25.90, 26.82]], GC_P),
     off("b03", "OFF2", cenas=[[BED, 185.0, "pb"], [BED, 205.0, "pb"]]),
     son("b04", "v1", [[39.96, 44.20]]),
     off("b05", "OFF3", cenas=[[BED, 232.0], [CAMA_MAE, 27.0]]),
     son("b06", "v3", [[0.80, 2.74]], GC_M),
     off("b07", "OFF4", foto="GAZE.png", etiqueta=True),
     son("b08", "v4", [[17.64, 17.64], [18.88, 20.26]], etiqueta=True),
     off("b09", "OFF5", foto="20241107_202353.jpg", final=True)],
    ZM(0.80)))
# v5 — o calor piorando as feridas (valor de R$ 5, como a mae fala)
P.append(plano(5, "good_b_music-melody-of-nature-main-6672.mp3",
    ["CALOR PIORA AS FERIDAS DE MENINO", "COM “PELE DE BORBOLETA”"], "R$ 5 já ajuda ❤️",
    {"OFF1": "O calor está piorando as feridas do Pedrinho.",
     "OFF2": "Ele tem epidermólise bolhosa, a doença da pele de borboleta. E as feridas estão cada vez mais abertas.",
     "OFF3": "À noite, a dor não deixa ele dormir.",
     "OFF4": "A Sos Human Help está arrecadando doações para os curativos do Pedrinho. Cinco reais já ajudam.",
     "OFF5": "Toque em Saiba mais e entre nessa corrente."},
    [off("b01", "OFF1", foto="20260628_131414.jpg", pb=True),
     son("b02", "v3", [[0.80, 2.74], [8.12, 8.84]], GC_M),
     off("b03", "OFF2", cenas=[[BED, 165.0, "pb"], [CINCO, 30.0, "pb"]]),
     son("b04", "v1", [[30.40, 31.08], [31.54, 33.24], [34.00, 34.00], [35.02, 36.22], [37.18, 39.20]], GC_P),
     off("b05", "OFF3", cenas=[[DORMIR, 18.0, "pb"]]),
     son("b06", "v2", [[3.22, 4.76], [11.50, 12.88]]),
     son("b07", "v3", [[26.54, 29.72]]),
     off("b08", "OFF4", foto="Pomada.png", etiqueta=True),
     son("b09", "v1", [[48.30, 48.62], [49.64, 49.94], [50.64, 52.50]], etiqueta=True),
     off("b10", "OFF5", foto="20230603_203654.jpg", final=True)],
    ZM(0.80) + ZM(26.54)))
# v6 — "um pouco com Deus e muito"
P.append(plano(6, "rockymetal-ambient-acoustic-239252.mp3",
    ["“UM POUCO COM DEUS É MUITO”,", "DIZ MENINO COM DOENÇA RARA"], "R$ 10 ajuda o Pedrinho ❤️",
    {"OFF1": "Ele tem a pele frágil como a asa de uma borboleta. E uma fé que não se quebra.",
     "OFF2": "O Pedrinho tem epidermólise bolhosa. O curativo é feito duas vezes por dia e já chegou a durar cinco horas.",
     "OFF3": "Os cuidados com a pele dele passam de quarenta mil reais por mês.",
     "OFF4": "A Sos Human Help está arrecadando doações para os curativos. Dez reais já ajudam o Pedrinho a seguir lutando.",
     "OFF5": "Toque em Saiba mais e faça parte dessa corrente de fé."},
    [off("b01", "OFF1", foto="20240402_095732.jpg", pb=True),
     son("b02", "v1", [[0.94, 2.64]], GC_P),
     off("b03", "OFF2", cenas=[[BED, 175.0, "pb"], [BED, 290.0]]),
     son("b04", "v1", [[3.82, 3.82], [4.82, 6.86], [7.98, 9.52]]),
     off("b05", "OFF3", foto="Curativos 2 x ao Dia.png"),
     son("b06", "v3", [[10.50, 11.20], [11.88, 12.18]], GC_M),
     off("b07", "OFF4", cenas=[[EVENTO, 12.0]], etiqueta=True),
     son("b08", "v4", [[17.64, 17.64], [18.88, 20.26], [21.24, 24.04]], etiqueta=True),
     off("b09", "OFF5", foto="20250401_204159.jpg", final=True)],
    ZM(10.50)))

for p in P:
    os.makedirs(PL + p["nome"], exist_ok=True)
    json.dump(p, open(PL + p["nome"] + "/plano.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("plano", p["nome"], len(p["blocos"]), "blocos")
