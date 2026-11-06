import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
a = s.index("def make_audio(P, plano):")
b = s.index("# ---------- texto com emoji ----------")
new = '''def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key:
        return key
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as reg:
            return winreg.QueryValueEx(reg, "ELEVENLABS_API_KEY")[0]
    except OSError:
        sys.exit("Falta a variavel ELEVENLABS_API_KEY (ou coloque os mp3 em audio_br).")


def make_audio(P, plano):
    """Gera so as falas que faltam, pela API REST (o SDK do Python do sistema esta quebrado)."""
    import urllib.error
    import urllib.request
    os.makedirs(P + "/audio", exist_ok=True)
    need = [k for k in plano.get("narracao", {}) if not os.path.exists(apath(P, k))]
    if not need:
        return
    key = api_key()
    voz = plano.get("voz", {})
    vid = voz.get("voice_id", "XrExE9yKIg1WjnnlVkGX")
    for k in need:
        body = json.dumps({"text": plano["narracao"][k],
                           "model_id": voz.get("model_id", "eleven_multilingual_v2"),
                           "voice_settings": {"stability": 0.55, "similarity_boost": 0.75, "style": 0.25,
                                              "use_speaker_boost": True}}).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128", data=body,
            headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                open(f"{P}/audio/{k}.mp3", "wb").write(r.read())
        except urllib.error.HTTPError as e:
            sys.exit(f"ElevenLabs recusou {k}: {e.code} {e.read()[:300]!r}")
        print("narracao", k)


'''
s = s[:a] + new + s[b:]
open(p, "w", encoding="utf-8").write(s)
print("ok", p)
