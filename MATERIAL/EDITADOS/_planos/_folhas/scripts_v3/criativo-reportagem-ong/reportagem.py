"""Monta um criativo no estilo "Reportagem": parece uma materia jornalistica sobre a crianca.

Uso:  python -I reportagem.py "<pasta do plano>\\plano.json"

Estrutura de reportagem de TV adaptada ao vertical:
- OFF: narracao do reporter (ElevenLabs) sobre b-roll;
- SONORA: a crianca ou a mae falando com o PROPRIO audio, com tarja de nome (GC);
- manchete fixa em caixa branca com etiqueta vermelha (na zona segura, nunca em cima de rosto);
- selo "REPORTAGEM ESPECIAL • <marca>" pequeno na zona segura;
- legenda de jornal (texto branco em faixa preta), frase curta;
- etiqueta de valor e tela final "Toque em SAIBA MAIS" (o botao do anuncio e Saiba mais).
NUNCA imitar emissora real (nome, logo, vinheta): a marca do selo e da ONG.

Blocos do plano:
  {"nome": "b01", "tipo": "off", "fala": "OFF1", "cenas": [[video, inicio], ...] | "foto": img}
  {"nome": "b02", "tipo": "sonora", "fonte": video, "tx": transcricao.json,
   "cortes": [[inicio_1a_palavra, inicio_ultima], ...], "gc": ["NOME", "descricao"]}
  opcionais: "etiqueta": true, "final": true, "pausa": 0.3
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
import comum as C  # noqa: E402
import nucleo as N  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

W, H, FPS = N.W, N.H, N.FPS
F = "C:/Windows/Fonts/"
BOLD, BLACK, EMOJI = F + "segoeuib.ttf", F + "seguibl.ttf", F + "seguiemj.ttf"
RED, NAVY = (204, 16, 30), (16, 24, 48)
LEAD = 0.08
TOPO_MAX = 470  # a manchete fica no alto da tela (y 290 a 470); nunca no meio


# ---------- grafismos de jornal ----------
def title_img(lines, tag="ESPECIAL", maxw=860):
    """Manchete: etiqueta vermelha + caixa branca com texto preto (estilo materia em video vertical)."""
    size = 54
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while True:
        f, fe = ImageFont.truetype(BLACK, size), ImageFont.truetype(EMOJI, int(size * 0.8))
        if max(N.text_w(tmp, ln, f, fe) for ln in lines) <= maxw - 40 or size <= 30:
            break
        size -= 2
    lh = int(size * 1.28)
    ft = ImageFont.truetype(BLACK, 34)
    tag_w = int(tmp.textlength(tag, font=ft)) + 36
    box_w = int(max(N.text_w(tmp, ln, f, fe) for ln in lines)) + 48
    x0 = (W - box_w) // 2
    h = 52 + lh * len(lines) + 26
    im = Image.new("RGBA", (W, h + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([x0, 52, x0 + box_w, h], fill=(255, 255, 255, 250))
    d.rectangle([x0, 52, x0 + 10, h], fill=RED)
    d.rectangle([x0, 4, x0 + tag_w, 52], fill=RED)
    d.text((x0 + 18, 8), tag, font=ft, fill="white")
    for i, ln in enumerate(lines):
        N.draw_text(d, x0 + 30, 52 + 12 + i * lh, ln, f, fe, (15, 15, 15))
    return im


def selo_img(marca):
    """Selo pequeno: REPORTAGEM ESPECIAL • marca da ONG."""
    f1, f2 = ImageFont.truetype(BLACK, 30), ImageFont.truetype(BOLD, 30)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    a, b = "REPORTAGEM ESPECIAL", f"  {marca}"
    wa, wb = int(tmp.textlength(a, font=f1)), int(tmp.textlength(b, font=f2))
    im = Image.new("RGBA", (wa + wb + 60, 56), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, wa + 30, 56], fill=RED)
    d.rectangle([wa + 30, 0, wa + wb + 60, 56], fill=(16, 24, 48, 235))
    d.text((15, 9), a, font=f1, fill="white")
    d.text((wa + 30, 9), b, font=f2, fill="white")
    return im


def gc_img(name, desc):
    """Tarja de nome (GC): faixa vermelha com o nome e faixa branca com a descricao."""
    f1, f2 = ImageFont.truetype(BLACK, 46), ImageFont.truetype(BOLD, 36)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    w1, w2 = int(tmp.textlength(name, font=f1)) + 44, int(tmp.textlength(desc, font=f2)) + 44
    im = Image.new("RGBA", (W, 136), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 70
    d.rectangle([x, 0, x + w1, 70], fill=RED)
    d.text((x + 22, 6), name, font=f1, fill="white")
    d.rectangle([x, 70, x + w2, 130], fill=(255, 255, 255, 245))
    d.text((x + 22, 76), desc, font=f2, fill=NAVY)
    return im


def caption_img(text, size=52):
    """Legenda de jornal: texto branco em faixa preta translucida, ate 2 linhas."""
    f = ImageFont.truetype(BOLD, size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tmp.textlength(t, font=f) <= 900:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    lh = size + 20
    im = Image.new("RGBA", (W, lh * len(lines) + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        x0 = (W - tw) / 2
        d.rectangle([x0 - 18, i * lh + 4, x0 + tw + 18, i * lh + lh + 4], fill=(0, 0, 0, 185))
        d.text((x0, i * lh + 8), ln, font=f, fill="white")
    return im


def chunks_text(words_t, max_words=6):
    """Junta palavras com tempo em frases curtas de jornal (quebra em pontuacao ou a cada 6 palavras)."""
    out, cur = [], []
    for w in words_t:
        cur.append(w)
        if len(cur) >= max_words or w[2].endswith((".", ",", "?", "!", ":")):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    res = []
    for i, g in enumerate(out):
        a = g[0][0]
        b = out[i + 1][0][0] if i + 1 < len(out) else g[-1][1] + 0.2
        res.append((a, b, " ".join(x[2] for x in g).strip(" ,")))
    return res


def approx_words(text, t0, t1):
    """Tempo aproximado por palavra para a narracao gerada (sem transcricao)."""
    ws = text.split()
    weights = [len(w) + 2 for w in ws]
    tot, t, out = sum(weights), t0, []
    for w, wt in zip(ws, weights):
        dt = (t1 - t0) * wt / tot
        out.append((t, t + dt, w))
        t += dt
    return out


# ---------- audio/video da sonora ----------
def cut_sonora(WK, b):
    """Corta a fala real (video + audio juntos) e devolve (clip.mp4, wav limpo, duracao, palavras)."""
    words = [w for w in json.load(open(b["tx"], encoding="utf-8"))["words"] if w.get("type") == "word"]
    vparts, aparts, timed, acc = [], [], [], 0.0
    for i, (a, z) in enumerate(b["cortes"]):
        sel = [w for w in words if a - 0.02 <= w["start"] <= z + 0.02]
        t0, t1 = max(0.0, sel[0]["start"] - 0.06), sel[-1]["end"] + 0.10
        v = f"{WK}/{b['nome']}_v{i}.mp4"
        tv = t1 - t0 + (1.6 if i == len(b["cortes"]) - 1 else 0.0)
        N.run(["ffmpeg", "-y", "-ss", f"{t0:.3f}", "-t", f"{tv:.3f}", "-i", b["fonte"],
               "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
               "-an", *N.ENC, v])
        wv = f"{WK}/{b['nome']}_a{i}.wav"
        N.run(["ffmpeg", "-y", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", b["fonte"], "-vn", "-ac", "1",
               "-ar", "48000", "-af", f"highpass=f=80,afftdn=nf=-25,afade=t=in:d=0.02,"
               f"afade=t=out:st={max(0.0, t1 - t0 - 0.04):.3f}:d=0.04", wv])
        vparts.append(v)
        aparts.append(wv)
        for w in sel:
            timed.append((acc + w["start"] - t0, acc + w["end"] - t0, w["text"]))
        acc += t1 - t0
    for kind, parts in (("v", vparts), ("a", aparts)):
        with open(f"{WK}/{b['nome']}_{kind}.txt", "w", encoding="utf-8") as f:
            for p in parts:
                f.write(f"file '{p}'\n")
    clip, wav = f"{WK}/{b['nome']}_clip.mp4", f"{WK}/{b['nome']}.wav"
    N.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"{WK}/{b['nome']}_v.txt", "-c", "copy", clip])
    N.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"{WK}/{b['nome']}_a.txt",
           "-af", "loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", "48000", wav])
    return clip, wav, acc, timed


# ---------- bloco ----------
def render_block(WK, plano, b, d, caps, out, manual, clip=None):
    """Sempre tela cheia. Selo+manchete na zona segura e nunca em rosto (se o rosto ocupa a zona
    segura inteira, somem so naquela cena). A tarja (GC) procura lugar livre de rosto."""
    # selo e etiqueta juntos na manchete (ocupa menos altura): "REPORTAGEM ESPECIAL • SOS HUMAN HELP"
    title = title_img(plano["manchete"], f"REPORTAGEM ESPECIAL • {plano.get('marca', 'SOS HUMAN HELP')}")
    title_small = N.smaller(title, 0.8)
    final = b.get("final", False)
    pl = N.pill_img(plano["etiqueta_final"] if final else plano["etiqueta"])
    show_pill = b.get("etiqueta", False) or final
    gc = gc_img(*b["gc"]) if b.get("gc") else None
    cmd, fc, windows = ["ffmpeg", "-y"], [], []
    card = b.get("foto")
    shots = [[clip, 0.0]] if clip else (b.get("cenas") or [])
    if card:
        png, chain, fb = N.photo_input(WK, b, d, card)
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", png]
        fc.append(chain)
        windows.append([0.0, d, fb])
        n_in = 1
    else:
        each = d / len(shots)
        labels = []
        for i, scene in enumerate(shots):
            src, st = scene[0], scene[1]
            fb = N.faces(WK, src, st, min(each, N.dur(src) - st - 0.05) if clip else each, f"{b['nome']}_{i}")
            key = b.get("fonte") if clip else src
            st_key = b["cortes"][0][0] if clip else st
            fb += [tuple(z["caixa"]) for z in manual
                   if os.path.basename(z["arquivo"]) == os.path.basename(key) and abs(z["inicio"] - st_key) < 0.01]
            windows.append([i * each, (i + 1) * each, fb])
            cmd += ["-ss", f"{st:.2f}", "-t", f"{each + 0.1:.3f}", "-i", src]
            fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                      f"setsar=1,fps={FPS}{N.PB if (not clip and N.is_pb(b, scene)) else ''},"
                      f"tpad=stop_mode=clone:stop_duration=1,"
                      f"trim=duration={each:.3f},setpts=PTS-STARTPTS[b{i}]")
            labels.append(f"[b{i}]")
        fc.append("".join(labels) + f"concat=n={len(shots)}:v=1:a=0[bg]")
        n_in = len(shots)

    cap_h, gc_h = 170, gc.height if gc else 0
    plans = []
    for _, _, busy in windows:
        taken = list(busy)
        y_pl = None
        if show_pill:
            y_pl = N.place(pl.height, list(range(N.SAFE_BOTTOM - pl.height, 860, -10)), taken)  # zona segura
            taken.append((0, y_pl, W, y_pl + pl.height))
        y_cap = N.place(cap_h, sorted(range(700, N.SAFE_BOTTOM - cap_h + 1, 10), key=lambda y: abs(y - 1060)), taken)
        taken.append((0, y_cap, W, y_cap + cap_h))
        y_sel, use = None, title
        for cand in (title, title_small):  # normal; se nao couber, 80%; se ainda nao, some na cena
            xr = N.xrange_of(cand)
            y = N.place(cand.height, list(range(N.SAFE_TOP, TOPO_MAX + 1, 10)), taken, xr)
            if not N.hits(y, cand.height, taken, xr):
                y_sel, use = y, cand
                taken.append((xr[0], y, xr[1], y + cand.height))
                break
        y_gc = None
        if gc:
            xr = N.xrange_of(gc)
            cands = sorted(range(N.SAFE_TOP, N.SAFE_BOTTOM - gc_h + 1, 10), key=lambda y: -y)  # so na zona segura
            y_gc = N.place(gc_h, cands, taken, xr)
            if N.hits(y_gc, gc_h, taken, xr):
                y_gc = None
        plans.append((y_sel, y_pl, y_cap, y_gc, use))
        print(f"  {b['nome']}: manchete={'ESCONDIDA (rosto)' if y_sel is None else y_sel} "
              f"gc={'-' if not gc else ('ESCONDIDA (rosto)' if y_gc is None else y_gc)} legenda={y_cap} etiqueta={y_pl}")

    last, k = "[bg]", n_in
    for wi, ((t0, t1, _), (y_sel, y_pl, y_cap, y_gc, use)) in enumerate(zip(windows, plans)):
        base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if y_sel is not None:
            base.alpha_composite(use, (0, y_sel))
        if y_pl is not None:
            base.alpha_composite(pl, (0, y_pl))
        if y_gc is not None:
            base.alpha_composite(gc, (0, y_gc))
        png = f"{WK}/{b['nome']}_base{wi}.png"
        base.save(png)
        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", png]
        fc.append(f"{last}[{k}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[o{k}]")
        last, k = f"[o{k}]", k + 1
        for j, (a, z, txt) in enumerate(caps):
            a2, b2 = max(a, t0), min(z, t1)
            if b2 - a2 < 0.02:
                continue
            cp = f"{WK}/{b['nome']}_c{j}.png"
            caption_img(txt).save(cp)
            cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", cp]
            fc.append(f"{last}[{k}:v]overlay=0:{y_cap}:enable='between(t,{a2:.3f},{b2:.3f})'[o{k}]")
            last, k = f"[o{k}]", k + 1
    N.run(cmd + ["-filter_complex", ";".join(fc), "-map", last, "-an", *N.ENC, out])


def main():
    plano_path = os.path.abspath(sys.argv[1])
    P = os.path.dirname(plano_path).replace("\\", "/")
    plano = json.load(open(plano_path, encoding="utf-8-sig"))
    saida = C.destino(plano_path, plano, "reportagem")
    WK = P + "/render"
    os.makedirs(WK, exist_ok=True)
    N.make_audio(P, plano)
    plano["narracao"] = {k: C.para_tela(v) for k, v in plano.get("narracao", {}).items()}
    manual = plano.get("zonas_protegidas", [])

    segs = []
    for b in plano["blocos"]:
        pad = b.get("pausa", 1.4 if b.get("final") else 0.3)
        if b["tipo"] == "sonora":
            clip, wav, a, timed = cut_sonora(WK, b)
            d = a + LEAD + pad
            caps = chunks_text([(s + LEAD, e + LEAD, t) for s, e, t in timed])
            render_block(WK, plano, b, d, caps, f"{WK}/{b['nome']}.mp4", manual, clip=clip)
            texto = " ".join(t for _, _, t in timed)
        else:
            wav = N.apath(P, b["fala"])
            a = N.dur(wav)
            d = a + LEAD + pad
            caps = chunks_text(approx_words(plano["narracao"][b["fala"]], LEAD, LEAD + max(0.4, a - 0.1)))
            render_block(WK, plano, b, d, caps, f"{WK}/{b['nome']}.mp4", manual)
            texto = plano["narracao"][b["fala"]]
        segs.append({"nome": b["nome"], "tipo": b["tipo"], "wav": wav, "d": d, "texto": texto})
        print("ok", b["nome"], b["tipo"], f"{d:.2f}s", texto)

    with open(WK + "/lista.txt", "w", encoding="utf-8") as f:
        for s in segs:
            f.write(f"file '{WK}/{s['nome']}.mp4'\n")
    N.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", WK + "/lista.txt", "-c", "copy", WK + "/video.mp4"])

    cmd, parts, t = ["ffmpeg", "-y"], [], 0.0
    for i, s in enumerate(segs):
        cmd += ["-i", s["wav"]]
        vol = plano.get("volume_sonora", 1.0) if s["tipo"] == "sonora" else 1.0
        parts.append(f"[{i}:a]volume={vol},adelay={int((t + LEAD) * 1000)}:all=1[a{i}]")
        t += s["d"]
    total, n = t, len(segs)
    mix = "".join(f"[a{i}]" for i in range(n))
    if plano.get("musica"):
        cmd += ["-stream_loop", "-1", "-i", plano["musica"]]
        parts.append(f"[{n}:a]atrim=0:{total:.3f},volume={plano.get('musica_volume', 0.08)},"
                     f"afade=t=out:st={total - 1.8:.3f}:d=1.8[m]")
        mix += "[m]"
        n += 1
    parts.append(f"{mix}amix=inputs={n}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    N.run(cmd + ["-filter_complex", ";".join(parts), "-map", "[aout]", "-t", f"{total:.3f}",
                 "-c:a", "pcm_s16le", WK + "/audio.wav"])
    N.run(["ffmpeg", "-y", "-i", WK + "/video.mp4", "-i", WK + "/audio.wav", "-map", "0:v", "-map", "1:a",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", saida])
    json.dump({"total": total, "blocos": [{k: s[k] for k in ("nome", "tipo", "d", "texto")} for s in segs]},
              open(P + "/linha_do_tempo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK {saida} duracao={total:.1f}s")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
