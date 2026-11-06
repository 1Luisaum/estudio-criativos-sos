"""Folhas de contato: olhar muito material gastando uma imagem so.

  videos   --out f.jpg [--frames 12] v1.mp4 v2.mp4 ...   uma linha por video (rotulos B01, B02...)
  timeline --out f.jpg [--every 12] video.mp4             quadros com o tempo escrito (achar o trecho do b-roll)
  photos   --out f.jpg pasta                               fotos numeradas (ignora copias "(1)")
  frames   --out f.jpg --at 0.4,3,38.8 video.mp4          quadros lado a lado (conferir o video final)

Uso: python -I sheets.py videos --out C:/tmp/folha.jpg "C:/.../banco/a.mp4" "C:/.../banco/b.mp4"
"""
import argparse, os, shutil, subprocess, sys, tempfile

TILE_W, TILE_H = 160, 284


def work():
    d = tempfile.mkdtemp(prefix="sheet_")
    # drawtext com caminho absoluto do Windows quebra no escape do "C:"; fonte relativa + cwd resolve
    shutil.copy(r"C:\Windows\Fonts\arialbd.ttf", os.path.join(d, "f.ttf"))
    return d


def ff(args, cwd):
    r = subprocess.run(["ffmpeg", "-v", "error", "-y"] + args, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode:
        sys.exit(r.stderr[-1500:])


def duration(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                         capture_output=True, text=True).stdout.strip()
    return float(out)


def label(text):
    return f"drawtext=fontfile=f.ttf:text='{text}':fontcolor=yellow:fontsize=34:x=4:y=4:box=1:boxcolor=black@0.7"


def videos(a):
    d = work()
    rows = []
    for i, v in enumerate(a.inputs, start=1):
        n = a.frames
        row = os.path.join(d, f"r{i:02d}.png")
        ff(["-i", v, "-vf", f"fps={n}/{duration(v)},scale={TILE_W}:{TILE_H}:force_original_aspect_ratio=decrease,"
            f"pad={TILE_W}:{TILE_H}:(ow-iw)/2:(oh-ih)/2,tile={n}x1,pad={TILE_W * n}:{TILE_H}:0:0:black,{label(f'B{i:02d}')}",
            "-frames:v", "1", row], d)
        rows.append(row)
        print(f"B{i:02d} = {v}  ({duration(v):.1f}s, {n} quadros)")
    inputs = sum([["-i", r] for r in rows], [])
    ff(inputs + ["-filter_complex", f"vstack={len(rows)}" if len(rows) > 1 else "null", a.out], d)


def timeline(a):
    d = work()
    v = a.inputs[0]
    n = int(duration(v) // a.every) + 1
    cols = min(n, 14)
    rows = -(-n // cols)
    ff(["-i", v, "-vf", f"fps=1/{a.every},scale=200:356:force_original_aspect_ratio=decrease,pad=200:356:(ow-iw)/2:(oh-ih)/2,"
        "drawtext=fontfile=f.ttf:text='%{pts\\:hms}':fontcolor=yellow:fontsize=22:x=4:y=4:box=1:boxcolor=black,"
        f"tile={cols}x{rows}", "-frames:v", "1", a.out], d)
    print(f"{n} quadros, 1 a cada {a.every}s")


def photos(a):
    d = work()
    folder = a.inputs[0]
    names = sorted(f for f in os.listdir(folder)
                   if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) and "(1)" not in f)
    for i, f in enumerate(names, start=1):
        ff(["-i", os.path.join(folder, f), "-vf", f"scale=200:356:force_original_aspect_ratio=decrease,"
            f"pad=200:356:(ow-iw)/2:(oh-ih)/2,{label(str(i))}", os.path.join(d, f"{i:03d}.png")], d)
        print(f"{i:3d} = {f}")
    ff(["-framerate", "1", "-start_number", "1", "-i", "%03d.png", "-vf", "tile=13x4", "-frames:v", "1", a.out], d)


def frames(a):
    d = work()
    v = a.inputs[0]
    ts = [float(t) for t in a.at.split(",")]
    for i, t in enumerate(ts):
        ff(["-ss", f"{t}", "-i", v, "-frames:v", "1", "-vf", f"scale=270:480,{label(f'{t:g}s')}", f"q{i:02d}.png"], d)
    ff(["-framerate", "1", "-i", "q%02d.png", "-vf", f"tile={min(len(ts), 6)}x{-(-len(ts) // 6)}",
        "-frames:v", "1", a.out], d)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["videos", "timeline", "photos", "frames"])
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--frames", type=int, default=12)
    ap.add_argument("--every", type=float, default=12)
    ap.add_argument("--at", default="0.4,3,10,20,30")
    a = ap.parse_args()
    a.out = os.path.abspath(a.out)
    {"videos": videos, "timeline": timeline, "photos": photos, "frames": frames}[a.mode](a)
    print("folha:", a.out)
