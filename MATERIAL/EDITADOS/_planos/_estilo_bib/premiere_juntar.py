"""Junta os XMLs de sequencia (premiere_xml.py) num arquivo unico para importar de uma vez no Premiere.
Cada midia entra uma vez so (id "midia-N") e as sequencias apontam para ela. Confere no fim que cada clipe aponta
para o mesmo arquivo que na sequencia separada.
Uso: python -I premiere_juntar.py <pasta PREMIERE> <nome do arquivo final.xml> <nome da pasta no Premiere>"""
import glob
import os
import re
import sys
import xml.etree.ElementTree as E

sys.stdout.reconfigure(encoding="utf-8")
pasta, nome, bin_ = sys.argv[1], sys.argv[2], sys.argv[3]
fs = sorted(glob.glob(os.path.join(pasta, "AEB *", "AEB *.xml")) + glob.glob(os.path.join(pasta, "PEB *", "PEB *.xml")),
            key=lambda f: (os.path.basename(f)[:3], int(re.search(r"[AP]EB (\d+)", f).group(1))))
gids, DEF, seqs = {}, set(), []
for k, f in enumerate(fs):
    s = open(f, encoding="utf-8").read().split('<xmeml version="4">', 1)[1].rsplit("</xmeml>", 1)[0]
    s = re.sub(r'id="(seq|clip)-(\d+)"', lambda m: f'id="{m.group(1)}-{k}-{m.group(2)}"', s)
    local = {}
    for m in re.finditer(r'<file id="(file-\d+)"><name>[^<]*</name><pathurl>([^<]*)</pathurl>', s):
        gids.setdefault(m.group(2), f"midia-{len(gids) + 1}")
        local[m.group(1)] = gids[m.group(2)]

    def full(m):
        g = local[m.group(1)]
        if g in DEF:
            return f'<file id="{g}"/>'
        DEF.add(g)
        return m.group(0).replace(f'id="{m.group(1)}"', f'id="{g}"', 1)
    s = re.sub(r'<file id="(file-\d+)"><name>[^<]*</name><pathurl>[^<]*</pathurl>.*?</file>', full, s)
    s = re.sub(r'<file id="(file-\d+)"/>', lambda m: f'<file id="{local[m.group(1)]}"/>', s)
    seqs.append(s)
x = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4"><project>'
     f"<name>{bin_}</name><children><bin><name>{bin_}</name><children>" + "".join(seqs)
     + "</children></bin></children></project></xmeml>\n")
out = os.path.join(pasta, nome)
open(out, "w", encoding="utf-8").write(x)


def mapa(seq, nm):
    return [[(c.find("start").text, nm[c.find("file").get("id")]) for c in t.findall("clipitem")] for t in seq.iter("track")]


R = E.parse(out).getroot()
nmR = {g.get("id"): g.find("pathurl").text for g in R.iter("file") if g.find("pathurl") is not None}
erros = 0
for seq, f in zip(R.iter("sequence"), fs):
    r1 = E.parse(f).getroot()
    nm1 = {g.get("id"): g.find("pathurl").text for g in r1.iter("file") if g.find("pathurl") is not None}
    if mapa(next(r1.iter("sequence")), nm1) != mapa(seq, nmR):
        erros += 1
        print("diferente:", f)
print(f"{len(fs)} sequencias, {len(gids)} midias, {'ok' if not erros else str(erros) + ' com erro'} -> {out}")
