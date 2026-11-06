"""Escreve os 10 planos dos criativos modelados nas bibliotecas (03/11/2026). Uso: python -I gerar_planos.py
v2 (pedido do usuario, 03/11/2026): posicoes, tamanhos e fontes medidos nas referencias (quadros 360x640 x3),
musicas tristes da Magnific (MUSICAS\\magnific_tristes) e o 209 abrindo com takes fortes."""
import json
import os

try:  # pasta do material deste PC (gravada pelo instalar.py); sem ela, o padrao da Area de Trabalho
    RAIZ = json.load(open(os.path.join(os.path.expanduser("~"), ".claude", "estudio-ong.json"), encoding="utf-8-sig"))["raiz"]
except (OSError, ValueError, KeyError):
    RAIZ = os.path.join(os.path.expanduser("~"), "Desktop", "EDIÇÃO COM CLAUDE")
D = os.path.join(RAIZ, "VÍDEOS PARA EDITAR", "PEDRINHO 02-11-2026")
BN = os.path.join(RAIZ, "banco de vídeos do pedrinho")
REF = os.path.join(RAIZ, "EDITADOS", "_referencias", "bibliotecas")
MT = os.path.join(RAIZ, "MÚSICAS", "magnific_tristes")
PL = os.path.join(RAIZ, "EDITADOS", "_planos")


def r(n):
    return os.path.join(D, n + ".mp4")


def mus(nome):
    return os.path.join(MT, nome + ".mp3")


A, B = r("20261102_144645"), r("lv_0_20261102155438")
P1, P3 = r("20261102_151540"), r("20261102_151715")
S1, S2, S3, S4 = r("20261102_152542"), r("20261102_152631"), r("20261102_152739"), r("20261102_153323")
K1, K2, K3, K4, K5, K6 = (r(x) for x in ("20261102_104706", "20261102_104943", "20261102_113535", "20261102_113735",
                                         "20261102_113918", "20261102_114148"))
# trechos do banco usados, recortados em _clipes_bib (o pacote do outro editor leva so eles): tempos relativos
# ao recorte (bn1 comeca em 20 s do original, bn2 em 92 s, bn3 em 155 s)
CL = os.path.join(BN, "_clipes_bib")
BN1 = os.path.join(CL, "bn1_curativos_cama_20s.mp4")
BN2 = os.path.join(CL, "bn2_1760826007_92s.mp4")
BN3 = os.path.join(CL, "bn3_1792347808_155s.mp4")


def fala(arq, ini, fim, **k):
    return dict(arq=arq, ini=ini, fim=fim, som=True, **k)


def mudo(arq, ini, fim, **k):
    return dict(arq=arq, ini=ini, fim=fim, som=False, **k)


# pedacos da fala sem as pausas longas (tempos da transcricao)
a = {1: (1.50, 2.95), 2: (3.45, 7.05), 3: (10.35, 12.85), 4: (13.25, 16.95), 5: (19.00, 22.40), 6: (22.70, 23.70),
     7: (26.90, 28.65), 8: (31.70, 34.55), 9: (34.90, 38.25), 11: (38.70, 40.60), 12: (41.00, 43.00)}
b = {1: (1.65, 6.20), 2: (7.55, 9.95), 3: (10.50, 14.55), 4: (15.25, 18.40), 5: (23.70, 26.60), 6: (26.95, 27.95),
     7: (28.40, 30.60), 8: (32.25, 34.25), 9: (34.75, 37.35)}
FIM_CTA = {"linhas": ["CLIQUE EM", "SAIBA MAIS"], "cor": "vermelho", "size": 70, "escuro": 0.45}
# volume da musica: faixa a -31 LUFS sob a fala, a -16 LUFS quando so tem musica (LUFS medidos em 03/11/2026)
LUFS = {"Moonlight_Sonata": -22.7, "Ill_Die_on_This_Hill": -13.1, "A_Violins_Lament": -15.2,
        "You_Cant_Come_Back": -14.9, "No_Return": -15.8, "Faded_Ink": -14.1, "The_Weight_of_Time": -15.8,
        "One_Last_Goodbye": -16.3, "Fading_Ember": -16.3, "Goodbyes": -16.0}


