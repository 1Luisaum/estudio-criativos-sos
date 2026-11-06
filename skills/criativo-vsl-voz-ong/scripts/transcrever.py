"""Transcreve um video/audio com ElevenLabs Scribe v2 (timestamps por palavra, vicios mantidos).

Usa a API REST direto porque o SDK Python instalado nesta maquina esta quebrado.
A chave vem de ELEVENLABS_API_KEY no ambiente ou, se faltar, das variaveis do usuario do Windows.

Uso: python -I transcrever.py <video_ou_audio> <saida.json> [--keyterms "Pedrinho,curativo"] [--from 24]
"""
import argparse, json, os, subprocess, sys, tempfile, urllib.error, urllib.request, uuid

DEFAULT_KEYTERMS = ["Pedrinho", "Adrielly", "curativo", "curativos", "epidermólise bolhosa", "anjo"]


def api_key():
    k = os.environ.get("ELEVENLABS_API_KEY")
    if k:
        return k
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            return winreg.QueryValueEx(key, "ELEVENLABS_API_KEY")[0]
    except OSError:
        sys.exit("ELEVENLABS_API_KEY nao encontrada (nem no ambiente nem nas variaveis do usuario).")


def to_wav(media, wav, start=0.0):
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if start:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-i", media, "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav]
    subprocess.run(cmd, check=True)


def transcribe(media, keyterms=DEFAULT_KEYTERMS, start=0.0, diarize=False):
    """Devolve o JSON do Scribe. Com start>0, os tempos ja vem somados ao offset."""
    tmp = tempfile.mkdtemp(prefix="stt_")
    wav = os.path.join(tmp, "audio.wav")
    to_wav(media, wav, start)
    fields = [("model_id", "scribe_v2"), ("language_code", "por"), ("timestamps_granularity", "word"),
              ("tag_audio_events", "true")]
    fields += [("keyterms", t) for t in keyterms]
    if diarize:   # marca speaker_0, speaker_1... em cada palavra (videos com crianca e mae falando)
        fields.append(("diarize", "true"))
    b = uuid.uuid4().hex
    parts = [f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in fields]
    with open(wav, "rb") as fh:
        parts.append(f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="audio.wav"\r\n'
                     f'Content-Type: audio/wav\r\n\r\n'.encode() + fh.read() + b"\r\n")
    parts.append(f"--{b}--\r\n".encode())
    req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=b"".join(parts), method="POST",
                                 headers={"xi-api-key": api_key(),
                                          "Content-Type": f"multipart/form-data; boundary={b}"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"Scribe HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:400]}")
    if start:
        for w in data.get("words", []):
            w["start"] += start
            w["end"] += start
    return data


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("media")
    ap.add_argument("out")
    ap.add_argument("--keyterms", default=",".join(DEFAULT_KEYTERMS))
    ap.add_argument("--from", dest="start", type=float, default=0.0)
    ap.add_argument("--diarize", action="store_true", help="identifica quem fala (speaker_id em cada palavra)")
    a = ap.parse_args()
    data = transcribe(a.media, [t.strip() for t in a.keyterms.split(",") if t.strip()], a.start, a.diarize)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    sys.stdout.reconfigure(encoding="utf-8")
    print(data.get("text", ""))
