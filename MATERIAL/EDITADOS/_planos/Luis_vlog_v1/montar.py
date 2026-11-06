# Vlog do Luis: um dia de editor no evento do Ronaldinho (Galacticos Games).
# Corta a fala pelas palavras da transcricao, cobre com b-roll, tonemap do HLG, legenda, trilha com ducking.
import hashlib, json, os, re, subprocess, sys, unicodedata
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
R = 'C:/Users/EDITING_SECTOR/Desktop/TODAS AS PASTAS/TUDO'
L = R + '/VLOGS/LUIS/'
BL = R + '/b-roll/b-roll lucas/'
J = R + '/b-roll/JOGO/'
T = R + '/b-roll/telao/'
M = R + '/b-roll/MONTAGEM DO STAND/'
MUS = 'C:/Users/EDITING_SECTOR/Desktop/TODAS AS PASTAS/VÍDEOS/MEU BANCO DE IMAGENS E SONS/MÚSICAS/MUSICA ANIMADA/gr0za-vlog-vlog-music-596442.mp3'
SAIDA = sys.argv[1] if len(sys.argv) > 1 else R + '/VLOGS/LUIS/EDITADOS/Luis_vlog_v1.mp4'
W = HERE + '/render'
FPS = 30
PAD = 0.07

CLIPES = {'C145': 'A001_10031328_C145.mov', '0138': 'IMG_0138.MOV', 's': 's.MOV', '0034': 'IMG_0034.MOV',
          '7111': 'IMG_7111.MOV', '0033': 'IMG_0033.MOV', '7160': 'IMG_7160.MOV', 'L16': 'L (16).MOV',
          'L32': 'L (32).MOV', 'L4': 'L (4).MOV'}
TX = {}
def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return re.sub(r'[^a-z0-9 ]', '', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))
def palavras(k):
    if k not in TX:
        n = CLIPES[k].rsplit('.', 1)[0]
        d = json.load(open(f'{HERE}/tr/{n}.json', encoding='utf8'))
        TX[k] = [w for w in d['words'] if w['type'] == 'word']
    return TX[k]
def frase(k, txt, depois=0.0):
    ws = palavras(k); alvo = norm(txt).split()
    for i in range(len(ws) - len(alvo) + 1):
        if ws[i]['start'] < depois: continue
        if [norm(w['text']).strip() for w in ws[i:i + len(alvo)]] == alvo:
            return ws[i]['start'], ws[i + len(alvo) - 1]['end'], ws[i:i + len(alvo)]
    raise SystemExit(f'frase nao achada em {k}: {txt}')

CORR = {'Uma': 'Human', 'SOS-': 'SOS'}
LADO = {'C145': (0.5, 0.47, 1.75)}   # fx, fy, zoom padrao por clipe

SEG = []   # cada um: dict(dur, voz, amb, vis=[(src,vin,dur,fx,fy,z)], cap=[...], capy)
def fala(k, txt, depois=0.0, over=None, z=None, capy=1085, cauda=0.0, vin=None, sem_leg=False):
    a, b, ws = frase(k, txt, depois)
    ini = max(0, a - PAD); fim = b + PAD + cauda
    d = round((fim - ini) * FPS) / FPS
    fx, fy, zz = LADO.get(k, (0.5, 0.5, 1.0))
    if z: zz = z
    src = L + CLIPES[k]
    vis = []; pos = 0.0
    if over:
        for o in over:
            s, vi, du = o[:3]; kw = o[3] if len(o) > 3 else {}
            if s is None:   # o proprio clipe
                vis.append((src, ini + pos, du, fx, fy, zz, None)); pos += du
            else:
                vis.append((s, vi, du, kw.get('fx', .5), kw.get('fy', .5), kw.get('z', 1.0), kw.get('box'))); pos += du
    if d - pos > 0.02:
        vis.append((src, (vin if vin is not None else ini + pos), d - pos, fx, fy, zz, None))
    caps = [] if sem_leg else [(w['start'] - ini, w['end'] - ini, CORR.get(w['text'], w['text'])) for w in ws]
    SEG.append(dict(dur=d, voz=(src, ini, d), amb=None, vis=vis, cap=caps, capy=capy))