def vol(nome, alvo):
    return round(10 ** ((alvo - LUFS[nome]) / 20), 3)


SOB_FALA, SO_MUSICA = -31, -16
planos = {}

# 1. Lar Maos Amigas 1850852882715660: pergunta em faixas pretas por linha no alto a esquerda (y 8-18%), legenda
#    de 2-3 palavras em caixa alta com a falada em amarelo (y 58%), frase fixa branca no meio-baixo (y 76%),
#    b-roll nos fatos, cartela final.
planos["maos_amigas_coragem"] = dict(
    ref=os.path.join(REF, "maosamigas_1850852882715660.mp4"), estilo="BIB MAOS AMIGAS",
    base=[fala(A, *a[i]) for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12)],
    broll=[[0, 2.9, K1, 0.5], [7.55, 11.25, K6, 9], [15.65, 17.4, K2, 2], [20.25, 23.6, K4, 6]],
    textos=[{"de": 0, "ate": 2.9, "linhas": ["QUEM TEM CORAGEM DE", "PASSAR DIRETO POR", "ELE? 💔"],
             "estilo": "caixa", "por_linha": True, "bg": "preto", "fg": "branco", "size": 52, "fonte": "arial",
             "y": 250, "alinha": "esq", "x": 50, "pad": [10, 0], "lh": 1.0},
            {"de": 2.9, "ate": 25.3, "linhas": ["Curativos no fim…", "quem vai ajudar", "o Pedrinho agora? 💔"],
             "estilo": "seco", "size": 50, "y": 1460, "contorno": 0, "lh": 1.12}],
    legenda={"estilo": "amarelo", "y": 1113, "size": 54, "fonte": "bold", "contorno": 3},
    fim=dict(FIM_CTA, de=25.3, sub=["Sua ajuda vira curativo", "na pele do Pedrinho"]),
    musica=mus("A_Violins_Lament"), musica_volume=vol("A_Violins_Lament", SOB_FALA))

# 2. Lar Maos Amigas 1961085214849293: so musica, frase pequena branca no centro (y 48%), cena nova a cada ~3 s.
planos["maos_amigas_compartilhe"] = dict(
    ref=os.path.join(REF, "maosamigas_1961085214849293.mp4"), estilo="BIB COMPARTILHE",
    base=[mudo(K4, 3, 6), mudo(K1, 2, 5), mudo(K2, 4, 7), mudo(BN2, 10, 13), mudo(K5, 2, 5), mudo(S3, 4, 7),
          mudo(K3, 5, 8), mudo(P3, 3, 6.5)],
    textos=[{"de": 0, "ate": 21.5, "linhas": ["Se 2 mil pessoas compartilharem", "este vídeo, mais gente vai ajudar",
                                               "nos curativos do Pedrinho"],
             "estilo": "seco", "size": 31, "y": 925, "contorno": 0, "lh": 1.08}],
    fim=dict(FIM_CTA, de=21.5, sub=["e compartilhe este vídeo"]),
    musica=mus("Moonlight_Sonata"), musica_volume=vol("Moonlight_Sonata", SO_MUSICA))

# 3. Lar Maos Amigas 2109425177114400: agradecimento em letra branca grossa com contorno (y 70%), so musica,
#    takes longos; abre com os takes mais fortes (pedido do usuario: pernas enfaixadas em P&B, placa
#    "meus curativos estao acabando") e fecha com ele agradecendo com a propria voz.
planos["maos_amigas_obrigado"] = dict(
    ref=os.path.join(REF, "maosamigas_2109425177114400.mp4"), estilo="BIB OBRIGADO",
    base=[mudo(K6, 0.5, 4.5, pb=True), mudo(S1, 3.0, 6.5), mudo(K4, 8, 12), mudo(K1, 3, 6.5), mudo(K3, 0, 3.5),
          mudo(K2, 0, 3.0), fala(B, *b[9])],
    textos=[{"de": 0, "ate": 21.5, "linhas": ["Cada real que chega vira", "curativo e pomada na", "pele do Pedrinho.",
                                               "OBRIGADO DE CORAÇÃO 🙏"],
             "estilo": "seco", "size": 50, "y": 1345, "contorno": 4, "lh": 1.1}],
    fim=dict(FIM_CTA, de=23.1, escuro=0.3),
    musica=mus("You_Cant_Come_Back"), musica_volume=vol("You_Cant_Come_Back", SO_MUSICA),
    musica_depois=[21.5, vol("You_Cant_Come_Back", SOB_FALA)])

