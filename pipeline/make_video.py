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
TEAL = (0, 150, 160)
SERIES = None          # Serien-Name fürs Logo, aus slides.json ("series")
THEME = "tag"          # "tag" (Mo–Fr) · "erklaert" (Sonntag) · "ausblick" (Samstag, Serie WOCHENRÜCKBLICK)
ACCENT = AMBER
LAND, LAND_EDGE, HL, HL_EDGE = (24, 37, 66), (48, 68, 108), (232, 72, 72), (255, 120, 120)
def accent(): return ACCENT
COLORS = {"TEAL": TEAL, "AMBER": AMBER, "RED": RED, "GREEN": GREEN, "WHITE": WHITE, "BLUE": BLUE}

def apply_theme(name):
    """Serien-Looks. Sonntag = helles Atlas-Papier, Samstag = Anthrazit mit Kalenderkarten."""
    global BG, BG2, WHITE, GREY, DIM, ACCENT, LAND, LAND_EDGE, HL, HL_EDGE, THEME, GREEN, RED
    THEME = name or "tag"
    if THEME == "erklaert":
        BG, BG2 = (246, 241, 230), (232, 224, 206)
        WHITE, GREY, DIM = (22, 30, 48), (110, 108, 100), (210, 200, 180)
        ACCENT = TEAL
        LAND, LAND_EDGE = (225, 214, 190), (196, 182, 152)
        HL, HL_EDGE = (0, 150, 160), (0, 110, 120)
        GREEN, RED = (20, 140, 80), (200, 50, 50)
    elif THEME == "ausblick":
        BG, BG2 = (16, 16, 19), (40, 36, 31)
        WHITE, GREY, DIM = (244, 240, 232), (168, 160, 148), (70, 64, 56)
        ACCENT = AMBER
        LAND, LAND_EDGE = (44, 41, 37), (78, 72, 64)
        HL, HL_EDGE = (245, 180, 60), (255, 215, 130)
    COLORS.update({"WHITE": WHITE, "RED": RED, "GREEN": GREEN})

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

def series_badge(d, x, y):
    f = font(34, black=True); tw = d.textlength(SERIES, font=f)
    d.rounded_rectangle([x, y, x + tw + 44, y + 58], 29, fill=ACCENT)
    d.text((x + 22, y + 9), SERIES, font=f, fill=(255, 255, 255) if THEME == "erklaert" else (20, 18, 15))

def base(idx, total, date, hook=False, bar=True, globe=True):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(BG[i] + (BG2[i] - BG[i]) * k) for i in range(3)))
    import math
    if not globe:   # Weltkarte statt Globus (wird in layout() gezeichnet)
        cx = None
    # dezenter Globus als Wasserzeichen
    cx, cy, R, LC = W * 0.78, H * 0.80, 520, (28, 42, 74)
    for k in (range(1, 6) if globe else []):
        rx = abs(R * math.cos(k * math.pi / 6)) or 1
        d.ellipse([cx-rx, cy-R, cx+rx, cy+R], outline=LC, width=3)
    if globe: d.ellipse([cx-R, cy-R, cx+R, cy+R], outline=LC, width=4)
    for lat in ((-60, -30, 0, 30, 60) if globe else ()):
        yy = cy + R * math.sin(math.radians(lat)); hw = R * math.cos(math.radians(lat)); hh = hw * 0.3
        if globe: d.arc([cx-hw, yy-hh, cx+hw, yy+hh], 0, 180, fill=LC, width=3)
    # Fortschrittsbalken
    seg = (W - 140 - (total - 1) * 12) / total
    for i in (range(total) if bar else []):
        x = 70 + i * (seg + 12)
        d.rounded_rectangle([x, 90, x + seg, 100], 5, fill=AMBER if i <= idx else DIM)
    if hook and SERIES:   # Serien-Logo auch auf dem Hook (klein, oben)
        series_badge(d, 70, 140)
    if hook:   # Hook-Folie: nichts, was nach Info-Tafel aussieht (Analyse 20.10.: Absprung bei 0:01)
        return im, d
    # Kopfzeile: GEOPOLITICAL_
    f = font(44, black=True)
    d.text((70, 140), "GEOPOLITICAL", font=f, fill=WHITE)
    tw = d.textlength("GEOPOLITICAL", font=f)
    d.rectangle([70 + tw + 6, 180, 70 + tw + 40, 188], fill=accent())
    d.text((70, 200), date, font=font(32, False), fill=GREY)
    if SERIES: series_badge(d, 70 + tw + 70, 143)
    # Fußzeile (Pflicht: KI-Hinweis + keine Anlageberatung) – über der TikTok-UI
    d.text((70, H - 300), "KI-Stimme · Keine Anlageberatung · Quellen in der Beschreibung",
           font=font(26, False), fill=GREY)
    return im, d

