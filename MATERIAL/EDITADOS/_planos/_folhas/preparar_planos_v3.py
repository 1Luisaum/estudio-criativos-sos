"""Prepara os planos para a rodada v3 (26/10/2026):
- conserta caminhos de brutos renomeados (ganharam "_" no fim);
- narrador brasileiro em todos os videos com narrador (Kaique no narrado, Leonardo na reportagem e na lista);
- tira "Doar agora" que sobrou nos narrados antigos;
- apaga as falas que precisam ser regravadas (voz trocada ou com "gaze");
- lista: produtos com mais tempo na tela (0,45 s depois da fala), resto com 0,08 s; tira as copias de audio_br da rodada anterior.
"""
import glob, json, os, shutil

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAIZ = os.path.dirname(os.path.dirname(P))
BR = os.path.join(RAIZ, "VÍDEOS PARA EDITAR").replace("\\", "/")
KAIQUE, LEONARDO = "Hmn4B9B77pf6ttydteJ8", "4XmhZ74tBbUVCXIYNMMo"
BRUTOS = glob.glob(os.path.join(BR, "*.mp4"))


def conserta(v):
    if isinstance(v, str) and "VÍDEOS PARA EDITAR" in v and v.lower().endswith(".mp4") and not os.path.exists(v):
        base = os.path.splitext(os.path.basename(v))[0]
        hit = [b for b in BRUTOS if os.path.basename(b).startswith(base)]
        return hit[0].replace("\\", "/") if hit else v
    if isinstance(v, list):
        return [conserta(x) for x in v]
    if isinstance(v, dict):
        return {k: conserta(x) for k, x in v.items()}
    return v


def apaga(d, chaves):
    for k in chaves:
        for f in glob.glob(os.path.join(d, "audio", f"{k}.*")) + glob.glob(os.path.join(d, "audio", "raw", f"{k}.*")):
            os.remove(f)


for d in sorted(glob.glob(os.path.join(P, "Pedrinho_*"))):
    nome = os.path.basename(d)
    f = os.path.join(d, "plano.json")
    if not os.path.exists(f):
        continue
    p = conserta(json.load(open(f, encoding="utf-8-sig")))
    for z in p.get("zonas_protegidas", []):  # o nome do arquivo tambem mudou
        hit = [b for b in BRUTOS if os.path.basename(b).startswith(os.path.splitext(z["arquivo"])[0])]
        if hit:
            z["arquivo"] = os.path.basename(hit[0])
    if "_narrado_" in nome or nome == "Pedrinho_narrado_v1":
        ra = os.path.join(d, "roteiro_audio.json")
        r = json.load(open(ra, encoding="utf-8-sig"))
        if r.get("voice_id") != KAIQUE:
            r["voice_id"] = KAIQUE
            apaga(d, list(r["narracao"]))
        for k, t in r["narracao"].items():
            if "Doar agora" in t:
                r["narracao"][k] = t.replace("Doar agora", "Saiba mais")
                apaga(d, [k])
            elif "gaze" in t.lower():
                apaga(d, [k])
        json.dump(r, open(ra, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        for b in p["blocks"]:
            if b.get("txt"):
                b["txt"] = b["txt"].replace("Doar agora", "Saiba mais")
            if b.get("button") == "DOAR AGORA":
                b["button"] = "SAIBA MAIS"
    elif "_reportagem_" in nome or "_lista_" in nome:
        if p.get("voz", {}).get("voice_id") != LEONARDO:
            p["voz"] = {"voice_id": LEONARDO, "model_id": "eleven_multilingual_v2"}
            apaga(d, list(p["narracao"]))
        apaga(d, [k for k, t in p["narracao"].items() if "gaze" in t.lower()])
        if "_lista_" in nome:
            shutil.rmtree(os.path.join(d, "audio_br"), ignore_errors=True)
            for b in p["blocos"]:
                b["pausa"] = 1.6 if b.get("final") else (0.45 if b["nome"].startswith("i") else 0.08)
    json.dump(p, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok", nome)
