"""Monta o criativo "Caixas Aspas" (skill criativo-caixas-aspas-ong).

Corpo: a fala real da crianca cortada sem pausas, b-roll por cima, caixa no alto e caixa de valor
embaixo paradas (visual copiado dos anuncios validados da Causas do Bem, 26/10/2026). Veja SKILL.md.

Uso:  python -I caixas.py "<pasta do plano>\plano.json"
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
import comum as C  # noqa: E402
import nucleo as N  # noqa: E402

GAP = 0.18      # respiro entre frases
LEAD = 0.05     # a voz entra 50 ms depois do corte de imagem


def words_of(tx):
    d = json.load(open(tx, encoding="utf-8"))
    return [w for w in d["words"] if w.get("type") == "word"]


def resolve(words, a, b):
    """[inicio da 1a palavra, inicio da ultima] -> (t0, t1, palavras) com margens."""
    sel = [w for w in words if a - 0.02 <= w["start"] <= b + 0.02]
    if not sel:
        sys.exit(f"nenhuma palavra entre {a} e {b}")
    return max(0.0, sel[0]["start"] - 0.06), sel[-1]["end"] + 0.10, sel


def cut_audio(WK, frase):
    """Corta e junta os trechos da fala, limpa e nivela. Devolve (wav, duracao, palavras com tempo)."""
    words = words_of(frase["tx"])
    parts, timed, acc = [], [], 0.0
    for i, (a, b) in enumerate(frase["cortes"]):
        t0, t1, sel = resolve(words, a, b)
        wav = f"{WK}/{frase['nome']}_p{i}.wav"
        N.run(["ffmpeg", "-y", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", frase["fonte"], "-vn",
               "-ac", "1", "-ar", "48000", "-af", "highpass=f=80,afftdn=nf=-25,afade=t=in:d=0.02,"
               f"afade=t=out:st={max(0.0, t1 - t0 - 0.04):.3f}:d=0.04", wav])
        parts.append(wav)
        for w in sel:
            timed.append((acc + w["start"] - t0, acc + w["end"] - t0, w["text"]))
        acc += t1 - t0
    lst = f"{WK}/{frase['nome']}_partes.txt"
    with open(lst, "w", encoding="utf-8") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    out = f"{WK}/{frase['nome']}.wav"
    N.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
           "-af", "loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", "48000", out])
    return out, acc, timed


def chunks_real(timed, size=3):
    """Blocos de ate 3 palavras com o tempo real (cada bloco fica ate o inicio do proximo)."""
    groups = [timed[i:i + size] for i in range(0, len(timed), size)]
    out = []
    for gi, g in enumerate(groups):
        a = g[0][0] + LEAD
        b = (groups[gi + 1][0][0] + LEAD) if gi + 1 < len(groups) else g[-1][1] + LEAD + 0.15
        out.append((a, b, [t.upper() for _, _, t in g]))
    return out


ESTILO = "CAIXAS ASPAS"  # pasta de saida em EDITADOS


def narr_audio(WK, P, plano, fr):
    """Frase de narrador (gancho urgente): gera a fala no ElevenLabs se faltar (sem respiro) e usa inteira."""
    N.make_audio(P, {"narracao": {fr["narracao"]: plano["narracao"][fr["narracao"]]}, "voz": plano.get("voz", {})})
    mp3 = f"{P}/audio/{fr['narracao']}.mp3"
    out = f"{WK}/{fr['nome']}.wav"
    N.run(["ffmpeg", "-y", "-i", mp3, "-af", "loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", "48000", "-ac", "1", out])
    texto = C.para_tela(plano["narracao"][fr["narracao"]])
    return out, N.dur(out), [(0, 0, w) for w in texto.split()]


def main():
    plano_path = os.path.abspath(sys.argv[1])
    P = os.path.dirname(plano_path).replace("\\", "/")
    plano = json.load(open(plano_path, encoding="utf-8-sig"))
    saida = C.destino(plano_path, plano, plano.get("estilo_pasta", ESTILO))
    WK = P + "/render"
    os.makedirs(WK, exist_ok=True)
    manual = plano.get("zonas_protegidas", [])

    segs = []
    for fr in plano["frases"]:
        wav, a, timed = narr_audio(WK, P, plano, fr) if fr.get("narracao") else cut_audio(WK, fr)
        d = a + LEAD + (plano.get("respiro", GAP) if not fr.get("final") else plano.get("final_extra", 1.4))
        words_t = chunks_real(timed)
        N.render_block(WK, plano, fr, d, words_t, f"{WK}/{fr['nome']}.mp4", manual)
        segs.append({"nome": fr["nome"], "wav": wav, "d": d,
                     "texto": " ".join(t for _, _, t in timed)})
        print("ok", fr["nome"], f"{d:.2f}s", segs[-1]["texto"])

    with open(WK + "/lista.txt", "w", encoding="utf-8") as f:
        for s in segs:
            f.write(f"file '{WK}/{s['nome']}.mp4'\n")
    N.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", WK + "/lista.txt", "-c", "copy", WK + "/video.mp4"])

    cmd, parts, t = ["ffmpeg", "-y"], [], 0.0
    for i, s in enumerate(segs):
        cmd += ["-i", s["wav"]]
        parts.append(f"[{i}:a]adelay={int((t + LEAD) * 1000)}:all=1[a{i}]")
        t += s["d"]
    total, n = t, len(segs)
    mix = "".join(f"[a{i}]" for i in range(n))
    if plano.get("musica"):
        cmd += ["-stream_loop", "-1", "-i", plano["musica"]]
        vol = plano.get("musica_volume", 0.10)
        parts.append(f"[{n}:a]atrim=0:{total:.3f},volume={vol},afade=t=out:st={total - 1.8:.3f}:d=1.8[m]")
        mix += "[m]"
        n += 1
    parts.append(f"{mix}amix=inputs={n}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    N.run(cmd + ["-filter_complex", ";".join(parts), "-map", "[aout]", "-t", f"{total:.3f}",
                 "-c:a", "pcm_s16le", WK + "/audio.wav"])
    N.run(["ffmpeg", "-y", "-i", WK + "/video.mp4", "-i", WK + "/audio.wav", "-map", "0:v", "-map", "1:a",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", saida])
    json.dump({"total": total, "blocos": [{"nome": s["nome"], "d": s["d"], "texto": s["texto"]} for s in segs]},
              open(P + "/linha_do_tempo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    import marca  # logo SOS andando pela tela, opacidade baixa (26/10/2026)
    marca.no_fim(plano, saida)
    print(f"OK {saida} duracao={total:.1f}s")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
