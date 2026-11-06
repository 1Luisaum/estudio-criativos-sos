"""4 videos da Adrielly nos modelos "Oracoes" (peb221) e "Presta atencao neste conselho" (peb223), com video de IA
da Magnific no gancho, como os PEB 226-229 do Pedrinho. Pedido de 05/11/2026: videos de IA novos, sem reaproveitar
e sem animais. Copy nova so com fatos reais das falas da Adrielly.
Uso: python -I gerar_planos4_adrielly.py"""
import base64
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
IMG, NAR, VID = os.path.join(AQUI, "imagens"), os.path.join(AQUI, "narracoes"), os.path.join(AQUI, "videos_ia")
BK = os.path.join(RAIZ, "adrielly", "BANCO DE VÍDEOS ADRIELY")
CL = os.path.join(PL, "_clipes_adrielly")
TRANSCREVER = os.path.expanduser(r"~\.claude\skills\criativo-reportagem-ong\scripts\transcrever.py")


def b(n):
    return os.path.join(BK, n)


def cl(n):
    return os.path.join(CL, "adrielly_" + n + ".mp4")


def wa(k=None):
    return b("WhatsApp Video 2026-07-07 at 19.32.36" + (f" ({k})" if k else "") + ".mp4")


def cena(arq, ini, fim, **k):
    return dict(arq=arq, ini=ini, fim=fim, som=False, **k)


