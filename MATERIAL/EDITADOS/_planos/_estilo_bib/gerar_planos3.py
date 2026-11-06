"""4 videos novos nos modelos "Presta atencao neste conselho" (peb223) e "Oracoes" (peb221), pedido de 03/11/2026.
Copy nova em cada um (so fatos reais dos brutos e das placas), imagens simbolicas novas da Magnific e cenas diferentes.
Gera o que falta (narracao do Leonardo sem respiro + transcricao, imagens Seedream) e escreve os planos.
Uso: python -I gerar_planos3.py"""
import copy
import json
import os
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
IMG, NAR = os.path.join(AQUI, "imagens"), os.path.join(AQUI, "narracoes")
D = os.path.join(RAIZ, "VÍDEOS PARA EDITAR", "PEDRINHO 02-11-2026")
CL = os.path.join(RAIZ, "banco de vídeos do pedrinho", "_clipes_bib")
TRANSCREVER = os.path.expanduser(r"~\.claude\skills\criativo-reportagem-ong\scripts\transcrever.py")


def r(n):
    return os.path.join(D, n + ".mp4")


B = r("lv_0_20261102155438")
A = r("20261102_144645")
P1, P3 = r("20261102_151540"), r("20261102_151715")
S1, S2, S3, S4 = r("20261102_152542"), r("20261102_152631"), r("20261102_152739"), r("20261102_153323")
K1, K2, K3, K4, K5, K6 = (r(x) for x in ("20261102_104706", "20261102_104943", "20261102_113535", "20261102_113735",
                                         "20261102_113918", "20261102_114148"))
BN1, BN2, BN3 = (os.path.join(CL, x) for x in ("bn1_curativos_cama_20s.mp4", "bn2_1760826007_92s.mp4",
                                                "bn3_1792347808_155s.mp4"))


def cena(arq, ini, fim, **k):
    return dict(arq=arq, ini=ini, fim=fim, som=False, **k)


IMAGENS = {
    "cruz_amanhecer": "A simple wooden cross on top of a green hill at golden sunrise, soft rays of light breaking "
                      "through clouds, peaceful and hopeful, photorealistic, cinematic, vertical composition",
    "pomba_luz": "A white dove flying through soft heavenly light and clouds, golden rays, peaceful, photorealistic, "
                 "cinematic, vertical composition",
    "cordeiro": "A small white lamb resting in a green pasture under soft divine morning light, gentle and peaceful, "
                "photorealistic, cinematic, vertical composition",
    "maos_oracao": "Close-up of hands clasped in prayer resting on an old open Bible, warm candlelight, dark "
                   "background, photorealistic, cinematic, vertical composition",
    "biblia_vela": "Upright view from above a wooden table at night: an open Bible lying flat on the table and a tall "
                   "white candle standing upright beside it, the flame pointing straight up, warm golden glow, natural "
                   "upright orientation, photorealistic, calm and hopeful, vertical composition",
    "biblia_janela": "An old open Bible on a windowsill at sunrise with a wooden rosary beside it, soft warm light, "
                     "photorealistic, calm, vertical composition",
}

