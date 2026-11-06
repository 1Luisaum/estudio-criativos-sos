def photo_faces(img):
    """Rostos numa foto (caixas no tamanho da propria imagem, com margem)."""
    import cv2
    import numpy as np
    g = cv2.cvtColor(np.array(img.convert("RGB")), cv2.COLOR_RGB2GRAY)
    found = []
    for n in ("haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt2.xml"):
        found += list(cv2.CascadeClassifier(cv2.data.haarcascades + n).detectMultiScale(g, 1.1, 6, minSize=(70, 70)))
    return [(x - w * 0.25, y - h * 0.45, x + w * 1.25, y + h * 1.6) for (x, y, w, h) in found]


def photo_input(WK, b, d, card):
    """Foto SEMPRE em tela cheia (nunca reduzida com fundo desfocado).
    Com rosto: quadro parado, centrado nos rostos. Sem rosto (produto largo): panoramica lenta
    da esquerda para a direita, para a foto inteira aparecer."""
    img = Image.open(card).convert("RGB")
    s = max(W / img.width, H / img.height)
    big = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    oy = (big.height - H) // 2
    big = big.crop((0, oy, big.width, oy + H))
    fb = photo_faces(big)
    extra = big.width - W
    png = f"{WK}/{b['nome']}_foto.png"
    if fb or extra < 8:
        cx = (min(x0 for x0, _, _, _ in fb) + max(x1 for _, _, x1, _ in fb)) / 2 if fb else big.width / 2
        x0 = int(max(0, min(extra, cx - W / 2)))
        big.crop((x0, 0, x0 + W, H)).save(png)
        return png, f"[0:v]{push(d)}[bg]", [(a - x0, b_, c - x0, e) for a, b_, c, e in fb]
    big.save(png)
    return png, f"[0:v]crop={W}:{H}:x='{extra}*t/{d:.3f}':y=0,setsar=1,fps={FPS}[bg]", []


def render_block(WK, plano, b, d, words_t, out, manual):
    """Video SEMPRE em tela cheia. A chamada fica na zona segura e nunca em cima de rosto:
    se o rosto ocupa a zona segura inteira (close), a chamada some so naquela cena."""
    hl = headline_img(plano["chamada"])
    final = b.get("final", False)
    pl = pill_img(plano["etiqueta_final"] if final else plano["etiqueta"])
    show_pill = b.get("etiqueta", False) or final
    key = {w.upper() for w in plano.get("palavras_chave", [])}
    cmd, fc, windows = ["ffmpeg", "-y"], [], []
    card = b.get("foto")
    shots = b.get("cenas") or []
    if card:
        png, chain, fb = photo_input(WK, b, d, card)
        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", png]
        fc.append(chain)
        windows.append([0.0, d, fb])
        n_in = 1
    else:
        each = d / len(shots)
        labels = []
        for i, (src, st) in enumerate(shots):
            fb = faces(WK, src, st, each, f"{b['nome']}_{i}")
            fb += [tuple(z["caixa"]) for z in manual
                   if os.path.basename(z["arquivo"]) == os.path.basename(src) and abs(z["inicio"] - st) < 0.01]
            windows.append([i * each, (i + 1) * each, fb])
            cmd += ["-ss", f"{st:.2f}", "-t", f"{each + 0.1:.3f}", "-i", src]
            fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                      f"{push(each)},trim=duration={each:.3f},setpts=PTS-STARTPTS[b{i}]")
            labels.append(f"[b{i}]")
        fc.append("".join(labels) + f"concat=n={len(shots)}:v=1:a=0[bg]")
        n_in = len(shots)

    plans = []
    for _, _, busy in windows:
        y_pl, y_cap = layout(busy, pl.height, show_pill)
        taken = list(busy) + [(0, y_cap, W, y_cap + CAP_H)]
        if y_pl is not None:
            taken.append((0, y_pl, W, y_pl + pl.height))
        y_hl = place(hl.height, list(range(SAFE_TOP, SAFE_BOTTOM - hl.height + 1, 10)), taken)
        if hits(y_hl, hl.height, taken):
            y_hl = None  # nao cabe sem cobrir rosto: some nesta cena
        plans.append((y_hl, y_pl, y_cap))
        print(f"  {b['nome']}: chamada={'ESCONDIDA (rosto ocupa a zona segura)' if y_hl is None else y_hl} "
              f"legenda={y_cap} etiqueta={y_pl}")

    last, k = "[bg]", n_in
    for wi, ((t0, t1, _), (y_hl, y_pl, y_cap)) in enumerate(zip(windows, plans)):
        base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if y_hl is not None:
            base.alpha_composite(hl, (0, y_hl))
        if y_pl is not None:
            base.alpha_composite(pl, (0, y_pl))
        png = f"{WK}/{b['nome']}_base{wi}.png"
        base.save(png)
        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", png]
        fc.append(f"{last}[{k}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[o{k}]")
        last, k = f"[o{k}]", k + 1
        for j, (a, bb, ws) in enumerate(words_t):
            a2, b2 = max(a, t0), min(bb, t1)
            if b2 - a2 < 0.02:
                continue
            cp = f"{WK}/{b['nome']}_c{j}.png"
            caption_img(ws, key).save(cp)
            cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", cp]
            fc.append(f"{last}[{k}:v]overlay=0:{y_cap}:enable='between(t,{a2:.3f},{b2:.3f})'[o{k}]")
            last, k = f"[o{k}]", k + 1
    run(cmd + ["-filter_complex", ";".join(fc), "-map", last, "-an", *ENC, out])


