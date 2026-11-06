"""Gera os 5 planos do pedido 2026-10-26_105743 (estilo narrado), cada um com angulo, copy e cenas proprios."""
import glob, json, os, shutil

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
P = os.path.join(RAIZ, "EDITADOS", "_planos")
BR = os.path.join(RAIZ, "VÍDEOS PARA EDITAR")
BANK = os.path.join(RAIZ, "banco de vídeos do pedrinho")
TX = os.path.join(P, "_tx_brutos")
MUS = os.path.join(RAIZ, "MÚSICAS")
CUR = "Vídeo Mostrando itens de curativos em cima da Cama  e  Finalizando os Curativos_.mp4"
FX_DE = os.path.join(P, "Pedrinho_narrado_verdade_v1", "audio")


def bruto(chave):
    return next(p for p in glob.glob(os.path.join(BR, "*.mp4")) if chave in os.path.basename(p)).replace("\\", "/")


def tx(n):
    return os.path.join(TX, n + ".json").replace("\\", "/")


def real(chave, t, cuts, crops, txt, tag="PEDRINHO"):
    return {"type": "real", "tag": tag, "src": bruto(chave), "tx": tx(t), "cuts": cuts, "crops": crops, "txt": txt}


def narr(k, look, broll, **kw):
    return {"type": "narr", "audio": f"audio/{k}.mp3", "look": look, "broll": broll, **kw}


C_819 = [{"z": 1.0}, {"z": 1.35, "center": [520, 620]}, {"z": 1.6, "center": [520, 500]}]
C_1530 = [{"z": 1.3, "center": [490, 640]}, {"z": 1.0}, {"z": 1.55, "center": [490, 560]}]
C_5338 = [{"z": 1.25, "center": [690, 700]}, {"z": 1.0}, {"z": 1.5, "center": [690, 560]}]
C_R9 = [{"z": 1.0}, {"z": 1.35, "center": [580, 700]}, {"z": 1.6, "center": [580, 560]}]
C_R8 = [{"z": 1.25, "center": [550, 860]}, {"z": 1.0}, {"z": 1.4, "center": [550, 880]}]
C_MAE1 = [{"z": 1.0}, {"z": 1.3, "center": [550, 650]}]
C_MAE2 = [{"z": 1.35, "center": [550, 1100]}, {"z": 1.5, "center": [550, 1080]}]
C_PED = [{"z": 1.6, "center": [760, 1000]}, {"z": 1.4, "center": [740, 1000]}]
FX = {"boom": {"text": "deep cinematic boom impact hit, dark trailer, short tail", "dur": 2.0},
      "whoosh": {"text": "fast soft cinematic whoosh transition", "dur": 0.8}}
RED = ["CURATIVO", "CURATIVOS", "FERIDAS", "FERIDA", "ACABANDO", "ACABOU", "DOR", "CHORAR", "ARDE"]

V = {}

# ---------------------------------------------------------------- 1. os curativos acabaram
V["Pedrinho_narrado_acabou_v1"] = {
    "music": "echoes_of_lumen-sad-piano-591198.mp3", "music_start": 8.0,
    "hook": {"t1": 4.4, "y": 1258, "label": "URGENTE",
             "lines": [{"text": "*ACABARAM*", "fs": 150}, {"text": "OS CURATIVOS DO PEDRINHO", "fs": 66}]},
    "narracao": {
        "N1": "Foi assim que o Pedrinho recebeu a notícia. O material dos curativos chegou ao fim.",
        "N2": "Ele tem a doença da pele de borboleta. Sem atadura, cada ferida fica descoberta.",
        "N3": "E o material não dura. A gaze de hoje já não serve amanhã.",
        "N4": "Acabou o curativo. A coragem dele, não.",
        "N5": "Toque em Saiba mais e ajude a repor o material do Pedrinho hoje."},
    "blocks": [
        real("20260917_000819", "t_000819", [[1.44, 1.80], [3.54, 4.44], [6.00, 6.58]], C_819,
             "É o quê, mãe? Os curativo tão acabando? Meu Deus, e agora?"),
        narr("N1", "pb", [{"src": CUR, "start": 20.0}, {"src": "20260127_110703.jpg"}]),
        real("20260917_000819", "t_000819", [[31.48, 31.62], [32.76, 32.76], [40.38, 41.84], [43.86, 45.82]],
             [{"z": 1.35, "center": [520, 620]}, {"z": 1.0}, {"z": 1.6, "center": [520, 500]}],
             "Na verdade, acabou. A gente não tem como comprar nem uns dois, três pacotes de atadura."),
        narr("N2", "pb", [{"src": "20240411_123226.jpg"}, {"src": CUR, "start": 232.0}]),
        real("20260917_001530", "t_001530", [[4.60, 9.30], [15.22, 16.48]], C_1530,
             "A minha mamãe, ela precisa fazer os meus curativos todos os dias. Duas vezes ao dia."),
        {"type": "card", "lines": ["2 VEZES", "POR DIA"], "dur": 1.3},
        narr("N3", "pb", [{"src": "20260825_134710.jpg"}, {"src": "20260825_134438.jpg"},
                          {"src": "20260825_134808.jpg"}, {"src": CUR, "start": 290.0}]),
        real("20260917_001530", "t_001530", [[28.22, 29.60], [31.06, 33.18]], C_1530,
             "A gente usa curativo e logo depois acaba rapidamente."),
        narr("N4", "cor", [{"src": "20221127_220927.jpg"}, {"src": "20241110_104724.mp4", "start": 4.0}]),
        real("20260917_000819", "t_000819", [[56.10, 59.10], [60.72, 61.96]], C_819,
             "Seja com dois ou cinco reais, não importa o valor, já vai tá ajudando muito."),
        narr("N5", "cor", [{"src": "20260410_210553.mp4", "start": 30.0}]),
        {"type": "end", "dur": 3.6, "broll": {"src": "20260729_164523.jpg", "look": "cor"},
         "lines": ["REPONHA O *CURATIVO*", "DO PEDRINHO"], "button": "SAIBA MAIS"}]}

