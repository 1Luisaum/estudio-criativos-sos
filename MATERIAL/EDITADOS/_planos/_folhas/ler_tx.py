"""Mostra uma transcricao em frases: [inicio] falante: texto (cada palavra com o tempo de inicio)."""
import json, sys

sys.stdout.reconfigure(encoding="utf-8")
for path in sys.argv[1:]:
    words = [w for w in json.load(open(path, encoding="utf-8"))["words"] if w.get("type") == "word"]
    print(f"\n##### {path.split(chr(92))[-1]}")
    linha, ini, spk, fim = [], None, None, 0
    for w in words:
        quebra = linha and (w.get("speaker_id") != spk or w["start"] - fim > 0.7 or linha[-1][-1:] in ".?!")
        if quebra:
            print(f"[{ini:6.2f}] {spk[-1] if spk else '?'}: " + " ".join(linha))
            linha = []
        if not linha:
            ini, spk = w["start"], w.get("speaker_id")
        linha.append(f"{w['text']}|{w['start']:.2f}")
        fim = w["end"]
    if linha:
        print(f"[{ini:6.2f}] {spk[-1] if spk else '?'}: " + " ".join(linha))
