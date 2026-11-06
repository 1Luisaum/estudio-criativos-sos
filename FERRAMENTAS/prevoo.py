"""Pre-voo de um plano, ANTES de montar (27/10/2026): acha em segundos o que no lote so aparecia depois da
montagem e obrigava a remontar.

Confere:
- cada foto e cada trecho de b-roll com "start" contra o catalogo de rostos: rosto dentro de uma faixa de texto
  do estilo -> aviso, com ate 3 fotos do banco sugeridas que deixam o rosto livre;
- arquivo que nao existe; foto .jpg na Mae desesperada (o montador corta o video, bug conhecido);
- musica que nao existe; narracao (roteiro_audio.json) ainda nao gerada.
Os trechos da crianca falando (bruto com in/out e zoom) nao entram: o enquadramento deles vem do "face" do plano.

Uso: python -I prevoo.py <plano.json ou pasta>   (saida 0 = ok, 2 = avisos, 1 = erro)
"""
import glob, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
import catalogo  # noqa: E402
import conferir_auto  # noqa: E402
import rostos  # noqa: E402

MIDIA = rostos.FOTO + (".mp4", ".mov", ".m4v", ".mkv")
# palavra no nome da pasta do plano -> estilo (as faixas de texto ficam em conferir_auto.ESTILOS)
ESTILO_POR_NOME = [("caixas_pedido", "CAIXAS PEDIDO DE TEMPO"), ("caixas_aspas", "CAIXAS ASPAS"),
                   ("caixas_urgente", "CAIXAS URGENTE"), ("unicef", "UNICEF"), ("lettering", "CORTES COM LETTERING"),
                   ("narrado", "NARRADO DE IMPACTO"), ("reportagem", "REPORTAGEM"), ("esperanca", "DA DOR À ESPERANÇA"),
                   ("corrente", "CORRENTE DO BEM"), ("mae_desesperada", "MÃE DESESPERADA"), ("salva_vida", "SALVA VIDA"),
                   ("", "CORTES COM GANCHO")]
IGNORAR = ("raw", "transcript", "bank", "music", "musica", "musica_tensa", "musica_esperanca", "saida", "out",
           "chamada", "logo", "fonte_original")


def estilo_do(pd):
    n = os.path.basename(pd).lower()
    return next(e for k, e in ESTILO_POR_NOME if k in n)


def achar(src, bases, raiz):
    """O arquivo pelo caminho completo, na pasta do plano, no banco do plano ("bank" ou "banco"), nos brutos,
    em qualquer "banco de videos" da raiz ou na raiz."""
    if os.path.isabs(src) and os.path.isfile(src):
        return src
    adri = glob.glob(os.path.join(raiz, "adrielly", "BANCO*"))
    adri += [os.path.join(b, x) for b in adri for x in ("_tratadas", "_jpg_do_heic")]
    adri += [d for d in glob.glob(os.path.join(raiz, "adrielly", "BRUTOS*", "**"), recursive=True) if os.path.isdir(d)]
    for base in [*bases, os.path.join(raiz, "VÍDEOS PARA EDITAR"), *glob.glob(os.path.join(raiz, "banco de v*")),
                 *adri, raiz]:
        p = os.path.join(base or "", src)
        if base and os.path.isfile(p):
            return p
    return None