# cenas de cada video: nenhuma se repete dentro do mesmo video; as do sofa/cadeira ficam longe do texto do alto
V = {
    "oracoes_sinal": dict(
        modelo="peb221_l2_oracoes", imgs=["cruz_amanhecer", "pomba_luz"],
        caixa=["talvez este seja o sinal", "que você pediu a Deus ❤️"],
        texto="Talvez você tenha pedido a Deus um sinal hoje. Um sinal de que ainda dá tempo de fazer o bem. Esse vídeo "
              "pode ser esse sinal. O Pedrinho tem epidermólise bolhosa, a pele de borboleta. Ele mesmo conta que deita "
              "para dormir e o corpo todo dói. Os curativos que aliviam essa dor estão acabando, e uma caixa custa mil e "
              "quinhentos reais. Cinco reais pode parecer pouco pra você, mas pra ele é mais um dia sem dor. Se Deus "
              "tocou o seu coração, não deixe passar. Que Deus abençoe você e a sua família.",
        cenas=[cena(K6, 13, 16.5, pb=True), cena(P1, 0.5, 4), cena(K2, 1, 4.5), cena(K3, 9, 12.5), cena(BN2, 9, 12.5),
               cena(K5, 6, 9.5), cena(K4, 22, 25.5), cena(P3, 1, 4.5), cena(K1, 5, 8.5), cena(A, 7.2, 10.7)]),
    "oracoes_saude": dict(
        modelo="peb221_l2_oracoes", imgs=["cordeiro", "maos_oracao"],
        caixa=["Deus coloca as pessoas certas", "no caminho de quem precisa ❤️"],
        texto="Toda noite, muita gente ora pedindo saúde para quem ama. O Pedrinho também precisa dessa oração, e de "
              "mais uma coisa: da sua ajuda. Ele tem uma doença rara, e a pele dele é toda cheia de feridas. O "
              "tratamento dele é caro, mas é ele que alivia as dores. Hoje, o pedido é simples: dois ou cinco reais "
              "para os curativos dessa semana. Deus coloca as pessoas certas no caminho de quem precisa. Talvez hoje "
              "seja você. Que Deus abençoe a sua casa.",
        cenas=[cena(K4, 10, 13.5), cena(S2, 3, 6.5), cena(K1, 0, 3.5), cena(BN1, 0, 3.5), cena(K6, 4, 7.5, pb=True),
               cena(K3, 1, 4.5), cena(P3, 4.5, 8), cena(K2, 6, 9.5), cena(BN3, 0, 3.5), cena(B, 15, 18.5)]),
    "conselho_semear": dict(
        modelo="peb223_l2_conselho", imgs=["biblia_vela"],
        versiculo=["Tudo o que o homem semear,", "isso ceifará – Gálatas 6:7"],
        caixa=["DOE 5 reais", "e AJUDE O PEDRINHO 💗"],
        texto="Guarde este conselho. Quem planta o bem, colhe o bem. A Bíblia diz em Gálatas: tudo o que o homem "
              "semear, isso também ceifará. Hoje você pode semear o bem na vida do Pedrinho. Ele tem uma doença rara, "
              "e os curativos dele estão acabando. Doe cinco reais e ajude no tratamento dessa semana. Que Deus "
              "multiplique na sua vida.",
        cenas=[cena(K6, 0.5, 3.5, pb=True), cena(K2, 3, 6), cena(P1, 3, 6), cena(K5, 0, 3), cena(K4, 18, 21),
               cena(BN2, 2, 5), cena(K1, 4, 7), cena(K3, 10, 13)]),
    "conselho_hoje": dict(
        modelo="peb223_l2_conselho", imgs=["biblia_janela"],
        versiculo=["Não negues o bem a quem", "precisa – Provérbios 3:27"],
        caixa=["DOE 2 ou 5 reais", "e AJUDE O PEDRINHO 💗"],
        texto="Escuta esse conselho até o fim. Nunca deixe para amanhã o bem que você pode fazer hoje. O Pedrinho tem "
              "a pele de borboleta, e cada curativo alivia a dor dele. Uma caixa de curativos custa mil e quinhentos "
              "reais, e eles estão acabando. Com dois ou cinco reais você já ajuda muito. Que Deus abençoe você e toda "
              "a sua família.",
        cenas=[cena(K4, 25, 28), cena(S3, 3.5, 7), cena(K1, 1, 4), cena(K3, 5, 8), cena(BN1, 1, 4), cena(K5, 7, 10),
               cena(P3, 2, 5), cena(K2, 8, 11)]),
}


def chave(nome):
    return winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment"), nome)[0]