def glow(im, cx, cy, r, col, strength=0.55):
    if THEME == "erklaert": return im
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
    for bn, b in enumerate(s.get("bullets", []), 1):
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


# ======================= Animations-Engine (seit 20.10.2026) =======================
# Jede Folie wird Bild für Bild gerendert: Elemente fliegen nacheinander ein, Stichpunkte
# erscheinen im Takt der Stimme, der Fortschrittsbalken läuft mit, Zahlen zählen hoch.

def ease(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def sprite(w, h):
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)


# ============================ Weltkarte (seit 20.10.2026) ============================
# Hintergrund = Weltkarte (Natural Earth, gemeinfrei). Betroffene Länder leuchten rot und
# pulsieren; die Karte zoomt automatisch auf die Region. Steuerung pro Folie in slides.json:
#   "map": ["SAU", "YEM"]   Ländercodes (ISO-3/ADM0_A3) – sonst automatisch aus dem Tag
#   "map": []               nur Weltkarte, nichts markiert
#   "map_box": [lon1, lat1, lon2, lat2]   Ausschnitt manuell
_WORLD = None
def world():
    global _WORLD
    if _WORLD is None:
        p = os.path.join(HERE, "assets", "welt.json")
        _WORLD = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
    return _WORLD

ALIAS = {   # Wörter aus Tags -> Ländercodes
    "USA": ["USA"], "US": ["USA"], "WASHINGTON": ["USA"], "RUSSLAND": ["RUS"], "MOSKAU": ["RUS"],
    "UKRAINE": ["UKR"], "KIEW": ["UKR"], "CHINA": ["CHN"], "PEKING": ["CHN"], "TAIWAN": ["TWN"], "TAIPEH": ["TWN"],
    "IRAN": ["IRN"], "TEHERAN": ["IRN"], "ISRAEL": ["ISR"], "GAZA": ["PSX", "ISR"], "LIBANON": ["LBN"],
    "JEMEN": ["YEM"], "HUTHIS": ["YEM"], "SAUDI-ARABIEN": ["SAU"], "RIAD": ["SAU"], "KATAR": ["QAT"],
    "VAE": ["ARE"], "DUBAI": ["ARE"], "OMAN": ["OMN"], "IRAK": ["IRQ"], "SYRIEN": ["SYR"], "TÜRKEI": ["TUR"],
    "ÄGYPTEN": ["EGY"], "SUEZ": ["EGY"], "HORMUS": ["IRN", "OMN", "ARE"], "ROTES": ["YEM", "ERI", "SAU"],
    "NORDKOREA": ["PRK"], "SÜDKOREA": ["KOR"], "JAPAN": ["JPN"], "INDIEN": ["IND"], "PAKISTAN": ["PAK"],
    "DEUTSCHLAND": ["DEU"], "BERLIN": ["DEU"], "FRANKREICH": ["FRA"], "POLEN": ["POL"], "EU": ["EUR"],
    "NATO": ["NATO"], "VENEZUELA": ["VEN"], "BRASILIEN": ["BRA"], "PHILIPPINEN": ["PHL"], "OPEC": ["SAU", "IRQ", "ARE", "KWT", "IRN"],
}
GROUPS = {"EUR": ["DEU", "FRA", "ITA", "ESP", "POL", "NLD", "BEL", "AUT", "SWE", "FIN", "DNK", "PRT", "GRC", "CZE", "HUN", "ROU", "BGR", "SVK", "HRV", "SVN", "IRL", "LTU", "LVA", "EST", "LUX"],
          "NATO": ["USA", "CAN", "GBR", "DEU", "FRA", "ITA", "ESP", "POL", "NLD", "BEL", "NOR", "TUR", "SWE", "FIN", "DNK", "PRT", "GRC", "CZE", "HUN", "ROU", "BGR", "SVK", "HRV", "SVN", "LTU", "LVA", "EST", "LUX", "ALB", "MNE", "MKD", "ISL"]}