def referencias(x, caminho=""):
    """[(caminho no plano, dict)] de todo dict com um arquivo de midia em src/foto/imagem."""
    out = []
    if isinstance(x, dict):
        for k in ("src", "foto", "imagem", "arquivo"):
            v = x.get(k)
            if isinstance(v, str) and v.lower().endswith(MIDIA):
                out.append((caminho, k, x))
        for k, v in x.items():
            if k not in IGNORAR:
                out += referencias(v, f"{caminho}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            out += referencias(v, f"{caminho}[{i}]")
    return out


def rostos_por_quadro(path, cat, t0=None, t1=None):
    """[[rostos] por quadro]: 1 quadro na foto; 1 por segundo no trecho do video."""
    it = cat.get(os.path.basename(path))
    if it and it.get("mtime") == os.path.getmtime(path):
        if it["tipo"] == "foto":
            return [it["rostos"]]
        return [rs for t, rs in it["por_segundo"].items() if t0 - 0.5 <= float(t) <= t1 + 0.5]
    if path.lower().endswith(rostos.FOTO):  # fora do catalogo: detecta na hora
        q = rostos.ler_foto(path)
        return [rostos.no_quadro(q) if q is not None else []]
    return [rostos.no_quadro(q) for _, q in rostos.quadros_video(path, passo=1.0, inicio=t0, dur=t1 - t0 + 1)]


def sugestoes(zonas, cat, usados, n=3, crianca="Pedrinho"):
    out = []
    fo, ev = catalogo.fortes(), catalogo.evitar()
    for nome, a in sorted(cat.items()):
        if a["grupo"] == "banco" and a["tipo"] == "foto" and nome not in usados and nome not in ev \
                and nome not in fo and a.get("crianca", catalogo.crianca_de(a["caminho"])) == crianca \
                and catalogo._livre(a["rostos"], zonas):
            out.append(nome)
            if len(out) == n:
                break
    return out


def prevoo(plano_path):
    pd = os.path.dirname(plano_path)
    p = json.load(open(plano_path, encoding="utf-8-sig"))
    raiz = catalogo.raiz()
    estilo = estilo_do(pd)
    cfg = conferir_auto.ESTILOS.get(estilo, {})
    zonas = cfg.get("zonas", [])
    cat = catalogo.carregar()["arquivos"]
    erros, avisos = [], []
    refs = referencias(p)
    usados = {os.path.basename(r[2][r[1]]) for r in refs}
    bases = [pd, p.get("bank", ""), p.get("banco", "")]
    proibidos = catalogo.evitar()
    fortes = catalogo.fortes()
    crianca = "Adrielly" if "adriel" in os.path.basename(pd).lower() else "Pedrinho"
    for onde, chave, d in refs:
        src = d[chave]
        path = achar(src, bases, raiz)
        if not path:
            erros.append(f"{onde}: arquivo não encontrado: {src}")
            continue
        if os.path.basename(path) in fortes:
            t = fortes[os.path.basename(path)]
            ext = ".mp4" if path.lower().endswith((".mov", ".mp4")) else ".jpg"
            erros.append(f"{onde}: {os.path.basename(path)} é imagem muito forte: use a versão tratada "
                         f"_tratadas/{os.path.splitext(os.path.basename(path))[0]}_{t}{ext}")
        if catalogo.crianca_de(path) != crianca and "lettings" not in path.lower():
            erros.append(f"{onde}: {os.path.basename(path)} é material de {catalogo.crianca_de(path)}, "
                         f"mas o plano é de {crianca}")
        if os.path.basename(path) in proibidos:
            erros.append(f"{onde}: {os.path.basename(path)} não pode entrar em vídeo ({proibidos[os.path.basename(path)]})")
        if estilo == "MÃE DESESPERADA" and path.lower().endswith((".jpg", ".jpeg")):
            erros.append(f"{onde}: foto .jpg na Mãe desesperada corta o vídeo (bug conhecido): use .png ou vídeo")
        # cena do gancho do UNICEF: a faixa e a legenda do gancho, nao o lettering
        zs = zonas
        if estilo == "UNICEF" and onde.startswith(".gancho"):
            y = (p.get("gancho") or {}).get("legenda_y", 1190)
            zs = [(y - 90, y + 90)]
        video = not path.lower().endswith(rostos.FOTO)
        if video and "start" not in d:
            continue  # trecho da crianca falando: o enquadramento vem do "face"
        t0 = float(d.get("start", 0)) if video else None
        t1 = (t0 + float(d.get("dur", d.get("t1", 0) - d.get("t0", 0) if "t1" in d else 3))) if video else None
        quadros = rostos_por_quadro(path, cat, t0, t1)
        com = [[r for r in rs if r[3] - r[1] >= 70 and any(rostos.cruza(r, z, folga=-40) for z in zs)] for rs in quadros]
        bate = [r for rs in com for r in rs]
        # no video so avisa se o rosto fica na faixa em pelo menos metade do trecho (o movimento engana o detector)
        if bate and sum(bool(x) for x in com) >= max(1, len(com) / 2):
            sug = sugestoes(zs, cat, usados, crianca=crianca) if not video else []
            avisos.append({"onde": onde, "arquivo": os.path.basename(src), "rosto_y": [bate[0][1], bate[0][3]],
                           "faixas": [list(z) for z in zs],
                           "sugestoes": sug, "texto": f"{onde}: rosto de {os.path.basename(src)} (y {bate[0][1]}-"
                           f"{bate[0][3]}) cai numa faixa de texto {zs}" + (f"; troque por: {', '.join(sug)}" if sug else
                                                                             "; escolha outro trecho (catalogo.py livres)")})
    for k in ("music", "musica", "musica_tensa", "musica_esperanca"):
        if isinstance(p.get(k), str) and p[k] and not achar(p[k], os.path.join(raiz, "MÚSICAS"), raiz):
            erros.append(f"música não encontrada: {p[k]}")
    ra = os.path.join(pd, "roteiro_audio.json")
    if os.path.isfile(ra):
        ns = json.load(open(ra, encoding="utf-8-sig")).get("narracao", {})
        falta = [n for n in ns if not os.path.isfile(os.path.join(pd, "audio", n + ".mp3"))]
        if falta:
            erros.append(f"narração ainda não gerada: {', '.join(falta)} (rode o gerar_audio.py da skill)")
    return {"plano": os.path.basename(pd), "estilo": estilo, "erros": erros, "avisos": avisos}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    alvo = os.path.abspath(sys.argv[1])
    r = prevoo(os.path.join(alvo, "plano.json") if os.path.isdir(alvo) else alvo)
    print(f"{r['plano']} ({r['estilo']}): {len(r['erros'])} erro(s), {len(r['avisos'])} aviso(s)")
    for e in r["erros"]:
        print("  ERRO ", e)
    for a in r["avisos"]:
        print("  AVISO", a["texto"])
    sys.exit(1 if r["erros"] else 2 if r["avisos"] else 0)