def gerar_imagens():
    falta = {n: p for n, p in IMAGENS.items() if not os.path.exists(os.path.join(IMG, n + ".png"))}
    if not falta:
        return
    h = {"x-magnific-api-key": chave("magnific"), "Content-Type": "application/json"}
    url = "https://api.magnific.com/v1/ai/text-to-image/seedream-v4-5"

    def call(u, data=None):
        rq = urllib.request.Request(u, data=json.dumps(data).encode() if data else None, headers=h,
                                    method="POST" if data else "GET")
        return json.load(urllib.request.urlopen(rq))
    ids = {n: (call(url, {"prompt": p, "aspect_ratio": "social_story_9_16"}).get("data") or {})["task_id"]
           for n, p in falta.items()}
    for _ in range(80):
        for n in list(ids):
            d = call(f"{url}/{ids[n]}").get("data") or {}
            if d.get("status") == "COMPLETED" and d.get("generated"):
                urllib.request.urlretrieve(d["generated"][0], os.path.join(IMG, n + ".png"))
                print("imagem", n)
                ids.pop(n)
            elif d.get("status") in ("FAILED", "ERROR"):
                sys.exit(f"imagem {n} falhou: {d}")
        if not ids:
            return
        time.sleep(5)
    sys.exit("imagens nao ficaram prontas")


MOVIMENTO = {  # pedido do usuario (03/11/2026): no lugar da imagem parada, video gerado na Magnific a partir dela
    "cruz_amanhecer": "slow cinematic push-in toward the wooden cross, sun rays moving gently, clouds drifting slowly",
    "pomba_luz": "the white dove flies slowly forward through the golden light, gentle wing flaps, clouds drifting",
    "cordeiro": "the lamb breathes softly and moves its head slightly, grass sways in a gentle breeze, slow push-in",
    "maos_oracao": "the candle flame flickers softly, the hands stay still in prayer, very slow push-in",
    "biblia_vela": "the candle flame flickers, slow push-in toward the open Bible, warm moving light",
    "biblia_janela": "sunlight slowly grows through the window, dust particles float in the light, gentle push-in",
}
VID = os.path.join(AQUI, "videos_ia")


def gerar_videos():
    """Kling 2.5 Pro (image-to-video, 5 s) a partir de cada imagem simbolica."""
    import base64
    os.makedirs(VID, exist_ok=True)
    falta = [n for n in MOVIMENTO if not os.path.exists(os.path.join(VID, n + ".mp4"))]
    if not falta:
        return
    h = {"x-magnific-api-key": chave("magnific"), "Content-Type": "application/json"}
    url = "https://api.magnific.com/v1/ai/image-to-video/kling-v2-5-pro"

    def call(u, data=None):
        rq = urllib.request.Request(u, data=json.dumps(data).encode() if data else None, headers=h,
                                    method="POST" if data else "GET")
        return json.load(urllib.request.urlopen(rq))
    ids = {}
    for n in falta:
        jpg = os.path.join(VID, n + "_in.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(IMG, n + ".png"), "-vf", "scale=1080:-2",
                        "-q:v", "3", jpg], check=True)
        b64 = base64.b64encode(open(jpg, "rb").read()).decode()
        d = call(url, {"image": b64, "prompt": MOVIMENTO[n], "duration": "5", "cfg_scale": 0.5,
                       "negative_prompt": "text, watermark, human face, distortion, morphing, blur"})
        ids[n] = (d.get("data") or d)["task_id"]
        print("video pedido", n)
    for _ in range(180):
        for n in list(ids):
            d = call(f"{url}/{ids[n]}").get("data") or {}
            if d.get("status") == "COMPLETED" and d.get("generated"):
                urllib.request.urlretrieve(d["generated"][0], os.path.join(VID, n + ".mp4"))
                print("video pronto", n)
                ids.pop(n)
            elif d.get("status") in ("FAILED", "ERROR"):
                sys.exit(f"video {n} falhou: {d}")
        if not ids:
            return
        time.sleep(10)
    sys.exit("videos nao ficaram prontos")


