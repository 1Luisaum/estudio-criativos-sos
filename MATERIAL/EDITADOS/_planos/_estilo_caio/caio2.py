"""Edicao copiada dos anuncios do Caio protetor (CP 54 e CP 1027) sobre uma fala real validada (29/10/2026).
Audio: a fala inteira do video validado. Video: tomadas curtas (pessoa falando x b-roll) com o ritmo do Caio;
textos desenhados igual aos dele (estilo.py); marca @soshumanhelppt no fim (marca.py da skill).
Uso: python -I caio2.py "<pasta do plano>\\plano.json"
Plano: estilo cp54|cp1027, pasta_estilo, base {arquivo, fim, tx}, tomadas [[t0, t1, arquivo|"BASE", inicio]],
       gancho {ate, linhas, y}, topo [{de, ate, linhas}] (cp1027), cta {de, linhas, y} (cp54), musica?, legenda_y."""
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.expanduser(r"~\.claude\skills\criativo-reportagem-ong\scripts"))
import comum as C  # noqa: E402
import marca  # noqa: E402
from estilo import BLK, RED, WHITE, YEL, caixa_texto, legenda_cp54, legenda_salto, texto_seco  # noqa: E402

PP = os.path.abspath(sys.argv[1])
P = os.path.dirname(PP)
R = os.path.join(P, "render")
os.makedirs(R, exist_ok=True)
p = json.load(open(PP, encoding="utf-8"))
est = p["estilo"]
H, FPS = 1920, 30


def png(nome, im):
    f = os.path.join(R, nome + ".png")
    im.save(f)
    return f


def palavras():
    d = json.load(open(p["base"]["tx"], encoding="utf-8"))
    return [(w["start"], w["end"], w["text"].upper()) for w in d["words"]
            if w.get("type", "word") == "word" and w["start"] < p["base"]["fim"]]


def grupos(ws, maxp):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) >= maxp or re.search(r"[.,?!]$", w[2]):
            out.append(cur)
            cur = []
    return out + ([cur] if cur else [])


def linhas(txts):
    return [l.split() for l in txts]