def bx(src, vin, dur, fx=.5, fy=.5, z=1.0, amb=0.0, box=None):
    d = round(dur * FPS) / FPS
    SEG.append(dict(dur=d, voz=None, amb=(src, vin, d, amb) if amb else None, vis=[(src, vin, d, fx, fy, z, box)], cap=[], capy=1085))

# === GANCHO
fala('C145', 'Achou que eu ia ficar de fora do evento do Ronaldinho', depois=50)
fala('C145', 'Junto com a SOS Uma Help', depois=50, z=1.95)
fala('C145', 'venha com a gente acompanhar', depois=50)
fala('C145', 'um dia de filmmaking e editor de vídeo nesse evento', depois=50, capy=1400,
     over=[(BL + 'A001_10031824_C192.mov', 30, .85, dict(z=1.0)),
           (T + 'A001_10031308_C132.mov', 5, .85, dict(box=(.13, .06, .75, .54))),
           (J + 'L (106).MOV', 32, .9, dict())])
fala('C145', 'Vamos nessa', depois=50, z=2.05, cauda=.15)

# === VESPERA
i_vesp = len(SEG)
fala('0138', 'separei aqui alguns equipamentos que a gente vai levar hoje')
fala('0138', 'Hoje não é o dia oficial')
fala('0138', 'hoje é só um dia de backstage mesmo')
fala('0138', 'Peguei um bastão de LED', z=1.15)
fala('0138', 'Um microfone aqui pro nosso entrevistador', z=1.1)
fala('0138', 'Nós vamos levar esse gimbal grande')
fala('0138', 'que esse vai ficar com o Lucas')
fala('0138', 'E eu vou levar o gimbal pequeno', z=1.15)
fala('0138', 'pra fazer as minhas gravações')
fala('s', 'A minha dupla hoje', z=1.1)
fala('s', 'Dá um salve aqui, ô Lucas', z=1.0, cauda=.1)
fala('s', 'Beleza', cauda=.2)
fala('0034', 'Esse aqui é de quem tá na ONG há um mês', z=1.0)
fala('0034', 'equipamento de quem tá na ONG', z=1.1)
fala('0034', 'já tem um ano', z=1.1, cauda=.25)
fala('7111', 'A melhor parte de você ser um filmmaker')
fala('7111', 'nesses eventos que você gosta')
fala('7111', 'é que você conhece tudo, né', z=1.1)
fala('7111', 'Aqui é a loja oficial do Furacão', z=1.0)
bx(L + 'IMG_7112.MOV', 1.5, 2.0)
bx(L + 'IMG_0032.MOV', 1.5, 2.4)
bx(L + 'IMG_0070.MOV', 6.0, 2.0)
fala('0033', 'E pensar que amanhã', capy=1420)
fala('0033', 'isso aqui tudo vai tá lotado', capy=1420)
fala('0033', 'E o homem aqui vai tá em campo, hein', capy=1420, z=1.1)
fala('0033', 'E quem vai tá jogando lá', capy=1420)
fala('0033', 'Ronaldinho', capy=1420, z=1.15, cauda=.1)
fala('0033', 'Nada. Nada. Esse aqui, ó. Matheuzinho', capy=1420, cauda=.25)
bx(M + 'IMG_0081.MOV', 12, 1.3)
bx(M + 'montando (15).MOV', 14, 1.3)
bx(BL + 'A001_10031147_C078.mov', 3, 1.5, z=1.0)
fala('7160', 'Fala devagar, mano', capy=1300)
fala('7160', 'Cê tá emocionado, eu acho', capy=1300)
fala('7160', 'Não, não, eu falo assim mesmo', capy=1300)
fala('7160', 'Não é não, eu te conheço', capy=1300, cauda=.2)