def gerar_narracao(nome, texto):
    mp3, sr = os.path.join(NAR, nome + ".mp3"), os.path.join(NAR, nome + "_sr.mp3")
    if not os.path.exists(mp3):
        rq = urllib.request.Request(
            "https://api.elevenlabs.io/v1/text-to-speech/4XmhZ74tBbUVCXIYNMMo?output_format=mp3_44100_128",
            data=json.dumps({"text": C.para_voz(texto), "model_id": "eleven_multilingual_v2",
                             "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}}).encode(),
            headers={"xi-api-key": chave("ELEVENLABS_API_KEY"), "Content-Type": "application/json"}, method="POST")
        open(mp3, "wb").write(urllib.request.urlopen(rq).read())
    if not os.path.exists(sr):
        C.sem_respiro(mp3, sr)
    tx = os.path.join(NAR, nome + "_sr.json")
    if not os.path.exists(tx):
        subprocess.run([sys.executable, "-I", TRANSCREVER, sr, tx], check=True, capture_output=True)
    return sr, tx, C._duracao(sr)


def main():
    gerar_imagens()
    gerar_videos()
    for nome, v in V.items():
        m = json.load(open(os.path.join(SK, "modelos", v["modelo"] + ".json"), encoding="utf-8"))
        p = copy.deepcopy(m)
        sr, tx, dur = gerar_narracao("n_" + nome, v["texto"])
        oracoes = v["modelo"].startswith("peb221")
        de = 0.3 if oracoes else 0.2
        base = [dict(arq=os.path.join(VID, i + ".mp4"), ini=0, fim=5 if oracoes else 4.5, som=False)
                for i in v["imgs"]]
        fim_cta = de + dur + 0.3
        for c in v["cenas"]:  # cenas ate cobrir a narracao + a cartela final (~2,7 s)
            if sum(x["fim"] - x["ini"] for x in base) >= fim_cta + 2.6:
                break
            base.append(c)
        sobra = sum(x["fim"] - x["ini"] for x in base) - (fim_cta + 2.8)
        if sobra > 0.2:  # cartela final de ~2,8 s, nao mais (a ultima cena fica com pelo menos 1,5 s)
            base[-1] = dict(base[-1], fim=round(max(base[-1]["ini"] + 1.5, base[-1]["fim"] - sobra), 2))
        tot = sum(x["fim"] - x["ini"] for x in base)
        if tot < fim_cta + 2.4:
            sys.exit(f"{nome}: faltam cenas ({tot:.1f}s para {fim_cta + 2.4:.1f}s)")
        p["base"] = base
        p["voz"] = {"arq": sr, "tx": tx, "de": de}
        p["fim"]["de"] = round(fim_cta, 2)
        if oracoes:
            p["textos"][0].update(linhas=v["caixa"], ate=round(fim_cta, 2))
        else:
            p["textos"][0].update(linhas=v["versiculo"], ate=4.5, lh=1.08)
            p["textos"][1].update(linhas=v["caixa"], ate=round(fim_cta, 2))
        p["estilo"] = "BIB " + nome.upper().replace("_", " ")
        p["modelo"] = dict(m["modelo"], variacao=nome)
        pasta = os.path.join(PL, f"Pedrinho_bib3_{nome}_v1")
        os.makedirs(os.path.join(pasta, "render"), exist_ok=True)
        f = os.path.join(pasta, "plano.json")
        antigo = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
        if antigo.get("saida"):
            p["saida"] = antigo["saida"]  # remontagem: mesmo PEB
        p.pop("crianca", None)
        p = dict(crianca="Pedrinho", **p)
        json.dump(p, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{nome}: narracao {dur:.1f}s, video {tot:.1f}s, {len(base)} cenas")


main()
