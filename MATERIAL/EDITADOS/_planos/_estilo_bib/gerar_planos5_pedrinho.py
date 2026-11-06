"""Os 12 modelos novos da Adrielly (AEB 91-102, 05/11/2026) refeitos para o Pedrinho, com as gravacoes de 02/11,
videos de IA novos da Magnific (sem animais, igreja catolica), feridas com borrao leve, legenda UNICEF, caixa vermelha,
sem P&B e poucos takes dele falando. Pedido do usuario de 05/11/2026.
Imagens de IA: tem de parecer cristas (cruz, crucifixo, Biblia, terco, igreja); poucas velas (muitas pareceram
umbanda), nada de plantacoes, plantas ou animais.
Copy nova so com fatos reais: falas de 02/11 (20261102_144645, lv_0_20261102155438) e as placas (R$1.500, acabando).
Uso: python -I gerar_planos5_pedrinho.py [--so-imagens] [nomes...]"""
import base64
import copy
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.request
import winreg

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(os.path.expanduser("~"), ".claude", "skills", "criativo-bibliotecas-ong")
sys.path.insert(0, os.path.join(SK, "scripts"))
import comum as C  # noqa: E402

RAIZ = C.raiz()
PL = os.path.join(RAIZ, "EDITADOS", "_planos")
REND = os.path.join(RAIZ, "EDITADOS", "RENDERIZADOS")
IMG, NAR, VID = os.path.join(AQUI, "imagens"), os.path.join(AQUI, "narracoes"), os.path.join(AQUI, "videos_ia")
D = os.path.join(RAIZ, "VÍDEOS PARA EDITAR", "PEDRINHO 02-11-2026")
CP = os.path.join(PL, "_clipes_pedrinho")
BN = os.path.join(RAIZ, "banco de vídeos do pedrinho", "_clipes_bib")
TRANSCREVER = os.path.expanduser(r"~\.claude\skills\criativo-reportagem-ong\scripts\transcrever.py")


def r(n):
    return os.path.join(D, n + ".mp4")


def cena(arq, ini, fim, **k):
    return dict(arq=arq, ini=ini, fim=fim, som=False, **k)


FOTOS = [os.path.join(CP, f"foto_ferida_{n}.mp4") for n in (
    "rosto_feridas", "peito_bracos", "bracos_curativo", "braco_estendido", "pescoco", "perna_curativo",
    "sentado_feridas", "perna_close", "pe_tornozelo", "rosto_faixas", "braco_faixa", "costas", "costas_inteiras",
    "bracos_close")]
VIDS = [(r("20261102_104706"), 0.5), (r("20261102_114148"), 2.0), (r("20261102_113735"), 8.0),
        (r("20261102_114148"), 12.0), (r("20261102_104706"), 4.5), (os.path.join(BN, "bn1_curativos_cama_20s.mp4"), 2.0),
        (r("20261102_113535"), 6.0), (os.path.join(BN, "bn3_1792347808_155s.mp4"), 20.0)]
FALA = [(r("20261102_144645"), 6.0), (r("lv_0_20261102155438"), 12.0), (r("20261102_152542"), 3.0),
        (r("20261102_152739"), 3.0), (r("20261102_151540"), 2.0), (r("20261102_153323"), 3.0)]
MAE = (r("20261102_104706"), 0.3)  # a mae fazendo o curativo