# 4. Lar Mae Ritinha 931067246550453: abre em P&B (~7 s) com a manchete "VIRALIZOU:" em faixas pretas no alto a
#    esquerda; depois a fala em cor, caixa vermelha fixa no alto (y 16%, letra fina) e uma palavra por vez (y 65%).
planos["mae_ritinha_viralizou"] = dict(
    ref=os.path.join(REF, "maeritinha_931067246550453.mp4"), estilo="BIB VIRALIZOU",
    base=[fala(B, *b[1], pb=True), fala(B, *b[2], pb=True)] + [fala(B, *b[i]) for i in (3, 4, 5, 6, 7, 8, 9)],
    broll=[[8.5, 11.0, K3, 3], [11.0, 13.2, K6, 8], [18.05, 20.25, K4, 14], [20.25, 22.25, BN2, 1]],
    textos=[{"de": 0, "ate": 6.95, "linhas": ["VIRALIZOU: Menino com pele de borboleta",
                                              "pede ajuda para os curativos"],
             "estilo": "caixa", "por_linha": True, "bg": "preto", "fg": "branco", "size": 33, "fonte": "arial",
             "y": 255, "alinha": "esq", "x": 22, "pad": [8, 0], "lh": 1.12},
            {"de": 6.95, "ate": 23.9, "linhas": ["faça a sua parte", "e doe 5 reais"], "estilo": "caixa",
             "bg": "vermelho", "fg": "branco", "size": 54, "y": 300, "fonte": "regular", "pad": [28, 10],
             "lh": 1.12}],
    legenda={"estilo": "palavra", "y": 1250, "size": 54},
    fim=dict(FIM_CTA, de=23.9, escuro=0.5),
    musica=mus("Ill_Die_on_This_Hill"), musica_volume=vol("Ill_Die_on_This_Hill", SOB_FALA))

# 5. Lar Mae Ritinha 1746937610772060: so musica, cenas lentas, frase branca fixa no meio (y ~50%).
planos["mae_ritinha_mil_pessoas"] = dict(
    ref=os.path.join(REF, "maeritinha_1746937610772060.mp4"), estilo="BIB MIL PESSOAS",
    base=[mudo(K1, 0, 3), mudo(K4, 15, 18), mudo(A, 7.2, 10.2), mudo(K5, 0, 3), mudo(P1, 0.2, 3.2),
          mudo(K6, 12, 15), mudo(S4, 0.2, 3.2), mudo(BN2, 1, 4), mudo(K3, 9, 12.5)],
    textos=[{"de": 0, "ate": 24.5, "linhas": ["Precisamos encontrar 1.000", "pessoas dispostas a doar apenas",
                                               "R$5 para os curativos do Pedrinho.", "Você pode ser uma delas? ❤️"],
             "estilo": "seco", "size": 40, "y": 985, "contorno": 0, "lh": 1.05}],
    fim=dict(FIM_CTA, de=24.5, escuro=0.4),
    musica=mus("No_Return"), musica_volume=vol("No_Return", SO_MUSICA))

