"""
Geopolitical_ – TEST-Renderer „Satellitenkarte“ (neuer Stil, Stand 24.10.2026)

Aufruf:   python make_video_karte.py <Video-Ordner>
          liest slides_karte.json (gleiches Format wie slides.json) und schreibt <outfile>.

Unterschiede zum Standard-Renderer (make_video.py, bleibt unverändert):
- Hintergrund = NASA Blue Marble (Satellit, gemeinfrei) statt Vektorkarte
- Kamera fliegt: Hook startet auf texturiertem 3D-Globus, danach Flüge zwischen Schauplätzen,
  langsames Hineinzoomen während jeder Folie
- Länder knallig eingefärbt, Name in Handschrift (Kalam, OFL) auf dem Land
- Markierungen pro Folie (optional, "marks"):
    {"type": "point", "at": [lon, lat], "text": "Abuja"}
    {"type": "line", "from": [lon, lat], "to": [lon, lat], "text": "29 km"}
    {"type": "route", "pts": [[lon, lat], ...], "text": "40 %"}
    {"type": "ring", "at": [lon, lat]}
- Optional pro Folie: "label": {"text": "Jemen", "at": [lon, lat], "rot": -12}  (sonst automatisch)
                      "cam": [lon, lat, breite_in_grad]                       (sonst automatisch)
"""
import json, math, os, shutil, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_video as mv

W, H, FPS = mv.W, mv.H, mv.FPS
TEX_PATH = os.path.join(HERE, "assets", "bluemarble_5400.jpg")
HAND = os.path.join(HERE, "fonts", "Kalam-Bold.ttf")

# ---------------------------------------------------------------- Textur
_TEX = None
def tex():
    """Farbkorrigierte Satellitentextur, horizontal doppelt (für Datumsgrenze)."""
    global _TEX
    if _TEX is None:
        im = Image.open(TEX_PATH).convert("RGB")
        a = np.asarray(im).astype(np.float32)
        a = (a - 128) * 1.12 + 128                     # Kontrast
        g = a.mean(axis=2, keepdims=True)
        a = g + (a - g) * 1.25                         # Sättigung
        a = a * 0.78                                   # etwas dunkler (Text bleibt lesbar)
        a = np.clip(a, 0, 255).astype(np.uint8)
        wide = np.concatenate([a, a, a], axis=1)       # 3x horizontal (Datumsgrenze)
        pad = np.zeros((PADY, wide.shape[1], 3), np.uint8); pad[:] = (5, 10, 20)
        _TEX = (Image.fromarray(np.concatenate([pad, wide, pad], axis=0)), a)
    return _TEX

TPD = 15.0   # Texturpixel pro Grad (5400 / 360)
PADY = 1350  # dunkler Rand oben/unten (90°), damit Zoom-Out nie aus der Textur läuft

def flat_bg(clon, clat, span):
    """Equirektangulärer Ausschnitt: Breite = span Grad Länge, kx-korrigiert."""
    timg, _ = tex()
    kx = math.cos(math.radians(max(min(clat, 70), -70)))
    s = W / (span * kx)                               # px pro Breitengrad
    latr = H / s
    x0 = (clon - span / 2 + 180) % 360 * TPD + 5400
    y0 = (90 - (clat + latr / 2)) * TPD + PADY
    if span > 300: span = 300
    y0 = max(0, y0)
    box = (x0, y0, x0 + span * TPD, y0 + latr * TPD)
    im = timg.resize((W, H), Image.BICUBIC, box=box)
    if span < 45:   # bei starkem Zoom nachschärfen (Textur hat 15 px/Grad)
        im = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=int(70 + (45 - span) * 2), threshold=2))
    return im, s, kx