NEG = "text, letters, watermark, person, human face, animal, bird, dog, cat, lamb, dove, distortion, morphing, blur"
IMAGENS = {
    "p_sacrario": "A golden Catholic tabernacle on a white marble altar, two tall white candles burning beside it, a "
                  "red sanctuary lamp glowing, soft warm light in a quiet church, no people, photorealistic, cinematic, "
                  "vertical composition",
    "p_nave_manha": "Interior of an empty traditional Catholic church in the early morning, sunlight beams from high "
                    "windows across wooden pews toward a crucifix above the altar, no people, reverent and hopeful, "
                    "photorealistic, cinematic, vertical composition",
    "p_biblia_terco": "An open Bible on a rustic wooden table by a window at sunrise, a wooden rosary with a small "
                      "crucifix resting on the pages, warm soft light, no people, photorealistic, cinematic, vertical "
                      "composition",
    "p_nossa_senhora": "A serene statue of Our Lady (Virgin Mary) in a Catholic chapel, many small white candles "
                       "burning at her feet, soft blue and golden light, no people, photorealistic, cinematic, vertical "
                       "composition",
    "p_terco_travesseiro": "A light blue rosary resting on a small white pillow on a child's bed, gentle morning light "
                           "through a curtain, peaceful and tender, no people, photorealistic, cinematic, vertical "
                           "composition",
    "p_vitral_pastor": "A colorful Catholic stained glass window with a golden cross and radiant light rays, no "
                       "figures, no animals, warm sunlight shining through it and casting colors on stone walls, no people, photorealistic, cinematic, "
                       "vertical composition",
    "p_velas_vermelhas": "Rows of red votive candles in glass holders burning in a Catholic church in front of a "
                         "wooden crucifix, warm glow, soft bokeh, no people, photorealistic, cinematic, vertical "
                         "composition",
    "p_mudas_sol": "A small young green plant sprouting from soil in a simple clay pot standing on a wooden windowsill, "
                   "golden sunrise light coming through the window, dew drops on the leaves, upright, vertical portrait "
                   "framing, hopeful, no people, photorealistic, cinematic, vertical composition",
    "p_biblia_banco_igreja": "An old open Bible resting on a wooden church pew in a Catholic church, soft light from "
                             "stained glass windows, a crucifix blurred in the background, no people, photorealistic, "
                             "cinematic, vertical composition",
    "p_nossa_senhora2": "A serene white statue of Our Lady (Virgin Mary) with praying hands in a Catholic church, soft "
                        "daylight from a window, a wooden crucifix on the wall behind, no candles, no people, reverent, "
                        "photorealistic, cinematic, vertical composition",
    "p_crucifixo_parede": "A large wooden crucifix hanging on the white wall of a Catholic church, soft warm daylight "
                          "from a side window, stained glass colors on the wall, no candles, no people, reverent, "
                          "photorealistic, cinematic, vertical composition",
    "p_biblia_cruz_janela": "An open Bible on a wooden windowsill at sunrise with a small wooden cross standing beside "
                            "it, soft golden light, no candles, no plants, no people, Christian and hopeful, "
                            "photorealistic, cinematic, vertical composition",
    "a_capela_colina": "A small white Christian chapel with a cross on its roof on a green hill at sunrise, soft "
                       "clouds and golden light, no people, peaceful and hopeful, photorealistic, cinematic, vertical "
                       "composition",
    "a_capela_altar_biblia": "Interior of a small simple Christian chapel, a wooden altar with an open Bible and a "
                             "wooden cross on it, soft morning light from a window, no candles, no people, "
                             "photorealistic, cinematic, vertical composition",
}
MOVIMENTO = {
    "p_sacrario": "the candle flames flicker gently, the red lamp glows softly, very slow push-in toward the tabernacle",
    "p_nave_manha": "sunbeams slowly move across the pews, dust particles float in the light, slow push-in toward the altar",
    "p_biblia_terco": "the sunlight slowly grows over the pages, a page lifts slightly in a soft breeze, gentle push-in",
    "p_nossa_senhora": "the candle flames flicker softly, warm light breathes on the statue, very slow push-in",
    "p_terco_travesseiro": "soft morning light slowly moves across the pillow, the curtain sways gently, slow push-in",
    "p_vitral_pastor": "the colored light shifts slowly on the stone walls, dust floats in the beams, slow push-in",
    "p_velas_vermelhas": "the candle flames flicker gently, warm glow pulses softly, slow push-in toward the crucifix",
    "p_mudas_sol": "the little plant leaves move slightly, dew drops shimmer, sunlight slowly grows, gentle push-in",
    "p_biblia_banco_igreja": "colored light slowly moves across the Bible pages, dust particles float, slow push-in",
    "p_nossa_senhora2": "soft daylight slowly moves over the statue, dust particles float, very slow push-in",
    "p_crucifixo_parede": "the colored light slowly shifts on the wall, very slow push-in toward the crucifix",
    "p_biblia_cruz_janela": "the sunrise light slowly grows over the Bible pages, a page lifts slightly, gentle push-in",
    "a_capela_colina": "clouds drift slowly, the sun rises behind the chapel, the grass sways gently, slow push-in",
    "a_capela_altar_biblia": "morning light slowly moves across the altar and the Bible, dust floats, slow push-in",
}
CAIXA_VERM = dict(estilo="caixa", bg="vermelho", fg="branco", size=50, y=185, fonte="black", pad=[28, 10], lh=1.15,
                  raio=16, sombra_caixa=True)