def map_codes(s):
    if "map" in s: codes = s["map"]
    else:
        codes = []
        for w in s.get("tag", "").replace("·", " ").split():
            codes += ALIAS.get(w.upper(), [])
        names = {c["de"].upper(): c["a3"] for c in world() if c.get("de")}
        for w in s.get("tag", "").split("·"):
            if w.strip().upper() in names: codes.append(names[w.strip().upper()])
    out = []
    for c in codes: out += GROUPS.get(c, [c])
    return list(dict.fromkeys(out))

def draw_map(bg, s, hook):
    """Zeichnet die Karte auf bg; gibt (Hintergrund, Markierungs-Ebene RGBA oder None) zurück."""
    import math
    from PIL import ImageFilter
    W_ = world()
    if not W_: return bg, None
    codes = set(map_codes(s))
    sel = [c for c in W_ if c["a3"] in codes]
    def bbox(cs):
        xs = [x for c in cs for poly in c["p"] for x, _ in poly[0]]
        ys = [y for c in cs for poly in c["p"] for _, y in poly[0]]
        return min(xs), min(ys), max(xs), max(ys)
    world_view = False
    if s.get("map_box"): lo1, la1, lo2, la2 = s["map_box"]
    elif sel:   # Ausschnitt = zuerst genanntes Land (Hauptschauplatz)
        first = ([c for c in sel if c["a3"] == map_codes(s)[0]] or sel[:1])[0]
        def area(poly):
            xs = [x for x, _ in poly[0]]; ys = [y for _, y in poly[0]]
            return (max(xs) - min(xs)) * (max(ys) - min(ys))
        core = max(first["p"], key=area)        # Hauptfläche (ohne Alaska/Hawaii/Inseln)
        lo1, la1, lo2, la2 = bbox([{"p": [core]}])
        if lo2 - lo1 > 300: lo1, lo2 = 20, 180               # Russland über Datumsgrenze
    else:
        lo1, la1, lo2, la2 = -50, 0, 110, 60; world_view = True   # Europa/Nahost/Asien im Blick
    clat = (la1 + la2) / 2; kx = math.cos(math.radians(max(min(clat, 70), -70)))
    if world_view:
        sc = W / ((lo2 - lo1) * kx)
    else:   # Markierung passt in das untere Feld (ca. 55–83 % der Höhe)
        sc = min(W * 0.58 / max((lo2 - lo1) * kx, 10), H * 0.21 / max(la2 - la1, 7))
        sc = max(sc, W / 110)
    cxl, cyl = (lo1 + lo2) / 2, clat
    ox, oy = W * 0.52, H * 0.68
    if s.get("cal") and not world_view: sc *= 0.75; oy = H * 0.74     # Kalenderkarte braucht Platz
    fx1, fy1, fx2, fy2 = lo1, la1, lo2, la2
    def P(x, y): return (ox + (x - cxl) * kx * sc, oy - (y - cyl) * sc)
    mc = map_codes(s)
    draw_map.last = dict(lon=cxl, lat=cyl, sc=sc, ox=ox, oy=oy, codes=set(mc), main=(mc[0] if mc else None),
                         world=world_view or not sel)
    land = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(land)
    for c in W_:
        if c["a3"] in codes: continue
        for poly in c["p"]:
            pts = [P(x, y) for x, y in poly[0]]
            if len(pts) > 2: dl.polygon(pts, fill=LAND + (255,), outline=LAND_EDGE + (255,))
    hl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dh = ImageDraw.Draw(hl)
    farea = max((fx2 - fx1) * (fy2 - fy1), 1)
    mainl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dm = ImageDraw.Draw(mainl)
    for c in sel:
        bx1, by1, bx2, by2 = bbox([c])
        main = c["a3"] == map_codes(s)[0]
        huge = not main and (bx2 - bx1) * (by2 - by1) > 4 * farea   # Riesenland (z. B. Russland) nur andeuten
        for poly in c["p"]:
            pts = [P(x, y) for x, y in poly[0]]
            if len(pts) > 2:
                dh.polygon(pts, fill=HL + (255 if main else (0 if huge else 90),), outline=HL_EDGE + (255,))
                if main: dm.polygon(pts, fill=HL + (255,))
                if huge: dh.line(pts + pts[:1], fill=HL_EDGE + (200,), width=3)
    # sanft nach oben ausblenden, damit Text lesbar bleibt
    fade = Image.linear_gradient("L").resize((W, H))      # 0 oben … 255 unten
    fade = fade.point(lambda v: int(min(255, max(0, (v - 40) * 1.6))))
    land.putalpha(Image.composite(land.getchannel("A"), Image.new("L", (W, H), 0), fade))
    bg = bg.convert("RGBA"); bg.alpha_composite(land)
    if sel:
        g = mainl.filter(ImageFilter.GaussianBlur(40))   # Schein nur ums Hauptland
        g.putalpha(g.getchannel("A").point(lambda v: int(v * 0.8)))
        bg.alpha_composite(g)                              # roter Schein (statisch)
        return bg.convert("RGB"), hl
    return bg.convert("RGB"), None