# 6. Movamor 1080789844796360: a crianca falando quase sem corte, "saiba mais" amarelo italico (y 65%),
#    caixa branca com a historia em letra serifada (y 69%), cartela escura com caixa verde, texto verde e setas.
planos["movimento_amor_vaquinha"] = dict(
    ref=os.path.join(REF, "movamor_1080789844796360.mp4"), estilo="BIB CAMPANHA",
    base=[fala(A, 1.5, 7.05), fala(A, 10.35, 16.95), fala(A, 19.0, 28.65), fala(A, 31.7, 40.6), fala(A, 41.0, 43.0),
          mudo(K3, 3, 6.5)],
    textos=[{"de": 1.5, "ate": 32.7, "linhas": ["Ajude pelo", "“saiba mais”"], "estilo": "seco", "fg": "amarelo",
             "size": 52, "y": 1215, "contorno": 2, "fonte": "italico", "lh": 1.0},
            {"de": 8.0, "ate": 32.7, "linhas": ["Pedrinho tem epidermólise bolhosa, a pele de",
                                                 "borboleta. Uma caixa de curativos custa R$1.500.",
                                                 "A SOS Human Help pede ajuda para o tratamento dele."],
             "estilo": "caixa", "bg": "branco", "fg": "preto", "size": 31, "y": 1350, "fonte": "serif",
             "pad": [14, 6], "lh": 1.12}],
    fim={"de": 32.7, "linhas": ["FAÇA PARTE DESSA", "CORRENTE DO BEM!"], "cor": [22, 170, 50], "size": 56, "y": 865,
         "escuro": 0.62, "sub": ["CLIQUE EM", "“SAIBA MAIS”"], "size_sub": 52, "cor_sub": [190, 255, 190],
         "gap_sub": 120, "setas": True, "y_setas": 1440},
    musica=mus("The_Weight_of_Time"), musica_volume=vol("The_Weight_of_Time", SOB_FALA))

# 7. Movamor 1822868738727036: video cru de celular, a crianca falando direto, e so no fim uma frase pequena
#    amarela (y 66%). Musica triste bem baixa (pedido do usuario: musica em todos).
planos["movimento_amor_cru"] = dict(
    ref=os.path.join(REF, "movamor_1822868738727036.mp4"), estilo="BIB CRU",
    base=[fala(B, 1.6, 18.45), fala(B, 23.7, 37.4), mudo(K6, 0, 5)],
    textos=[{"de": 23.0, "ate": 35.5, "linhas": ["Clique em “saiba mais” e ajude", "no tratamento do Pedrinho"],
             "estilo": "seco", "fg": "amarelo", "size": 40, "y": 1270, "contorno": 2, "lh": 1.05}],
    musica=mus("Fading_Ember"), musica_volume=vol("Fading_Ember", -34))

# 8. Florisbela 1494659885944630: abre com a fala mais forte e legenda de uma linha com a palavra falada em
#    amarelo (y 67%); depois so musica e a frase amarela grossa fixa no alto (y 16%). (A referencia usa um rosto
#    feito por IA; aqui e a fala real dele.)
planos["florisbela_sinal"] = dict(
    ref=os.path.join(REF, "florisbela_1494659885944630.mp4"), estilo="BIB SEU SINAL",
    base=[fala(A, *a[8]), fala(A, *a[9]), fala(A, *a[11]), mudo(K4, 20, 24), mudo(K1, 4, 7.5), mudo(K5, 6, 9),
          mudo(BN3, 1, 5), mudo(K2, 7, 10)],
    textos=[{"de": 8.1, "ate": 23.5, "linhas": ["ESSE É O SEU SINAL:", "AJUDE O PEDRINHO COM R$5 🙏"],
             "estilo": "seco", "fg": "amarelo", "size": 60, "y": 315, "contorno": 4, "lh": 1.05}],
    legenda={"estilo": "amarelo", "y": 1280, "size": 50, "fonte": "bold", "caixa_alta": False, "contorno": 3},
    fim=dict(FIM_CTA, de=23.5, escuro=0.4),
    musica=mus("Goodbyes"), musica_volume=vol("Goodbyes", SOB_FALA),
    musica_depois=[8.1, vol("Goodbyes", SO_MUSICA)])