V = {
    "oracoes_dor": dict(
        tpl="Adrielly_bib_oracoes_v1", imgs=["p_sacrario", "p_nave_manha"], caixa=["Deus vê cada dor", "que ninguém vê ❤️"],
        texto="Tem orações que a gente faz em silêncio, antes de dormir. O Pedrinho conta que, quando deita pra dormir, "
              "o corpo todo dói, e dói muito. Ele tem uma doença rara, e a pele dele é toda cheia de feridas. O "
              "tratamento é caro, mas é ele que ameniza as dores. E os curativos estão acabando. Se você pode ajudar "
              "com dois ou cinco reais, ajude hoje. Que Deus abençoe a sua casa.",
        fatos={"corpo todo doi ao deitar": "20261102_144645 1,6-7,0", "doenca rara, pele cheia de feridas": "20261102_144645 10,4-16,9",
               "tratamento caro que ameniza as dores": "lv_0_20261102155438 7,6-14,4", "curativos acabando": "placa 20261102_151715/152542",
               "dois ou cinco reais": "20261102_144645 19,1-28,6"}),
    "conselho_salmo": dict(
        tpl="Adrielly_bib_conselho_v1", imgs=["p_biblia_terco"],
        versiculo=["Bem-aventurado é aquele que", "atende ao pobre – Salmos 41:1"], caixa=["DOE 2 reais", "e AJUDE O PEDRINHO 💗"],
        texto="Presta atenção nesse conselho. A Bíblia diz: bem-aventurado é aquele que atende ao pobre. O Pedrinho "
              "precisa de quem atenda hoje. As feridas dele aumentaram, estão em carne viva, e ele tem sentido muita "
              "dor. Uma caixa de curativos custa mil e quinhentos reais, e eles estão acabando. Doe dois reais e ajude "
              "o Pedrinho. Que Deus te abençoe.",
        fatos={"feridas aumentaram, carne viva, muita dor": "lv_0_20261102155438 15,3-23,3",
               "caixa de curativos R$1.500": "placa 20261102_152739", "curativos acabando": "placa 20261102_151715/152542",
               "R$2": "placa 20261102_151635/152631"}),
    "lucas_dia_de_vida": dict(
        tpl="Adrielly_bib_lucas_v1", imgs=[],
        texto="Lucas, capítulo seis, versículo trinta e oito: dai, e vos será dado. Quem dá com amor nunca fica sem. "
              "Hoje o pedido é para o Pedrinho. Ele tem epidermólise bolhosa, uma doença rara que faz surgir bolhas "
              "pelo corpo todo. Ele mesmo diz que cinco reais pode parecer pouco, mas, pra ele, é mais um dia sem dor "
              "e mais um dia de vida. Doe o que puder e faça parte dessa missão de amor. Que Deus multiplique na sua vida.",
        fatos={"doenca rara que faz surgir bolhas": "lv_0_20261102155438 1,7-6,1",
               "cinco reais = mais um dia sem dor e de vida": "20261102_144645 31,8-40,5"}),
    "oracoes_mae": dict(
        tpl="Adrielly_bib4_oracoes_mae_v1", imgs=["cruz_amanhecer", "p_terco_travesseiro"], mae=True,
        caixa=["uma mãe que ora", "nunca cuida sozinha ❤️"],
        texto="Toda mãe ora pelo filho antes de dormir. A mãe do Pedrinho ora e cuida: é ela quem troca cada "
              "curativo, faixa por faixa. Ele conta que, quando deita, o corpo todo dói. Os curativos que aliviam essa "
              "dor estão acabando, e uma caixa custa mil e quinhentos reais. Se essa oração tocou você, ajude com dois "
              "reais. Que Deus abençoe a sua família.",
        fatos={"mae troca os curativos": "20261102_104706 (mae enfaixando)", "corpo doi ao deitar": "20261102_144645 1,6-5,1",
               "caixa R$1.500 / acabando": "placas 20261102_152739 e 151715", "R$2": "placa 20261102_151635"}),
    "oracoes_sinal": dict(
        tpl="Adrielly_bib4_oracoes_resposta_v1", imgs=["p_vitral_pastor", "maos_oracao"],
        caixa=["às vezes Deus responde", "através de você ❤️"],
        texto="Quantas vezes você já pediu a Deus um sinal? Hoje, o sinal pode ser este vídeo. O Pedrinho tem uma "
              "doença rara, e a pele dele é cheia de feridas, algumas em carne viva. Ele mesmo pede ajuda para o "
              "tratamento dessa semana. Dois ou cinco reais já ajudam muito. Que Deus abençoe você e a sua casa.",
        fatos={"doenca rara, feridas": "20261102_144645 10,4-16,9", "carne viva": "lv_0_20261102155438 19,6-23,3",
               "ajuda no tratamento da semana, dois ou cinco reais": "lv_0_20261102155438 23,8-34,2"}),
    "conselho_generosa": dict(
        tpl="Adrielly_bib4_conselho_semear_v1", imgs=["biblia_janela"],
        versiculo=["A alma generosa", "prosperará – Provérbios 11:25"], caixa=["DOE 2 reais", "e AJUDE O PEDRINHO 💗"],
        texto="Guarda esse conselho: a alma generosa prosperará. Está em Provérbios. Hoje você pode ser generoso com o "
              "Pedrinho. Ele deita pra dormir e o corpo todo dói, e dói muito. O tratamento é caro, mas é o que ameniza "
              "as dores dele. Doe dois reais e ajude o Pedrinho. Que Deus multiplique na sua vida.",
        fatos={"corpo doi ao deitar": "20261102_144645 1,6-7,0", "tratamento caro ameniza as dores": "lv_0_20261102155438 7,6-14,4",
               "R$2": "placa 20261102_151635"}),
    "conselho_necessidade": dict(
        tpl="Adrielly_bib4_conselho_emprestar_v1", imgs=["p_biblia_banco_igreja"],
        versiculo=["O que dá ao pobre não", "terá necessidade – Provérbios 28:27"], caixa=["DOE 2 ou 5 reais", "e AJUDE O PEDRINHO 💗"],
        texto="Ouve esse conselho: o que dá ao pobre não terá necessidade. Provérbios, capítulo vinte e oito. Os "
              "curativos do Pedrinho estão acabando, e uma caixa custa mil e quinhentos reais. Ele pede ajuda para o "
              "tratamento dessa semana. Com dois ou cinco reais, você já faz diferença. Que Deus abençoe você e toda "
              "a sua família.",
        fatos={"curativos acabando, caixa R$1.500": "placas 20261102_151715 e 152739",
               "tratamento da semana, dois ou cinco reais": "20261102_144645 19,1-28,6"}),
    # sem narracao
    "mais_um_dia": dict(tpl="Adrielly_bib_mais_um_dia_v1", textos=[["Mais um dia postando porque", "os curativos do Pedrinho",
                                                                   "estão acabando 💔"], ["5 reais já fazem a diferença"]],
                        fatos={"curativos acabando": "placa 20261102_151715", "5 reais": "20261102_144645"}),
    "esqueceram": dict(tpl="Adrielly_bib_esqueceram_v1", textos=[["esqueceram do Pedrinho? 💔", "os curativos dele estão acabando",
                                                                 "e uma caixa custa R$1.500 😭"]],
                       fatos={"acabando / R$1.500": "placas 20261102_151715 e 152739"}),
    "mateus": dict(tpl="Adrielly_bib_mateus_v1", textos=[None, ["5 reais ajudam nos curativos", "do Pedrinho ❤️"]],
                   fatos={"5 reais": "20261102_144645"}),
    "obrigado": dict(tpl="Adrielly_bib_obrigado_v1", textos=[["Cada real que chega vira", "curativo e pomada na",
                                                             "pele do Pedrinho.", "OBRIGADO DE CORAÇÃO 🙏"]],
                     fim_fala=(r("lv_0_20261102155438"), 34.78, 37.32),
                     fatos={"obrigado de coracao": "lv_0_20261102155438 34,8-37,3"}),
    "deus_te_trouxe": dict(tpl="Adrielly_bib_deus_te_trouxe_v1",
                           textos=[["Deus te trouxe aqui, ajude", "o Pedrinho, os curativos", "dele estão acabando."]],
                           fatos={"falas": "20261102_151635 (gancho) e 20261102_144645", "acabando": "placa 20261102_151715"}),
    "lucas_alegria": dict(
        tpl="Adrielly_bib_lucas_v1", imgs=[], faixa=["Deus ama quem dá com alegria – 2 Coríntios 9:7"],
        caixa_l=["Doe R$2 com alegria", "e ajude o Pedrinho 🙏"],
        texto="Segunda Coríntios, capítulo nove, versículo sete: Deus ama quem dá com alegria. Não precisa ser muito; "
              "precisa ser de coração. O Pedrinho tem uma doença rara, e as feridas dele aumentaram: algumas estão em "
              "carne viva. O tratamento é caro, mas é ele que ameniza as dores. Uma caixa de curativos custa mil e "
              "quinhentos reais. Doe dois reais com alegria e ajude o Pedrinho. Que Deus abençoe você.",
        fatos={"doenca rara": "lv_0_20261102155438 1,7-3,1", "feridas aumentaram, carne viva": "lv_0_20261102155438 15,3-23,3",
               "tratamento caro ameniza as dores": "lv_0_20261102155438 7,6-14,4", "caixa R$1.500": "placa 20261102_152739",
               "R$2": "placa 20261102_151635/152631"}),
    "deus_te_trouxe_peco": dict(
        tpl="Adrielly_bib_deus_te_trouxe_v1", gancho="20261102_152631", falas="lv_0_20261102155438",
        cortes=((1.6, 6.25), (7.5, 14.6), (15.2, 23.4), (23.6, 30.7), (34.7, 37.4)),
        textos=[["Deus te trouxe aqui, o", "Pedrinho precisa de você.", "Ajude com R$2 ❤️"]],
        fatos={"falas": "20261102_152631 (gancho) e lv_0_20261102155438", "R$2": "placa 20261102_152631"}),
    "obrigado_dois_reais": dict(
        tpl="Adrielly_bib_obrigado_v1", textos=[["Seus 2 reais viram curativo", "na pele do Pedrinho.",
                                                 "Cada um ajuda muito.", "OBRIGADO DE CORAÇÃO 🙏"]],
        fim_fala=(r("20261102_144645"), 40.95, 43.05),
        fatos={"R$2": "placa 20261102_151635/152631", "muito obrigado": "20261102_144645 41,0-42,9"}),
}
NUM = {"oracoes_dor": 240, "conselho_salmo": 241, "lucas_dia_de_vida": 242, "oracoes_mae": 243, "oracoes_sinal": 244,
       "conselho_generosa": 245, "conselho_necessidade": 246, "mais_um_dia": 247, "esqueceram": 248, "mateus": 249,
       "obrigado": 250, "deus_te_trouxe": 251,
       "lucas_alegria": 252, "deus_te_trouxe_peco": 253, "obrigado_dois_reais": 254}