# ---------------------------------------------------------------- 2. noite em claro
V["Pedrinho_narrado_noite_v1"] = {
    "music": "alex-morgan-sad-piano-emotional-rain-story-575883.mp3", "music_start": 2.0,
    "hook": {"t1": 4.4, "y": 1258, "label": "URGENTE",
             "lines": [{"text": "*NOITE EM CLARO*", "fs": 112}, {"text": "“EU VI O DIA AMANHECER”", "fs": 68}]},
    "narracao": {
        "N1": "Pedrinho tem epidermólise bolhosa. As feridas não dão trégua nem de madrugada.",
        "N2": "De dia, a mãe troca os curativos duas vezes. E mesmo assim a dor volta.",
        "N3": "Doze reais de cada uma garantem os itens do curativo dessa semana.",
        "N4": "Ele não pede um milagre. Pede uma noite sem dor.",
        "N5": "Toque em Saiba mais e seja uma das seis pessoas que o Pedrinho pediu."},
    "caption_fix": {"DOZE": "12", "SEIS": "6"},
    "blocks": [
        real("20260916_235338", "t_235338", [[33.24, 36.00], [37.40, 38.50]], C_5338,
             "A noite passada eu passei ela em claro. Eu vi o dia amanhecer."),
        narr("N1", "pb", [{"src": "20260113_023031.jpg"}, {"src": "20240402_095757.jpg"}]),
        real("roteiro 9", "t_roteiro9", [[52.64, 52.98], [54.56, 58.42]], C_R9,
             "Tem noites, que eu chego até a chorar por causa das feridas doloridas."),
        narr("N2", "pb", [{"src": CUR, "start": 180.0}, {"src": CUR, "start": 260.0}]),
        real("20260917_001530", "t_001530", [[58.10, 61.70]], C_1530,
             "Já não basta as dores do dia a dia e durante a noite."),
        real("20260916_235338", "t_235338", [[1.58, 2.82], [4.20, 4.42], [5.88, 6.14], [7.14, 7.42], [8.46, 8.80]],
             C_5338, "Eu só tenho cinco dias pra conseguir pelo menos seis pessoas pra me ajudar."),
        {"type": "card", "lines": ["6 PESSOAS", "EM 5 DIAS"], "dur": 1.4, "fs": 190},
        narr("N3", "pb", [{"src": "20260825_134438.jpg"}, {"src": "20260825_134710.jpg"},
                          {"src": "20260825_134340.jpg"}, {"src": "20260825_134039.jpg"}]),
        narr("N4", "cor", [{"src": "20260410_210553.mp4", "start": 5.0}]),
        real("20260916_235338", "t_235338", [[28.56, 28.76], [30.04, 31.76]], C_5338,
             "Me ajude, a passar essa noite sem dor."),
        narr("N5", "cor", [{"src": "20241107_202353.jpg"}, {"src": "IMG-20241205-WA0070.jpg"}]),
        {"type": "end", "dur": 3.6, "broll": {"src": "20230603_203654.jpg", "look": "cor"},
         "lines": ["SEJA UMA DAS *6*", "PESSOAS DO PEDRINHO"], "button": "SAIBA MAIS"}]}

