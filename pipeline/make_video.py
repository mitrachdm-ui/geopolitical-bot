"""
Geopolitical_ – TikTok-Video-Generator (9:16, 1080x1920)

Aufruf:   python make_video.py <Video-Ordner>
          (der Ordner enthält slides.json; das Video landet im selben Ordner)

Stimme:   Ist das Paket "edge-tts" installiert (pip install edge-tts) und hat eine
          Folie ein Feld "say", wird der Text automatisch mit KI-Stimme vertont.
          Die Folie bleibt dann so lange stehen, wie der Satz dauert.
          Ohne edge-tts entsteht ein stummes Video (Stimme dann z. B. in CapCut).

Benötigt: Python 3.10+, Pillow, ffmpeg im PATH.
"""
import asyncio, json, os, shutil, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, XF = 1080, 1920, 30, 0.35          # XF = Überblendung in Sekunden
RM = 150                                       # rechter Rand frei für TikTok-Buttons
VOICE_DEFAULT = "de-DE-SeraphinaMultilingualNeural"   # gewählt 18.10.2026 (Stimmprobe Nr. 6)

# --- Farben (Markenfarben Geopolitical_) ---
BG, BG2 = (8, 13, 26), (22, 34, 62)
WHITE, GREY, DIM = (240, 243, 248), (150, 162, 185), (50, 62, 90)
AMBER, RED, GREEN, BLUE = (245, 180, 60), (232, 72, 72), (70, 200, 120), (90, 150, 240)
COLORS = {"AMBER": AMBER, "RED": RED, "GREEN": GREEN, "WHITE": WHITE, "BLUE": BLUE}

def _font_path(bold):
    cands = [os.path.join(HERE, "fonts", "Inter-Bold.otf" if bold else "Inter-Regular.otf"),
             r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    return next(p for p in cands if os.path.exists(p))
_FB, _FR = _font_path(True), _font_path(False)
_BLACK = os.path.join(HERE, "fonts", "Inter-Black.otf")
def font(size, bold=True, black=False):
    return ImageFont.truetype(_BLACK if black and os.path.exists(_BLACK) else (_FB if bold else _FR), size)

def wrap(d, text, fnt, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def base(idx, total, date, hook=False):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(BG[i] + (BG2[i] - BG[i]) * k) for i in range(3)))
    # dezenter Globus als Wasserzeichen
    import math
    cx, cy, R, LC = W * 0.78, H * 0.80, 520, (28, 42, 74)
    d.ellipse([cx-R, cy-R, cx+R, cy+R], outline=LC, width=4)
    for k in range(1, 6):
        rx = abs(R * math.cos(k * math.pi / 6)) or 1
        d.ellipse([cx-rx, cy-R, cx+rx, cy+R], outline=LC, width=3)
    for lat in (-60, -30, 0, 30, 60):
        yy = cy + R * math.sin(math.radians(lat)); hw = R * math.cos(math.radians(lat)); hh = hw * 0.3
        d.arc([cx-hw, yy-hh, cx+hw, yy+hh], 0, 180, fill=LC, width=3)
    # Fortschrittsbalken
    seg = (W - 140 - (total - 1) * 12) / total
    for i in range(total):
        x = 70 + i * (seg + 12)
        d.rounded_rectangle([x, 90, x + seg, 100], 5, fill=AMBER if i <= idx else DIM)
    if hook:   # Hook-Folie: nichts, was nach Info-Tafel aussieht (Analyse 20.10.: Absprung bei 0:01)
        return im, d
    # Kopfzeile: GEOPOLITICAL_
    f = font(44, black=True)
    d.text((70, 140), "GEOPOLITICAL", font=f, fill=WHITE)
    tw = d.textlength("GEOPOLITICAL", font=f)
    d.rectangle([70 + tw + 6, 180, 70 + tw + 40, 188], fill=AMBER)
    d.text((70, 200), date, font=font(32, False), fill=GREY)
    # Fußzeile (Pflicht: KI-Hinweis + keine Anlageberatung) – über der TikTok-UI
    d.text((70, H - 300), "KI-Stimme · Keine Anlageberatung · Quellen in der Beschreibung",
           font=font(26, False), fill=GREY)
    return im, d

