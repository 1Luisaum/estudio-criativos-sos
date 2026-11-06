"""Monta (ou atualiza) a pasta do repositorio do GitHub com tudo o que outro Claude precisa para continuar o trabalho
do Estudio de Criativos da SOS Human Help. Mesmo formato do pacote "PARA O NOVO EDITOR" (instalar.py funciona igual),
sem as midias grandes (brutos, banco, videos prontos, exemplos), que o GitHub nao aceita.
Pedido do usuario em 05/11/2026 ("suba tudo dessa conversa para o github para eu continuar no outro Claude").
Uso: python -I montar_repo.py <pasta do repositorio>"""
import glob
import json
import os
import re
import shutil
import sys
import winreg

sys.stdout.reconfigure(encoding="utf-8")
HOME = os.path.expanduser("~")
DESK = os.path.join(HOME, "Desktop")
RAIZ = os.path.join(DESK, "EDIÇÃO COM CLAUDE")
PACOTE = os.path.join(DESK, "PARA O NOVO EDITOR")
PROJ = os.path.join(HOME, ".claude", "projects", "C--Users-EDITING-SECTOR-Desktop-PARA-O-NOVO-EDITOR")
DST = os.path.abspath(sys.argv[1])
MAX = 90 * 1024 * 1024  # o GitHub recusa arquivo acima de 100 MB
IGNORA = ("__pycache__", ".pyc", "render", "Thumbs.db", "desktop.ini")
pulados = []


def ok(p):
    return not any(x in p.replace("\\", "/").split("/") or p.endswith(x) for x in IGNORA)


def copiar_arq(src, dst):
    if os.path.getsize(src) > MAX:
        pulados.append((src, os.path.getsize(src)))
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


def copiar_arvore(src, dst, filtro=None):
    for base, dirs, arqs in os.walk(src):
        dirs[:] = [d for d in dirs if ok(d)]
        for f in arqs:
            s = os.path.join(base, f)
            if not ok(f) or (filtro and not filtro(s)):
                continue
            copiar_arq(s, os.path.join(dst, os.path.relpath(s, src)))


def limpar(dst):
    for item in os.listdir(dst) if os.path.isdir(dst) else []:
        if item in (".git", ".gitattributes"):
            continue
        p = os.path.join(dst, item)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)


