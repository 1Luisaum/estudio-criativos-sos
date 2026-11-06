# Troca o cenario sem tocar na crianca: recorta o video real e poe atras um fundo gerado na Magnific.
import sys,os,subprocess,time
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np,cv2
from PIL import Image
from rembg import remove,new_session
AQUI=os.path.dirname(os.path.abspath(__file__))
R=r"C:\Users\EDITING_SECTOR\Desktop\EDIÇÃO COM CLAUDE"
V=R+"\VÍDEOS PARA EDITAR\\"
SAIDA=R+"\EDITADOS\GANCHOS COM CENÁRIO"
FF=os.path.join(os.environ["LOCALAPPDATA"],"Programs","Python","Python312","ffmpeg.exe")
if not os.path.exists(FF): FF="ffmpeg"
# nome, bruto, inicio, fim, fundo, espelhar fundo, ganho do recorte (b,g,r)
G=[("pior noticia","20260917_000819.mp4",11.45,16.1,"sala",False,(.96,.97,.97)),
("e agora","20260917_000819.mp4",3.4,7.2,"quarto",False,(.95,.98,1.0)),
("amanhecer","20260916_235338.mp4",33.1,39.3,"amanhecer",False,(.95,.90,.88)),
("noites chorando","roteiro 9.mp4",52.5,59.35,"noite",False,(.80,.84,.88)),
("nao podem esperar","roteiro 9.mp4",48.95,52.2,"sala",True,(.96,.97,.97))]
ses=new_session("isnet-general-use",providers=["CPUExecutionProvider"])
os.makedirs(SAIDA,exist_ok=True)
so=sys.argv[1:]
for n,f,a,b,fu,esp,ganho in G:
    if so and n not in so: continue
    t0=time.time();src=V+f
    bg=cv2.imdecode(np.fromfile(f"{AQUI}/fundos/fundo_{fu}.jpg",np.uint8),1)  # imread nao abre caminho com acento
    h0,w0=bg.shape[:2];e=1080/w0;bg=cv2.resize(bg,(1080,int(h0*e)),interpolation=cv2.INTER_AREA)[:1920]
    if bg.shape[0]<1920: bg=cv2.resize(bg,(1080,1920))
    if esp: bg=bg[:,::-1]
    bg=cv2.GaussianBlur(bg,(0,0),2.2).astype(np.float32)
    ler=subprocess.Popen([FF,"-loglevel","error","-ss",str(a),"-t",str(b-a),"-i",src,"-vf","fps=30,scale=1080:1920","-f","rawvideo","-pix_fmt","bgr24","-"],stdout=subprocess.PIPE)
    tmp=f"{SAIDA}\_{n}.mp4";out=f"{SAIDA}\Gancho - {n}.mp4"
    esc=subprocess.Popen([FF,"-y","-loglevel","error","-f","rawvideo","-pix_fmt","bgr24","-s","1080x1920","-r","30","-i","-","-ss",str(a),"-t",str(b-a),"-i",src,"-map","0:v","-map","1:a","-c:v","libx264","-crf","17","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest",out],stdin=subprocess.PIPE)
    ant=None;i=0
    while True:
        b_=ler.stdout.read(1080*1920*3)
        if len(b_)<1080*1920*3: break
        fr=np.frombuffer(b_,np.uint8).reshape(1920,1080,3)
        m=np.array(remove(Image.fromarray(fr[:,:,::-1]),session=ses,only_mask=True,post_process_mask=False)).astype(np.float32)/255
        ant=m if ant is None else .55*m+.45*ant
        k=cv2.erode(ant,np.ones((3,3),np.uint8))
        k=cv2.GaussianBlur(k,(0,0),1.1)[...,None]
        sombra=cv2.GaussianBlur(np.roll(ant,18,0),(0,0),32)[...,None]
        fundo=bg*(1-.45*sombra)
        fg=fr.astype(np.float32)*np.array(ganho,dtype=np.float32)
        esc.stdin.write(np.clip(fg*k+fundo*(1-k),0,255).astype(np.uint8).tobytes());i+=1
        if i%30==0: print(n,i,f"{(time.time()-t0)/i:.1f}s/q",flush=True)
    esc.stdin.close();esc.wait();ler.wait()
    print("PRONTO",n,i,"quadros",round(time.time()-t0),"s",flush=True)