def glow(im, cx, cy, r, col, strength=0.55):
    """Weicher Farbschein hinter der Hook-Zahl (mehr Kontrast im Feed)."""
    from PIL import ImageFilter
    g = Image.new("RGB", (W, H), (0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], fill=tuple(int(c * strength) for c in col))
    g = g.filter(ImageFilter.GaussianBlur(160))
    from PIL import ImageChops
    return ImageChops.add(im, g)

def render(s, idx, total, date, big_override=None):
    hook = idx == 0
    im, d = base(idx, total, date, hook)
    if hook and s.get("big"):
        im = glow(im, W * 0.42, 720, 620, COLORS.get(s.get("bigcolor", "RED"), RED))
        d = ImageDraw.Draw(im)
    y = 330 if hook else 400
    if s.get("tag"):
        tf = font(38)
        tw = d.textlength(s["tag"], font=tf) + 50
        d.rounded_rectangle([70, y, 70 + tw, y + 70], 14, fill=COLORS.get(s.get("tagcolor", "RED"), RED))
        d.text((95, y + 12), s["tag"], font=tf, fill=WHITE)
        y += 120
    if s.get("big"):
        bf = font(330 if hook else 230, black=True)
        while d.textlength(s["big"], font=bf) > W - 140: bf = font(bf.size - 10, black=True)
        d.text((62, y - 20), big_override if big_override is not None else s["big"], font=bf,
               fill=COLORS.get(s.get("bigcolor", "WHITE"), WHITE))
        y += bf.size + 40
    tf = font(96 if hook else 80)
    for line in wrap(d, s.get("title", ""), tf, W - 70 - RM):
        d.text((70, y), line, font=tf, fill=WHITE); y += tf.size + 16
    y += 40
    bfnt = font(48, False)
    for b in s.get("bullets", []):
        inv = b.startswith("!")          # "!▲ VIX" = steigt, ist aber schlecht -> rot
        b = b.lstrip("!")
        arrow = b[:1] in ("▲", "▼")
        col = GREEN if b.startswith("▲") else RED if b.startswith("▼") else WHITE
        if inv and arrow: col = RED if col == GREEN else GREEN
        x0 = 70 if arrow else 120
        if not arrow: d.ellipse([75, y + 20, 95, y + 40], fill=AMBER)
        for line in wrap(d, b, bfnt, W - x0 - RM):
            d.text((x0, y), line, font=bfnt, fill=col); y += 62
        y += 26
    if s.get("source") and not hook:
        d.text((70, H - 360), "Quelle: " + s["source"], font=font(26, False), fill=GREY)
    return im

def slide(s, idx, total, date, outdir):
    p = os.path.join(outdir, f"slide_{idx:02d}.png"); render(s, idx, total, date).save(p); return p

def countup_values(big, n):
    """'110 $' -> ['0 $', ..., '110 $'] (n Schritte). None, wenn keine Zahl am Anfang steht."""
    import re
    m = re.match(r"^([^0-9]*)([0-9][0-9.,]*)(.*)$", big)
    if not m: return None
    pre, num, post = m.groups()
    if re.fullmatch(r"(19|20)\d\d", num): return None          # Jahreszahlen nicht hochzählen
    dec = "," if "," in num else None
    val = float(num.replace(".", "").replace(",", "."))
    nd = len(num.split(",")[1]) if dec else 0
    out = []
    for k in range(1, n + 1):
        e = 1 - (1 - k / n) ** 3                                    # ease-out
        v = val * e
        t = f"{v:,.{nd}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        out.append(pre + t + post)
    return out

def hook_clip(s, total, date, dur, path):
    """Hook-Folie mit Bewegung ab Frame 1: Zahl zählt hoch, Bild zoomt von 108 % auf 100 %, danach langsamer Zoom."""
    nf = int(dur * FPS)
    cu_n = int(0.7 * FPS)
    vals = countup_values(s.get("big", ""), cu_n) if s.get("big") else None
    final = render(s, 0, total, date)
    cache = {}
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for f in range(nf):
        if vals and f < cu_n:
            v = vals[f]
            if v not in cache: cache[v] = render(s, 0, total, date, big_override=v)
            im = cache[v]
        else:
            im = final
        t = f / FPS
        z = 1.08 - 0.08 * min(t / 0.5, 1) ** 0.5 if t < 0.5 else 1.0 + 0.012 * (t - 0.5)   # Punch-in, dann Drift
        if z != 1.0:
            cw, ch = int(W / z), int(H / z)
            x0, y0 = (W - cw) // 2, int((H - ch) * 0.35)
            im = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)
        proc.stdin.write(im.tobytes())
    proc.stdin.close(); proc.wait()
    if proc.returncode: raise SystemExit("Hook-Clip fehlgeschlagen")

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

