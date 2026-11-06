def render_block(WK, plano, b, d, caps, out, manual, clip=None):
    """Sempre tela cheia. Selo+manchete na zona segura e nunca em rosto (se o rosto ocupa a zona
    segura inteira, somem so naquela cena). A tarja (GC) procura lugar livre de rosto."""
    title = title_img(plano["manchete"], plano.get("etiqueta_manchete", "ESPECIAL"))
    selo = selo_img(plano.get("marca", "SOS HUMAN HELP"))
    final = b.get("final", False)
    pl = N.pill_img(plano["etiqueta_final"] if final else plano["etiqueta"])
    show_pill = b.get("etiqueta", False) or final
    gc = gc_img(*b["gc"]) if b.get("gc") else None
    cmd, fc, windows = ["ffmpeg", "-y"], [], []
    card = b.get("foto")
    shots = [[clip, 0.0]] if clip else (b.get("cenas") or [])
    if card:
        png, chain, fb = N.photo_input(WK, b, d, card)
        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", png]
        fc.append(chain)
        windows.append([0.0, d, fb])
        n_in = 1
    else:
        each = d / len(shots)
        labels = []
        for i, (src, st) in enumerate(shots):
            fb = N.faces(WK, src, st, min(each, N.dur(src) - st - 0.05) if clip else each, f"{b['nome']}_{i}")
            key = b.get("fonte") if clip else src
            st_key = b["cortes"][0][0] if clip else st
            fb += [tuple(z["caixa"]) for z in manual
                   if os.path.basename(z["arquivo"]) == os.path.basename(key) and abs(z["inicio"] - st_key) < 0.01]
            windows.append([i * each, (i + 1) * each, fb])
            cmd += ["-ss", f"{st:.2f}", "-t", f"{each + 0.1:.3f}", "-i", src]
            fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                      f"{N.push(each, 0.02)},tpad=stop_mode=clone:stop_duration=1,"
                      f"trim=duration={each:.3f},setpts=PTS-STARTPTS[b{i}]")
            labels.append(f"[b{i}]")
        fc.append("".join(labels) + f"concat=n={len(shots)}:v=1:a=0[bg]")
        n_in = len(shots)

    cap_h, gc_h = 170, gc.height if gc else 0
    head_h = selo.height + 14 + title.height
    plans = []
    for _, _, busy in windows:
        taken = list(busy)
        y_pl = None
        if show_pill:
            y_pl = N.place(pl.height, list(range(1720, 1380, -40)), taken)
            taken.append((0, y_pl, W, y_pl + pl.height))
        y_cap = N.place(cap_h, sorted(range(900, 1720, 20), key=lambda y: abs(y - 1300)), taken)
        taken.append((0, y_cap, W, y_cap + cap_h))
        y_sel = N.place(head_h, list(range(N.SAFE_TOP, N.SAFE_BOTTOM - head_h + 1, 10)), taken)
        if N.hits(y_sel, head_h, taken):
            y_sel = None
        else:
            taken.append((0, y_sel, W, y_sel + head_h))
        y_gc = None
        if gc:
            cands = sorted(range(N.SAFE_TOP, N.SAFE_BOTTOM - gc_h + 1, 10), key=lambda y: -y) + \
                list(range(N.SAFE_BOTTOM - gc_h + 10, 1560, 10))
            y_gc = N.place(gc_h, cands, taken)
            if N.hits(y_gc, gc_h, taken):
                y_gc = None
        plans.append((y_sel, y_pl, y_cap, y_gc))
        print(f"  {b['nome']}: selo+manchete={'ESCONDIDOS (rosto)' if y_sel is None else y_sel} "
              f"gc={'-' if not gc else ('ESCONDIDA (rosto)' if y_gc is None else y_gc)} legenda={y_cap} etiqueta={y_pl}")

    last, k = "[bg]", n_in
    for wi, ((t0, t1, _), (y_sel, y_pl, y_cap, y_gc)) in enumerate(zip(windows, plans)):
        base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if y_sel is not None:
            base.alpha_composite(selo, (60, y_sel))
            base.alpha_composite(title, (0, y_sel + selo.height + 14))
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