# === DIA DO EVENTO
i_dia = len(SEG)
fala('L16', 'contagem regressiva pro evento', capy=1400)
fala('L16', 'Ontem foi o dia dos backstages', capy=1400)
fala('L16', 'tamo chegando aqui', capy=1400)
fala('L16', 'no estádio', capy=1400, depois=11.5)
fala('L16', 'e falaram pra gente que', capy=1400)
fala('L16', 'colocaram em todas as TVs', capy=1400)
fala('L16', 'imagens nossas da SOS', capy=1400,
     over=[(BL + 'A001_10031149_C083.mov', 9, .55, dict(fx=.32, fy=.5, z=1.15))])
bx(BL + 'A001_10031150_C084.mov', 12, 1.2, fx=.5, z=1.1)
fala('L16', 'acabei de pegar nossa credencial', capy=1400, depois=22.5)
fala('L16', 'pra gente entrar', capy=1400)
fala('L16', 'vamo ver lá dentro', capy=1400, cauda=-.06)
bx(T + 'A001_10031308_C132.mov', 4, 1.8, box=(.13, .06, .75, .54))
bx(T + 'IMG_0145.MOV', 5.3, 2.4, box=(.07, .08, .91, .62))
fala('L32', 'Pô, a sensação é muito massa, né')
fala('L32', 'desde criança, a gente se imagina num campo desse', z=1.12)
fala('L32', 'Eu nunca me imaginei pisando')
fala('L32', 'num gramado', depois=20.6)
fala('L32', 'e principalmente depois de velho', z=1.15, cauda=.1)
fala('L32', 'Mas', depois=23.9, z=1.0)
fala('L32', 'você estar aqui', z=1.0)
fala('L32', 'você vê no telão o trabalho da equipe toda sendo exposta', capy=1400,
     over=[(BL + 'A001_10031309_C135.mov', 4, 1.7, dict(box=(.15, .08, .85, .52))),
           (T + 'IMG_0144.MOV', 8, 1.45, dict(box=(.08, .08, .78, .62)))])
fala('L32', 'é algo muito gratificante', z=1.12)
fala('L32', 'Quando eu olhei a primeira vez', z=1.0)
fala('L32', 'eu fiquei todo arrepiado', z=1.2)
fala('L32', 'Isso motiva cada vez mais a gente continuar fazendo o que a gente faz', z=1.0, cauda=.1)

# === O EVENTO (musica sobe)
i_show = len(SEG)
bx(BL + 'A001_10031654_C147.mov', 60, 2.0, fx=.45, amb=.35)
bx(BL + 'A001_10031721_C157.mov', 3, 1.1, amb=.35)
bx(BL + 'A001_10032027_C206.mov', 3, 1.6, fx=.6, amb=.35)
bx(BL + 'A001_10031822_C188.mov', 2, 1.3, amb=.4)
bx(J + 'L (85).MOV', 1.5, 2.2)
bx(BL + 'A001_10031824_C192.mov', 28, 1.8, fx=.5, amb=.5)
bx(J + 'L (105).MOV', 30, 1.5, amb=.4)
bx(J + 'L (106).MOV', 30, 1.7)
bx(BL + 'A001_10031904_C196.mov', 48, 1.5, amb=.4)
bx(J + 'L (118).MOV', 20, 1.5, amb=.5)
bx(J + 'L (92).MOV', 40, 1.6, amb=.5)
bx(BL + 'A001_10031918_C199.mov', 30, 2.0, amb=.5)

# === FINAL
i_fim = len(SEG)
fala('L4', 'É, acho que no final o evento deu certo', depois=10, capy=1420)
fala('L4', 'Bora lá', depois=13, capy=1420, cauda=.9)

def sh(c, **k):
    r = subprocess.run(c, capture_output=True, text=True, encoding='utf8', errors='replace', **k)
    if r.returncode: raise SystemExit(' '.join(map(str, c))[:400] + '\n' + r.stderr[-1500:])
    return r.stdout