def leva(n):  # LEVA 62 ja tem PEB 236-239; depois LEVAs so do Pedrinho a partir da 66 (63-65 sao da Adrielly)
    return 62 if n == 240 else 66 + (n - 241) // 5


def chave(nome):
    return winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment"), nome)[0]


def api(url, data=None):
    h = {"x-magnific-api-key": chave("magnific"), "Content-Type": "application/json"}
    rq = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, headers=h,
                                method="POST" if data else "GET")
    return json.load(urllib.request.urlopen(rq))


def esperar(url, ids, destino, ext, voltas, pausa):
    for _ in range(voltas):
        for n in list(ids):
            d = api(f"{url}/{ids[n]}").get("data") or {}
            if d.get("status") == "COMPLETED" and d.get("generated"):
                urllib.request.urlretrieve(d["generated"][0], os.path.join(destino, n + ext))
                print("pronto", n, flush=True)
                ids.pop(n)
            elif d.get("status") in ("FAILED", "ERROR"):
                sys.exit(f"{n} falhou: {d}")
        if not ids:
            return
        time.sleep(pausa)
    sys.exit("nao ficou pronto a tempo: " + ", ".join(ids))


def gerar_imagens():
    falta = {n: p for n, p in IMAGENS.items() if n not in ("p_nossa_senhora", "p_velas_vermelhas", "p_mudas_sol") and not os.path.exists(os.path.join(IMG, n + ".png"))}
    if falta:
        url = "https://api.magnific.com/v1/ai/text-to-image/seedream-v4-5"
        ids = {n: (api(url, {"prompt": p, "aspect_ratio": "social_story_9_16"}).get("data") or {})["task_id"]
               for n, p in falta.items()}
        esperar(url, ids, IMG, ".png", 80, 5)


