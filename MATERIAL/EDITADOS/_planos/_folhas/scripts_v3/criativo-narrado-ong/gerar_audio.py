"""Gera a narracao (com tempo por palavra) e os efeitos sonoros no ElevenLabs.

Uso: python -I gerar_audio.py <roteiro.json> <pasta_saida>
roteiro.json: {"voice_id": "...", "narracao": {"N1": "texto", ...}, "efeitos": {"boom": {"text": "...", "dur": 2.0}}}
"""
import base64, json, os, sys, urllib.error, urllib.request, winreg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
import comum as C  # noqa: E402

with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
    KEY = os.environ.get("ELEVENLABS_API_KEY") or winreg.QueryValueEx(k, "ELEVENLABS_API_KEY")[0]


def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:400]}")


def words_from_alignment(al):
    """Junta os caracteres em palavras com inicio/fim."""
    words, cur, t0, t1 = [], "", None, None
    for ch, s, e in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                words.append({"text": cur, "start": t0, "end": t1})
            cur, t0 = "", None
            continue
        if t0 is None:
            t0 = s
        cur += ch
        t1 = e
    if cur:
        words.append({"text": cur, "start": t0, "end": t1})
    return words


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cfg = json.load(open(sys.argv[1], encoding="utf-8-sig"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    vs = cfg.get("voice_settings", {"stability": 0.45, "similarity_boost": 0.8, "style": 0.3,
                                    "use_speaker_boost": True, "speed": 0.95})
    os.makedirs(os.path.join(out, "raw"), exist_ok=True)
    for name, text in cfg["narracao"].items():
        mp3, js = os.path.join(out, f"{name}.mp3"), os.path.join(out, f"{name}.json")
        raw_mp3, raw_js = os.path.join(out, "raw", f"{name}.mp3"), os.path.join(out, "raw", f"{name}.json")
        if not os.path.exists(raw_mp3):
            if os.path.exists(mp3) and os.path.exists(js):  # fala antiga, gerada antes de tirar o respiro
                os.replace(mp3, raw_mp3)
                os.replace(js, raw_js)
            else:
                r = json.loads(post(f"https://api.elevenlabs.io/v1/text-to-speech/{cfg['voice_id']}/with-timestamps"
                                    "?output_format=mp3_44100_128",
                                    {"text": C.para_voz(text), "model_id": cfg.get("model_id", "eleven_multilingual_v2"),
                                     "voice_settings": vs}))
                open(raw_mp3, "wb").write(base64.b64decode(r["audio_base64"]))
                json.dump({"text": C.para_tela(text), "words": C.juntar_sos(words_from_alignment(r["alignment"]))},
                          open(raw_js, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if not os.path.exists(mp3):  # versao usada no video: sem respiro, com o tempo das palavras reajustado
            words = C.sem_respiro(raw_mp3, mp3, json.load(open(raw_js, encoding="utf-8"))["words"])
            json.dump({"text": C.para_tela(text), "words": words}, open(js, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            print(f"{name}: {words[-1]['end']:.2f}s  {text}")
    for name, fx in cfg.get("efeitos", {}).items():
        mp3 = os.path.join(out, f"fx_{name}.mp3")
        if os.path.exists(mp3):
            continue
        open(mp3, "wb").write(post("https://api.elevenlabs.io/v1/sound-generation",
                                   {"text": fx["text"], "duration_seconds": fx["dur"], "prompt_influence": 0.6}))
        print(f"fx_{name} ok")


if __name__ == "__main__":
    main()

