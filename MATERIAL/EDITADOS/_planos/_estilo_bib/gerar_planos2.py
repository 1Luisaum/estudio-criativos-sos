"""Planos da 2a demanda das bibliotecas (03/11/2026): um criativo do Pedrinho para cada um dos 14 anuncios do Doc
"LEVA 01/02/03", com a MUSICA DO PROPRIO ANUNCIO (as que deram certo). Anuncio so com musica: o audio inteiro dele.
Anuncio com fala: a musica separada da voz (separar_musica.py, Demucs). LEVA 02 usa imagens geradas na Magnific
(imagens\\) e narracao do Leonardo (narracoes\\). Uso: python -I gerar_planos2.py"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
try:
    RAIZ = json.load(open(os.path.join(os.path.expanduser("~"), ".claude", "estudio-ong.json"), encoding="utf-8-sig"))["raiz"]
except (OSError, ValueError, KeyError):
    RAIZ = os.path.join(os.path.expanduser("~"), "Desktop", "EDIÇÃO COM CLAUDE")
D = os.path.join(RAIZ, "VÍDEOS PARA EDITAR", "PEDRINHO 02-11-2026")
CL = os.path.join(RAIZ, "banco de vídeos do pedrinho", "_clipes_bib")
REF = os.path.join(RAIZ, "EDITADOS", "_referencias", "bibliotecas")
MB = os.path.join(RAIZ, "MÚSICAS", "ANÚNCIOS QUE DERAM CERTO")  # musicas dos anuncios, com indice musicas.json
PL = os.path.join(RAIZ, "EDITADOS", "_planos")
IMG, NAR = os.path.join(AQUI, "imagens"), os.path.join(AQUI, "narracoes")


def r(n):
    return os.path.join(D, n + ".mp4")


A, B = r("20261102_144645"), r("lv_0_20261102155438")
P1, P3 = r("20261102_151540"), r("20261102_151715")
S1, S2, S3, S4 = r("20261102_152542"), r("20261102_152631"), r("20261102_152739"), r("20261102_153323")
K1, K2, K3, K4, K5, K6 = (r(x) for x in ("20261102_104706", "20261102_104943", "20261102_113535", "20261102_113735",
                                         "20261102_113918", "20261102_114148"))
BN1, BN2, BN3 = (os.path.join(CL, x) for x in ("bn1_curativos_cama_20s.mp4", "bn2_1760826007_92s.mp4",
                                                "bn3_1792347808_155s.mp4"))
a = {1: (1.50, 2.95), 2: (3.45, 7.05), 3: (10.35, 12.85), 4: (13.25, 16.95), 5: (19.00, 22.40), 6: (22.70, 23.70),
     7: (26.90, 28.65), 8: (31.70, 34.55), 9: (34.90, 38.25), 11: (38.70, 40.60), 12: (41.00, 43.00)}
FIM_CTA = {"linhas": ["CLIQUE EM", "SAIBA MAIS"], "cor": "vermelho", "size": 70, "escuro": 0.45}


def ref(n):
    return os.path.join(REF, n + ".mp4")


IDX = {m["anuncio"].rsplit("=", 1)[1]: m for m in json.load(open(os.path.join(MB, "musicas.json"), encoding="utf-8"))}


def mus(n, separada=False):
    """Musica do anuncio pelo numero da biblioteca (ex.: 'maosamigas_1342577441148988')."""
    return os.path.join(MB, IDX[n.rsplit("_", 1)[1]]["arquivo"])


def volm(n):
    return IDX[n.rsplit("_", 1)[1]]["volume"]


def fala(arq, ini, fim, **k):
    return dict(arq=arq, ini=ini, fim=fim, som=True, **k)


def mudo(arq, ini, fim, **k):
    return dict(arq=arq, ini=ini, fim=fim, som=False, **k)


def vid_ia(nome, dur):
    """Video gerado na Magnific (Kling 2.5) a partir da imagem simbolica."""
    return dict(arq=os.path.join(AQUI, "videos_ia", nome + ".mp4"), ini=0, fim=dur, som=False)


def img(nome, dur):
    return dict(arq=os.path.join(IMG, nome + ".png"), ini=0, fim=dur, som=False, kb=True)


def voz(nome, de=0.2):
    return {"arq": os.path.join(NAR, nome + "_sr.mp3"), "tx": os.path.join(NAR, nome + "_sr.json"), "de": de}


planos = {}

# ---------------- LEVA 01 (Lar Maos Amigas): so musica, cenas de ~3 s, um texto fixo
# 1342577441148988: faixas brancas por linha com letra preta, embaixo (y 72%)
planos["l1_esqueceram"] = dict(
    ref=ref("maosamigas_1342577441148988"), estilo="BIB L1 ESQUECERAM",
    base=[mudo(K6, 0.5, 3.5, pb=True), mudo(S1, 3, 6), mudo(K4, 5, 8), mudo(P3, 2, 5), mudo(K1, 2, 5), mudo(K2, 3, 6),
          mudo(S3, 4, 7), mudo(K5, 1, 4), mudo(K3, 4, 7.5)],
    textos=[{"de": 0, "ate": 25.5, "linhas": ["esqueceram do Pedrinho? 💔", "os curativos dele estão acabando",
                                               "e uma caixa custa R$1.500 😭"],
             "estilo": "caixa", "por_linha": True, "bg": "branco", "fg": "preto", "size": 44, "y": 1370,
             "pad": [14, 0], "lh": 1.1}],
    fim=dict(FIM_CTA, de=25.5), musica=mus("maosamigas_1342577441148988"), musica_volume=1.0)

# 2241390946718073: versiculo pequeno no alto (y 12%) e frase pequena embaixo (y 72%)
planos["l1_mateus"] = dict(
    ref=ref("maosamigas_2241390946718073"), estilo="BIB L1 MATEUS",
    base=[mudo(K4, 10, 13), mudo(BN1, 0, 3), mudo(K1, 4, 7), mudo(K3, 8, 11), mudo(K2, 6, 9), mudo(P1, 3, 6),
          mudo(K5, 5, 8), mudo(BN3, 0, 2)],
    textos=[{"de": 0, "ate": 21, "linhas": ["Mateus 25:35-40", "ensina que servir aos necessitados",
                                             "é servir a Cristo."], "estilo": "seco", "size": 34, "y": 240,
             "contorno": 3, "lh": 1.1},
            {"de": 0, "ate": 21, "linhas": ["5 reais ajudam nos curativos", "do Pedrinho ❤️"], "estilo": "seco",
             "size": 34, "y": 1395, "contorno": 3, "lh": 1.1}],
    fim=dict(FIM_CTA, de=21), musica=mus("maosamigas_2241390946718073"), musica_volume=1.0)

# 1126949516397141: letra branca grossa com contorno no meio (y 63%)
planos["l1_cansados"] = dict(
    ref=ref("maosamigas_1126949516397141"), estilo="BIB L1 PEDIR AJUDA",
    base=[mudo(K2, 0, 3), mudo(K4, 14, 17), mudo(A, 10.4, 13.4), mudo(K6, 10, 13), mudo(S4, 3, 6), mudo(K1, 0, 3),
          mudo(K5, 7, 10), mudo(P1, 5, 8), mudo(K3, 1, 4.5)],
    textos=[{"de": 0, "ate": 25.5, "linhas": ["Os curativos do Pedrinho", "estão acabando,", "a gente precisa muito",
                                               "da sua ajuda 😭💔"], "estilo": "seco", "size": 52, "y": 1210,
             "contorno": 4, "lh": 1.1}],
    fim=dict(FIM_CTA, de=25.5), musica=mus("maosamigas_1126949516397141"), musica_volume=1.0)

# 907048145709918: letra branca com contorno (y 66%) e faixa azul "5 reais ja fazem a diferenca" (y 77%)
planos["l1_mais_um_dia"] = dict(
    ref=ref("maosamigas_907048145709918"), estilo="BIB L1 MAIS UM DIA",
    base=[mudo(S2, 1, 4), mudo(K4, 18, 21), mudo(K1, 5, 8), mudo(B, 15, 18), mudo(K3, 10, 13), mudo(K6, 15, 18),
          mudo(K2, 8, 11), mudo(BN2, 2, 5), mudo(K5, 3, 6.5)],
    textos=[{"de": 0, "ate": 25.5, "linhas": ["Mais um dia postando porque", "os curativos do Pedrinho",
                                               "estão acabando 💔"], "estilo": "seco", "size": 46, "y": 1275,
             "contorno": 4, "lh": 1.08},
            {"de": 0, "ate": 25.5, "linhas": ["5 reais já fazem a diferença"], "estilo": "caixa",
             "bg": [24, 70, 215], "fg": "branco", "size": 40, "y": 1480, "pad": [16, 4]}],
    fim=dict(FIM_CTA, de=25.5), musica=mus("maosamigas_907048145709918"), musica_volume=1.0)


def de_plano(pasta, **troca):
    """Copia um plano ja aprovado (PEB 204/207/208) trocando so o que muda (a musica)."""
    p = json.load(open(os.path.join(PL, pasta, "plano.json"), encoding="utf-8"))
    for k in ("saida", "crianca", "musica_depois"):
        p.pop(k, None)
    p.update(troca)
    return p


# 1961085214849293: mesmo molde do PEB 208, com a musica do anuncio
planos["l1_compartilhe"] = de_plano("Pedrinho_bib_maos_amigas_compartilhe_v1", estilo="BIB L1 COMPARTILHE",
                                    musica=mus("maosamigas_1961085214849293"), musica_volume=1.0)

# ---------------- LEVA 02 (Lar Mae Ritinha)
# 931067246550453: mesmo molde do PEB 207, com a musica do anuncio (separada da voz)
planos["l2_viralizou"] = de_plano("Pedrinho_bib_mae_ritinha_viralizou_v1", estilo="BIB L2 VIRALIZOU",
                                  musica=mus("maeritinha_931067246550453", True), musica_volume=volm("maeritinha_931067246550453"))

# 1403709941748846: imagens de IA no gancho (leao, Jesus), narracao, caixa branca no alto, legenda pequena
planos["l2_oracoes"] = dict(
    ref=ref("maeritinha_1403709941748846"), estilo="BIB L2 SEU SINAL",
    base=[vid_ia("leao", 5), vid_ia("jesus", 5), mudo(K4, 3, 6.5), mudo(K1, 2, 5.5), mudo(S1, 3, 6), mudo(K3, 4, 7.5),
          mudo(K5, 2, 5), mudo(P3, 3, 6), mudo(K2, 5, 8), mudo(B, 8, 13)],  # imagens viraram video (03/11)
    voz=voz("n_1403_oracoes", 0.3),
    textos=[{"de": 12, "ate": 34.8, "linhas": ["esse é o seu sinal para fazer", "uma boa ação hoje ❤️"],
             "estilo": "caixa", "bg": "branco", "fg": "preto", "size": 34, "y": 140, "pad": [16, 8],
             "fonte": "serif_bold", "lh": 1.1}],
    legenda={"estilo": "amarelo", "y": 1500, "size": 38, "fonte": "bold", "caixa_alta": False, "contorno": 3},
    fim=dict(FIM_CTA, de=34.8), musica=mus("maeritinha_1403709941748846", True), musica_volume=volm("maeritinha_1403709941748846"))

# 1433775218854991: so musica, faixas pretas com letra branca serifada no alto, caixa branca, faixa vermelha
planos["l2_toque"] = dict(
    ref=ref("maeritinha_1433775218854991"), estilo="BIB L2 DEUS TOQUE",
    base=[mudo(K4, 20, 23), mudo(K1, 0, 3), mudo(K3, 0, 3), mudo(K5, 6, 9), mudo(P1, 0.5, 3.5), mudo(K2, 0, 3),
          mudo(BN1, 1, 4), mudo(BN2, 9, 12), mudo(P3, 4.5, 7.5)],
    textos=[{"de": 0, "ate": 25, "linhas": ["Que Deus toque seu coração e não deixe", "faltar ajuda para o Pedrinho!",
                                             "Cada gesto de amor faz a diferença! 😊❤️"], "estilo": "caixa",
             "por_linha": True, "bg": "preto", "fg": "branco", "size": 36, "y": 260, "fonte": "serif",
             "pad": [10, 0], "lh": 1.12},
            {"de": 0, "ate": 25, "linhas": ["Doe R$ 5,00 e ajude nos curativos."], "estilo": "caixa", "bg": "branco",
             "fg": "preto", "size": 34, "y": 440, "fonte": "serif", "pad": [12, 4]},
            {"de": 0, "ate": 25, "linhas": ["👇 Clique em SAIBA MAIS"], "estilo": "caixa", "bg": [225, 20, 30],
             "fg": "branco", "size": 34, "y": 1325, "fonte": "serif", "pad": [12, 4]}],
    fim=dict(FIM_CTA, de=25), musica=mus("maeritinha_1433775218854991"), musica_volume=1.0)

# 1289222076667000: faixa preta "Dai, e vos sera dado - Lucas 6:38", depois texto amarelo no alto e legenda com a
# palavra falada em verde; narracao
planos["l2_lucas"] = dict(
    ref=ref("maeritinha_1289222076667000"), estilo="BIB L2 LUCAS",
    # abre com ele sentado no cobertor azul, em cor; nada em P&B (pedidos de 03/11)
    base=[mudo(BN2, 0.5, 4), mudo(K4, 0, 3.5), mudo(K1, 0, 3.5), mudo(K2, 0, 3.5), mudo(K3, 0, 3.5),
          mudo(P1, 0, 3.5), mudo(K6, 9, 12.5), mudo(K5, 0, 3.5), mudo(BN1, 0, 3.5), mudo(BN3, 0, 3.5),
          mudo(S4, 3, 6.5)],
    voz=voz("n_1289_lucas", 0.3),
    textos=[{"de": 0, "ate": 5.8, "linhas": ["Dai, e vos será dado – Lucas 6:38"], "estilo": "caixa", "bg": "preto",
             "fg": "branco", "size": 40, "y": 300, "pad": [16, 6], "destaque": ["Lucas", "6:38"],
             "cor_destaque": [120, 200, 255]},
            {"de": 5.8, "ate": 34.8, "linhas": ["Doe R$5 e faça parte", "dessa missão de amor 🙏"], "estilo": "seco",
             "fg": "amarelo", "size": 44, "y": 355, "contorno": 2, "lh": 1.05}],
    legenda={"estilo": "amarelo", "y": 1290, "size": 50, "fonte": "bold", "caixa_alta": False, "contorno": 3,
             "cor": [40, 210, 70]},
    fim=dict(FIM_CTA, de=34.8), musica=mus("maeritinha_1289222076667000", True), musica_volume=volm("maeritinha_1289222076667000"))

# 1658330079039610: gancho com a Biblia (IA, no lugar do homem falando no carro) e o versiculo em amarelo; depois
# caixa rosa "DOE ... e AJUDE" no alto e legenda pequena; narracao
planos["l2_conselho"] = dict(
    ref=ref("maeritinha_1658330079039610"), estilo="BIB L2 CONSELHO",
    base=[img("biblia", 4), mudo(K4, 5, 8), mudo(P3, 0.5, 3.5), mudo(K3, 6, 9), mudo(K1, 3, 6), mudo(K2, 2, 5),
          mudo(BN3, 1, 4)],
    voz=voz("n_1658_conselho", 0.2),
    textos=[{"de": 0, "ate": 4, "linhas": ["Dai, e vos será dado – Lucas 6:38"], "estilo": "seco", "fg": "amarelo",
             "size": 44, "y": 220, "contorno": 3},
            {"de": 4, "ate": 19.8, "linhas": ["DOE 5 reais", "e AJUDE O PEDRINHO 💗"], "estilo": "caixa",
             "bg": [255, 214, 226], "fg": [60, 20, 40], "size": 46, "y": 310, "fonte": "serif_bold", "pad": [18, 6],
             "lh": 1.08}],
    legenda={"estilo": "pequena", "y": 1380, "size": 38, "contorno": 2},
    fim=dict(FIM_CTA, de=19.8), musica=mus("maeritinha_1658330079039610", True), musica_volume=volm("maeritinha_1658330079039610"))

# ---------------- LEVA 03
# Florisbela 1445110604492533: so musica, 4 tomadas longas (~6 s), letra preta com contorno branco no alto,
# frase branca em caixa escura no meio
planos["l3_sinal_que_faltava"] = dict(
    ref=ref("florisbela_1445110604492533"), estilo="BIB L3 SINAL QUE FALTAVA",
    base=[mudo(P3, 1, 7), mudo(K4, 0, 6), mudo(K1, 2, 8), mudo(K3, 4, 10)],  # comeca pelo 2o take (pedido 03/11)
    textos=[{"de": 0, "ate": 21.5, "linhas": ["Talvez este seja o sinal", "que faltava:"], "estilo": "seco",
             "fg": "vermelho", "cor_contorno": "branco", "size": 60, "y": 300, "contorno": 3, "lh": 1.05},
            {"de": 0, "ate": 21.5, "linhas": ["doe R$ 5,00 e ajude o", "Pedrinho! 🙏❤️"], "estilo": "caixa",
             "bg": [0, 0, 0, 150], "fg": "branco", "size": 44, "y": 1400, "pad": [14, 4], "raio": 8, "lh": 1.1}],
    fim=dict(FIM_CTA, de=21.5), musica=mus("florisbela_1445110604492533"), musica_volume=1.0)

# Florisbela 2388547078640410: mesmo molde do PEB 204, com a musica do anuncio (separada da voz)
planos["l3_deus_te_trouxe"] = de_plano("Pedrinho_bib_florisbela_30_segundos_v1", estilo="BIB L3 DEUS TE TROUXE",
                                       musica=mus("florisbela_2388547078640410", True), musica_volume=volm("florisbela_2388547078640410"))

# Leao de Juda 29061162426836111: gancho curto com faixa branca e barra ("Urgente!!"), depois ele falando direto
# com faixas pretas por linha no alto em letra condensada; musica do anuncio por baixo
planos["l3_urgente"] = dict(
    ref=ref("leaodejuda_29061162426836111"), estilo="BIB L3 URGENTE",
    base=[mudo(K6, 0.5, 3.0, pb=True)] + [fala(A, *a[i]) for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12)],
    textos=[{"de": 0, "ate": 2.5, "linhas": ["Urgente!! Os curativos do", "Pedrinho estão acabando 😢"],
             "estilo": "caixa", "por_linha": True, "barra": True, "bg": "branco", "fg": "preto", "size": 48,
             "y": 1355, "alinha": "esq", "x": 70, "pad": [12, 0], "lh": 1.12, "fonte": "medium"},
            {"de": 2.5, "ate": 28.0, "linhas": ["COM APENAS R$5,00", "VOCÊ AJUDA NOS CURATIVOS", "DO PEDRINHO"],
             "estilo": "caixa", "por_linha": True, "bg": "preto", "fg": "branco", "size": 50, "y": 280,
             "fonte": "impact", "pad": [12, 0], "lh": 1.08}],
    fim=dict(FIM_CTA, de=28.0),  # a musica separada do anuncio ficou bugada (03/11): Magnific triste
    musica=os.path.join(RAIZ, "MÚSICAS", "magnific_tristes", "Fading_Ember.mp3"), musica_volume=0.18)

# Mae Ritinha 1629309275506783: so musica, "POV:" em caixa preta com letra serifada no meio
planos["l3_pov"] = dict(
    ref=ref("maeritinha_1629309275506783"), estilo="BIB L3 POV",
    base=[mudo(K4, 8, 11), mudo(K1, 0, 3), mudo(K3, 9, 12), mudo(K5, 0, 3), mudo(K2, 3, 6), mudo(BN1, 0, 3),
          mudo(K6, 3, 6.5)],
    textos=[{"de": 0, "ate": 19.5, "linhas": ["POV: seus 5 reais acabaram", "de virar curativo ❤️"],
             "estilo": "caixa", "bg": "preto", "fg": "branco", "size": 44, "y": 920, "fonte": "serif",
             "pad": [16, 6], "lh": 1.12}],
    fim=dict(FIM_CTA, de=19.5), musica=mus("maeritinha_1629309275506783"), musica_volume=1.0)

# volume das musicas separadas: a faixa fica a -27 LUFS por baixo da fala (medido depois da separacao)
for nome, pl in planos.items():
    pasta = os.path.join(PL, f"Pedrinho_bib2_{nome}_v1")
    os.makedirs(os.path.join(pasta, "render"), exist_ok=True)
    f = os.path.join(pasta, "plano.json")
    antigo = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
    pl = dict(crianca="Pedrinho", **pl)
    if antigo.get("saida"):
        pl["saida"] = antigo["saida"]  # remontagem: mesmo PEB
    json.dump(pl, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    tot = sum(x["fim"] - x["ini"] for x in pl["base"])
    print(f"{nome}: {tot:.1f}s")