def gerar_videos():
    EM_USO = {i for v in V.values() for i in v.get("imgs", [])} | {"a_capela_colina", "a_capela_altar_biblia"}
    falta = [n for n in MOVIMENTO if n in EM_USO and not os.path.exists(os.path.join(VID, n + ".mp4"))]
    if not falta:
        return
    url = "https://api.magnific.com/v1/ai/image-to-video/kling-v2-5-pro"
    ids = {}
    for n in falta:
        jpg = os.path.join(VID, n + "_in.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(IMG, n + ".png"), "-vf", "scale=1080:-2",
                        "-q:v", "3", jpg], check=True)
        d = api(url, {"image": base64.b64encode(open(jpg, "rb").read()).decode(), "prompt": MOVIMENTO[n],
                      "duration": "5", "cfg_scale": 0.5, "negative_prompt": NEG})
        ids[n] = (d.get("data") or d)["task_id"]
        print("video pedido", n, flush=True)
    esperar(url, ids, VID, ".mp4", 180, 10)


def gerar_narracao(nome, texto):
    """Leonardo em 192 kbps, voz estavel; pausas longas viram 0,18 s com fade (o corte seco atropelava a fala)."""
    mp3, sr = os.path.join(NAR, nome + ".mp3"), os.path.join(NAR, nome + "_sr.mp3")
    if not os.path.exists(mp3):
        rq = urllib.request.Request(
            "https://api.elevenlabs.io/v1/text-to-speech/4XmhZ74tBbUVCXIYNMMo?output_format=mp3_44100_192",
            data=json.dumps({"text": C.para_voz(texto), "model_id": "eleven_multilingual_v2",
                             "voice_settings": {"stability": 0.6, "similarity_boost": 0.75, "style": 0.0,
                                                "use_speaker_boost": True}}).encode(),
            headers={"xi-api-key": chave("ELEVENLABS_API_KEY"), "Content-Type": "application/json"}, method="POST")
        open(mp3, "wb").write(urllib.request.urlopen(rq).read())
    if not os.path.exists(sr):
        rr = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp3, "-af", "silencedetect=n=-42dB:d=0.25", "-f", "null", "-"],
                            capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
        ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", rr)]
        fim = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", rr)]
        tot = C._duracao(mp3)
        keep, t = [], 0.0
        for a, b in zip(ini, fim):
            if a <= 0.02:
                t = max(t, b - 0.03)
                continue
            if b >= tot - 0.02:
                keep.append((t, a + 0.08))
                t = None
                break
            keep.append((t, a + 0.09))
            t = b - 0.09
        if t is not None:
            keep.append((t, tot))
        fc = ";".join(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,"
                      f"afade=t=out:st={max(b - a - 0.015, 0):.4f}:d=0.015[k{i}]" for i, (a, b) in enumerate(keep))
        fc += ";" + "".join(f"[k{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[a]"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-filter_complex", fc, "-map", "[a]", "-c:a",
                        "libmp3lame", "-b:a", "192k", sr], check=True)
    tx = os.path.join(NAR, nome + "_sr.json")
    if not os.path.exists(tx):
        subprocess.run([sys.executable, "-I", TRANSCREVER, sr, tx], check=True, capture_output=True)
    return sr, tx, C._duracao(sr)


