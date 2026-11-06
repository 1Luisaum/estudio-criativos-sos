"""Listas narradas (26/10/2026, pedido do usuario): todas com narrador brasileiro (Leonardo) e sem pausas de respiracao.
- v1 refeita no visual aprovado com copy nova (calor); v2 ganha a voz brasileira; v3-v5 ja eram Leonardo.
- cada fala gerada vai para audio\\ e uma copia sem respiros/silencios vai para audio_br\\ (que o lista.py usa primeiro);
- pausas entre blocos caem para 0,08 s (a tela final mantem 1,6 s).
"""
import glob, json, os, shutil, subprocess, sys

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAIZ = os.path.dirname(os.path.dirname(P))
K = os.path.join(os.path.expanduser("~"), ".claude", "skills", "criativo-lista-ong", "scripts")
sys.path.insert(0, K)
import lista as L  # noqa: E402

LEONARDO = "4XmhZ74tBbUVCXIYNMMo"
BANK = os.path.join(RAIZ, "banco de vídeos do pedrinho").replace("\\", "/")
BR = os.path.join(RAIZ, "VÍDEOS PARA EDITAR")
CUR = BANK + "/Vídeo Mostrando itens de curativos em cima da Cama  e  Finalizando os Curativos_.mp4"
# tira trechos sem fala (respiro e silencio) maiores que 0,12 s, deixando 0,04 s; e apara inicio e fim
SEM_RESPIRO = ("silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.02:"
               "stop_periods=-1:stop_duration=0.12:stop_threshold=-40dB:stop_silence=0.04")
os.environ.pop("ELEVENLABS_API_KEY", None)


def bruto(chave):
    return next(p for p in glob.glob(os.path.join(BR, "*.mp4")) if chave in os.path.basename(p)).replace("\\", "/")


def nova_v1():
    r8 = bruto("roteiro 8")
    return {
        "nome": "Pedrinho_lista_v1", "pedido": "refeita 26/10/2026 (visual aprovado, narrador brasileiro)",
        "voz": {"voice_id": LEONARDO, "model_id": "eleven_multilingual_v2"},
        "musica": os.path.join(RAIZ, "MÚSICAS", "rockymetal-ambient-acoustic-239252.mp3").replace("\\", "/"),
        "musica_volume": 0.12, "chamada": ["46 GRAUS NA PELE DE BORBOLETA 💔", "DOE R$ 3 E PROTEJA O PEDRINHO 👼"],
        "etiqueta": "R$ 3 já ajuda ❤️", "etiqueta_final": "👇 Toque em SAIBA MAIS",
        "palavras_chave": ["QUARENTA", "SEIS", "GRAUS", "CALOR", "BOLHAS", "FERIDAS", "DOR", "FAIXAS", "ACABANDO",
                           "MEDO", "DOIS", "TRÊS", "REAIS", "SAIBA", "MAIS"],
        "narracao": {"N01": "Quase quarenta e seis graus. Esse é o calor na cidade do Pedrinho.",
                     "N02": "Para a pele dele, o calor traz:", "I1": "Mais bolhas.", "I2": "Feridas piores.", "I3": "Mais dor.",
                     "N03": "E as faixas que protegem a pele dele estão acabando.",
                     "N04": "Ele mesmo diz: está com muito medo.",
                     "N05": "Dois ou três reais já ajudam, segundo ele.",
                     "N06": "Toque em Saiba mais e proteja a pele do Pedrinho."},
        "fatos": {"calor de quase 46 graus, ruim pra pele; bolhas piores; faixas acabando; medo; 2 ou 3 reais": "Pedrinho, roteiro 8"},
        "blocos": [
            {"nome": "s01", "fala": "N01", "pausa": 0.08, "cenas": [[r8, 58.0, "pb"], [CUR, 185.0, "pb"]]},
            {"nome": "s02", "fala": "N02", "pausa": 0.08, "cenas": [[CUR, 160.0, "pb"]]},
            {"nome": "i1", "fala": "I1", "pausa": 0.08, "foto": BANK + "/20240402_095757.jpg", "pb": True},
            {"nome": "i2", "fala": "I2", "pausa": 0.08, "foto": BANK + "/20240411_123226.jpg", "pb": True},
            {"nome": "i3", "fala": "I3", "pausa": 0.08, "cenas": [[r8, 92.0, "pb"]]},
            {"nome": "s03", "fala": "N03", "pausa": 0.08, "foto": BANK + "/crepe bandagem.png"},
            {"nome": "s04", "fala": "N04", "pausa": 0.08, "cenas": [[r8, 72.0]]},
            {"nome": "s05", "fala": "N05", "pausa": 0.08, "etiqueta": True, "cenas": [[BANK + "/20260410_210553.mp4", 25.0]]},
            {"nome": "s06", "fala": "N06", "pausa": 1.6, "final": True, "foto": BANK + "/20241109_123330.jpg"}],
        "zonas_protegidas": []}


for n in range(1, 6):
    d = os.path.join(P, f"Pedrinho_lista_v{n}")
    f = os.path.join(d, "plano.json")
    if n == 1:
        antigo = os.path.join(d, "_rascunho_antigo")  # o rascunho reprovado fica guardado, nao apagado
        os.makedirs(antigo, exist_ok=True)
        for x in os.listdir(d):
            if x != "_rascunho_antigo":
                shutil.move(os.path.join(d, x), os.path.join(antigo, x))
        p = nova_v1()
    else:
        p = json.load(open(f, encoding="utf-8-sig"))
        if p["voz"].get("voice_id") != LEONARDO:  # v2: troca a voz e regrava as falas
            p["voz"] = {"voice_id": LEONARDO, "model_id": "eleven_multilingual_v2"}
            for mp3 in glob.glob(os.path.join(d, "audio", "*.mp3")):
                os.remove(mp3)
        for bl in p["blocos"]:
            bl["pausa"] = 1.6 if bl.get("final") else 0.08
    json.dump(p, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    P_ = d.replace("\\", "/")
    L.make_audio(P_, p)
    os.makedirs(os.path.join(d, "audio_br"), exist_ok=True)
    for k in p["narracao"]:
        src, dst = os.path.join(d, "audio", f"{k}.mp3"), os.path.join(d, "audio_br", f"{k}.mp3")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", SEM_RESPIRO, "-c:a", "libmp3lame", "-b:a", "192k", dst],
                       check=True)
    r = subprocess.run([sys.executable, "-I", os.path.join(K, "lista.py"), f], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    open(os.path.join(d, "render_log.txt"), "w", encoding="utf-8").write(r.stdout + r.stderr)
    ok = [l for l in r.stdout.splitlines() if l.startswith("OK")]
    print(f"v{n}:", ok[-1] if ok and r.returncode == 0 else "ERRO " + (r.stdout + r.stderr)[-400:], flush=True)