def globe_bg(lon0, lat0, R, cx, cy):
    """Texturierter Globus (orthografisch), Hintergrund dunkel."""
    _, a = tex()
    out = np.zeros((H, W, 3), np.uint8); out[:] = (6, 10, 20)
    x0, x1 = max(0, int(cx - R)), min(W, int(cx + R) + 1)
    y0, y1 = max(0, int(cy - R)), min(H, int(cy + R) + 1)
    if x1 > x0 and y1 > y0:
        xs = (np.arange(x0, x1) - cx) / R
        ys = (cy - np.arange(y0, y1)) / R
        X, Y = np.meshgrid(xs, ys)
        rho = np.sqrt(X * X + Y * Y)
        m = rho <= 1
        c = np.arcsin(np.clip(rho, 0, 1))
        p0, l0 = math.radians(lat0), math.radians(lon0)
        with np.errstate(invalid="ignore", divide="ignore"):
            lat = np.arcsin(np.cos(c) * math.sin(p0) + np.where(rho > 0, Y * np.sin(c) * math.cos(p0) / rho, 0))
            lon = l0 + np.arctan2(X * np.sin(c), rho * math.cos(p0) * np.cos(c) - Y * math.sin(p0) * np.sin(c))
        ty = np.clip(((math.pi / 2 - lat) / math.pi * a.shape[0]).astype(int), 0, a.shape[0] - 1)
        tx = (((lon + math.pi) % (2 * math.pi)) / (2 * math.pi) * a.shape[1]).astype(int) % a.shape[1]
        shade = np.clip(np.cos(c) * 0.55 + 0.45, 0, 1)[..., None]     # Kugel-Schattierung
        px = (a[ty, tx] * shade).astype(np.uint8)
        reg = out[y0:y1, x0:x1]
        reg[m] = px[m]
    im = Image.fromarray(out)
    d = ImageDraw.Draw(im, "RGBA")
    for k, al in ((30, 25), (18, 45), (8, 80)):
        d.ellipse([cx - R - k, cy - R - k, cx + R + k, cy + R + k], outline=(120, 180, 255, al), width=6)
    return im

def globe_proj(lon0, lat0, R, cx, cy):
    p0, l0 = math.radians(lat0), math.radians(lon0)
    sp0, cp0 = math.sin(p0), math.cos(p0)
    def P(lon, lat):
        p, l = math.radians(lat), math.radians(lon) - l0
        cosc = sp0 * math.sin(p) + cp0 * math.cos(p) * math.cos(l)
        x = math.cos(p) * math.sin(l); y = cp0 * math.sin(p) - sp0 * math.cos(p) * math.cos(l)
        if cosc < 0:
            n = math.hypot(x, y) or 1; x, y = x / n, y / n
        return cx + R * x, cy - R * y, cosc >= 0
    return P

# ---------------------------------------------------------------- Länder
def countries_by_code():
    return {c["a3"]: c for c in mv.world()}

def core_poly(c):
    def area(poly):
        xs = [x for x, _ in poly[0]]; ys = [y for _, y in poly[0]]
        return (max(xs) - min(xs)) * (max(ys) - min(ys))
    return max(c["p"], key=area)

def bbox_pts(pts):
    xs = [x for x, _ in pts]; ys = [y for _, y in pts]
    return min(xs), min(ys), max(xs), max(ys)