def layout(s, idx, total, date):
    """Hintergrund (statisch) + Liste animierter Elemente: dict(img, x, y, kind, fx)."""
    hook = idx == 0
    has_map = bool(world())
    bg, d = base(idx, total, date, hook, bar=False, globe=not has_map)
    hl = None
    plain = bg.copy()
    layout.last_map = None
    if has_map:
        bg, hl = draw_map(bg, s, hook); d = ImageDraw.Draw(bg)
        layout.last_map = draw_map.last
    dbig = {"erklaert": "TEAL", "ausblick": "AMBER"}.get(THEME, "RED" if hook else "WHITE")
    col_big = COLORS.get(s.get("bigcolor", dbig), WHITE)
    def decorate(img):
        dd_ = ImageDraw.Draw(img)
        if has_map and not hook:
            dd_.text((70, H - 300), "KI-Stimme · Keine Anlageberatung · Quellen in der Beschreibung",
                     font=font(26, False), fill=GREY)
        if s.get("big"):
            img = glow(img, W * 0.42, 720 if hook else 640, 620 if hook else 480, col_big, 0.55 if hook else 0.35)
            dd_ = ImageDraw.Draw(img)
        if s.get("source") and not hook:
            dd_.text((70, H - 360), "Quelle: " + s["source"], font=font(26, False), fill=GREY)
        return img
    bg = decorate(bg); d = ImageDraw.Draw(bg)
    layout.last_plain = decorate(plain) if has_map else None
    els, y = [], (330 if hook else 400)
    if s.get("tag"):
        tf = font(38); tw = d.textlength(s["tag"], font=tf) + 50
        im, dd = sprite(tw, 70)
        dflt = {"erklaert": "TEAL", "ausblick": "AMBER"}.get(THEME, "RED")
        dd.rounded_rectangle([0, 0, tw - 1, 69], 14, fill=COLORS.get(s.get("tagcolor", dflt), RED))
        dd.text((25, 12), s["tag"], font=tf, fill=(255, 255, 255) if THEME != "ausblick" else (20, 18, 15))
        els.append(dict(img=im, x=70, y=y, kind="tag", fx="left")); y += 120
    if s.get("cal"):
        wd, day, mon = (s["cal"] + ["", "", ""])[:3]
        cw, ch = 300, 330
        im, dd = sprite(cw, ch)
        dd.rounded_rectangle([0, 0, cw - 1, ch - 1], 28, fill=(250, 246, 238))
        dd.rounded_rectangle([0, 0, cw - 1, 96], 28, fill=AMBER); dd.rectangle([0, 60, cw - 1, 96], fill=AMBER)
        f1 = font(52, black=True); dd.text(((cw - dd.textlength(wd, font=f1)) / 2, 18), wd, font=f1, fill=(20, 18, 15))
        f2 = font(150, black=True); dd.text(((cw - dd.textlength(day, font=f2)) / 2, 100), day, font=f2, fill=(20, 18, 15))
        f3 = font(44); dd.text(((cw - dd.textlength(mon, font=f3)) / 2, 262), mon, font=f3, fill=(120, 110, 95))
        els.append(dict(img=im, x=70, y=y, kind="tag", fx="up")); y += ch + 50
    if s.get("big"):
        bf = font(330 if hook else 230, black=True)
        while d.textlength(s["big"], font=bf) > W - 140: bf = font(bf.size - 10, black=True)
        els.append(dict(text=s["big"], font=bf, col=col_big, x=62, y=y - 20, kind="big", fx="pop"))
        y += bf.size + 40
    tf = font(96 if hook else 80)
    lines = wrap(d, s.get("title", ""), tf, W - 70 - RM)
    if lines and lines[0]:
        lh = tf.size + 16
        im, dd = sprite(W - 70, lh * len(lines) + 20)
        for k, line in enumerate(lines): dd.text((0, k * lh), line, font=tf, fill=WHITE)
        els.append(dict(img=im, x=70, y=y, kind="title", fx="up")); y += lh * len(lines)
    y += 40
    bfnt = font(48, False)
    for bn, b in enumerate(s.get("bullets", []), 1):
        inv = b.startswith("!"); b = b.lstrip("!")
        arrow = b[:1] in ("▲", "▼")
        col = GREEN if b.startswith("▲") else RED if b.startswith("▼") else WHITE
        if inv and arrow: col = RED if col == GREEN else GREEN
        x0 = 70 if arrow else 120
        bl = wrap(d, b, bfnt, W - x0 - RM)
        im, dd = sprite(W - 70, 62 * len(bl) + 10)
        if not arrow and THEME == "erklaert":
            dd.ellipse([0, 4, 40, 44], fill=ACCENT)
            nf = font(28, black=True); dd.text((20 - dd.textlength(str(bn), font=nf) / 2, 8), str(bn), font=nf, fill=(255, 255, 255))
        elif not arrow: dd.ellipse([5, 20, 25, 40], fill=accent())
        for k, line in enumerate(bl): dd.text((x0 - 70, k * 62), line, font=bfnt, fill=col)
        els.append(dict(img=im, x=70, y=y, kind="bullet", fx="right")); y += 62 * len(bl) + 26
    if not hook and els and not world():   # ohne Karte: Inhalt mittig im sichtbaren Bereich (unten liegt die TikTok-Beschriftung)
        top, bottom = 330, H - 520
        shift = max(0, int((bottom - top - (y - els[0]["y"])) / 2 + top - els[0]["y"]))
        for e in els: e["y"] += shift
    return bg, els, hl


