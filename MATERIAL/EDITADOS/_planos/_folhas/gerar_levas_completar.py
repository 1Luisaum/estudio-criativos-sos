"""Planos para completar as LEVAs (26/10/2026): 2 narrados, 4 reportagens, 3 listas, 4 VSLs e 3 cortes.
Cada video tem angulo, gancho, copy e cenas proprios. So fatos ditos nos brutos (transcricoes em _tx_brutos)."""
import glob, json, os, shutil

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
P = os.path.join(RAIZ, "EDITADOS", "_planos")
BR = os.path.join(RAIZ, "VÍDEOS PARA EDITAR")
BANK = os.path.join(RAIZ, "banco de vídeos do pedrinho").replace("\\", "/")
TXD = os.path.join(P, "_tx_brutos")
MUS = os.path.join(RAIZ, "MÚSICAS").replace("\\", "/")
KAIQUE, LEONARDO = "Hmn4B9B77pf6ttydteJ8", "4XmhZ74tBbUVCXIYNMMo"
FIM = "👇 Toque em SAIBA MAIS"


def bruto(chave):
    return next(p for p in glob.glob(os.path.join(BR, "*.mp4")) if chave in os.path.basename(p)).replace("\\", "/")


def b(nome):  # arquivo do banco
    return BANK + "/" + nome


def tx(n):
    return os.path.join(TXD, n + ".json").replace("\\", "/")


FONTE = {"819": ("20260917_000819", "t_000819"), "1530": ("20260917_001530", "t_001530"),
         "5338": ("20260916_235338", "t_235338"), "r9": ("roteiro 9", "t_roteiro9"), "r8": ("roteiro 8", "t_roteiro8"),
         "r7": ("roteiro 7", "t_roteiro7b"), "mae1": ("Nenhuma mãe", "t_nenhuma_mae"),
         "mae2": ("absurdo de caro", "t_absurdo_caro"), "ped": ("peço perdão", "t_peco_perdao")}
CUR = b("Vídeo Mostrando itens de curativos em cima da Cama  e  Finalizando os Curativos_.mp4")
EVENTO, GUITAR, CAMA_MAE, SOFA_MAE = b("20241110_104724.mp4"), b("20260410_210553.mp4"), b("20260824_182501.mp4"), b("VID-20260702-WA0016.mp4")
PLANOS = {}


