"""Confere o MP4 final do estilo narrado: buracos no audio e fala (real + narrador) x legenda.

Uso: python -I conferir.py <final.mp4> <linha_do_tempo.json>
"""
import difflib, json, os, re, subprocess, sys, tempfile, unicodedata, urllib.error, urllib.request, uuid, winreg


def key():
    if os.environ.get("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"]
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
        return winreg.QueryValueEx(k, "ELEVENLABS_API_KEY")[0]


def transcribe(media):
    wav = os.path.join(tempfile.mkdtemp(), "a.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", media, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    b = uuid.uuid4().hex
    fields = [("model_id", "scribe_v2"), ("language_code", "por"), ("timestamps_granularity", "word")]
    body = b"".join(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in fields)
    body += (f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="a.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode()
             + open(wav, "rb").read() + f"\r\n--{b}--\r\n".encode())
    req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=body, method="POST",
                                 headers={"xi-api-key": key(), "Content-Type": f"multipart/form-data; boundary={b}"})
    return json.loads(urllib.request.urlopen(req, timeout=300).read().decode("utf-8"))


def norm(s):
    s = unicodedata.normalize("NFD", s.upper())
    return re.sub(r"[^A-Z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def same(a, b):
    a, b = norm(a), norm(b)
    num = {"QUARENTA": "40", "TRINTA": "30", "CINCO": "5"}
    a, b = num.get(a, a), num.get(b, b)
    return a == b or a.rstrip("S") == b.rstrip("S") or (len(a) > 2 and len(b) > 2 and (a.startswith(b) or b.startswith(a))) \
        or difflib.SequenceMatcher(None, a, b).ratio() >= 0.75


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    video, tl = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "packet=pts_time,duration_time",
                        "-of", "csv=p=0", video], capture_output=True, text=True)
    pk = [tuple(map(float, l.split(",")[:2])) for l in r.stdout.split() if l]
    holes = [(round(x[0], 2), round(y[0], 2)) for x, y in zip(pk, pk[1:]) if y[0] - x[0] - x[1] > 0.02]
    print(f"[audio] {pk[-1][0] + pk[-1][1]:.2f}s, buracos: {holes or 'nenhum'}")
    spoken = [w for w in transcribe(video)["words"] if w["type"] == "word"]
    cap = [(w[0], w[2]) for w in tl["palavras"]]
    miss = [f"  {w['start']:6.2f}s falou '{w['text']}'" for w in spoken if len(norm(w["text"])) > 2
            and not any(abs(t - w["start"]) <= 0.35 and same(w["text"], c) for t, c in cap)]
    orphan = [f"  {t:6.2f}s legenda '{c}' sem fala" for t, c in cap if len(norm(c)) > 2
              and not any(abs(t - w["start"]) <= 0.5 and same(w["text"], c) for w in spoken)]
    print(f"[sincronia] {len(spoken)} faladas / {len(cap)} na legenda; {len(miss)} faladas sem legenda, {len(orphan)} legendas sem fala")
    for l in miss[:20] + orphan[:20]:
        print(l)
    bad = len(holes) + (len(miss) + len(orphan) if len(miss) + len(orphan) > 4 else 0)
    print("RESULTADO:", "OK" if not bad else f"{bad} problema(s)",
          f"({len(miss) + len(orphan)} diferenca(s) isolada(s))" if not bad and miss + orphan else "")


if __name__ == "__main__":
    main()