NEG = "text, letters, watermark, person, human face, animal, bird, dog, cat, lamb, dove, distortion, morphing, blur"
IMAGENS = {
    "vitral_capela": "Warm sunlight streaming through a colorful stained glass window into an empty quiet chapel, rays of "
                     "light over simple wooden pews, no people, peaceful and hopeful, photorealistic, cinematic, vertical "
                     "composition",
    "velas_altar": "Many small prayer candles burning on a simple stone altar in a dim old church, warm golden glow, soft "
                   "bokeh, no people, photorealistic, cinematic, vertical composition",
    "altar_catolico": "Interior of a traditional Catholic church: a white marble altar with a golden crucifix in the "
                      "center, tall white candles on golden candlesticks, a statue of Our Lady in soft light at the side, "
                      "red sanctuary lamp, stained glass windows, wooden pews, no people, reverent and peaceful, "
                      "photorealistic, cinematic, vertical composition",
    "terco_linho": "A wooden rosary resting on soft white linen next to a few small white flowers, gentle morning sunlight "
                   "from a window, no people, calm and hopeful, photorealistic, cinematic, vertical composition",
    "trigo_amanhecer": "A golden wheat field at sunrise with a narrow path leading toward a bright warm light on the "
                       "horizon, no people, hopeful, photorealistic, cinematic, vertical composition",
    "broto_terra": "A small green sprout growing from dark rich soil in a garden, tiny water droplets on the leaves, soft "
                   "golden morning light, close-up, no people, photorealistic, cinematic, vertical composition",
    "biblia_jardim": "An old open Bible lying on a weathered wooden bench in a quiet garden at golden hour, soft warm "
                     "light, blurred green leaves behind, no people, photorealistic, cinematic, vertical composition",
}
MOVIMENTO = {
    "vitral_capela": "light rays slowly shift through the stained glass, dust particles float in the light, slow push-in",
    "velas_altar": "the candle flames flicker gently, warm light breathes softly, very slow push-in",
    "altar_catolico": "the candle flames flicker gently, soft light moves over the altar and the crucifix, very slow push-in",
    "terco_linho": "sunlight slowly moves across the linen, the small flowers sway slightly, gentle push-in",
    "trigo_amanhecer": "the wheat sways in a gentle breeze, the sun slowly rises, slow push-in along the path",
    "broto_terra": "the sprout slowly unfolds its leaves, water droplets shimmer in the sunlight, gentle push-in",
    "biblia_jardim": "the Bible pages flutter gently in the breeze, leaves move softly behind, slow push-in",
}
V = {
    "oracoes_resposta": dict(
        modelo="peb221_l2_oracoes", imgs=["vitral_capela", "altar_catolico"],
        caixa=["às vezes a resposta da sua oração", "é ser a resposta de alguém ❤️"],
        texto="Às vezes a gente ora pedindo uma resposta, e Deus responde colocando alguém no nosso caminho. Hoje, esse "
              "alguém é a Adrielly. Ela tem epidermólise bolhosa, a pele de borboleta, uma doença rara e sem cura. Ela "
              "mesma conta que a pele arde, sangra, e que só consegue chorar de dor. O que alivia são os curativos "
              "especiais, e eles estão acabando. Com dois ou cinco reais, você já ajuda no tratamento dessa semana. Que "
              "Deus abençoe você e a sua casa.",
        fatos={"EB distrofica, rara e sem cura": "IMG_3868 / IMG_5709",
               "a pele arde, sangra e ela so consegue chorar de dor": "IMG_4227 0,76-6,10",
               "os curativos aliviam": "IMG_4484 / IMG_5709",
               "curativos acabando": "IMG_6452 (30/10) 'Nao temos quase nada de curativo para os cuidados dessa semana'",
               "dois ou cinco reais, tratamento dessa semana": "IMG_6418 (30/10)"},
        cenas=[cena(cl("lencol_sangue_pb"), 0, 3.5), cena(b("85fe8774-511b-460c-a587-4ae5d58e0b82.mov"), 5, 8.5, pb=True),
               cena(cl("mepilex"), 0, 3.5), cena(wa(3), 3, 6.5), cena(cl("urgotul"), 0, 3.5),
               cena(b("375B0806-B2AE-4470-938C-26C98249DAD2.mov"), 10, 13.5), cena(wa(7), 2, 5.5),
               cena(cl("curativos_juntos"), 0, 3.5), cena(b("rot 1 (2).mp4"), 2, 5.5), cena(wa(9), 8, 11.5)]),
    "oracoes_mae": dict(
        modelo="peb221_l2_oracoes", imgs=["terco_linho", "trigo_amanhecer"],
        caixa=["a oração de uma mãe", "chega até Deus ❤️"],
        texto="Muitas mães oram toda noite pela saúde dos filhos. A mãe da Adrielly dorme num colchão ao lado da cama "
              "dela, para socorrer a filha nas madrugadas de crise de dor. É ela quem dá o banho e faz cada curativo. "
              "Mas o dinheiro do tratamento acabou. A Adrielly tem uma doença rara, e cada curativo alivia a dor dela. "
              "Se essa oração tocou o seu coração, ajude com cinco reais. Que Deus abençoe a sua família.",
        fatos={"mae dorme no colchao ao lado para socorrer nas crises de dor": "IMG_3726",
               "mae da o banho e faz os curativos": "IMG_5475",
               "a mae ja nao tem dinheiro para o tratamento": "IMG_4725 1,36-5,60",
               "os curativos aliviam": "IMG_4484",
               "cinco reais": "IMG_4205 / IMG_4493"},
        cenas=[cena(b("1d7c619d-834b-46cb-b378-dd3ff4e03ef5.mov"), 2, 5.5), cena(b("IMG_9180.MOV"), 10, 13.5, pb=True),
               cena(cl("costas_faixas"), 0, 3.5), cena(b("48EF4D37-1EF3-4375-B93D-B76770D944E0.mov"), 20, 23.5),
               cena(cl("allevyn"), 0, 3.5), cena(wa(5), 4, 7.5), cena(cl("infusao_cama"), 0, 3.5),
               cena(b("Rot 2 (2).mp4"), 2, 5.5), cena(cl("urgo_verde"), 0, 3.5), cena(wa(1), 6, 9.5)]),
    "conselho_semear": dict(
        modelo="peb223_l2_conselho", imgs=["broto_terra"],
        versiculo=["Quem semeia com fartura, com fartura", "também colherá – 2 Coríntios 9:6"],
        caixa=["DOE 5 reais", "e AJUDE A ADRIELLY 💗"],
        texto="Guarde esse conselho. Quem semeia com fartura, com fartura também colherá. Está em segunda Coríntios, "
              "capítulo nove. Hoje você pode semear na vida da Adrielly. Ela tem a pele de borboleta, e tem dias que a "
              "dor nem deixa ela levantar da cama. O tratamento dela é caro, mas ficar sem ele custa a vida dela. Doe "
              "cinco reais e ajude a Adrielly. Que Deus multiplique na sua vida.",
        fatos={"dor que nao deixa levantar da cama": "IMG_4216 0,56-6,28",
               "tratamento caro, ficar sem ele custa a vida": "IMG_6212 / IMG_6224",
               "cinco reais": "IMG_4205 / IMG_4493"},
        cenas=[cena(b("IMG_0211.MOV"), 10, 13, pb=True), cena(cl("pernas_faixas"), 0, 3), cena(wa(4), 3, 6),
               cena(cl("sulfadiazina"), 0, 3), cena(b("5E4503B5-C565-45B5-B01D-A5C3A8D3F443.mov"), 15, 18),
               cena(wa(8), 3, 6), cena(cl("urgotul_silver"), 0, 3), cena(b("rot 1 (4).mp4"), 1, 4), cena(wa(2), 9, 12)]),
    "conselho_emprestar": dict(
        modelo="peb223_l2_conselho", imgs=["biblia_jardim"],
        versiculo=["Quem se compadece do pobre", "empresta ao Senhor – Provérbios 19:17"],
        caixa=["DOE 2 ou 5 reais", "e AJUDE A ADRIELLY 💗"],
        texto="Ouve esse conselho até o fim. Quem se compadece do pobre empresta ao Senhor, diz Provérbios. A Adrielly "
              "tem uma doença rara, e não tem quase nada de curativo para os cuidados dessa semana. Os curativos dela "
              "custam mais de noventa mil reais, e a mãe dela já não tem dinheiro para o tratamento. Com dois ou cinco "
              "reais, você já faz diferença. Que Deus abençoe você e toda a sua família.",
        fatos={"quase nada de curativo para a semana": "IMG_6452 (30/10) 3,62-10,18",
               "mais de R$ 90.000 em curativo": "IMG_6227 / IMG_6231",
               "a mae ja nao tem dinheiro para o tratamento": "IMG_4725 1,36-5,60",
               "dois ou cinco reais": "IMG_6418 (30/10)"},
        cenas=[cena(b("IMG_0850.MOV"), 2, 5, pb=True), cena(b("8AA60297-571C-438D-B8EF-92B439C2CEE0.mov"), 5, 8),
               cena(cl("remedios_juntos"), 0, 3), cena(wa(), 13, 16),
               cena(b("79212854-35CA-4B92-85A4-9354BFBE7E30.mov"), 20, 23), cena(cl("ferropurum"), 0, 3),
               cena(wa(6), 2, 5), cena(b("Rot 2 (5).mp4"), 2, 5), cena(b("1d7c619d-834b-46cb-b378-dd3ff4e03ef5.mov"), 12, 15)]),
}


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
    falta = {n: p for n, p in IMAGENS.items() if not os.path.exists(os.path.join(IMG, n + ".png"))}
    if falta:
        url = "https://api.magnific.com/v1/ai/text-to-image/seedream-v4-5"
        ids = {n: (api(url, {"prompt": p, "aspect_ratio": "social_story_9_16"}).get("data") or {})["task_id"]
               for n, p in falta.items()}
        esperar(url, ids, IMG, ".png", 80, 5)