def salvar(nome, plano, extra=None):
    d = os.path.join(P, nome)
    os.makedirs(d, exist_ok=True)
    plano = {"nome": nome, **plano}
    json.dump(plano, open(os.path.join(d, "plano.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for arq, conteudo in (extra or {}).items():
        json.dump(conteudo, open(os.path.join(d, arq), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    PLANOS[nome] = d


# ===================================================================== NARRADO (Kaique)
FX = {"boom": {"text": "deep cinematic boom impact hit, dark trailer, short tail", "dur": 2.0},
      "whoosh": {"text": "fast soft cinematic whoosh transition", "dur": 0.8}}
RED = ["CURATIVO", "CURATIVOS", "FERIDAS", "FERIDA", "ACABANDO", "ACABOU", "DOR", "DORES", "MEDO", "ARDE"]
C_R7 = [{"z": 1.0}, {"z": 1.3, "center": [580, 860]}]
C_R8 = [{"z": 1.25, "center": [550, 860]}, {"z": 1.0}, {"z": 1.4, "center": [550, 880]}]
C_819 = [{"z": 1.0}, {"z": 1.35, "center": [520, 620]}, {"z": 1.6, "center": [520, 500]}]
C_1530 = [{"z": 1.3, "center": [490, 640]}, {"z": 1.0}, {"z": 1.55, "center": [490, 560]}]
C_PED = [{"z": 1.6, "center": [760, 1000]}, {"z": 1.4, "center": [740, 1000]}]


def real(f, cuts, crops, txt, tag="PEDRINHO"):
    return {"type": "real", "tag": tag, "src": bruto(FONTE[f][0]), "tx": tx(FONTE[f][1]), "cuts": cuts, "crops": crops, "txt": txt}


def narr(k, look, broll):
    return {"type": "narr", "audio": f"audio/{k}.mp3", "look": look, "broll": broll}


def narrado(nome, musica, ms, hook, narracao, blocks, fix=None):
    for bl in blocks:
        if bl["type"] == "narr":
            bl["txt"] = narracao[bl["audio"][6:-4]]
    salvar(nome, {"pedido": "completar LEVA 02 (26/10/2026)", "bank": BANK, "music": f"{MUS}/{musica}",
                  "music_start": ms, "red": RED, "caption_fix": fix or {}, "hook": hook, "blocks": blocks},
           {"roteiro_audio.json": {"voice_id": KAIQUE, "narracao": narracao, "efeitos": FX}})
    a = os.path.join(P, nome, "audio")
    os.makedirs(a, exist_ok=True)
    for fx in ("fx_boom.mp3", "fx_whoosh.mp3"):
        shutil.copy2(os.path.join(P, "Pedrinho_narrado_acabou_v1", "audio", fx), os.path.join(a, fx))


narrado("Pedrinho_narrado_oracao_v1", "alex-morgan-sad-piano-emotional-rain-story-575883.mp3", 40.0,
        {"t1": 4.6, "y": 1258, "label": "URGENTE",
         "lines": [{"text": "*“DEUS TE ABENÇOE”*", "fs": 92}, {"text": "E AS FAIXAS ACABANDO", "fs": 74}]},
        {"N1": "Pedrinho tem epidermólise bolhosa. Cada mensagem de carinho chega até ele. Mas as faixas continuam acabando.",
         "N2": "Duas vezes por dia, a mãe dele desfaz e refaz cada faixa do corpo.",
         "N3": "Oração ele já tem. Falta a faixa.",
         "N4": "Toque em Saiba mais e transforme o seu carinho em curativo."},
        [real("r7", [[38.22, 39.54], [43.06, 43.06], [44.54, 47.20]], C_R7,
              "Muita gente nos meus vídeo comentam: “ah, Deus te abençoe”, “ah, vai dar tudo certo”."),
         narr("N1", "pb", [{"src": "20240411_115750.jpg"}, {"src": CUR, "start": 140.0}]),
         real("r7", [[50.92, 51.10], [52.04, 52.74], [54.80, 56.04], [56.88, 57.38]], C_R7,
              "De verdade, o que Jesus ensinou, é ajudar ao próximo. Ajudar mesmo."),
         narr("N2", "pb", [{"src": CUR, "start": 250.0}, {"src": CUR, "start": 300.0}]),
         real("r8", [[65.54, 67.42], [70.00, 70.54], [71.54, 72.00], [73.02, 73.72]], C_R8,
              "As minhas ataduras, que são as faixas, elas estão acabando e eu estou com muito medo mesmo."),
         narr("N3", "cor", [{"src": "20241109_123330.jpg"}, {"src": "20250401_204159.jpg"}]),
         real("r7", [[119.48, 120.88], [121.90, 122.70], [123.20, 124.48]], C_R7,
              "Por favor, me ajuda, eu não quero ter que ficar sem os meus cuidados que eu preciso."),
         {"type": "card", "lines": ["1 FAIXA", "JÁ AJUDA"], "dur": 1.3, "fs": 220},
         narr("N4", "cor", [{"src": GUITAR, "start": 36.0}]),
         {"type": "end", "dur": 3.6, "broll": {"src": "20260729_180353.jpg", "look": "cor"},
          "lines": ["SEU CARINHO", "VIRA *CURATIVO*"], "button": "SAIBA MAIS"}])

narrado("Pedrinho_narrado_alivio_v1", "echoes_of_lumen-sad-piano-591198.mp3", 50.0,
        {"t1": 4.4, "y": 1258, "label": "URGENTE",
         "lines": [{"text": "*ALÍVIO*", "fs": 150}, {"text": "É O QUE O CURATIVO DÁ A ELE", "fs": 62}]},
        {"N1": "Pedrinho nasceu com epidermólise bolhosa. Para ele, pomada e gaze não são luxo. São remédio.",
         "N2": "Duas trocas por dia. Em poucos dias, o estoque inteiro vai embora.",
         "N3": "Um curativo não cura a doença. Mas muda o dia dele.",
         "N4": "Toque em Saiba mais e dê ao Pedrinho um dia com menos dor."},
        [real("r7", [[131.72, 132.24], [134.54, 136.04]], C_R7, "Com os meus curativos, alivia bastante as minhas dores."),
         narr("N1", "pb", [{"src": "20240402_095757.jpg"}, {"src": "Pomada.png"}]),
         real("819", [[16.56, 16.72], [18.20, 18.42], [19.76, 20.14], [20.86, 22.18]], C_819,
              "Os curativos, que é usado pro meu tratamento e pra aliviar as dores do meu esfolamento."),
         narr("N2", "pb", [{"src": CUR, "start": 175.0}, {"src": CUR, "start": 280.0}]),
         real("ped", [[30.30, 30.80], [32.88, 33.44], [34.96, 38.78]], C_PED,
              "Se não ter um soro fisiológico, a minha mãe vai ter que usar água pra me dar banho."),
         {"type": "card", "lines": ["SEM SORO,", "O BANHO ARDE"], "dur": 1.4, "fs": 170},
         narr("N3", "cor", [{"src": "20260729_180353.jpg"}, {"src": GUITAR, "start": 30.0}]),
         real("1530", [[78.38, 81.90], [82.64, 83.08], [84.48, 85.48], [86.46, 88.90]], C_1530,
              "Seja com um, dois reais, três reais, cinco reais, não importa. O que importa é ajudar nas minhas dores a dar uma aliviada."),
         narr("N4", "cor", [{"src": EVENTO, "start": 14.0}]),
         {"type": "end", "dur": 3.6, "broll": {"src": "20221127_220927.jpg", "look": "cor"},
          "lines": ["UM DIA COM", "*MENOS DOR*"], "button": "SAIBA MAIS"}])

# ===================================================================== REPORTAGEM (Leonardo)
GC_P = ["PEDRINHO GUERREIRO", "tem epidermólise bolhosa"]
GC_M = ["MÃE DO PEDRINHO", "cuida dos curativos todos os dias"]


def son(nome, f, cortes, gc=None, **kw):
    bl = {"nome": nome, "tipo": "sonora", "fonte": bruto(FONTE[f][0]), "tx": tx(FONTE[f][1]), "cortes": cortes}
    if gc:
        bl["gc"] = gc
    bl.update(kw)
    return bl


def off(nome, fala, cenas=None, foto=None, **kw):
    bl = {"nome": nome, "tipo": "off", "fala": fala}
    if cenas:
        bl["cenas"] = cenas
    if foto:
        bl["foto"] = b(foto)
    bl.update(kw)
    return bl


def zona(f, ini, caixa, quem):
    return {"arquivo": os.path.basename(bruto(FONTE[f][0])), "inicio": ini, "caixa": caixa, "quem": quem}


def ZPED(ini):  # selfie da mae com o Pedrinho falando ao lado
    return [zona("ped", ini, [0, 500, 560, 1500], "rosto da mae"), zona("ped", ini, [600, 760, 980, 1180], "Pedrinho (quem fala)")]


def reportagem(n, musica, manchete, etiqueta, narr_, blocos, zonas, fatos):
    salvar(f"Pedrinho_reportagem_v{n}", {
        "pedido": "completar LEVA 02 (26/10/2026)",
        "voz": {"voice_id": LEONARDO, "model_id": "eleven_multilingual_v2", "obs": "Leonardo (brasileiro), conta paga"},
        "musica": f"{MUS}/{musica}", "musica_volume": 0.07, "marca": "SOS HUMAN HELP", "manchete": manchete,
        "etiqueta": etiqueta, "etiqueta_final": FIM, "narracao": narr_, "fatos": fatos, "blocos": blocos,
        "zonas_protegidas": zonas})


reportagem(7, "paulyudin-sad-sad-music-485935 (2).mp3", ["“AS PESSOAS SE ESQUECERAM", "DE MIM”, DIZ MENINO COM EB"],
           "R$ 10 lembra o Pedrinho ❤️",
           {"OFF1": "Há quase quatro anos, uma vaquinha garantiu quase um ano de curativos para o Pedrinho.",
            "OFF2": "Ele tem epidermólise bolhosa, a doença da pele de borboleta. O curativo é trocado duas vezes por dia.",
            "OFF3": "Cada atadura e cada gaze pesam no orçamento da família.",
            "OFF4": "A SOS Human Help está arrecadando doações para o Pedrinho. Dez reais já ajudam.",
            "OFF5": "Toque em Saiba mais e mostre ao Pedrinho que ele não foi esquecido."},
           [off("b01", "OFF1", foto="20240411_123226.jpg", pb=True),
            son("b02", "r8", [[22.88, 23.14], [24.64, 26.00], [27.58, 29.30], [32.32, 33.16]], GC_P),
            off("b03", "OFF2", cenas=[[CUR, 160.0, "pb"], [CUR, 232.0]]),
            son("b04", "r7", [[14.90, 16.36], [17.28, 18.20]]),
            off("b05", "OFF3", foto="crepe bandagem.png"),
            son("b06", "1530", [[65.28, 69.86]]),
            son("b07", "mae2", [[17.72, 21.08]], GC_M),
            off("b08", "OFF4", cenas=[[EVENTO, 6.0]], etiqueta=True),
            son("b09", "r7", [[119.48, 120.88], [121.90, 122.70], [123.20, 124.48]], etiqueta=True),
            off("b10", "OFF5", foto="20241107_202353.jpg", final=True)],
           [zona("mae2", 17.72, [120, 300, 960, 1330], "rosto da mae (quem fala)")],
           {"vaquinha ha quase 4 anos, quase 1 ano de curativos; pessoas sumiram": "Pedrinho, roteiro 8",
            "acham que ele esta bem de ajuda": "Pedrinho, roteiro 7", "custos altos de atadura e gaze": "Pedrinho, 20260917_001530",
            "curativo 2x por dia": "Pedrinho, 20260917_001530", "absurdo de caro": "mae, Roteiro_ os curativos... absurdo de caro"})

reportagem(8, "monument_music-wander-143535 (2).mp3", ["MENINO COM DOENÇA RARA", "NÃO PODE ESPERAR A JUSTIÇA"],
           "R$ 10 ajuda hoje ❤️",
           {"OFF1": "O processo na Justiça já começou. A resposta, não.",
            "OFF2": "Pedrinho tem epidermólise bolhosa. Duas vezes por dia, a mãe troca os curativos do corpo inteiro.",
            "OFF3": "Sem dinheiro para o material, a família não consegue manter os cuidados.",
            "OFF4": "A SOS Human Help está arrecadando doações para os curativos. Dez reais ajudam hoje.",
            "OFF5": "Toque em Saiba mais. O tratamento do Pedrinho não pode esperar a Justiça."},
           [off("b01", "OFF1", foto="20240402_095757.jpg", pb=True),
            son("b02", "r9", [[27.58, 29.20], [29.84, 31.10], [32.18, 33.10], [34.24, 35.96]], GC_P),
            off("b03", "OFF2", cenas=[[CUR, 200.0, "pb"], [CUR, 290.0]]),
            son("b04", "r9", [[52.64, 52.98], [54.56, 58.42]]),
            off("b05", "OFF3", foto="Remédios, Pomadas e Cremes.png"),
            son("b06", "mae1", [[33.92, 34.86], [36.24, 37.82]], GC_M),
            son("b07", "r9", [[44.18, 45.46], [46.98, 48.42]]),
            off("b08", "OFF4", cenas=[[CAMA_MAE, 20.0]], etiqueta=True),
            son("b09", "r9", [[79.36, 80.98], [82.22, 83.64]], etiqueta=True),
            off("b10", "OFF5", foto="20260729_164523.jpg", final=True)],
           [],
           {"processo contra o governo demora": "Pedrinho, roteiro 9", "chora a noite de dor": "Pedrinho, roteiro 9",
            "quem e EB nao pode esperar": "Pedrinho, roteiro 9", "nao consegue nem o basico": "mae, Roteiro_ Nenhuma mae...",
            "curativo 2x por dia": "Pedrinho, 20260917_001530"})

reportagem(9, "rockymetal-ambient-acoustic-239252.mp3", ["MÃE DE MENINO COM DOENÇA RARA:", "“NÃO CONSIGO NEM O BÁSICO”"],
           "R$ 10 ajuda essa mãe ❤️",
           {"OFF1": "Ela faz todos os curativos do filho. Mesmo assim, ouviu que é culpada pela doença dele.",
            "OFF2": "O Pedrinho tem epidermólise bolhosa, uma doença genética. A pele forma feridas com facilidade.",
            "OFF3": "Com esse valor, ela precisa dar conta de gaze, atadura, pomada e soro.",
            "OFF4": "A SOS Human Help está arrecadando doações para essa família. Dez reais já ajudam.",
            "OFF5": "Toque em Saiba mais e caminhe junto com essa mãe."},
           [off("b01", "OFF1", cenas=[[CUR, 205.0, "pb"]]),
            son("b02", "mae1", [[1.74, 3.78], [4.08, 6.98]], GC_M),
            off("b03", "OFF2", foto="20240411_123226.jpg", pb=True),
            son("b04", "mae2", [[35.86, 38.34]]),
            off("b05", "OFF3", foto="Curativos 2 x ao Dia.png"),
            son("b06", "819", [[40.38, 41.84], [43.86, 45.82]], GC_P),
            off("b07", "OFF4", cenas=[[SOFA_MAE, 150.0]], etiqueta=True),
            son("b08", "mae1", [[44.90, 48.62]], etiqueta=True),
            off("b09", "OFF5", foto="Ana e Pedro sorrindo.png", final=True)],
           [zona("mae2", 35.86, [120, 300, 960, 1330], "rosto da mae (quem fala)")],
           {"nenhuma mae deveria ouvir 'culpada'": "mae, Roteiro_ Nenhuma mae...", "mil e quinhentos nao da": "mae, Roteiro_ ... absurdo de caro",
            "nao tem como comprar 2 ou 3 pacotes de atadura": "Pedrinho, 20260917_000819",
            "EB e genetica": "conhecimento geral sobre a doenca"})

reportagem(10, "good_b_music-melody-of-nature-main-6672.mp3", ["SEM SORO, BANHO DE MENINO COM", "“PELE DE BORBOLETA” ARDE"],
           "R$ 4 já é esperança ❤️",
           {"OFF1": "Sem soro fisiológico, o banho do Pedrinho é feito com água. E a água arde na pele dele.",
            "OFF2": "Ele tem epidermólise bolhosa. Cada troca de curativo precisa de soro, gaze e pomada.",
            "OFF3": "A mãe dele nunca imaginou que um dia precisaria pedir ajuda.",
            "OFF4": "A SOS Human Help está arrecadando doações para os curativos do Pedrinho. Quatro reais já ajudam.",
            "OFF5": "Toque em Saiba mais e ajude o Pedrinho a ter um banho sem dor."},
           [off("b01", "OFF1", foto="foto em close.png", pb=True),
            son("b02", "ped", [[30.30, 30.80], [32.88, 33.44], [34.96, 38.78]], GC_P),
            off("b03", "OFF2", foto="soro fisiológico.png"),
            son("b04", "ped", [[21.46, 24.26]]),
            son("b05", "ped", [[40.08, 41.70], [42.36, 43.76]]),
            off("b06", "OFF3", cenas=[[CUR, 245.0, "pb"]]),
            son("b07", "mae2", [[22.36, 24.20], [26.08, 26.44], [27.80, 28.04], [29.82, 30.22]], GC_M),
            off("b08", "OFF4", cenas=[[GUITAR, 8.0]], etiqueta=True),
            son("b09", "ped", [[63.00, 66.92], [67.72, 67.72], [69.44, 69.72], [71.56, 74.14]], etiqueta=True),
            off("b10", "OFF5", foto="20230603_203654.jpg", final=True)],
           ZPED(30.30) + ZPED(21.46) + ZPED(40.08) + ZPED(63.00) + [zona("mae2", 22.36, [120, 300, 960, 1330], "rosto da mae")],
           {"sem soro, banho com agua que arde": "Pedrinho, Roteiro_ peco perdao...", "cada item e importante na troca": "Pedrinho, idem",
            "4, 5, 10 reais = esperanca de um dia sem dor": "Pedrinho, idem", "nunca pensou que precisaria pedir ajuda": "mae, ... absurdo de caro"})

# ===================================================================== LISTA (Leonardo)
KW = ["ATADURA", "GAZE", "POMADA", "SORO", "FISIOLÓGICO", "ESPARADRAPO", "ÓLEO", "GIRASSOL", "DUAS", "VEZES",
      "DOR", "ÁGUA", "ARDE", "SAIBA", "MAIS", "DOZE", "REAIS", "MIL", "QUINHENTOS", "BOLHAS", "FERIDAS", "NOITE"]


def bloco(nome, fala, pausa=0.35, cenas=None, foto=None, **kw):
    bl = {"nome": nome, "fala": fala, "pausa": pausa}
    if cenas:
        bl["cenas"] = cenas
    if foto:
        bl["foto"] = b(foto)
    bl.update(kw)
    return bl


def lista(n, musica, chamada, etiqueta, narr_, blocos, fatos, zonas=None):
    salvar(f"Pedrinho_lista_v{n}", {
        "pedido": "completar LEVA 01 (26/10/2026)",
        "voz": {"voice_id": LEONARDO, "model_id": "eleven_multilingual_v2", "obs": "Leonardo (brasileiro), conta paga"},
        "musica": f"{MUS}/{musica}", "musica_volume": 0.12, "chamada": chamada, "etiqueta": etiqueta,
        "etiqueta_final": FIM, "palavras_chave": KW, "narracao": narr_, "fatos": fatos, "blocos": blocos,
        "zonas_protegidas": zonas or []})


R5338, R9V, R8V, R1530, R819 = (bruto(FONTE[k][0]) for k in ("5338", "r9", "r8", "1530", "819"))

lista(3, "echoes_of_lumen-sad-piano-591198.mp3", ["UM BANHO SEM DOR 💔", "DOE R$ 10 PRO SORO DO PEDRINHO 👼"],
      "R$ 10 já ajuda ❤️",
      {"N01": "Esses são os itens de um banho do Pedrinho.", "I1": "Soro fisiológico.", "I2": "Gaze.", "I3": "Pomada.",
       "I4": "Óleo de girassol.", "I5": "Atadura.",
       "N03": "Sem o soro, o banho é com água. E a água arde na pele dele.",
       "N04": "Ele tem epidermólise bolhosa. A pele vive cheia de bolhas e feridas.",
       "N05": "Por isso, a troca é feita duas vezes por dia.",
       "N06": "Quatro, cinco, dez reais. Para ele, é a esperança de um dia sem dor.",
       "N07": "Toque em Saiba mais e garanta o soro do Pedrinho."},
      [bloco("s01", "N01", cenas=[[R9V, 3.0, "pb"], [CUR, 185.0, "pb"]]),
       bloco("i1", "I1", 0.25, foto="soro fisiológico.png"), bloco("i2", "I2", 0.25, foto="GAZE.png"),
       bloco("i3", "I3", 0.25, foto="Pomada.png"), bloco("i4", "I4", 0.25, foto="OLeo de girassol.png"),
       bloco("i5", "I5", 0.25, foto="crepe bandagem.png"),
       bloco("s03", "N03", cenas=[[CUR, 245.0, "pb"], [CUR, 260.0, "pb"]]),
       bloco("s04", "N04", cenas=[[R1530, 30.0, "pb"], [CUR, 300.0]]),
       bloco("s05", "N05", 0.4, foto="Curativos 2 x ao Dia.png"),
       bloco("s06", "N06", cenas=[[GUITAR, 20.0], [CAMA_MAE, 60.0]], etiqueta=True),
       bloco("s07", "N07", 1.6, foto="20260729_164523.jpg", final=True)],
      {"sem soro o banho e com agua que arde; 4, 5, 10 reais = um dia sem dor": "Pedrinho, Roteiro_ peco perdao...",
       "2x por dia": "Pedrinho, 20260917_001530", "itens": "fotos do banco"})

lista(4, "alex-morgan-sad-piano-emotional-rain-story-575883.mp3", ["NOITE EM CLARO DE DOR 💔", "DOE R$ 12 PRO PEDRINHO DORMIR 👼"],
      "R$ 12 já ajuda ❤️",
      {"N01": "A noite passada, o Pedrinho não dormiu. Ele viu o dia amanhecer.",
       "N02": "O que tira o sono dele:", "I1": "Feridas abertas.", "I2": "Bolhas novas.", "I3": "Dor nos músculos.",
       "I4": "E o calor.", "N03": "O que alivia:", "I5": "Pomada.", "I6": "Gaze.", "I7": "Atadura.",
       "N04": "Mas o material está no fim.",
       "N05": "Ele pediu ajuda de seis pessoas, em cinco dias. Doze reais de cada uma.",
       "N06": "Toque em Saiba mais e ajude o Pedrinho a dormir sem dor."},
      [bloco("s01", "N01", cenas=[[R5338, 33.0, "pb"], [R5338, 37.5, "pb"]]),
       bloco("s02", "N02", 0.2, cenas=[[CUR, 150.0, "pb"]]),
       bloco("i1", "I1", 0.25, foto="20240402_095757.jpg", pb=True), bloco("i2", "I2", 0.25, foto="20240411_123226.jpg", pb=True),
       bloco("i3", "I3", 0.25, cenas=[[R9V, 64.0, "pb"]]), bloco("i4", "I4", 0.3, cenas=[[R8V, 58.0, "pb"]]),
       bloco("s03", "N03", 0.2, cenas=[[CUR, 290.0]]),
       bloco("i5", "I5", 0.25, foto="Pomada.png"), bloco("i6", "I6", 0.25, foto="GAZE.png"),
       bloco("i7", "I7", 0.25, foto="crepe bandagem.png"),
       bloco("s04", "N04", 0.4, cenas=[[R819, 30.0]]),
       bloco("s05", "N05", 0.4, cenas=[[CAMA_MAE, 40.0], [EVENTO, 10.0]], etiqueta=True),
       bloco("s06", "N06", 1.6, foto="20241107_202353.jpg", final=True)],
      {"noite em claro, viu o dia amanhecer; 6 pessoas em 5 dias, R$ 12": "Pedrinho, 20260916_235338",
       "dor muscular, choro a noite": "Pedrinho, roteiro 9", "calor ruim pra pele; bolhas piores": "Pedrinho, roteiro 8",
       "material acabou": "Pedrinho, 20260917_000819"})

lista(5, "monument_music-wander-143535 (2).mp3", ["R$ 1.500 NÃO DÃO CONTA 💔", "DOE R$ 10 E ALIVIE ESSA MÃE ❤️"],
      "R$ 10 já ajuda ❤️",
      {"N01": "Mil e quinhentos reais. É o benefício que o Pedrinho recebe. E não dá conta.",
       "N02": "Só no curativo entram:", "I1": "Atadura.", "I2": "Gaze.", "I3": "Pomada.", "I4": "Soro.",
       "I5": "Esparadrapo.", "I6": "Suplemento.",
       "N03": "Duas vezes por dia. Todos os dias.",
       "N04": "A mãe dele resume: é absurdo de caro.",
       "N05": "Ela não pede obrigação. Pede ajuda para salvar o filho.",
       "N06": "Toque em Saiba mais e complete o que o benefício não cobre."},
      [bloco("s01", "N01", cenas=[[R1530, 5.0, "pb"], [CUR, 210.0, "pb"]]),
       bloco("s02", "N02", 0.2, cenas=[[CUR, 40.0]]),
       bloco("i1", "I1", 0.25, foto="crepe bandagem.png"), bloco("i2", "I2", 0.25, foto="GAZE.png"),
       bloco("i3", "I3", 0.25, foto="Pomada.png"), bloco("i4", "I4", 0.25, foto="soro fisiológico.png"),
       bloco("i5", "I5", 0.25, foto="esparadrapo impermeável.png"),
       bloco("i6", "I6", 0.25, foto="Cubitan -Suplementos e Dieta Terapêutica.png"),
       bloco("s03", "N03", 0.4, cenas=[[CUR, 232.0, "pb"], [CUR, 300.0]]),
       bloco("s04", "N04", 0.4, cenas=[[SOFA_MAE, 60.0]], etiqueta=True),
       bloco("s05", "N05", 0.4, cenas=[[CAMA_MAE, 70.0]], etiqueta=True),
       bloco("s06", "N06", 1.6, foto="Ana e Pedro sorrindo.png", final=True)],
      {"recebe mil e quinhentos (LOAS) e nao da": "mae, Roteiro_ os curativos... absurdo de caro (so o LOAS nao da)",
       "absurdo de caro": "mae, idem", "nao tem obrigacao, mas ajude a salvar meu filho": "mae, Roteiro_ Nenhuma mae...",
       "suplemento": "Pedrinho, Um Video Novo pra campanha", "2x por dia": "Pedrinho, 20260917_001530"})

# ===================================================================== VSL com a voz da crianca
KWV = ["CURATIVO", "CURATIVOS", "ACABANDO", "ACABOU", "DOR", "DORES", "MEDO", "ANJO", "NOITE", "AMANHECER",
       "ESPERAR", "ARDE", "ÁGUA", "SORO", "FAIXA", "ATADURA", "REAIS", "GRATIDÃO", "BATALHA", "ESQUECERAM", "SUMIRAM"]


def frase(nome, f, cortes, cenas=None, foto=None, **kw):
    fr = {"nome": nome, "fonte": bruto(FONTE[f][0]), "tx": tx(FONTE[f][1]), "cortes": cortes}
    if cenas:
        fr["cenas"] = cenas
    if foto:
        fr["foto"] = b(foto)
    fr.update(kw)
    return fr


def vsl(n, musica, chamada, etiqueta, frases, fix=None):
    salvar(f"Pedrinho_vsl_voz_v{n}", {
        "pedido": "completar LEVA 01 (26/10/2026)", "musica": f"{MUS}/{musica}", "musica_volume": 0.09,
        "chamada": chamada, "etiqueta": etiqueta, "etiqueta_final": FIM, "palavras_chave": KWV,
        "frases": frases, "zonas_protegidas": [], **({"fix": fix} if fix else {})})


vsl(2, "echoes_of_lumen-sad-piano-591198.mp3", ["O CURATIVO DO PEDRINHO ACABOU 💔", "DOE R$ 5 PRA REPOR O MATERIAL 👼"],
    "R$ 5 já ajuda ❤️",
    [frase("f01", "819", [[1.44, 1.80], [3.54, 4.44], [6.00, 6.58]], cenas=[[R819, 1.3, "pb"]]),
     frase("f02", "819", [[11.60, 15.52]], cenas=[[CUR, 20.0, "pb"]]),
     frase("f03", "819", [[16.56, 16.72], [18.20, 18.42], [19.76, 20.14], [20.86, 22.18], [22.86, 24.40], [25.06, 25.42]],
           cenas=[[CUR, 232.0], [CUR, 290.0]]),
     frase("f04", "819", [[29.86, 30.64], [31.48, 31.62], [32.76, 32.76]], foto="Remédios, Pomadas e Cremes.png"),
     frase("f05", "819", [[40.38, 41.84], [43.86, 45.82], [47.86, 49.72]], foto="crepe bandagem.png"),
     frase("f06", "819", [[51.80, 52.94], [56.10, 59.10]], cenas=[[GUITAR, 40.0]], etiqueta=True),
     frase("f07", "819", [[67.22, 67.62], [68.98, 69.28], [70.20, 71.26]], foto="20250401_204159.jpg", final=True)])

vsl(3, "alex-morgan-sad-piano-emotional-rain-story-575883.mp3", ["6 PESSOAS EM 5 DIAS 💔", "DOE R$ 12 PROS CURATIVOS DELE 👼"],
    "R$ 12 garante a semana ❤️",
    [frase("f01", "5338", [[33.24, 36.00], [37.40, 38.50]], cenas=[[R5338, 33.1, "pb"]]),
     frase("f02", "r9", [[52.64, 52.98], [54.56, 58.42]], cenas=[[CUR, 175.0, "pb"]]),
     frase("f03", "5338", [[1.58, 2.82], [4.20, 4.42], [5.88, 6.14], [7.14, 7.42], [8.46, 8.80]], foto="20260127_110703.jpg"),
     frase("f04", "5338", [[10.32, 10.86], [12.78, 14.06], [14.96, 17.28], [18.70, 21.66]], foto="Curativos 2 x ao Dia.png",
           etiqueta=True),
     frase("f05", "5338", [[28.56, 28.76], [30.04, 31.76]], cenas=[[CAMA_MAE, 20.0]], etiqueta=True),
     frase("f06", "5338", [[51.26, 52.48], [55.18, 56.80]], foto="20241107_202353.jpg", final=True)])

vsl(4, "paulyudin-sad-sad-music-485935 (2).mp3", ["ELE NÃO PODE SER ESQUECIDO 💔", "DOE R$ 3 PRAS FAIXAS DELE 👼"],
    "R$ 3 já ajuda ❤️",
    [frase("f01", "r8", [[22.88, 23.14], [24.64, 26.00]], cenas=[[R8V, 22.8, "pb"]]),
     frase("f02", "r8", [[27.58, 29.30], [32.32, 33.16]], cenas=[[CUR, 140.0, "pb"]]),
     frase("f03", "r8", [[2.56, 5.56], [7.56, 10.58], [12.04, 13.28]], foto="20240514_210632.jpg"),
     frase("f04", "r8", [[65.54, 67.42], [70.00, 70.54], [71.54, 72.00], [73.02, 73.72]], foto="crepe bandagem.png"),
     frase("f05", "r8", [[92.46, 94.54], [95.32, 95.88]], cenas=[[CUR, 245.0, "pb"]]),
     frase("f06", "r8", [[104.46, 104.84], [106.06, 106.58], [108.90, 109.92], [110.98, 110.98], [112.56, 112.56],
                         [115.14, 116.14], [117.24, 117.50], [119.00, 119.22]], cenas=[[GUITAR, 30.0]], etiqueta=True),
     frase("f07", "r8", [[127.62, 129.58]], foto="20241109_123330.jpg", final=True)],
    fix={"VAKINHA": "VAQUINHA"})

vsl(5, "monument_music-wander-143535 (2).mp3", ["ELE NÃO PODE ESPERAR 💔", "DOE R$ 4 POR UM DIA SEM DOR 👼"],
    "R$ 4 já é esperança ❤️",
    [frase("f01", "r9", [[44.18, 45.46], [46.98, 48.42], [49.06, 51.38]], cenas=[[R9V, 44.1, "pb"]]),
     frase("f02", "r9", [[27.58, 29.20], [29.84, 31.10], [32.18, 33.10], [34.24, 35.96]], cenas=[[CUR, 210.0, "pb"]]),
     frase("f03", "ped", [[30.30, 30.80], [32.88, 33.44], [34.96, 38.78]], foto="soro fisiológico.png"),
     frase("f04", "ped", [[40.08, 41.70], [42.36, 45.04]], cenas=[[CUR, 280.0, "pb"]]),
     frase("f05", "ped", [[46.82, 49.36]], cenas=[[CAMA_MAE, 50.0]]),
     frase("f06", "ped", [[63.00, 66.92], [67.72, 67.72], [69.44, 69.72], [71.56, 74.14]], cenas=[[EVENTO, 12.0]], etiqueta=True),
     frase("f07", "ped", [[75.12, 75.90]], foto="20230603_203654.jpg", final=True)],
    fix={"B": "EB"})

# ===================================================================== CORTES COM GANCHO (edicao-criativo-ong)


def segs(f, partes):
    """[[1a palavra, ultima palavra], ...] por segmento -> in/out pelas palavras da transcricao."""
    words = [w for w in json.load(open(tx(FONTE[f][1]), encoding="utf-8"))["words"] if w.get("type") == "word"]
    out = []
    for p in partes:
        a, z, extra = p[0], p[1], (p[2] if len(p) > 2 else {})
        i = min(range(len(words)), key=lambda k: abs(words[k]["start"] - a))
        j = min(range(len(words)), key=lambda k: abs(words[k]["start"] - z))
        prev_end = words[i - 1]["end"] if i else 0.0
        nxt = words[j + 1]["start"] if j + 1 < len(words) else words[j]["end"] + 0.5
        out.append({"in": round(max(words[i]["start"] - 0.07, prev_end + 0.02), 2),
                    "out": round(min(words[j]["end"] + 0.10, nxt - 0.02), 2),
                    "txt": " ".join(w["text"] for w in words[i:j + 1]), **extra})
    return out


def cortes(nome, f, face, partes, hook, endcard, red, fix=None):
    salvar(nome, {"pedido": "completar LEVA 01 (26/10/2026)", "raw": bruto(FONTE[f][0]), "transcript": tx(FONTE[f][1]),
                  "bank": BANK, "music": f"{MUS}/alex-morgan-sad-piano-emotional-rain-story-575883.mp3",
                  "face": face, "segments": segs(f, partes), "fix": fix or {}, "red": red, "hook": hook,
                  "endcard": endcard, "badge": "SAIBA MAIS"})


BR_CUR = lambda s: {"broll": [{"src": os.path.basename(CUR), "start": s}]}  # noqa: E731
cortes("Pedrinho_noite_v1", "5338", [690, 330],
       [[33.24, 36.00, {"zoom": "Z2"}], [37.40, 38.50, {"zoom": "ZF"}], [1.58, 2.82, {"zoom": "Z1"}], [4.20, 4.42, {"zoom": "Z3"}],
        [5.88, 6.14, {"zoom": "Z2"}], [7.14, 7.42, {"zoom": "Z3"}], [8.46, 8.80, {"zoom": "ZF"}],
        [10.32, 10.86, {"zoom": "Z1"}], [12.78, 14.06, {"zoom": "Z2"}], [14.96, 17.28, BR_CUR(232.0)], [18.70, 21.66, BR_CUR(290.0)],
        [28.56, 29.22, {"zoom": "ZF"}], [30.04, 31.76, {"zoom": "Z3"}],
        [42.66, 43.94, {"broll": [{"src": "20241110_104724.mp4", "start": 8.0}]}], [44.82, 45.24, {"zoom": "Z2"}],
        [46.96, 48.04, {"zoom": "Z1"}], [51.26, 52.48, {"zoom": "Z3"}], [55.18, 56.80, {"zoom": "Z2"}]],
       [{"t0": 0.0, "t1": 1.9, "lines": ["ELE NÃO DORMIU"], "fs": 100},
        {"t0": 1.9, "t1": 5.0, "lines": ["O PEDRINHO VIU", "O DIA AMANHECER", "*DE DOR*"], "fs": 92}],
       {"src": "20241110_104724.mp4", "start": 12.0, "dur": 3.4, "lines": ["DÊ AO PEDRINHO", "UMA NOITE SEM DOR"],
        "cta": "TOQUE EM SAIBA MAIS"},
       ["CURATIVO", "CURATIVOS", "DOR", "CLARO", "AMANHECER", "CINCO", "SEIS", "12", "ME", "AJUDE"])

cortes("Pedrinho_espera_v1", "r9", [583, 470],
       [[44.18, 45.46, {"zoom": "Z2"}], [46.98, 48.42, {"zoom": "Z3"}], [49.06, 51.38, {"zoom": "ZF"}],
        [1.22, 4.28, {"zoom": "Z1"}], [7.08, 8.28, {"zoom": "Z3"}],
        [27.58, 29.20, BR_CUR(200.0)], [29.84, 31.10, BR_CUR(215.0)], [32.18, 33.10, {"zoom": "Z2"}], [34.24, 35.96, {"zoom": "ZF"}],
        [52.64, 52.98, {"zoom": "Z1"}], [54.56, 58.42, {"zoom": "Z3"}],
        [79.36, 80.98, {"broll": [{"src": "20260825_134710.jpg"}, {"src": "20260825_134438.jpg"}, {"src": "20260825_134340.jpg"}]}],
        [82.22, 83.64, {"zoom": "Z2"}], [91.08, 91.80, {"zoom": "Z1"}]],
       [{"t0": 0.0, "t1": 1.9, "lines": ["ELE NÃO PODE ESPERAR"], "fs": 96},
        {"t0": 1.9, "t1": 5.2, "lines": ["A JUSTIÇA DEMORA.", "AS FERIDAS", "DO PEDRINHO *NÃO*"], "fs": 88}],
       {"src": "20260410_210553.mp4", "start": 20.0, "dur": 3.4, "lines": ["O TRATAMENTO DELE", "NÃO PODE ESPERAR"],
        "cta": "TOQUE EM SAIBA MAIS"},
       ["CURATIVO", "CURATIVOS", "FERIMENTOS", "FERIDAS", "ESPERAR", "CHORAR", "DEMORA"], fix={"B": "EB"})

cortes("Pedrinho_esquecido_v1", "r8", [551, 616],
       [[22.88, 23.14, {"zoom": "Z2"}], [24.64, 26.00, {"zoom": "ZF"}], [27.58, 29.30, {"zoom": "Z1"}], [32.32, 33.16, {"zoom": "Z3"}],
        [2.56, 4.00, {"zoom": "Z2"}], [4.84, 5.56, {"zoom": "Z1"}],
        [7.56, 10.58, {"broll": [{"src": "20240514_210632.jpg"}, {"src": "20260127_110703.jpg"}]}], [12.04, 13.28, {"zoom": "Z3"}],
        [65.54, 67.42, {"broll": [{"src": "crepe bandagem.png"}]}], [70.00, 70.54, {"zoom": "Z2"}], [71.54, 72.00, {"zoom": "Z1"}],
        [73.02, 73.72, {"zoom": "ZF"}], [92.46, 94.54, BR_CUR(245.0)], [95.32, 95.88, {"zoom": "Z3"}],
        [104.46, 104.84, {"zoom": "Z2"}], [106.06, 106.58, {"zoom": "Z1"}], [108.90, 109.92, {"zoom": "Z3"}],
        [110.98, 110.98, {"zoom": "Z2"}], [112.56, 112.56, {"zoom": "ZF"}], [127.62, 129.58, {"zoom": "Z1"}]],
       [{"t0": 0.0, "t1": 1.9, "lines": ["ELE FOI ESQUECIDO"], "fs": 100},
        {"t0": 1.9, "t1": 5.2, "lines": ["AS FAIXAS DO PEDRINHO", "ESTÃO ACABANDO", "E ELE TEM *MEDO*"], "fs": 88}],
       {"src": "20241110_104724.mp4", "start": 4.0, "dur": 3.4, "lines": ["NÃO DEIXE O PEDRINHO", "SER ESQUECIDO"],
        "cta": "TOQUE EM SAIBA MAIS"},
       ["CURATIVOS", "ATADURAS", "FAIXAS", "ACABANDO", "MEDO", "BOLHAS", "PIORES", "ESQUECERAM", "SUMIRAM"],
       fix={"VAKINHA": "VAQUINHA"})

json.dump(PLANOS, open(os.path.join(P, "_folhas", "planos_completar.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k in PLANOS:
    print("ok", k)