def pool(seed):
    rnd = random.Random(seed)
    f, v = FOTOS[:], VIDS[:]
    rnd.shuffle(f)
    rnd.shuffle(v)
    out = []
    for i in range(max(len(f), len(v))):  # 2 fotos de ferida para cada video de curativo
        out += f[2 * i:2 * i + 2] and [("f", x) for x in f[2 * i:2 * i + 2]]
        if i < len(v):
            out.append(("v", v[i]))
    return out


def preencher(base, ate, seed, uma_fala=True, dur_cena=3.2):
    """Cenas ate cobrir `ate` s, todas com a mesma duracao (<= dur_cena): fotos de ferida, videos dos curativos e
    uma fala dele (sem som) no meio."""
    import math
    fixo = sum(b["fim"] - b["ini"] for b in base)
    falta = ate - fixo
    n = max(1, math.ceil(falta / dur_cena - 0.05))
    d = round(falta / n, 3)
    escolha, usadas = [], set()
    fala = random.Random(seed).choice(FALA)
    for tipo, x in pool(seed):
        if len(escolha) >= n:
            break
        if uma_fala and len(escolha) == 3 and fala:
            escolha.append(("v", fala))
            fala = None
            if len(escolha) >= n:
                break
        if tipo == "v":
            if x in usadas:
                continue
            usadas.add(x)
        escolha.append((tipo, x))
    if len(escolha) < n:
        sys.exit("faltam cenas")
    for tipo, x in escolha:
        if tipo == "f":
            base.append(cena(x, 0, d))
        else:
            base.append(cena(x[0], x[1], round(x[1] + d, 3)))
    tot = sum(b["fim"] - b["ini"] for b in base)
    base[-1]["fim"] = round(base[-1]["fim"] + (ate - tot), 3)
    return base