def gerar_videos():
    """Kling 2.5 Pro (image-to-video, 5 s) a partir de cada imagem simbolica."""
    os.makedirs(VID, exist_ok=True)
    falta = [n for n in MOVIMENTO if n != "velas_altar" and not os.path.exists(os.path.join(VID, n + ".mp4"))]
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
    so = sys.argv[1:]
    gerar_imagens()
    if "--so-imagens" in so:
        return
    gerar_videos()
    for nome, v in V.items():
        if [a for a in so if not a.startswith("--")] and nome not in so:
            continue
        for c in v["cenas"]:
            if not os.path.exists(c["arq"]):
                sys.exit(f"{nome}: falta a cena {c['arq']}")
        m = json.load(open(os.path.join(SK, "modelos", v["modelo"] + ".json"), encoding="utf-8"))
        p = copy.deepcopy(m)
        sr, tx, dur = gerar_narracao("n_adrielly_" + nome, v["texto"])
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
        p["fatos"] = v["fatos"]
        pasta = os.path.join(PL, f"Adrielly_bib4_{nome}_v1")
        os.makedirs(os.path.join(pasta, "render"), exist_ok=True)
        f = os.path.join(pasta, "plano.json")
        antigo = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
        if antigo.get("saida"):
            p["saida"] = antigo["saida"]  # remontagem: mesmo AEB
        p.pop("crianca", None)
        p = dict(crianca="Adrielly", **p)
        json.dump(p, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{nome}: narracao {dur:.1f}s, video {tot:.1f}s, {len(base)} cenas", flush=True)


main()