# ---------------------------------------------------------------- 3. "culpada"
V["Pedrinho_narrado_culpa_v1"] = {
    "music": "echoes_of_lumen-sad-piano-591198.mp3", "music_start": 20.0,
    "hook": {"t1": 4.6, "y": 1258, "label": "URGENTE",
             "lines": [{"text": "*CULPADA?*", "fs": 150}, {"text": "NENHUMA MÃE DEVERIA OUVIR", "fs": 64}]},
    "narracao": {
        "N1": "A epidermólise bolhosa é uma doença genética. Não é culpa de ninguém.",
        "N2": "São duas trocas de curativo por dia. Quem faz cada uma delas é a mãe.",
        "N3": "Ela não tem culpa. Tem coragem.",
        "N4": "Toque em Saiba mais e mostre a ela que não está sozinha."},
    "caption_fix": {"QUINHENTOS": "500"},
    "blocks": [
        real("Nenhuma mãe", "t_nenhuma_mae", [[1.74, 3.78], [4.08, 6.98]], C_MAE1,
             "Nenhuma mãe deveria ouvir isso: “Você é culpada pelo que o seu filho passa”.", "MÃE DO PEDRINHO"),
        narr("N1", "pb", [{"src": "20240402_095732.jpg"}, {"src": CUR, "start": 200.0}]),
        real("Nenhuma mãe", "t_nenhuma_mae", [[9.84, 11.52], [12.72, 15.46]], C_MAE1,
             "Eu faço tudo o que tá no meu alcance, mas a EB, essa enfermidade, ela é terrível.", "MÃE DO PEDRINHO"),
        narr("N2", "pb", [{"src": CUR, "start": 245.0}, {"src": CUR, "start": 310.0}]),
        real("absurdo de caro", "t_absurdo_caro", [[17.72, 21.08]], C_MAE2,
             "Os curativo para os cuidado do Pedrinho são absurdo de caro.", "MÃE DO PEDRINHO"),
        real("absurdo de caro", "t_absurdo_caro", [[35.86, 38.34]], [{"z": 1.5, "center": [550, 1080]}],
             "O que eu faço com mil e quinhentos? Não consigo fazer nada.", "MÃE DO PEDRINHO"),
        {"type": "card", "lines": ["R$ 1.500", "NÃO DÃO CONTA"], "dur": 1.4, "fs": 200},
        real("Nenhuma mãe", "t_nenhuma_mae", [[33.92, 34.86], [36.24, 37.82]], C_MAE1,
             "E pela minha condição, eu não consigo nem o básico pra ele.", "MÃE DO PEDRINHO"),
        narr("N3", "cor", [{"src": "20250401_204159.jpg"}]),
        real("Nenhuma mãe", "t_nenhuma_mae", [[44.90, 48.62]], [{"z": 1.3, "center": [550, 650]}],
             "Você não tem obrigação, mas ajude a salvar o meu filho.", "MÃE DO PEDRINHO"),
        narr("N4", "cor", [{"src": "VID-20260702-WA0016.mp4", "start": 150.0}]),
        {"type": "end", "dur": 3.6, "broll": {"src": "Ana e Pedro sorrindo.png", "look": "cor"},
         "lines": ["ESSA MÃE NÃO", "ESTÁ *SOZINHA*"], "button": "SAIBA MAIS"}]}

# ---------------------------------------------------------------- 4. esquecido
V["Pedrinho_narrado_esquecido_v1"] = {
    "music": "alex-morgan-sad-piano-emotional-rain-story-575883.mp3", "music_start": 25.0,
    "hook": {"t1": 4.4, "y": 1258, "label": "URGENTE",
             "lines": [{"text": "*ESQUECIDO*", "fs": 150}, {"text": "“AS PESSOAS SUMIRAM”", "fs": 74}]},
    "narracao": {
        "N1": "Quase quatro anos atrás, uma vaquinha comprou quase um ano de curativos.",
        "N2": "Aquele estoque acabou faz tempo. E a pele do Pedrinho precisa de cuidado todo dia.",
        "N3": "Ele não precisa de pena. Precisa de gaze.",
        "N4": "Toque em Saiba mais e não deixe o Pedrinho ser esquecido."},
    "blocks": [
        real("roteiro 8", "t_roteiro8", [[22.88, 23.14], [24.64, 26.00]], C_R8,
             "As pessoas se esqueceram de mim."),
        real("roteiro 8", "t_roteiro8", [[27.58, 29.30], [32.32, 33.16]], [{"z": 1.0}, {"z": 1.4, "center": [550, 880]}],
             "Até mesmo pessoas que me ajudaram, elas também sumiram."),
        narr("N1", "pb", [{"src": "20240514_210632.jpg"}, {"src": "20240411_115750.jpg"}]),
        real("roteiro 7", "t_roteiro7b", [[14.90, 16.36], [17.28, 18.20]], C_R8,
             "Acham já que eu tô bem de ajuda. Só que não é bem assim."),
        narr("N2", "pb", [{"src": CUR, "start": 60.0}, {"src": "20240426_144311.jpg"}]),
        real("20260917_001530", "t_001530", [[65.28, 69.86]], C_1530,
             "Os custos são muito alto, de cada atadura, de cada gazes."),
        {"type": "card", "lines": ["1 ANO", "DE CURATIVOS. ACABOU."], "dur": 1.4, "fs": 210},
        narr("N3", "cor", [{"src": "20260825_134710.jpg"}, {"src": "20241109_123330.jpg"}]),
        real("roteiro 8", "t_roteiro8", [[104.46, 104.84], [106.06, 106.58], [108.90, 109.92], [110.98, 110.98],
                                          [112.56, 112.56]], C_R8, "E se você, puder me ajudar, com dois ou três reais."),
        narr("N4", "cor", [{"src": "20241110_104724.mp4", "start": 12.0}]),
        {"type": "end", "dur": 3.6, "broll": {"src": "20241107_202353.jpg", "look": "cor"},
         "lines": ["NÃO ESQUEÇA", "DO *PEDRINHO*"], "button": "SAIBA MAIS"}]}

