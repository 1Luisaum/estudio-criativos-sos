"""Cortes com gancho, ajustes de 26/10/2026 (sem mexer na skill; leva para a skill quando o usuario pedir "salvar"):
- sem selo no canto superior esquerdo (plano: "badge": null);
- caixa do gancho (e da tela final) vermelha em vez de rosa;
- depois do gancho, faixa vermelha de doacao ("chamada" no plano), sem risco branco por cima do texto.

Uso: python -I build_cortes_v2.py <plano.json>
"chamada": {"linhas": [["APENAS R$ 5", 112], ["PODEM MUDAR A VIDA DO", 58], ["PEDRINHO GUERREIRO!", 84]], "y": 1300}
"""
import json, os, sys

K = os.path.join(os.path.expanduser("~"), ".claude", "skills", "edicao-criativo-ong", "scripts")
sys.path.insert(0, K)
import build as B  # noqa: E402
import comum as C  # noqa: E402

RED = "&H002904D9&"       # #D90429
DARK = "&H0010036E&"      # vermelho escuro (borda/fundo da faixa)
_box = B.box_block
B.box_block = lambda t0, t1, lines, cy, fs, color=None, **kw: _box(t0, t1, lines, cy, fs, color=RED, **kw)
_ass = B.Builder.build_ass


def build_ass(self, words, total, end_start, path):
    _ass(self, words, total, end_start, path)
    ch = self.p.get("chamada")
    if not ch:
        return
    t0 = max([h["t1"] for h in self.p.get("hook", [])] + [0.0])
    t1 = end_start
    linhas = ch["linhas"]
    lh = [fs * 1.12 for _, fs in linhas]
    h = int(sum(lh) + 56)
    cy = ch.get("y", 1300)
    y0 = int(cy - h / 2)
    ts = B.ts
    ev = [
        # faixa: vermelho, com a metade de baixo mais escura (degrade simples) e filete escuro em cima e embaixo
        f"Dialogue: 5,{ts(t0)},{ts(t1)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\fad(180,0)\\1c{RED}\\p1}}m 0 {y0} l {B.W} {y0} {B.W} {y0 + h} 0 {y0 + h}{{\\p0}}",
        f"Dialogue: 6,{ts(t0)},{ts(t1)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\fad(180,0)\\1c{DARK}\\1a&H90&\\p1}}m 0 {y0 + h // 2} l {B.W} {y0 + h // 2} {B.W} {y0 + h} 0 {y0 + h}{{\\p0}}",
        f"Dialogue: 6,{ts(t0)},{ts(t1)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\fad(180,0)\\1c{DARK}\\p1}}m 0 {y0} l {B.W} {y0} {B.W} {y0 + 6} 0 {y0 + 6}{{\\p0}}",
        f"Dialogue: 6,{ts(t0)},{ts(t1)},Box,,0,0,0,,{{\\an7\\pos(0,0)\\fad(180,0)\\1c{DARK}\\p1}}m 0 {y0 + h - 6} l {B.W} {y0 + h - 6} {B.W} {y0 + h} 0 {y0 + h}{{\\p0}}",
    ]
    y = y0 + 28
    for (txt, fs), l in zip(linhas, lh):
        fs = min(fs, int(fs * 1000 / max(B.text_w(txt, fs), 1)))  # cabe em 1000 px
        ev.append(f"Dialogue: 7,{ts(t0)},{ts(t1)},Hook,,0,0,0,,{{\\an5\\pos(540,{y + l / 2:.0f})\\fs{fs}\\1c&HFFFFFF&"
                  f"\\3c{DARK}\\bord5\\4c&H000000&\\4a&H50&\\shad4\\fad(180,0)\\t(0,180,\\fscx100\\fscy100)\\fscx115\\fscy115}}{txt}")
        y += l
    with open(path, "a", encoding="utf-8") as fh:
        fh.write("\n".join(ev) + "\n")


B.Builder.build_ass = build_ass

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    plan_path = os.path.abspath(sys.argv[1])
    plan = json.load(open(plan_path, encoding="utf-8-sig"))
    out = C.destino(plan_path, plan, "cortes", chave="out")
    B.Builder(plan, os.path.dirname(plan_path), out).build()
