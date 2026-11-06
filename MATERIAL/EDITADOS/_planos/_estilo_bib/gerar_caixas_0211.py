"""5 criativos do Pedrinho no estilo do AEB 35 (Caixas: pedido de tempo, um gancho so) com os brutos de 02/11/2026.
Pedido de 03/11/2026. Uso: python -I gerar_caixas_0211.py
Cortes = [inicio da 1a palavra, inicio da ultima] (o caixas.py completa ate o fim da palavra)."""
import json
import os

H = os.path.expanduser("~")
RAIZ = os.path.join(H, "Desktop", "EDIÇÃO COM CLAUDE")
PL = os.path.join(RAIZ, "EDITADOS", "_planos")
D = os.path.join(RAIZ, "VÍDEOS PARA EDITAR", "PEDRINHO 02-11-2026")
TX = os.path.join(H, ".claude", "estudio-ong", "CONHECIMENTO", "transcricoes", "pedrinho_0211")
CL = os.path.join(RAIZ, "banco de vídeos do pedrinho", "_clipes_bib")
MUS = os.path.join(RAIZ, "MÚSICAS", "alex-morgan-sad-piano-emotional-rain-story-575883.mp3")


def r(n):
    return os.path.join(D, n + ".mp4")


def tx(n):
    return os.path.join(TX, n + ".json")


A, B = "20261102_144645", "lv_0_20261102155438"
K1, K2, K3, K4, K5 = (r("20261102_" + x) for x in ("104706", "104943", "113535", "113735", "113918"))
BN1, BN2, BN3 = (os.path.join(CL, x) for x in ("bn1_curativos_cama_20s.mp4", "bn2_1760826007_92s.mp4",
                                                "bn3_1792347808_155s.mp4"))
VERMELHO = {"cor_caixa": [200, 16, 28], "cor_texto": [235, 40, 40]}

# falas do corpo (bruto, cortes)
F = {
    "deito": (A, [[1.60, 2.42], [3.52, 4.78]]),                      # Eu deito pra dormir e meu corpo todo doi
    "doi_muito": (A, [[5.76, 6.54]]),                                # E doi muito mesmo
    "pele": (A, [[10.42, 12.46], [13.32, 13.72], [14.48, 15.10], [16.00, 16.18]]),  # doenca rara, pele cheia de feridas
    "me_ajude": (A, [[19.76, 19.98], [20.78, 21.52], [22.76, 23.14]]),  # por favor, me ajude no tratamento dessa semana
    "dois_cinco_a": (A, [[26.98, 28.00]]),                           # dois ou cinco reais
    "pode_parecer": (A, [[31.80, 34.14], [34.96, 35.44], [36.30, 37.92]]),  # 5 reais pode parecer pouco... sem dor
    "dia_de_vida": (A, [[38.76, 40.14]]),                            # e mais um dia de vida
    "obrigado_a": (A, [[42.10, 42.40]]),                             # muito obrigado
    "bolhas": (B, [[1.74, 2.78], [3.62, 5.70]]),                     # doenca rara que faz surgir bolhas por todo o corpo
    "caro": (B, [[7.64, 9.54], [10.56, 11.02], [11.80, 14.02]]),     # tratamento caro, ameniza todas as minhas dores
    "muita_dor": (B, [[15.34, 16.56], [17.40, 18.00]]),              # eu tenho sentido muita, muita dor mesmo
    "ajude_b": (B, [[23.76, 23.98], [25.00, 25.74], [27.00, 27.38]]),  # por favor, ajude no tratamento dessa semana
    "dois_cinco_b": (B, [[28.48, 30.02], [32.32, 33.86]]),           # seja com dois ou cinco reais, assim ja vai ajudar
    "obrigado_b": (B, [[34.82, 35.66], [36.56, 36.72]]),             # e o meu muito obrigado, de coracao
}


def frase(nome, chave, cenas=None, take=False, final=False):
    bruto, cortes = F[chave]
    f = {"nome": nome, "fonte": r(bruto), "tx": tx(bruto), "cortes": cortes}
    if take:  # take dele falando na camera: um corte so, a cena no mesmo segundo, sem a caixa do alto
        f["cenas"] = [[r(bruto), round(cortes[0][0] - 0.06, 2)]]
        f["sem_topo"] = True
    else:
        f["cenas"] = [list(c) for c in cenas]
    if final:
        f["final"] = True
    return f


def gancho(bruto, a, b, verde, y):
    return {"nome": "h1", "fonte": r(bruto), "tx": tx(bruto), "cortes": [[a, b]], "cenas": [[r(bruto), round(a - 0.06, 2)]],
            "sem_caixas": True, "texto_verde": verde, "texto_verde_y": y}