# ---------------------------------------------------------------- 5. nao pode esperar
V["Pedrinho_narrado_espera_v1"] = {
    "music": "echoes_of_lumen-sad-piano-591198.mp3", "music_start": 35.0,
    "hook": {"t1": 4.4, "y": 1258, "label": "URGENTE",
             "lines": [{"text": "*NÃO PODE ESPERAR*", "fs": 100}, {"text": "AS FERIDAS DO PEDRINHO", "fs": 72}]},
    "narracao": {
        "N1": "A família do Pedrinho entrou na Justiça. Mas o processo demora.",
        "N2": "Sem soro fisiológico, o banho dele tem que ser com água.",
        "N3": "A Justiça pode demorar. A ferida não espera.",
        "N4": "Toque em Saiba mais. A SOS Human Help leva a sua ajuda até o Pedrinho."},
    "caption_fix": {"B": "EB"},
    "blocks": [
        real("roteiro 9", "t_roteiro9", [[44.18, 45.46], [46.98, 48.42], [49.06, 51.38]], C_R9,
             "Quem é EB não pode esperar. E eu não posso esperar mais. Os meus ferimentos não podem esperar."),
        narr("N1", "pb", [{"src": "20240426_144311.jpg"}, {"src": CUR, "start": 215.0}]),
        real("roteiro 9", "t_roteiro9", [[32.18, 33.10], [34.24, 35.96]], C_R9,
             "Mas essas coisas, demora e demora muito mesmo."),
        narr("N2", "pb", [{"src": "20260825_134340.jpg"}, {"src": "IMG-20260624-WA0043.jpg"}]),
        real("peço perdão", "t_peco_perdao", [[40.08, 41.70], [42.36, 45.04]], C_PED,
             "E a água, se ela bater na pele, ela arde e arde muito que vocês não têm noção."),
        narr("N3", "cor", [{"src": "20241107_202353.jpg"}, {"src": "20260410_210553.mp4", "start": 20.0}]),
        real("peço perdão", "t_peco_perdao", [[63.00, 66.92], [67.72, 67.72], [69.44, 69.72], [71.56, 74.14]], C_PED,
             "Quatro, cinco reais, dez reais, parece pouco, mas pra mim, é uma nova esperança de um dia sem dor."),
        {"type": "card", "lines": ["R$ 4", "UM DIA SEM DOR"], "dur": 1.4, "fs": 230},
        narr("N4", "cor", [{"src": "IMG-20241205-WA0070.jpg"}, {"src": "20241108_111235(0).jpg"}]),
        {"type": "end", "dur": 3.6, "broll": {"src": "20250401_204159.jpg", "look": "cor"},
         "lines": ["O PEDRINHO NÃO", "PODE *ESPERAR*"], "button": "SAIBA MAIS"}]}

for nome, v in V.items():
    d = os.path.join(P, nome)
    os.makedirs(os.path.join(d, "audio"), exist_ok=True)
    for fx in ("fx_boom.mp3", "fx_whoosh.mp3"):
        if os.path.exists(os.path.join(FX_DE, fx)):
            shutil.copy2(os.path.join(FX_DE, fx), os.path.join(d, "audio", fx))
    json.dump({"voice_id": "nPczCjzI2devNBz1zQrb", "narracao": v["narracao"], "efeitos": FX},
              open(os.path.join(d, "roteiro_audio.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for b in v["blocks"]:
        if b["type"] == "narr":
            b["txt"] = v["narracao"][b["audio"][6:-4]]
    plano = {"nome": nome, "pedido": "2026-10-26_105743", "bank": BANK.replace("\\", "/"),
             "music": os.path.join(MUS, v["music"]).replace("\\", "/"), "music_start": v["music_start"],
             "red": RED, "caption_fix": v.get("caption_fix", {}), "hook": v["hook"], "blocks": v["blocks"]}
    json.dump(plano, open(os.path.join(d, "plano.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok", nome)