# 9. Florisbela 2388547078640410: abre com o pedido de "30 segundos" e caixa branca no alto (y 21%); a voz dele
#    passa por cima dos curativos com legenda branca de uma linha (y 62%); caixa branca fixa "qualquer valor";
#    fim com ele agradecendo (a caixa sai para nao cobrir o rosto).
planos["florisbela_30_segundos"] = dict(
    ref=os.path.join(REF, "florisbela_2388547078640410.mp4"), estilo="BIB DEUS TE TROUXE",
    base=[fala(P3, 1.7, 7.2)] + [fala(B, *b[i]) for i in (1, 2, 3, 5, 6, 7, 9)],
    broll=[[5.5, 10.05, K4, 2], [10.05, 12.45, K2, 3], [12.45, 16.5, K3, 1], [16.5, 19.4, K5, 1],
           [19.4, 20.4, BN1, 1], [20.4, 22.6, K1, 0]],
    textos=[{"de": 0, "ate": 5.5, "linhas": ["Deus te trouxe aqui, ajude", "o Pedrinho, os curativos",
                                             "dele estão acabando."],
             "estilo": "caixa", "bg": "branco", "fg": "preto", "size": 46, "y": 413, "pad": [26, 10], "lh": 1.08,
             "fonte": "medium"},
            {"de": 5.5, "ate": 22.6, "linhas": ["qualquer valor ajuda nos curativos,", "Deus te dê em dobro. ❤️"],
             "estilo": "caixa", "bg": "branco", "fg": "preto", "size": 42, "y": 432, "pad": [24, 10], "lh": 1.08,
             "fonte": "medium"}],
    legenda={"estilo": "pequena", "y": 1200, "size": 46, "contorno": 2},
    fim=dict(FIM_CTA, de=23.6, escuro=0.4),
    musica=mus("One_Last_Goodbye"), musica_volume=vol("One_Last_Goodbye", SOB_FALA))

# 10. Lar Leao de Juda 3420656938123702: citacao em faixas brancas por linha embaixo a esquerda (y 76%), com
#     "ACABANDO!" em destaque; depois faixa amarela por linha no alto (y 13%) e legenda condensada em caixa alta
#     com a falada em amarelo (y 66%).
planos["leao_de_juda_apelo"] = dict(
    ref=os.path.join(REF, "leaodejuda_3420656938123702.mp4"), estilo="BIB APELO",
    base=[fala(S1, 1.3, 2.0), fala(S1, 2.55, 9.3)] + [fala(A, *a[i]) for i in (1, 2, 3, 4, 5, 6, 7, 12)],
    broll=[[8.9, 12.5, K5, 2], [14.95, 18.65, K6, 3], [23.1, 24.85, K2, 5]],
    textos=[{"de": 0, "ate": 7.45, "linhas": ["Pedrinho faz um apelo", "desesperado: os curativos",
                                              "estão ACABANDO!"],
             "estilo": "caixa", "por_linha": True, "bg": "branco", "fg": "preto", "size": 50, "y": 1460,
             "alinha": "esq", "x": 95, "pad": [12, 0], "lh": 1.12, "fonte": "medium",
             "destaque": ["ACABANDO!"], "cor_destaque": [0, 105, 125]},
            {"de": 0, "ate": 7.45, "linhas": ["“"], "estilo": "caixa", "bg": [40, 160, 90], "fg": "branco",
             "size": 70, "fonte": "black", "y": 1335, "alinha": "esq", "x": 95, "pad": [16, 0], "lh": 0.8,
             "raio": 6},
            {"de": 7.45, "ate": 25.3, "linhas": ["Seja a resposta", "de Deus para o Pedrinho 🙏"], "estilo": "caixa",
             "por_linha": True, "bg": "amarelo", "fg": "preto", "size": 50, "y": 260, "pad": [14, 0],
             "lh": 1.08, "fonte": "medium"}],
    legenda={"estilo": "amarelo", "y": 1270, "size": 60},
    fim=dict(FIM_CTA, de=25.3, escuro=0.45),
    musica=mus("Faded_Ink"), musica_volume=vol("Faded_Ink", SOB_FALA))

for nome, pl in planos.items():
    pasta = os.path.join(PL, f"Pedrinho_bib_{nome}_v1")
    os.makedirs(os.path.join(pasta, "render"), exist_ok=True)
    f = os.path.join(pasta, "plano.json")
    antigo = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
    pl = dict(crianca="Pedrinho", **pl)
    if antigo.get("saida"):
        pl["saida"] = antigo["saida"]  # remontagem: mesmo PEB
    json.dump(pl, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    tot = sum(x["fim"] - x["ini"] for x in pl["base"])
    print(f"{nome}: {tot:.1f}s")