def main():
    total = p["base"]["fim"]
    g = p["gancho"]
    ovs = []
    cmd = ["ffmpeg", "-y", "-v", "error", "-t", f"{total:.3f}", "-i", p["base"]["arquivo"]]
    fc = [f"[0:v]scale=1080:{H}:force_original_aspect_ratio=increase,crop=1080:{H},fps={FPS},setsar=1,format=yuv420p[base]"]
    acc, k, face = "base", 1, []
    for t0, t1, arq, ini in p["tomadas"]:
        if arq == "BASE":
            face.append((t0, t1))
            continue
        cmd += ["-ss", str(ini), "-t", f"{t1 - t0 + 0.2:.3f}", "-i", arq]
        luz = g.get("escurecer", "") if t0 == 0 else ""  # gancho: imagem um pouco mais escura para o texto destacar
        fc.append(f"[{k}:v]scale=1080:{H}:force_original_aspect_ratio=increase,crop=1080:{H},fps={FPS},setsar=1,"
                  f"{luz + ',' if luz else ''}format=yuv420p,setpts=PTS-STARTPTS+{t0}/TB[c{k}]")
        fc.append(f"[{acc}][c{k}]overlay=0:0:eof_action=pass:enable='between(t,{t0},{t1})'[o{k}]")
        acc, k = f"o{k}", k + 1
    if g.get("seco"):  # texto seco, sem caixa (pedido do usuario, 29/10/2026)
        im = texto_seco(g["linhas"], g.get("size", 84), destaque=set(g.get("destaque", [])))
    elif est == "cp54":
        im = caixa_texto(None, 82, BLK, WHITE, padx=22, pady=10, raio=12, lh=1.08, linhas=linhas(g["linhas"]))
    else:
        im = caixa_texto(None, 64, WHITE, RED, padx=26, pady=14, lh=1.06, linhas=linhas(g["linhas"]))
    ovs.append((png("gancho", im), (1080 - im.width) // 2, g["y"] - im.height // 2, 0, g["ate"]))
    ws = [w for w in palavras() if w[0] >= g["ate"] - 0.1]
    if est == "cp54":
        for i, gr in enumerate(grupos(ws, 4)):
            nxt = ws.index(gr[-1]) + 1
            fim = min(gr[-1][1] + 0.6, ws[nxt][0] if nxt < len(ws) else total)
            if p.get("caixa_pula"):  # a caixa vermelha pula de palavra em palavra (pedido do usuario, 29/10/2026)
                for j, w in enumerate(gr):
                    b = gr[j + 1][0] if j + 1 < len(gr) else fim
                    im = legenda_salto([x[2] for x in gr], j, 72)
                    ovs.append((png(f"leg{i:02d}_{j:02d}", im), 0, p.get("legenda_y", 1150) - 15 - int(72 * 0.59), w[0], b))
                continue
            im = legenda_cp54([w[2] for w in gr], 72)
            ovs.append((png(f"leg{i:02d}", im), 0, p.get("legenda_y", 1150) - int(72 * 0.62), gr[0][0], fim))
    else:
        for i, gr in enumerate(grupos(ws, 7)):
            nxt = ws.index(gr[-1]) + 1
            fim = min(gr[-1][1] + 0.7, ws[nxt][0] if nxt < len(ws) else total)
            if p.get("legenda_seca"):  # texto seco: a frase inteira parada, sem karaoke (pedido do usuario, 29/10/2026)
                im = caixa_texto([x[2] for x in gr], 66, WHITE, RED, maxw=740, padx=22, pady=12, lh=0.98)
                ovs.append((png(f"leg{i:02d}", im), (1080 - im.width) // 2, p.get("legenda_y", 1415) - im.height // 2,
                            gr[0][0], fim))
                continue
            for j, w in enumerate(gr):  # karaoke: o que ja foi dito fica amarelo
                b = gr[j + 1][0] if j + 1 < len(gr) else fim
                im = caixa_texto([x[2] for x in gr], 66, WHITE, RED, maxw=740, padx=22, pady=12, lh=0.98,
                                 cores=[YEL if q <= j else WHITE for q in range(len(gr))])
                ovs.append((png(f"leg{i:02d}_{j:02d}", im), (1080 - im.width) // 2,
                            p.get("legenda_y", 1415) - im.height // 2, w[0], b))
    livre = "+".join(f"between(t,{a - 0.15:.2f},{b + 0.15:.2f})" for a, b in face) or "0"
    for i, tp in enumerate(p.get("topo", [])):  # faixa do alto: some quando a pessoa (rosto no alto) esta na tela
        im = caixa_texto(None, 66, WHITE, RED, padx=30, pady=18, lh=1.05, linhas=linhas(tp["linhas"]))
        ovs.append((png(f"topo{i}", im), (1080 - im.width) // 2, 145, tp["de"], tp["ate"], livre))
    if p.get("cta"):
        ct = p["cta"]
        im = caixa_texto(None, 48, WHITE, RED, padx=14, pady=10, lh=1.1, linhas=linhas(ct["linhas"]))
        ovs.append((png("cta", im), (1080 - im.width) // 2, ct["y"], ct["de"], total))
    n = k
    for j, o in enumerate(ovs):
        f, x, y, t0, t1 = o[:5]
        en = f"between(t,{t0:.2f},{t1:.2f})" + (f"*not({o[5]})" if len(o) > 5 else "")
        cmd += ["-loop", "1", "-t", f"{total + 1:.2f}", "-i", f]
        fc.append(f"[{acc}][{n + j}:v]overlay={x}:{y}:enable='{en}'[x{j}]")
        acc = f"x{j}"
    fc.append(f"[{acc}]trim=0:{total:.3f},setpts=PTS-STARTPTS,format=yuv420p[v]")
    fc.append(f"[0:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,loudnorm=I=-15:TP=-1.5:LRA=9[voz]")
    if p.get("musica"):
        cmd += ["-stream_loop", "-1", "-i", p["musica"]]
        fc.append(f"[{n + len(ovs)}:a]atrim=0:{total:.3f},volume={p.get('musica_volume', 0.08)},"
                  f"afade=t=out:st={total - 1.5:.3f}:d=1.5[m]")
        fc.append("[voz][m]amix=inputs=2:normalize=0[a]")
    else:
        fc.append("[voz]anull[a]")
    saida = C.destino(PP, p, p["pasta_estilo"])
    print("saida:", saida)
    r = subprocess.run(cmd + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-r", str(FPS),
                              *C.enc_final(), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(r.stderr[-2500:])
        sys.exit("ffmpeg falhou")
    marca.no_fim(p, saida)
    p["saida"] = saida
    json.dump(p, open(PP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK {saida} duracao={total:.2f}s")


main()