# ============================ Globus-Übergang (seit 22.10.2026) ============================
# Zu Beginn jeder Folie mit neuem Schauplatz: 3D-Globus dreht sich vom letzten Schauplatz zum
# neuen, das Zielland leuchtet, dann Zoom hinein und Überblendung in die flache Karte.
GLOBE_T = 1.4          # Dauer der Globus-Phase in Sekunden
LAST_CENTER = [None]   # (lon, lat) des vorherigen Schauplatzes

def ocean_col():
    return {"erklaert": (214, 228, 228), "ausblick": (30, 28, 25)}.get(THEME, (14, 26, 52))

def render_globe(lon0, lat0, R, cx, cy, codes, main):
    import math
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    # Atmosphäre + Ozean
    for k, a in ((26, 30), (16, 55), (8, 90)):
        d.ellipse([cx - R - k, cy - R - k, cx + R + k, cy + R + k], outline=ACCENT + (a,), width=6)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=ocean_col() + (255,))
    p0, l0 = math.radians(lat0), math.radians(lon0)
    sp0, cp0 = math.sin(p0), math.cos(p0)
    def proj(lon, lat):
        p, l = math.radians(lat), math.radians(lon) - l0
        cosc = sp0 * math.sin(p) + cp0 * math.cos(p) * math.cos(l)
        x = math.cos(p) * math.sin(l); y = cp0 * math.sin(p) - sp0 * math.cos(p) * math.cos(l)
        if cosc < 0:                       # Rückseite: auf den Rand projizieren
            n = math.hypot(x, y) or 1; x, y = x / n, y / n
        return cx + R * x, cy - R * y, cosc >= 0
    # Gradnetz
    gcol = LAND_EDGE + (90,)
    for lon in range(-180, 180, 30):
        seg = [proj(lon, la) for la in range(-90, 91, 5)]
        for a, b in zip(seg, seg[1:]):
            if a[2] and b[2]: d.line([a[:2], b[:2]], fill=gcol, width=2)
    for lat in range(-60, 61, 30):
        seg = [proj(lo, lat) for lo in range(-180, 181, 5)]
        for a, b in zip(seg, seg[1:]):
            if a[2] and b[2]: d.line([a[:2], b[:2]], fill=gcol, width=2)
    # Länder
    for c in world():
        hot = c["a3"] in codes; is_main = c["a3"] == main
        for poly in c["p"]:
            pts = [proj(x, y) for x, y in poly[0]]
            if not any(v for _, _, v in pts) or len(pts) < 3: continue
            xy = [(x, y) for x, y, _ in pts]
            if is_main: d.polygon(xy, fill=HL + (255,), outline=HL_EDGE + (255,))
            elif hot:   d.polygon(xy, fill=tuple((a + b) // 2 for a, b in zip(HL, LAND)) + (255,), outline=HL_EDGE + (255,))
            else:       d.polygon(xy, fill=LAND + (255,), outline=LAND_EDGE + (255,))
    return L

def globe_frames(mapinfo, prev, nf):
    """Liefert eine Funktion f(i) -> RGBA-Ebene für Bild i der Globus-Phase (oder None danach)."""
    import math
    lon1, lat1 = mapinfo["lon"], mapinfo["lat"]
    lon0, lat0 = prev if prev else (lon1 - 110, 20)
    dl = ((lon1 - lon0 + 180) % 360) - 180          # kürzester Weg
    if prev and abs(dl) < 25 and abs(lat1 - lat0) < 15:   # Nachbarland: etwas mehr Schwung
        lon0 = lon1 - 40; dl = 40
    R0 = 430
    R1 = mapinfo["sc"] * 180 / math.pi              # Maßstab der flachen Karte
    cx, cy = mapinfo["ox"], mapinfo["oy"]
    def f(i):
        t = i / FPS
        if t >= GLOBE_T: return None, 0.0
        r = ease(t / 0.8)                            # Drehung
        z = ease((t - 0.75) / 0.55)                  # Zoom
        lon = lon0 + dl * r; lat = lat0 + (lat1 - lat0) * r
        R = R0 * (R1 / R0) ** z if R1 > 0 else R0
        fade = max(0.0, min(1.0, (t - (GLOBE_T - 0.3)) / 0.3))   # Überblendung zur flachen Karte
        return render_globe(lon, lat, R, cx, cy, mapinfo["codes"], mapinfo["main"]), fade
    return f

def schedule(els, dur, hook):
    """Einblendzeitpunkte: Tag/Zahl/Titel sofort, Stichpunkte gleichmäßig über die Sprechzeit."""
    bullets = [e for e in els if e["kind"] == "bullet"]
    t = 0.0 if hook else 0.05
    for e in els:
        if e["kind"] in ("tag", "big", "title"):
            e["t"] = t; t += 0.0 if hook else 0.12
    span = max(dur - XF - 1.2, 0.5)
    for k, e in enumerate(bullets):
        e["t"] = 0.55 + span * k / max(len(bullets), 1)
    return [e["t"] for e in bullets]

def big_sprite(e, text, cache):
    if text not in cache:
        tw = int(ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(text, font=e["font"])) + 40
        im, dd = sprite(tw, e["font"].size * 1.3)
        dd.text((0, 0), text, font=e["font"], fill=e["col"])
        cache[text] = im
    return cache[text]

def anim_clip(s, idx, total, date, dur, path):
    hook = idx == 0
    bg, els, hl = layout(s, idx, total, date)
    pops = schedule(els, dur, hook)
    mi, plain = layout.last_map, layout.last_plain
    gf = None
    if mi and not mi["world"] and s.get("globe", True):
        prev = LAST_CENTER[0]
        same = prev and abs(((mi["lon"] - prev[0] + 180) % 360) - 180) < 3 and abs(mi["lat"] - prev[1]) < 3
        if not same: gf = globe_frames(mi, prev, int(GLOBE_T * FPS))
        LAST_CENTER[0] = (mi["lon"], mi["lat"])
    pulse = []
    if hl is not None:   # 12 Helligkeitsstufen vorberechnen, dann pulsieren lassen
        import math
        A = hl.getchannel("A")
        for k in range(12):
            lv = hl.copy(); lv.putalpha(A.point(lambda v, f=0.55 + 0.4 * k / 11: int(v * f))); pulse.append(lv)
    nf, cache = int(dur * FPS), {}
    cu = countup_values(s["big"], int(0.7 * FPS)) if s.get("big") else None
    seg = (W - 140 - (total - 1) * 12) / total
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for f in range(nf):
        t = f / FPS
        g_layer, g_fade = gf(f) if gf else (None, 1.0)
        if g_layer is not None:
            base_g = plain.copy().convert("RGBA"); base_g.alpha_composite(g_layer)
            fr = Image.blend(base_g, bg.convert("RGBA"), g_fade) if g_fade > 0 else base_g
        else:
            fr = bg.copy().convert("RGBA")
        if pulse and g_layer is None:
            ph = (math.sin(2 * math.pi * t / 1.4) + 1) / 2          # ein Puls alle 1,4 s
            fr.alpha_composite(pulse[int(ph * 11)])
        d = ImageDraw.Draw(fr)
        for i in range(total):                       # Fortschrittsbalken läuft mit
            x = 70 + i * (seg + 12)
            d.rounded_rectangle([x, 90, x + seg, 100], 5, fill=DIM)
            p = 1.0 if i < idx else (min(t / max(dur - XF, 0.1), 1.0) if i == idx else 0.0)
            if p > 0: d.rounded_rectangle([x, 90, x + max(seg * p, 10), 100], 5, fill=accent())
        for e in els:
            a = 1.0 if hook else ease((t - e["t"]) / 0.35)   # Hook: ab Frame 1 lesbar
            if a <= 0: continue
            if e["kind"] == "big":
                k = int((t - e["t"]) * FPS)
                txt = cu[k] if cu and k < len(cu) else e["text"]
                im = big_sprite(e, txt, cache)
                sc = 1.0 + 0.18 * (1 - ease((t - e["t"]) / 0.25))      # kurzer „Pop“
                if sc > 1.001:
                    im = im.resize((int(im.width * sc), int(im.height * sc)), Image.BILINEAR)
                x, y = e["x"], e["y"] - int((im.height - e["font"].size * 1.3) / 2)
            else:
                im, x, y = e["img"], e["x"], e["y"]
                off = int(70 * (1 - a))
                if e["fx"] == "left": x -= off
                elif e["fx"] == "right": x += off
                elif e["fx"] == "up": y += off
            if a < 1:
                im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
            fr.alpha_composite(im, (int(x), int(y)))
        fr = fr.convert("RGB")
        if hook:
            z = 1.08 - 0.08 * ease(t / 0.5) if t < 0.5 else 1.0 + 0.012 * (t - 0.5)
        else:
            z = 1.0 + 0.018 * t
        if z != 1.0:
            cw, ch = int(W / z), int(H / z)
            x0, y0 = (W - cw) // 2, int((H - ch) * 0.35)
            fr = fr.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)
        proc.stdin.write(fr.tobytes())
    proc.stdin.close(); proc.wait()
    if proc.returncode: raise SystemExit(f"Clip {idx} fehlgeschlagen")
    return pops

def make_sfx(tmp, total_len):
    """Dezente Soundeffekte, synthetisch erzeugt (keine Lizenzfragen)."""
    fx = {
        "whoosh": "anoisesrc=color=pink:d=0.45:a=0.5,highpass=f=400,lowpass=f=5000,afade=t=in:d=0.25,afade=t=out:st=0.25:d=0.2,volume=0.22",
        "pop":    "sine=f=880:d=0.09,afade=t=out:st=0.01:d=0.08,volume=0.10",
        "impact": "sine=f=55:d=0.6,afade=t=out:st=0.02:d=0.58,volume=0.9",
    }
    out = {}
    for k, f in fx.items():
        p = os.path.join(tmp, f"sfx_{k}.wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f, p], check=True); out[k] = p
    # leiser Puls als Spannungsbett (unter der Stimme kaum hörbar, füllt aber Pausen)
    p = os.path.join(tmp, "sfx_bed.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
        f"aevalsrc='0.5*sin(2*PI*1600*t)*exp(-90*mod(t,0.5))+0.35*sin(2*PI*65*t)*exp(-6*mod(t,1))':d={total_len:.2f}",
        "-af", "volume=0.07,afade=t=out:st=" + f"{max(total_len-1.5,0):.2f}" + ":d=1.5", p], check=True)
    out["bed"] = p
    return out

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
    global SERIES
    SERIES = data.get("series")
    apply_theme(data.get("theme") or {"SONNTAG ERKLÄRT": "erklaert", "WOCHENAUSBLICK": "ausblick", "WOCHENRÜCKBLICK": "ausblick"}.get(SERIES))
    tmp = tempfile.mkdtemp(prefix="geo_")
    try:
        voices = make_voice(slides, data, tmp)
        durs = []
        for i, s in enumerate(slides):
            dur = float(s.get("sec", 6))
            if voices and voices[i]: dur = probe(voices[i]) + (0.1 if i == 0 else 0.35) + XF
            durs.append(dur)
        clips, pops = [], []
        for i, (sl, dur) in enumerate(zip(slides, durs)):
            c = os.path.join(tmp, f"clip_{i:02d}.mp4")
            print(f"Folie {i+1}/{len(slides)} animieren …")
            pops.append(anim_clip(sl, i, len(slides), data["date"], dur, c)); clips.append(c)
        # Video mit Überblendungen
        inputs, filt, last, off, starts = [], "", "0:v", 0.0, [0.0]
        for c in clips: inputs += ["-i", c]
        for i in range(1, len(clips)):
            off += durs[i - 1] - XF; starts.append(off)
            filt += f"[{last}][{i}:v]xfade=transition=slideleft:duration={XF}:offset={off:.2f}[v{i}];"; last = f"v{i}"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", *inputs]
        amap = []
        n = len(clips); k = 0; labels = []
        total_len = sum(durs) - XF * (n - 1)
        if voices and any(voices):
            for i, v in enumerate(voices):
                if not v: continue
                cmd += ["-i", v]
                ms = 0 if i == 0 else int((starts[i] + 0.25) * 1000)   # Hook: Stimme ab Frame 1
                filt += f"[{n+k}:a]adelay={ms}|{ms}[a{k}];"; labels.append(f"[a{k}]"); k += 1
        if data.get("sfx", True):
            sfx = make_sfx(tmp, total_len)
            events = [("impact", 0.62)] if slides[0].get("big") else []
            events += [("whoosh", max(st - 0.2, 0)) for st in starts[1:]]
            events += [("pop", starts[i] + t) for i, ts in enumerate(pops) for t in ts]
            events += [("bed", 0.0)]
            for name, t0 in events:
                cmd += ["-i", sfx[name]]
                ms = int(t0 * 1000)
                filt += f"[{n+k}:a]adelay={ms}|{ms}[a{k}];"; labels.append(f"[a{k}]"); k += 1
        if k:
            filt += f"{''.join(labels)}amix=inputs={k}:normalize=0:duration=longest,atrim=0:{total_len:.2f}[aout];"
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