async def _tts(text, voice, rate, path):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=rate).save(path)

def make_voice(slides, data, tmp):
    try:
        import edge_tts  # noqa: F401
    except ImportError:
        print("Hinweis: edge-tts nicht installiert -> Video ohne Stimme.")
        return None
    voice, rate, files = data.get("voice", VOICE_DEFAULT), data.get("rate", "+18%"), []
    for i, s in enumerate(slides):
        if not s.get("say"): files.append(None); continue
        p = os.path.join(tmp, f"say_{i:02d}.mp3")
        print(f"Stimme Folie {i+1}/{len(slides)} …")
        raw = p.replace(".mp3", "_raw.mp3")
        asyncio.run(_tts(s["say"], voice, rate, raw))
        # lange Sprechpausen zwischen Sätzen kürzen (TikTok-Tempo)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
            "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.3:stop_threshold=-45dB:stop_silence=0.22",
            p], check=True)
        files.append(p)
    return files

def main():
    folder = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    data = json.load(open(os.path.join(folder, "slides.json"), encoding="utf-8"))
    slides = data["slides"]
    tmp = tempfile.mkdtemp(prefix="geo_")
    try:
        voices = make_voice(slides, data, tmp)
        durs = []
        for i, s in enumerate(slides):
            dur = float(s.get("sec", 6))
            if voices and voices[i]: dur = probe(voices[i]) + (0.1 if i == 0 else 0.35) + XF
            durs.append(dur)
        pngs = [slide(s, i, len(slides), data["date"], tmp) for i, s in enumerate(slides)]
        clips = []
        for i, (p, dur) in enumerate(zip(pngs, durs)):
            c = os.path.join(tmp, f"clip_{i:02d}.mp4")
            if i == 0:
                hook_clip(slides[0], len(slides), data["date"], dur, c); clips.append(c); continue
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", p, "-t", f"{dur:.2f}",
                "-vf", f"scale=1188:2112,zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(dur*FPS)}:s={W}x{H}:fps={FPS},format=yuv420p",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20", c], check=True)
            clips.append(c)
        # Video mit Überblendungen
        inputs, filt, last, off, starts = [], "", "0:v", 0.0, [0.0]
        for c in clips: inputs += ["-i", c]
        for i in range(1, len(clips)):
            off += durs[i - 1] - XF; starts.append(off)
            filt += f"[{last}][{i}:v]xfade=transition=slideleft:duration={XF}:offset={off:.2f}[v{i}];"; last = f"v{i}"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", *inputs]
        amap = []
        if voices and any(voices):
            n = len(clips); k = 0; labels = []
            for i, v in enumerate(voices):
                if not v: continue
                cmd += ["-i", v]
                ms = 0 if i == 0 else int((starts[i] + 0.25) * 1000)   # Hook: Stimme ab Frame 1
                filt += f"[{n+k}:a]adelay={ms}|{ms}[a{k}];"; labels.append(f"[a{k}]"); k += 1
            filt += f"{''.join(labels)}amix=inputs={k}:normalize=0[aout];"
            amap = ["-map", "[aout]", "-c:a", "aac", "-b:a", "160k"]
        out = os.path.join(folder, data["outfile"])
        cmd += ["-filter_complex", filt.rstrip(";"), "-map", f"[{last}]", *amap,
                "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
        if len(clips) == 1:  # Sonderfall: nur eine Folie
            shutil.copy(clips[0], out)
        else:
            subprocess.run(cmd, check=True)
        L = probe(out)
        print(f"Fertig: {out}  ({L:.0f} s)")
        if L > 60:
            print(f"::warning::Video ist {L:.0f} s lang – Limit 60 s. Text kürzen und neu rendern.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
