"""Video vertical (ate 1 min) da pagina de obrigado: quem doou para o Pedrinho ve o agradecimento, entende a doenca e
e convidado a doar tambem para a Adrielly (botao abaixo do video na pagina). Pedido do usuario de 05/11/2026.
Abre com o video de IA do vitral com a cruz e o narrador agradecendo.
Monta um plano do bib.py: trechos de narracao (Leonardo) intercalados com falas reais das criancas; a narracao vira
uma faixa so, com silencio onde as criancas falam.
Uso: python -I video_pagina_obrigado.py"""
import json
import os
import re
import subprocess
import sys
import urllib.request
import winreg

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(os.path.expanduser("~"), ".claude", "skills", "criativo-bibliotecas-ong")
sys.path.insert(0, os.path.join(SK, "scripts"))
import comum as C  # noqa: E402

RAIZ = C.raiz()
PL = os.path.join(RAIZ, "EDITADOS", "_planos")
PASTA = os.path.join(PL, "Obrigado_pedrinho_doe_adrielly_v1")
NAR = os.path.join(PASTA, "narracao")
os.makedirs(NAR, exist_ok=True)
TRANSCREVER = os.path.expanduser(r"~\.claude\skills\criativo-reportagem-ong\scripts\transcrever.py")
P02 = os.path.join(RAIZ, "VÍDEOS PARA EDITAR", "PEDRINHO 02-11-2026")
CP, CA = os.path.join(PL, "_clipes_pedrinho"), os.path.join(PL, "_clipes_adrielly")
TA = os.path.join(os.path.expanduser("~"), "Desktop", "TODAS AS PASTAS", "adriely")
AG = os.path.join(RAIZ, "adrielly", "BRUTOS DA ADRIELY", "SOS HUMAN HELP - GRAVAÇÕES  ADRIELLY", "Agosto")
VIA = os.path.join(AQUI, "videos_ia")

N = {
    "N1": "Obrigado! Você acabou de ajudar o Pedrinho. A sua doação vira curativo na pele dele.",
    "N3": "O Pedrinho não é o único. A Adrielly também tem epidermólise bolhosa, a pele de borboleta, e também "
          "precisa de ajuda.",
    "N4": "Se você puder, estenda essa mesma ajuda à Adrielly. Toque no botão abaixo e doe também para ela. "
          "Que Deus abençoe você.",
}


def chave(nome):
    return winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment"), nome)[0]


def narrar(k, texto):
    """06/11: forma padrao do ElevenLabs, sem mexer em nada (pedido do usuario): sem voice_settings, formato padrao,
    sem cortar pausas e sem tratamento. O arquivo do ElevenLabs entra direto no video."""
    mp3, tx = os.path.join(NAR, k + ".mp3"), os.path.join(NAR, k + ".json")
    if not os.path.exists(mp3):
        rq = urllib.request.Request(
            "https://api.elevenlabs.io/v1/text-to-speech/Hmn4B9B77pf6ttydteJ8",
            data=json.dumps({"text": C.para_voz(texto), "model_id": "eleven_multilingual_v2"}).encode(),
            headers={"xi-api-key": chave("ELEVENLABS_API_KEY"), "Content-Type": "application/json"}, method="POST")
        open(mp3, "wb").write(urllib.request.urlopen(rq).read())
    if not os.path.exists(tx):
        subprocess.run([sys.executable, "-I", TRANSCREVER, mp3, tx], check=True, capture_output=True)
    return mp3, json.load(open(tx, encoding="utf-8")), C._duracao(mp3)


def cena(arq, ini, fim, som=False):
    return dict(arq=arq, ini=ini, fim=fim, som=som)


def preencher(lista, dur):
    """Divide `dur` s entre as cenas da lista (todas com o mesmo tempo, no maximo 3,3 s cada)."""
    import math
    n = min(len(lista), max(1, math.ceil(dur / 3.3 - 0.05)))
    d = dur / n
    out = []
    for arq, a in lista[:n]:
        out.append(cena(arq, a, round(a + d, 3)))
    out[-1]["fim"] = round(out[-1]["fim"] + (dur - sum(x["fim"] - x["ini"] for x in out)), 3)
    return out


def broll_adrielly(base):
    """06/11: ela aparece falando na 1a fala (IMG_4227); a 2a fala (IMG_6452) fica coberta por b-roll das feridas."""
    t, a, z = 0.0, None, None
    for b in base:
        d = b["fim"] - b["ini"]
        if os.path.basename(b["arq"]).startswith("IMG_6452"):
            a = t if a is None else a
            z = t + d
        t += d
    if a is None:
        return []
    clipes = [os.path.join(CA, n) for n in ("ferida_perna_cama.mp4", "foto_ferida_pescoco.mp4", "foto_ferida_maos.mp4")]
    d = (z - a) / len(clipes)
    return [[round(a + i * d, 3), round(a + (i + 1) * d, 3), c, 0] for i, c in enumerate(clipes)]