CT = {}
def transf(p):
    if p not in CT:
        CT[p] = sh(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=color_transfer', '-of', 'csv=p=0', p]).split()[0].strip(',')
    return CT[p]
TM = ('zscale=tin=arib-std-b67:pin=bt2020:min=bt2020nc:t=linear:npl=400,format=gbrpf32le,zscale=p=bt709,'
      'tonemap=hable:desat=0:peak=6,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=contrast=1.04:saturation=1.22:brightness=0.015')
def video(a):
    i, (src, vin, dur, fx, fy, z, box) = a
    o = f"{W}/v_{hashlib.md5(repr(a[1]).encode()).hexdigest()[:12]}.mkv"
    if os.path.exists(o): return o
    # cobre 1080x1920 com folga do zoom e recorta no foco
    sc = (f"fps={FPS},scale='ceil(max(1080*{z}/iw\\,1920*{z}/ih)*iw/2)*2':'ceil(max(1080*{z}/iw\\,1920*{z}/ih)*ih/2)*2':flags=lanczos,"
          f"crop=1080:1920:'(iw-1080)*{fx}':'(ih-1920)*{fy}',setsar=1")
    if box:   # telao inteiro: quadro recortado por cima do mesmo plano desfocado
        x0, y0, x1, y1 = box
        sc = (f"fps={FPS},split[a][b];[a]{sc.split(',', 1)[1]},gblur=sigma=38,eq=brightness=-0.13[bg];"
              f"[b]crop=iw*{x1 - x0}:ih*{y1 - y0}:iw*{x0}:ih*{y0},scale=1080:-2:flags=lanczos[fg];"
              f"[bg][fg]overlay=0:(H-h)/2,setsar=1")
    vf = sc + (',' + TM if transf(src) == 'arib-std-b67' else ',format=yuv420p')
    sh(['ffmpeg', '-v', 'error', '-y', '-ss', f'{vin:.3f}', '-t', f'{dur + .2:.3f}', '-i', src, '-an', '-vf', vf,
        '-frames:v', str(round(dur * FPS)), '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-colorspace', 'bt709',
        '-color_primaries', 'bt709', '-color_trc', 'bt709', o])
    return o
def trilha(p, ini, d, nome, gain=1.0):
    sh(['ffmpeg', '-v', 'error', '-y', '-ss', f'{ini:.3f}', '-t', f'{d:.4f}', '-i', p, '-vn', '-af',
        f'aresample=48000,aformat=channel_layouts=mono,apad,atrim=0:{d:.4f},volume={gain},afade=t=in:d=0.012,afade=t=out:st={max(0, d - .02):.4f}:d=0.02',
        '-c:a', 'pcm_s16le', nome])
def silencio(d, nome):
    sh(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono', '-t', f'{d:.4f}', '-c:a', 'pcm_s16le', nome])
def audio(a):
    i, s = a
    d = s['dur']
    if s['voz']: trilha(s['voz'][0], s['voz'][1], d, f'{W}/av{i:03d}.wav')
    else: silencio(d, f'{W}/av{i:03d}.wav')
    if s['amb']: trilha(s['amb'][0], s['amb'][1], d, f'{W}/aa{i:03d}.wav', s['amb'][3])
    else: silencio(d, f'{W}/aa{i:03d}.wav')

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h}:{m:02d}:{s:05.2f}'
def legenda(marcas):
    cab = ('\ufeff[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\n'
           'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
           'Style: Cap,Poppins,50,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,0,3,5,0,0,0,1\n'
           'Style: Tit,Poppins,62,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,0,4,5,0,0,0,1\n\n'
           '[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')
    ev = []; t = 0.0
    for s in SEG:
        grupo = []
        def fecha(fim):
            if grupo:
                ev.append((t + grupo[0][0], t + fim, s['capy'], ' '.join(g[2] for g in grupo)))
                grupo.clear()
        for c in s['cap']:
            if grupo and (len(grupo) >= 3 or len(' '.join(g[2] for g in grupo)) + len(c[2]) > 18 or re.search(r'[,.?!]$', grupo[-1][2])):
                fecha(c[0])
            grupo.append(c)
        if grupo: fecha(min(s['dur'], grupo[-1][1] + .12))
        t += s['dur']
    lin = [cab]
    for a, b, y, txt in ev:
        lin.append(f"Dialogue: 2,{ts(a)},{ts(b)},Cap,,0,0,0,,{{\\an5\\pos(540,{y})}}{txt}\n")
    for ini, d, txt, y in marcas:
        lin.append(f"Dialogue: 3,{ts(ini)},{ts(ini + d)},Tit,,0,0,0,,{{\\an5\\pos(540,{y})\\fad(160,200)}}{txt}\n")
    open(f'{W}/legendas.ass', 'w', encoding='utf8').write(''.join(lin))

def inicio(i): return sum(s['dur'] for s in SEG[:i])
def main():
    total = sum(s['dur'] for s in SEG)
    print('segmentos', len(SEG), 'duracao', round(total, 1), flush=True)
    vis = [v for s in SEG for v in s['vis']]
    with ThreadPoolExecutor(4) as ex:
        vs = list(ex.map(video, enumerate(vis)))
        list(ex.map(audio, enumerate(SEG)))
    open(f'{W}/lista.txt', 'w').write(''.join(f"file '{os.path.basename(v)}'\n" for v in vs))
    sh(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'lista.txt', '-c', 'copy', 'aroll.mkv'], cwd=W)
    for pre, nome in (('av', 'voz.wav'), ('aa', 'amb.wav')):
        open(f'{W}/l{pre}.txt', 'w').write(''.join(f"file '{pre}{i:03d}.wav'\n" for i in range(len(SEG))))
        sh(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'l{pre}.txt', '-c', 'copy', nome], cwd=W)
    tv, td, tsh = inicio(i_vesp), inicio(i_dia), inicio(i_show)
    marcas = [(0.1, 3.0, 'Um dia de editor\\Nno evento do Ronaldinho', 300), (tv + .1, 2.4, 'Um dia antes', 300),
              (td + .1, 2.6, 'Dia do evento', 300), (tsh + 5.0, 3.2, 'Mais de 40 mil pessoas', 300),
              (tsh + 8.6, 3.6, 'Mais de 60 toneladas\\Nde alimentos arrecadadas', 300), (total - 2.3, 2.2, '@soshumanhelppt', 1560)]
    legenda(marcas)
    fc = (f"[0:a]highpass=f=80,dynaudnorm=f=200:g=11:m=8:p=0.9,asplit=2[v1][vk];"
          f"[2:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.42,afade=t=out:st={total - 1.6:.2f}:d=1.6,atrim=0:{total:.3f}[mu];"
          f"[vk]aformat=channel_layouts=stereo[vk2];"
          f"[mu][vk2]sidechaincompress=threshold=0.03:ratio=9:attack=25:release=420:makeup=1[mud];"
          f"[v1][1:a]amix=inputs=2:normalize=0,aformat=channel_layouts=stereo[vs];"
          f"[vs][mud]amix=inputs=2:normalize=0,alimiter=limit=0.95:level=disabled[out]")
    sh(['ffmpeg', '-v', 'error', '-y', '-i', 'voz.wav', '-i', 'amb.wav', '-i', MUS, '-filter_complex', fc,
        '-map', '[out]', '-c:a', 'pcm_s16le', 'mix0.wav'], cwd=W)
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', 'mix0.wav', '-af', 'loudnorm=I=-15:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True, encoding='utf8', errors='replace', cwd=W)
    li = float(json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1])['input_i'])
    g = 10 ** ((-15 - li) / 20)
    print('LUFS medido', li, 'ganho', round(g, 3), flush=True)
    sh(['ffmpeg', '-v', 'error', '-y', '-i', 'mix0.wav', '-af', f'volume={g:.4f},alimiter=limit=0.84:level=disabled', '-c:a', 'aac', '-b:a', '256k', 'mix.m4a'], cwd=W)
    sh(['ffmpeg', '-v', 'error', '-y', '-i', 'aroll.mkv', '-i', 'mix.m4a', '-map', '0:v', '-map', '1:a', '-vf', 'ass=legendas.ass:fontsdir=fonts',
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
        '-c:a', 'copy', '-movflags', '+faststart', '-write_tmcd', '0', '-shortest', SAIDA], cwd=W)
    print('ok', SAIDA, flush=True)
if __name__ == '__main__':
    main()
