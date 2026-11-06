"""Fila de montagem do lote (27/10/2026): monta os planos com o montador da skill certa, N por vez (padrao 2,
na placa de video), confere cada MP4 com conferir_auto.py e grava um resumo. Nao usa IA: o Claude so escreve
os planos antes e le o resumo no fim. A aba "Producao ao vivo" do Estudio mostra o andamento.

Antes de montar, roda o pre-voo (prevoo.py): plano com erro ou aviso nao e montado (veja o resumo).

Uso: python -I fila.py <plano.json ou pasta do plano> [...] [--paralelo 2] [--resumo fila_resumo.json]
     [--ignorar-prevoo]
Saida: 0 = todos montados sem aviso; 2 = algum aviso (veja o resumo); 1 = alguma montagem falhou.
"""
import argparse, json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I nao poe a pasta do script no path
import conferir_auto  # noqa: E402
import prevoo  # noqa: E402

SK = os.path.join(os.path.expanduser("~"), ".claude", "skills")
# palavra no nome da pasta do plano -> (skill, script). A ordem importa: "caixas_pedido" antes de "pedido".
MONTADORES = [("caixas_pedido", "criativo-caixas-pedido-ong", "caixas.py"),
              ("caixas_aspas", "criativo-caixas-aspas-ong", "caixas.py"),
              ("caixas_urgente", "criativo-caixas-urgente-ong", "caixas.py"),
              ("unicef", "criativo-unicef-ong", "montar.py"),
              ("lettering", "criativo-lettering-ong", "build.py"),
              ("narrado", "criativo-narrado-ong", "narrado.py"),
              ("reportagem", "criativo-reportagem-ong", "reportagem.py"),
              ("esperanca", "criativo-esperanca-ong", "montar.py"),
              ("corrente", "criativo-corrente-ong", "montar.py"),
              ("mae_desesperada", "criativo-mae-desesperada-ong", "montar.py"),
              ("salva_vida", "criativo-salva-vida-ong", "montar.py"),
              ("lista", "criativo-lista-ong", "lista.py"),
              ("vsl", "criativo-vsl-voz-ong", "vsl.py"),
              ("", "edicao-criativo-ong", "build.py")]  # o resto e "Cortes com gancho"


def montador(plano_path):
    p = json.load(open(plano_path, encoding="utf-8-sig"))
    nome = os.path.basename(os.path.dirname(plano_path)).lower()
    skill = p.get("skill")  # o plano pode dizer a skill
    # pelo conteudo, quando o nome da pasta nao diz: gancho com cenas = UNICEF; lettering pronto sem gancho = lettering
    if not skill and isinstance(p.get("gancho"), dict) and p["gancho"].get("cenas"):
        skill = "criativo-unicef-ong"
    elif not skill and (p.get("chamada") or {}).get("imagem") and "segments" in p and not any(
            k in nome for k, _, _ in MONTADORES if k):
        skill = "criativo-lettering-ong"
    for chave, sk, script in MONTADORES:
        if (skill and skill == sk) or (not skill and chave in nome):
            return sk, os.path.join(SK, sk, "scripts", script)
    raise SystemExit(f"nao sei o montador de {plano_path}")


def md5_audio(mp4):
    """Impressao digital so do audio: se nao mudou numa correcao, nao precisa transcrever de novo."""
    if not mp4 or not os.path.isfile(mp4):
        return None
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-map", "0:a", "-f", "md5", "-"],
                       capture_output=True, text=True)
    return r.stdout.strip() or None


def um(plano_path, log_dir, ignorar_prevoo=False):
    nome = os.path.basename(os.path.dirname(plano_path))
    sk, script = montador(plano_path)
    # pre-voo: o que antes so aparecia depois de montar (rosto no texto, arquivo faltando, .jpg na Mae...)
    pv = prevoo.prevoo(plano_path)
    if pv["erros"] or (pv["avisos"] and not ignorar_prevoo):
        print(f"  PARADO {nome} no pre-voo: " + "; ".join(pv["erros"] + [a["texto"] for a in pv["avisos"]]), flush=True)
        return {"plano": nome, "skill": sk, "ok": False, "prevoo": pv,
                "erro": "pre-voo: corrija o plano (ou rode com --ignorar-prevoo se o aviso nao for real)"}
    p0 = json.load(open(plano_path, encoding="utf-8-sig"))
    audio_antes = md5_audio(p0.get("saida") or p0.get("out"))
    t0 = time.time()
    log = os.path.join(log_dir, nome + ".log")
    with open(log, "w", encoding="utf-8") as fh:
        r = subprocess.run([sys.executable, "-I", script, plano_path], stdout=fh, stderr=subprocess.STDOUT,
                           text=True, encoding="utf-8", errors="replace")
    res = {"plano": nome, "skill": sk, "montagem_s": round(time.time() - t0), "log": log, "ok": r.returncode == 0}
    p = json.load(open(plano_path, encoding="utf-8-sig"))
    saida = p.get("saida") or p.get("out")
    res["saida"] = saida
    if not res["ok"] or not saida or not os.path.isfile(saida):
        res["ok"] = False
        res["erro"] = open(log, encoding="utf-8", errors="replace").read()[-1500:]
        print(f"  FALHOU  {nome}  (veja {log})", flush=True)
        return res
    desde = (p.get("gancho") or {}).get("fim", 0.0) if sk == "criativo-unicef-ong" else 0.0
    c = conferir_auto.conferir(saida, desde=desde, folha_dir=log_dir)
    audio_depois = md5_audio(saida)
    res.update({"duracao": c["duracao"], "avisos": c["avisos"], "folha_suspeitos": c.get("folha_suspeitos"),
                "prevoo_avisos": [a["texto"] for a in pv["avisos"]],
                # numa correcao: so transcreva de novo se o audio mudou
                "audio_mudou": audio_antes != audio_depois if audio_antes else None})
    print(f"  {'OK   ' if not c['avisos'] else 'AVISO'}  {os.path.basename(saida)}  {c['duracao']} s  "
          f"montagem {res['montagem_s']} s" + "".join(f"\n         - {a}" for a in c["avisos"]), flush=True)
    return res


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("planos", nargs="+")
    ap.add_argument("--paralelo", type=int, default=2)
    ap.add_argument("--resumo", default="")
    ap.add_argument("--ignorar-prevoo", action="store_true",
                    help="monta mesmo com aviso do pre-voo (erros continuam parando)")
    a = ap.parse_args()
    planos = [os.path.abspath(os.path.join(x, "plano.json") if os.path.isdir(x) else x) for x in a.planos]
    log_dir = os.path.join(os.path.dirname(os.path.dirname(planos[0])), "_fila")
    os.makedirs(log_dir, exist_ok=True)
    t0 = time.time()
    print(f"fila: {len(planos)} plano(s), {a.paralelo} por vez", flush=True)
    with ThreadPoolExecutor(a.paralelo) as ex:
        res = list(ex.map(lambda pp: um(pp, log_dir, a.ignorar_prevoo), planos))
    resumo = a.resumo or os.path.join(log_dir, time.strftime("resumo_%Y%m%d_%H%M%S.json"))
    json.dump({"total_s": round(time.time() - t0), "videos": res}, open(resumo, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    falhas = sum(not r["ok"] for r in res)
    avisos = sum(bool(r.get("avisos")) for r in res if r["ok"])
    print(f"fim: {len(res) - falhas} montado(s), {falhas} falha(s), {avisos} com aviso, "
          f"{round(time.time() - t0)} s no total -> {resumo}")
    sys.exit(1 if falhas else 2 if avisos else 0)