def centroid(pts):
    a = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        f = x0 * y1 - x1 * y0; a += f; cx += (x0 + x1) * f; cy += (y0 + y1) * f
    if abs(a) < 1e-9:
        b = bbox_pts(pts); return (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    return cx / (3 * a), cy / (3 * a)

NAMES_DE = {"COD": "Kongo", "USA": "USA", "GBR": "Großbritannien", "ARE": "VAE", "PSX": "Gaza"}

def slide_geo(s):
    """Hauptland, Kamera-Ziel (lon, lat, span), Labels."""
    cb = countries_by_code()
    codes = [c for c in mv.map_codes(s) if c in cb]
    cam = s.get("cam")
    labels = []
    if codes:
        main = cb[codes[0]]; core = core_poly(main)[0]
        bx = bbox_pts(core)
        if bx[2] - bx[0] > 300: bx = (20, bx[1], 180, bx[3])
        if not cam:
            # alle markierten Länder (Kernflächen) sollen ins Bild
            allb = [bbox_pts(core_poly(cb[c])[0]) for c in codes]
            lo1 = min(b[0] for b in allb); la1 = min(b[1] for b in allb)
            lo2 = max(b[2] for b in allb); la2 = max(b[3] for b in allb)
            if lo2 - lo1 > 45 or la2 - la1 > 40: lo1, la1, lo2, la2 = bx   # zu weit verstreut: aufs Hauptland
            clat = (la1 + la2) / 2; kx = math.cos(math.radians(max(min(clat, 70), -70)))
            span = min(max((lo2 - lo1) * 1.3, (la2 - la1) * 1.3 / kx * W / (H * 0.40), 8), 60)
            cam = [(lo1 + lo2) / 2, clat, span]
        for i, code in enumerate(codes[:4]):
            c = cb[code]; cp = core_poly(c)[0]
            lx, ly = centroid(cp)
            labels.append(dict(text=NAMES_DE.get(code) or c.get("de") or c.get("name"), at=(lx, ly),
                               rot=-8 if i % 2 == 0 else 6, main=(i == 0)))
    if s.get("label"):
        L = s["label"]; labels = [dict(text=L["text"], at=tuple(L["at"]), rot=L.get("rot", -8), main=True)] + labels[1:]
    if not cam:
        cam = [10.5, 50.5, 24]       # Deutschland/Mitteleuropa (Folien ohne Land)
    return codes, cam, labels

# ---------------------------------------------------------------- Zeichnen
def hand(size): return ImageFont.truetype(HAND, size)

def label_sprite(text, size, rot):
    f = hand(size)
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    tw = int(d0.textlength(text, font=f)) + 40; th = int(size * 1.5)
    im = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for dx, dy in ((3, 4), (2, 3)):
        d.text((20 + dx, 4 + dy), text, font=f, fill=(0, 0, 0, 170))
    d.text((20, 4), text, font=f, fill=(255, 255, 255, 255))
    return im.rotate(rot, resample=Image.BICUBIC, expand=True)

def draw_overlay(P, codes, t, slide_t0, labels, label_cache, marks, scale_px_per_deg, visible_test):
    """Länderflächen, Grenzen, Labels, Markierungen. P(lon,lat) -> (x, y, sichtbar)."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    cb = countries_by_code()
    HL = mv.HL
    # Grenzen aller Länder (dünn)
    for c in mv.world():
        for poly in c["p"]:
            pts = [P(x, y) for x, y in poly[0]]
            if len(pts) < 3 or not any(v for *_, v in pts): continue
            xy = [(x, y) for x, y, _ in pts]
            if not visible_test(xy): continue
            if max(x for x, _ in xy) - min(x for x, _ in xy) > W * 1.6: continue   # Datumsgrenze
            d.line(xy + xy[:1], fill=(255, 255, 255, 70), width=2)
    # Markierte Länder: Füllung blendet ein, Hauptland pulsiert
    a_in = mv.ease((t - 0.15) / 0.5)
    pulse = 0.85 + 0.15 * math.sin(2 * math.pi * t / 1.4)
    glow = Image.new("L", (W // 4, H // 4), 0); dg = ImageDraw.Draw(glow)
    for i, code in enumerate(codes):
        c = cb[code]
        for poly in c["p"]:
            pts = [P(x, y) for x, y in poly[0]]
            if len(pts) < 3 or not any(v for *_, v in pts): continue
            xy = [(x, y) for x, y, _ in pts]
            al = int((205 if i == 0 else 150) * a_in * (pulse if i == 0 else 1))
            d.polygon(xy, fill=HL + (al,))
            d.line(xy + xy[:1], fill=(255, 255, 255, int(230 * a_in)), width=4 if i == 0 else 3)
            if i == 0: dg.polygon([(x / 4, y / 4) for x, y in xy], fill=255)
    if codes and a_in > 0:
        g = glow.filter(ImageFilter.GaussianBlur(10)).resize((W, H), Image.BILINEAR)
        gl = Image.new("RGBA", (W, H), HL + (0,)); gl.putalpha(g.point(lambda v: int(v * 0.55 * a_in)))
        ov = Image.alpha_composite(gl, ov); d = ImageDraw.Draw(ov)
    # Markierungen
    for k, mk in enumerate(marks or []):
        t0 = mk.get("t", 0.9 + 0.6 * k)
        a = mv.ease((t - t0) / 0.4)
        if a <= 0: continue
        typ = mk.get("type", "point")
        col = (255, 220, 90)
        if typ in ("point", "ring"):
            x, y, v = P(*mk["at"])
            if not v or y < H * 0.5: continue
            ph = (t - t0) % 1.3 / 1.3
            for rr, aa in ((18 + 50 * ph, int(200 * (1 - ph))), (14, 255)):
                d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=col + (int(aa * a),), width=5)
            if typ == "point":
                d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(255, 255, 255, int(255 * a)))
            if mk.get("text"):
                key = ("m", mk["text"])
                if key not in label_cache: label_cache[key] = label_sprite(mk["text"], 70, 0)
                sp = label_cache[key]
                ov.alpha_composite(fade(sp, a), (int(x + 26), int(y - sp.height + 10)))
        elif typ in ("line", "route"):
            pts = [mk["from"], mk["to"]] if typ == "line" else mk["pts"]
            xy = [P(*p)[:2] for p in pts]
            # schrittweise zeichnen
            seg_len = [math.dist(a_, b_) for a_, b_ in zip(xy, xy[1:])]; total = sum(seg_len) or 1
            draw_to = total * mv.ease((t - t0) / 0.9); acc = 0; drawn = [xy[0]]
            for (p0, p1), L in zip(zip(xy, xy[1:]), seg_len):
                if acc + L <= draw_to: drawn.append(p1); acc += L
                else:
                    f = (draw_to - acc) / L if L else 0
                    drawn.append((p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)); break
            if len(drawn) > 1:
                d.line(drawn, fill=(0, 0, 0, 120), width=12, joint="curve")
                d.line(drawn, fill=col + (255,), width=7, joint="curve")
            for p in (xy[0], xy[-1]) if typ == "line" else (xy[0],):
                d.ellipse([p[0] - 10, p[1] - 10, p[0] + 10, p[1] + 10], fill=(255, 255, 255, int(255 * a)))
            if mk.get("text") and draw_to >= total * 0.6:
                key = ("m", mk["text"])
                if key not in label_cache: label_cache[key] = label_sprite(mk["text"], 84, -10)
                sp = label_cache[key]; mx = sum(p[0] for p in xy) / len(xy); my = sum(p[1] for p in xy) / len(xy)
                ov.alpha_composite(fade(sp, a), (int(mx - sp.width / 2), int(my - sp.height - 20)))
    # Ländernamen in Handschrift (weichen Markierungen aus)
    mpos = [P(*mk["at"])[:2] for mk in (marks or []) if "at" in mk]
    for i, L in enumerate(labels):
        a = mv.ease((t - 0.35 - 0.25 * i) / 0.45)
        if a <= 0: continue
        x, y, v = P(*L["at"])
        if not v: continue
        key = ("l", L["text"], L["main"])
        if key not in label_cache: label_cache[key] = label_sprite(L["text"], 108 if L["main"] else 78, L["rot"])
        sp = label_cache[key]
        for mx_, my_ in mpos:
            if abs(mx_ - x) < sp.width * 0.6 and abs(my_ - y) < 120:
                y = my_ + 95 if my_ + 95 < H - 400 else my_ - 110
        px_, py_ = int(x - sp.width / 2), int(y - sp.height / 2)
        if 0 < x < W and H * 0.53 < y < H - 120:
            ov.alpha_composite(fade(sp, a), (px_, py_))
    return ov

def fade(im, a):
    if a >= 1: return im
    im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a))); return im

_GRAD = None
def text_gradient():
    """Dunkler Verlauf oben (Text) und unten (Quellen) über der Karte."""
    global _GRAD
    if _GRAD is None:
        g = np.zeros((H, 1), np.float32)
        y = np.arange(H)[:, None] / H
        top = np.clip(1 - y / 0.54, 0, 1) ** 0.8 * 235
        bot = np.clip((y - 0.80) / 0.20, 0, 1) ** 1.5 * 200
        g = np.maximum(top, bot)
        A = Image.fromarray(np.repeat(g, W, axis=1).astype(np.uint8), "L")
        _GRAD = Image.new("RGBA", (W, H), (4, 8, 16, 0)); _GRAD.putalpha(A)
    return _GRAD

def header(d, date):
    f = mv.font(44, black=True)
    d.text((70, 140), "GEOPOLITICAL", font=f, fill=(244, 246, 250))
    tw = d.textlength("GEOPOLITICAL", font=f)
    d.rectangle([70 + tw + 6, 180, 70 + tw + 40, 188], fill=mv.ACCENT)
    d.text((70, 200), date, font=mv.font(32, False), fill=(190, 198, 214))
    if mv.SERIES: mv.series_badge(d, 70 + tw + 70, 143)

# ---------------------------------------------------------------- Kamera
LAST_CAM = [None]

def cam_path(target, prev, dur, hook):
    """Liefert cam(t) -> ('globe', lon, lat, R) oder ('flat', lon, lat, span)."""
    lon1, lat1, span1 = target
    span_start = span1 * 1.35
    if hook:
        G = 1.7
        lon0, lat0 = lon1 - 100, 18
        R0 = 470
        def cam(t):
            if t < G:
                r = mv.ease(t / 1.0); z = mv.ease((t - 0.85) / 0.85)
                lon = lon0 + (((lon1 - lon0 + 180) % 360) - 180) * r; lat = lat0 + (lat1 - lat0) * r
                kx = math.cos(math.radians(lat1)); s_start = W / (span_start * kx)
                R1 = s_start * 180 / math.pi
                return ("globe", lon, lat, R0 * (R1 / R0) ** z, max(0.0, (t - (G - 0.25)) / 0.25))
            tt = (t - G) / max(dur - G, 0.1)
            return ("flat", lon1, lat1, span_start + (span1 - span_start) * mv.ease(tt), 1.0)
        return cam
    if prev is None:
        prev = (lon1, lat1, span_start)
    plon, plat, pspan = prev
    dist = math.hypot((((lon1 - plon + 180) % 360) - 180) * math.cos(math.radians((lat1 + plat) / 2)), lat1 - plat)
    fly = dist > 2 or abs(math.log(span1 / pspan)) > 0.3
    F = 1.3 if fly else 0.0
    peak = min(max(pspan, span_start, dist * 1.6), 75)
    def cam(t):
        if t < F:
            u = mv.ease(t / F)
            dl = ((lon1 - plon + 180) % 360) - 180
            lon = plon + dl * u; lat = plat + (lat1 - plat) * u
            # Zoom raus und wieder rein (Parabel im Log-Raum)
            ls = math.log(pspan) * (1 - u) + math.log(span_start) * u
            ls += (math.log(peak) - max(math.log(pspan), math.log(span_start))) * 4 * u * (1 - u)
            return ("flat", lon, lat, math.exp(ls), 1.0)
        tt = (t - F) / max(dur - F, 0.1)
        return ("flat", lon1, lat1, span_start + (span1 - span_start) * mv.ease(tt), 1.0)
    return cam

# ---------------------------------------------------------------- Clip
def anim_clip(s, idx, total, date, dur, path):
    import subprocess
    hook = idx == 0
    _bg, els, _hl = mv.layout(s, idx, total, date)          # Text-Elemente wie gehabt
    pops = mv.schedule(els, dur, hook)
    st, sty = s.get("stack"), getattr(mv.layout, "stack_y", None)
    if st:
        sts, sth = mv.stack_times(st, dur)
        pops = pops + sts + ([sth] if sth is not None and sth < dur - mv.XF else [])
    codes, target, labels = slide_geo(s)
    cam = cam_path(target, LAST_CAM[0], dur, hook)
    end = cam(dur); LAST_CAM[0] = (end[1], end[2], end[3]) if end[0] == "flat" else tuple(target)
    marks = s.get("marks", [])
    lcache, bcache = {}, {}
    cu = mv.countup_values(s["big"], int(0.7 * FPS)) if s.get("big") else None
    seg = (W - 140 - (total - 1) * 12) / total
    grad = text_gradient()
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for f in range(int(dur * FPS)):
        t = f / FPS
        mode, lon, lat, z, blend = cam(t)
        if mode == "globe":
            R = z; cx, cy = W * 0.5, H * 0.70
            bg = globe_bg(lon, lat, R, cx, cy)
            P = globe_proj(lon, lat, R, cx, cy)
            ov = draw_overlay(P, codes, t, 0, [], lcache, [], None, lambda xy: True)
            fr = bg.convert("RGBA"); fr.alpha_composite(ov)
            if blend > 0:
                # Überblendung in die flache Karte am Ende der Globus-Phase
                kx = math.cos(math.radians(max(min(target[1], 70), -70)))
                span_s = target[2] * 1.35
                fb, s_, kx_ = flat_bg(target[0], target[1] + (H * 0.20) / (W / (span_s * kx)), span_s)
                fr = Image.blend(fr, fb.convert("RGBA"), blend)
        else:
            span = z
            kx = math.cos(math.radians(max(min(lat, 70), -70)))
            sc = W / (span * kx)
            # Kamera-Mitte so verschieben, dass das Ziel bei 70 % Höhe liegt
            clat = lat + (H * 0.20) / sc
            fb, sc, kx = flat_bg(lon, clat, span)
            def P(x, y, lon=lon, clat=clat, sc=sc, kx=kx):
                dx = ((x - lon + 180) % 360) - 180
                return W / 2 + dx * kx * sc, H / 2 - (y - clat) * sc, True
            def vis(xy):
                xs = [p[0] for p in xy]; ys = [p[1] for p in xy]
                return not (max(xs) < -50 or min(xs) > W + 50 or max(ys) < -50 or min(ys) > H + 50)
            ov = draw_overlay(P, codes, t, 0, labels, lcache, marks, sc, vis)
            fr = fb.convert("RGBA"); fr.alpha_composite(ov)
        fr.alpha_composite(grad)
        if st:   # Preis-Zerlegung braucht ruhigen, dunklen Hintergrund
            fr.alpha_composite(Image.new("RGBA", (W, H), (4, 8, 16, 165)))
        d = ImageDraw.Draw(fr)
        header(d, date) if not hook else (mv.series_badge(d, 70, 140) if mv.SERIES else None)
        for i in range(total):
            x = 70 + i * (seg + 12)
            d.rounded_rectangle([x, 90, x + seg, 100], 5, fill=(255, 255, 255, 60))
            p = 1.0 if i < idx else (min(t / max(dur - mv.XF, 0.1), 1.0) if i == idx else 0.0)
            if p > 0: d.rounded_rectangle([x, 90, x + max(seg * p, 10), 100], 5, fill=mv.ACCENT)
        if not hook:
            d.text((70, H - 300), "KI-Stimme · Keine Anlageberatung · Quellen in der Beschreibung",
                   font=mv.font(26, False), fill=(200, 205, 215))
            if s.get("source"):
                d.text((70, H - 345), "Quelle: " + s["source"], font=mv.font(26, False), fill=(200, 205, 215))
        for e in els:
            a = 1.0 if hook else mv.ease((t - e["t"]) / 0.35)
            if a <= 0: continue
            if e["kind"] == "big":
                k = int((t - e["t"]) * FPS)
                txt = cu[k] if cu and k < len(cu) else e["text"]
                im = mv.big_sprite(e, txt, bcache)
                sc_ = 1.0 + 0.18 * (1 - mv.ease((t - e["t"]) / 0.25))
                if sc_ > 1.001: im = im.resize((int(im.width * sc_), int(im.height * sc_)), Image.BILINEAR)
                x, y = e["x"], e["y"] - int((im.height - e["font"].size * 1.3) / 2)
            else:
                im, x, y = e["img"], e["x"], e["y"]
                off = int(70 * (1 - a))
                if e["fx"] == "left": x -= off
                elif e["fx"] == "right": x += off
                elif e["fx"] == "up": y += off
            fr.alpha_composite(fade(im, a), (int(x), int(y)))
        if st: mv.draw_stack(fr, st, sty, t, sts, sth)
        proc.stdin.write(fr.convert("RGB").tobytes())
    proc.stdin.close(); proc.wait()
    if proc.returncode: raise SystemExit(f"Clip {idx} fehlgeschlagen")
    return pops

def smaller_text():
    """Text kompakter als im Standard-Renderer, damit die Karte mehr Platz bekommt."""
    orig = mv.font
    if getattr(orig, "_karte", False): return
    def f(size, bold=True, black=False):
        size = {96: 84, 80: 68, 48: 41}.get(size, size)
        return orig(size, bold, black)
    f._karte = True
    mv.font = f

def main():
    folder = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    src = os.path.join(folder, "slides_karte.json")
    if not os.path.exists(src): src = os.path.join(folder, "slides.json")
    tmp = tempfile.mkdtemp(prefix="geok_")
    try:
        shutil.copy(src, os.path.join(tmp, "slides.json"))
        data = json.load(open(src, encoding="utf-8"))
        smaller_text()
        orig_theme = mv.apply_theme
        def theme_light(name):
            orig_theme(name)
            mv.WHITE, mv.GREY = (244, 246, 250), (190, 198, 214)
            mv.COLORS["WHITE"] = mv.WHITE
            if mv.THEME == "erklaert":
                mv.GREEN, mv.RED = (70, 200, 120), (232, 72, 72); mv.COLORS.update({"GREEN": mv.GREEN, "RED": mv.RED})
        mv.apply_theme = theme_light
        mv.anim_clip = anim_clip                # Standard-Ablauf (Stimme, Schnitt, Ton) wiederverwenden
        sys.argv = [sys.argv[0], tmp]
        mv.main()
        # Themes setzen Textfarben – für die Satellitenkarte immer heller Text
        shutil.move(os.path.join(tmp, data["outfile"]), os.path.join(folder, data["outfile"]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