def transcrever_conversa(jsonl, md, titulo):
    """Conversa em Markdown: so o que o usuario escreveu e o que o Claude respondeu (sem as saidas das ferramentas),
    com uma linha por ferramenta usada."""
    out = [f"# {titulo}\n", f"Arquivo original: `{os.path.basename(jsonl)}`\n"]
    for linha in open(jsonl, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(linha)
        except ValueError:
            continue
        m = d.get("message") or {}
        papel, c = m.get("role"), m.get("content")
        if papel not in ("user", "assistant") or d.get("isMeta"):
            continue
        quando = (d.get("timestamp") or "")[:16].replace("T", " ")
        partes = []
        if isinstance(c, str):
            partes.append(c)
        elif isinstance(c, list):
            for x in c:
                if x.get("type") == "text":
                    partes.append(x["text"])
                elif x.get("type") == "tool_use" and papel == "assistant":
                    i = x.get("input") or {}
                    desc = i.get("description") or i.get("caption") or i.get("prompt", "")[:120] or ""
                    partes.append(f"> 🔧 {x.get('name')}: {desc}".strip())
        txt = "\n".join(p for p in partes if p and not p.startswith("<system-reminder>")).strip()
        if not txt or (papel == "user" and txt.startswith("<task-notification>")):
            continue
        if papel == "user" and "tool_result" in json.dumps(c)[:200]:
            continue
        out.append(f"\n## {'USUÁRIO' if papel == 'user' else 'CLAUDE'} ({quando})\n\n{txt}\n")
    open(md, "w", encoding="utf-8").write("".join(out))


def segredos():
    vals = []
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment")
        i = 0
        while True:
            nome, valor, _ = winreg.EnumValue(k, i)
            i += 1
            if re.search(r"KEY|TOKEN|SECRET|magnific|API", nome, re.I) and isinstance(valor, str) and len(valor) >= 16:
                vals.append((nome, valor))
    except OSError:
        pass
    return vals


def main():
    os.makedirs(DST, exist_ok=True)
    limpar(DST)
    # 1) pacote base (instalador, CLAUDE.md, leia-me)
    for f in ("instalar.py", "CLAUDE.md", "COMECE AQUI.txt"):
        copiar_arq(os.path.join(PACOTE, f), os.path.join(DST, f))
    # 2) skills da ONG (versao atual, com tudo o que mudou na conversa)
    for s in sorted(glob.glob(os.path.join(HOME, ".claude", "skills", "*"))):
        if os.path.basename(s).endswith("-ong") or os.path.basename(s) == "edicao-criativo-ong":
            copiar_arvore(s, os.path.join(DST, "skills", os.path.basename(s)))
    # 3) agentes, ferramentas, conhecimento, raiz do estudio-ong
    copiar_arvore(os.path.join(HOME, ".claude", "agents"), os.path.join(DST, "AGENTES"))
    copiar_arvore(os.path.join(HOME, ".claude", "estudio-ong", "ferramentas"), os.path.join(DST, "FERRAMENTAS"))
    copiar_arvore(os.path.join(HOME, ".claude", "estudio-ong", "CONHECIMENTO"), os.path.join(DST, "CONHECIMENTO"))
    for f in ("biblioteca_falas.json", "catalogo_rostos.json", "marca.py", "logo_sos.png", "marca_soshumanhelppt.png"):
        p = os.path.join(HOME, ".claude", "estudio-ong", f)
        if os.path.exists(p):
            copiar_arq(p, os.path.join(DST, "ESTUDIO_ONG_RAIZ", f))
    # 4) Estudio (sem os videos de exemplo)
    copiar_arvore(os.path.join(RAIZ, "ESTUDIO"), os.path.join(DST, "ESTUDIO"),
                  filtro=lambda p: not p.lower().endswith((".mp4", ".mov")))
    # 5) material: musicas, planos (texto e audio pequeno), estilo Bibliotecas, clipes de feridas, banco do Pedrinho
    copiar_arvore(os.path.join(RAIZ, "MÚSICAS"), os.path.join(DST, "MATERIAL", "MÚSICAS"))
    pl = os.path.join(RAIZ, "EDITADOS", "_planos")
    for d in ("_estilo_bib", "_clipes_adrielly", "_clipes_pedrinho"):
        copiar_arvore(os.path.join(pl, d), os.path.join(DST, "MATERIAL", "EDITADOS", "_planos", d))
    texto = (".json", ".md", ".py", ".txt", ".ass", ".srt", ".csv")
    for p in glob.glob(os.path.join(pl, "*")):
        n = os.path.basename(p)
        if not os.path.isdir(p) or n in ("_estilo_bib", "_clipes_adrielly", "_clipes_pedrinho"):
            continue
        copiar_arvore(p, os.path.join(DST, "MATERIAL", "EDITADOS", "_planos", n),
                      filtro=lambda f: f.lower().endswith(texto) or (f.lower().endswith((".mp3", ".wav"))
                                                                     and os.path.getsize(f) < 5 * 1024 * 1024))
    for f in ("_demanda_atual.json",):
        p = os.path.join(RAIZ, "EDITADOS", f)
        if os.path.exists(p):
            copiar_arq(p, os.path.join(DST, "MATERIAL", "EDITADOS", f))
    copiar_arvore(os.path.join(PACOTE, "MATERIAL", "banco de vídeos do pedrinho"),
                  os.path.join(DST, "MATERIAL", "banco de vídeos do pedrinho"))
    # 6) memoria do Claude e a conversa transcrita
    copiar_arvore(os.path.join(PROJ, "memory"), os.path.join(DST, "MEMORIA"))
    os.makedirs(os.path.join(DST, "CONVERSAS"), exist_ok=True)
    for j in sorted(glob.glob(os.path.join(PROJ, "*.jsonl")), key=os.path.getmtime):
        nome = os.path.splitext(os.path.basename(j))[0]
        transcrever_conversa(j, os.path.join(DST, "CONVERSAS", f"conversa_{nome}.md"), f"Conversa {nome}")
    # 7) nenhum segredo pode ir junto (chaves do ElevenLabs, Magnific etc.): troca pelo nome da variavel
    achados = 0
    for nome, valor in segredos():
        for base, _, arqs in os.walk(DST):
            if ".git" in base:
                continue
            for f in arqs:
                p = os.path.join(base, f)
                if not f.lower().endswith(texto + (".html", ".bat", ".log")):
                    continue
                s = open(p, encoding="utf-8", errors="ignore").read()
                if valor in s:
                    open(p, "w", encoding="utf-8").write(s.replace(valor, f"<{nome} removida>"))
                    achados += 1
    tot = sum(os.path.getsize(os.path.join(b, f)) for b, _, fs in os.walk(DST) if ".git" not in b for f in fs)
    n = sum(len(fs) for b, _, fs in os.walk(DST) if ".git" not in b)
    print(f"repositorio montado: {n} arquivos, {tot / 1048576:.0f} MB; chaves encontradas e removidas: {achados}")
    for s, t in pulados:
        print(f"  ficou de fora (> 90 MB): {s} ({t / 1048576:.0f} MB)")


main()