V = {
    "Pedrinho_caixas_pedido_caixa_1500_v1": dict(
        gancho=gancho("20261102_152739", 2.38, 6.66, ["EU DEITO PRA DORMIR", "E MEU CORPO TODO DÓI"], 1310),
        corpo=[frase("c1", "pele", [(K4, 3), (K1, 2), (K3, 4), (K2, 1)]),
               frase("c2", "me_ajude", [(BN1, 0.5), (K5, 2)]),
               frase("c3", "dia_de_vida", take=True),
               frase("c4", "dois_cinco_a", [(K2, 6), (BN2, 1)], final=True)],
        topo=["PEDRINHO TEM EPIDERMÓLISE BOLHOSA E PRECISA DE", "CURATIVOS PARA ALIVIAR AS DORES"],
        valor_linhas=["DEIXAM O PEDRINHO MAIS PERTO DE COMPRAR", "OS CURATIVOS DESSA SEMANA"], cor={}),
    "Pedrinho_caixas_pedido_trinta_segundos_v1": dict(
        gancho=gancho("20261102_152542", 1.38, 6.12, ["EU TENHO SENTIDO MUITA,", "MUITA DOR MESMO"], 1310),
        corpo=[frase("c1", "bolhas", [(K4, 12), (K3, 8), (K1, 5)]),
               frase("c2", "caro", [(K2, 2), (BN1, 2), (K5, 5), (K4, 22)]),
               frase("c3", "muita_dor", take=True),
               frase("c4", "dois_cinco_b", [(K3, 1), (BN3, 1), (K1, 0)], final=True)],
        topo=["PEDRINHO TEM UMA DOENÇA RARA E PRECISA DE", "CURATIVOS QUE AMENIZAM AS DORES"],
        valor_linhas=["AJUDAM O PEDRINHO A COMPRAR", "UMA CAIXA DE CURATIVOS"], cor={}),
    "Pedrinho_caixas_pedido_curativos_acabando_v1": dict(
        gancho=gancho("20261102_151715", 1.82, 6.72, ["MINHA PELE É TODA", "CHEIA DE FERIDAS"], 1420),
        corpo=[frase("c1", "deito", [(K1, 3), (K4, 6), (K3, 10)]),
               frase("c2", "pode_parecer", [(K2, 4), (BN1, 1), (K5, 1), (K4, 25)]),
               frase("c3", "doi_muito", take=True),
               frase("c4", "dois_cinco_a", [(BN2, 9), (K3, 5)], final=True)],
        topo=["OS CURATIVOS DO PEDRINHO ESTÃO ACABANDO E", "UMA CAIXA CUSTA R$1.500"],
        valor_linhas=["DEIXAM O PEDRINHO MAIS PERTO DE", "MAIS UM DIA SEM DOR"], cor=VERMELHO),
    "Pedrinho_caixas_pedido_eu_te_peco_v1": dict(
        gancho=gancho("20261102_152631", 1.24, 5.74, ["MAS É ELE QUE FAZ AMENIZAR", "TODAS AS MINHAS DORES"], 1310),
        corpo=[frase("c1", "muita_dor", [(K5, 3), (K2, 7)]),
               frase("c2", "ajude_b", [(K4, 15), (K1, 6)]),
               frase("c3", "bolhas", take=True),
               frase("c4", "dois_cinco_b", [(BN1, 2), (K3, 11), (BN2, 1)], final=True)],
        topo=["PEDRINHO TEM EPIDERMÓLISE BOLHOSA E PRECISA DE", "AJUDA NO TRATAMENTO DESSA SEMANA"],
        valor_linhas=["JÁ AJUDAM MUITO NO", "TRATAMENTO DO PEDRINHO"], cor={}),
    "Pedrinho_caixas_pedido_chegou_ate_aqui_v1": dict(
        gancho=gancho("20261102_153323", 1.38, 7.58, ["PRA MIM É SEMPRE", "MAIS UM DIA SEM DOR"], 1310),
        corpo=[frase("c1", "bolhas", [(K3, 2), (K4, 9), (BN1, 3)]),
               frase("c2", "caro", [(K1, 1), (K5, 8), (K2, 9), (K4, 19)]),
               frase("c3", "me_ajude", take=True),
               frase("c4", "dois_cinco_b", [(BN3, 0.5), (K2, 0.5), (K3, 12)], final=True)],
        topo=["PEDRINHO TEM BOLHAS POR TODO O CORPO E PRECISA DE", "CURATIVOS PARA ALIVIAR AS DORES"],
        valor_linhas=["SÃO MAIS UM DIA SEM DOR", "PARA O PEDRINHO"], cor=VERMELHO),
}

for nome, v in V.items():
    vr = {"topo": v["topo"], "topo_y": 240, "valor": "R$5,00", "valor_linhas": v["valor_linhas"], "valor_y": 1300}
    vr.update(v["cor"])
    p = {"nome": nome, "skill": "criativo-caixas-pedido-ong", "crianca": "Pedrinho",
         "gancho": "pedido de tempo com a placa (brutos de 02/11/2026)", "musica": MUS, "musica_volume": 0.09,
         "modelo": "estrutura do AEB 35 (um gancho so, sem_caixas) da skill criativo-caixas-pedido-ong",
         "fatos": {"falas e placas": "Pedrinho, VÍDEOS PARA EDITAR\\PEDRINHO 02-11-2026 (gravados em 02/11/2026)",
                   "caixa de curativos R$1.500": "placa do 20261102_152739",
                   "R$5": "ele fala 'dois ou cinco reais' (144645 e lv_0)"},
         "frases": [v["gancho"]] + v["corpo"], "visual_ref": vr, "sem_legenda": True}
    pasta = os.path.join(PL, nome)
    os.makedirs(pasta, exist_ok=True)
    f = os.path.join(pasta, "plano.json")
    if os.path.exists(f):
        old = json.load(open(f, encoding="utf-8"))
        if old.get("saida"):
            p["saida"] = old["saida"]
    json.dump(p, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(nome)