def main():
    nar = {k: narrar(k, t) for k, t in N.items()}
    # (tipo, conteudo): "n" = narracao sobre cenas; "f" = fala real com som
    roteiro = [
        ("n", "N1", [(os.path.join(VIA, "p_vitral_pastor.mp4"), 0), (os.path.join(P02, "20261102_104706.mp4"), 0.5)]),
        ("f", [(os.path.join(P02, "lv_0_20261102155438.mp4"), 34.7, 37.4)]),
        ("n", "N3", [(os.path.join(CA, "foto_ferida_bracos.mp4"), 0), (os.path.join(CA, "ferida_maos_6454.mp4"), 0)]),
        ("f", [(os.path.join(AG, "IMG_4227.MOV"), 0.7, 2.2), (os.path.join(AG, "IMG_4227.MOV"), 2.55, 3.45),
               (os.path.join(AG, "IMG_4227.MOV"), 3.8, 6.25), (os.path.join(TA, "IMG_6452.MOV"), 3.55, 10.25)]),
        ("n", "N4", [(os.path.join(CA, "foto_ferida_costas.mp4"), 0), (os.path.join(CA, "ferida_braco_hospital.mp4"), 0),
                     (os.path.join(RAIZ, "adrielly", "BANCO DE VÍDEOS ADRIELY", "1d7c619d-834b-46cb-b378-dd3ff4e03ef5.mov"), 2.0)]),
    ]
    FIM = 3.2  # tela final "AJUDE A ADRIELLY TAMBEM" por cima da ultima cena
    base, voz_partes, palavras, t = [], [], [], 0.0
    for item in roteiro:
        if item[0] == "n":
            _, k, cenas = item
            sr, tx, dur = nar[k]
            slot = dur + 0.25 + (FIM if k == "N4" else 0)
            if k == "N1":  # o vitral fica inteiro (5 s) e a mae entra depois
                base.append(cena(cenas[0][0], 0, 5.0))
                base += preencher(cenas[1:], slot - 5.0) if slot > 5.2 else []
                if slot <= 5.2:
                    base[-1]["fim"] = round(slot, 3)
            else:
                base += preencher(cenas, slot)
            voz_partes.append(("a", sr, slot))
            palavras += [dict(w, start=w["start"] + t, end=w["end"] + t) for w in tx["words"] if w.get("type", "word") == "word"]
            t += slot
        else:
            for arq, a, b in item[1]:
                base.append(cena(arq, a, b, som=True))
                voz_partes.append(("s", None, b - a))
                t += b - a
    total = sum(x["fim"] - x["ini"] for x in base)
    # faixa unica de narracao: cada trecho no seu lugar, silencio onde a crianca fala
    voz = os.path.join(NAR, "narracao_completa.wav")
    cmd, fc, k = ["ffmpeg", "-v", "error", "-y"], [], 0
    for tipo, f, d in voz_partes:
        if tipo == "a":
            cmd += ["-i", f]
            fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{d:.3f}[p{len(fc)}]")
        else:
            cmd += ["-f", "lavfi", "-t", f"{d:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
            fc.append(f"[{k}:a]anull[p{len(fc)}]")
        k += 1
    fc.append("".join(f"[p{i}]" for i in range(len(fc))) + f"concat=n={len(voz_partes)}:v=0:a=1[a]")
    subprocess.run(cmd + ["-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s16le", voz],
                   check=True)
    txj = os.path.join(NAR, "narracao_completa.json")
    json.dump({"text": " ".join(N.values()), "words": palavras}, open(txj, "w", encoding="utf-8"), ensure_ascii=False)
    fim_de = round(total - FIM, 2)
    t_adr = sum(d for _, _, d in voz_partes[:2])  # comeco do trecho da Adrielly (N3)
    p = {
        "crianca": "Pedrinho",
        "estilo": "PAGINA DE OBRIGADO",
        "base": base,
        "voz": {"arq": voz, "tx": txj, "de": 0},
        # cada trecho original do ElevenLabs e onde ele comeca (para o Premiere: o usuario quer analisar os arquivos crus)
        "voz_partes": [{"arq": f, "de": round(sum(d for _, _, d in voz_partes[:i]), 3)}
                       for i, (tipo, f, _) in enumerate(voz_partes) if tipo == "a"],
        "textos": [
            dict(estilo="caixa", bg="vermelho", fg="branco", size=48, y=185, fonte="black", pad=[28, 10], lh=1.15, raio=16,
                 sombra_caixa=True, linhas=["OBRIGADO POR AJUDAR", "O PEDRINHO ❤️"], de=0, ate=round(t_adr, 2)),
            dict(estilo="caixa", bg="vermelho", fg="branco", size=48, y=185, fonte="black", pad=[28, 10], lh=1.15, raio=16,
                 sombra_caixa=True, linhas=["A ADRIELLY TAMBÉM", "PRECISA DE VOCÊ ❤️"], de=round(t_adr, 2), ate=fim_de),
        ],
        "legenda": {"estilo": "unicef", "y": 1190},
        "fim": {"linhas": ["AJUDE A ADRIELLY", "TAMBÉM ❤️"], "cor": "vermelho", "size": 72, "escuro": 0.5, "de": fim_de,
                "sub": ["Toque no botão abaixo"], "size_sub": 50, "setas": True, "y": 860},
        "musica": os.path.join(RAIZ, "MÚSICAS", "magnific_tristes", "The_Weight_of_Time.mp3"),
        "fatos": {"obrigado de coracao (Pedrinho)": "lv_0_20261102155438 34,7-37,4",
                  "Adrielly tem EB": "IMG_3868 / IMG_5709",
                  "a pele arde, sangra (Adrielly)": "IMG_4227 0,7-6,25",
                  "quase nada de curativo na semana (Adrielly)": "IMG_6452 (30/10) 3,6-10,2"},
        "saida": os.path.join(RAIZ, "EDITADOS", "RENDERIZADOS", "PAGINA DE OBRIGADO",
                              "Obrigado Pedrinho - doe tambem para a Adrielly.mp4"),
        "saida_fixa": True,
        # 06/11: o usuario nao quer a Adrielly falando na tela; a voz dela continua, com b-roll das feridas por cima
        "broll": broll_adrielly(base),
    }
    os.makedirs(os.path.join(PASTA, "render"), exist_ok=True)
    json.dump(p, open(os.path.join(PASTA, "plano.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"plano ok: {total:.1f}s, {len(base)} cenas, Adrielly a partir de {t_adr:.1f}s, tela final em {fim_de}s")


main()