def plano(nome, v):
    t = json.load(open(os.path.join(PL, v["tpl"], "plano.json"), encoding="utf-8-sig"))
    p = {k: copy.deepcopy(t[k]) for k in ("ref", "estilo", "textos", "legenda", "fim", "musica", "musica_volume", "modelo")
         if k in t}
    for k in ("musica_ini", "musica_volume_fixo", "musica_depois", "musica_lufs"):
        if k in t:
            p[k] = t[k]
    seed = NUM[nome]
    if v.get("texto"):
        sr, tx, dur = gerar_narracao("n_pedrinho_" + nome, v["texto"])
        oracoes = "oracoes" in nome
        de = 0.3 if oracoes else 0.2
        fim_cta = round(de + dur + 0.3, 2)
        base = []
        if v.get("mae"):  # IA curta e a mae entra quando a narracao fala dela ("A mae do Pedrinho")
            ws = [w for w in json.load(open(tx, encoding="utf-8"))["words"] if w.get("type", "word") == "word"]
            k = [i for i, w in enumerate(ws) if w["text"].lower().startswith("mãe")][1]
            tm = round(de + ws[k - 1]["start"], 2)
            for i in v["imgs"]:
                base.append(dict(arq=os.path.join(VID, i + ".mp4"), ini=0, fim=round(tm / len(v["imgs"]), 2), som=False))
            base.append(cena(MAE[0], MAE[1], MAE[1] + 4.2))
            p["textos"][0]["de"] = round(tm + 0.1, 2)
        else:
            for i in v["imgs"]:
                base.append(dict(arq=os.path.join(VID, i + ".mp4"), ini=0, fim=5 if oracoes else 4.5, som=False))
        base = preencher(base, fim_cta + 2.8, seed)
        p["base"] = base
        p["voz"] = {"arq": sr, "tx": tx, "de": de}
        p["fim"]["de"] = fim_cta
        if "versiculo" in v:
            p["textos"][0].update(linhas=v["versiculo"], de=0, ate=4.5, lh=1.08)
            p["textos"][1] = dict(p["textos"][1], **CAIXA_VERM, linhas=v["caixa"], de=4.6, ate=fim_cta)
        elif "caixa" in v:
            if v["imgs"] and not v.get("mae"):
                p["textos"][0]["de"] = round(sum(b["fim"] - b["ini"] for b in base[:len(v["imgs"])]) + 0.1, 2)
            p["textos"][0].update(linhas=v["caixa"], ate=fim_cta)
        else:  # lucas: faixa do versiculo e texto amarelo
            if v.get("faixa"):
                p["textos"][0]["linhas"] = v["faixa"]
            if v.get("caixa_l"):
                p["textos"][1]["linhas"] = v["caixa_l"]
            p["textos"][1]["ate"] = fim_cta
    elif nome.startswith("deus_te_trouxe"):
        gn = v.get("gancho", "20261102_151635")
        g = r(gn)
        tx = json.load(open(os.path.join(os.path.expanduser("~"), ".claude", "estudio-ong", "CONHECIMENTO", "transcricoes",
                                         "pedrinho_0211", gn + ".json"), encoding="utf-8"))
        ws = [w for w in tx["words"] if w.get("type", "word") == "word"]
        f = r(v.get("falas", "20261102_144645"))
        cortes = v.get("cortes", ((1.5, 7.05), (10.35, 16.95), (18.95, 23.7), (26.9, 28.65), (31.7, 40.6), (40.95, 43.0)))
        base = [dict(arq=g, ini=round(ws[0]["start"] - 0.12, 2), fim=round(ws[-1]["end"] + 0.15, 2), som=True)]
        for a, b in cortes:
            base.append(dict(arq=f, ini=a, fim=b, som=True))
        p["base"] = base
        tg = base[0]["fim"] - base[0]["ini"]
        tot = sum(b["fim"] - b["ini"] for b in base)
        fim_de = round(tot - (cortes[-1][1] - cortes[-1][0]), 2)
        p["textos"] = [dict(p["textos"][0], linhas=v["textos"][0], de=0, ate=round(tg, 2))]
        p["fim"]["de"] = fim_de
        br, t0 = [], round(tg, 2)
        for tipo, x in pool(seed):
            if t0 >= fim_de - 0.3:
                break
            d = min(2.8, fim_de - t0)
            arq, a = (x, 0) if tipo == "f" else x
            br.append([t0, round(t0 + d, 2), arq, a])
            t0 = round(t0 + d, 2)
        p["broll"] = br
        p.pop("voz", None)
    else:  # so musica e texto fixo (L1) ou obrigado (fala real no fim)
        tot = sum(b["fim"] - b["ini"] for b in t["base"])
        base = []
        if v.get("fim_fala"):
            arq, a, b = v["fim_fala"]
            base = preencher([], tot - (b - a), seed, dur_cena=3.0)
            base.append(dict(arq=arq, ini=a, fim=b, som=True))
        else:
            base = preencher([], tot, seed, dur_cena=3.0)
        p["base"] = base
        for i, l in enumerate(v["textos"]):
            if l:
                p["textos"][i]["linhas"] = l
    for b in p["base"]:
        b.pop("pb", None)
    p["estilo"] = "BIB " + nome.upper().replace("_", " ")
    p["modelo"] = dict(p.get("modelo", {}), variacao="pedrinho_" + nome)
    p["fatos"] = v["fatos"]
    n = NUM[nome]
    p["saida"] = os.path.join(REND, f"LEVA {leva(n)}", f"PEB {n} - {p['estilo']}.mp4")
    p["saida_fixa"] = True
    p = dict(crianca="Pedrinho", **p)
    pasta = os.path.join(PL, f"Pedrinho_bib5_{nome}_v1")
    os.makedirs(os.path.join(pasta, "render"), exist_ok=True)
    json.dump(p, open(os.path.join(pasta, "plano.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{nome}: PEB {n}, {sum(b['fim'] - b['ini'] for b in p['base']):.1f}s, {len(p['base'])} cenas", flush=True)


def main():
    # 05/11/2026: sem creditos na Magnific; o usuario mandou usar os videos de IA cristaos que ja existem
    so = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--sem-magnific" not in sys.argv:
        gerar_imagens()
    if "--so-imagens" in sys.argv:
        return
    if "--sem-magnific" not in sys.argv:
        gerar_videos()
    for nome, v in V.items():
        if so and nome not in so:
            continue
        plano(nome, v)


main()
