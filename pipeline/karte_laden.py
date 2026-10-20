"""Einmalig: Ländergrenzen (Natural Earth 1:50 Mio., gemeinfrei) laden, vereinfachen, kompakt speichern."""
import json, urllib.request, traceback
log = open("pipeline/assets/karte_log.txt", "w")
try:
    from shapely.geometry import shape, mapping
    URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson"
    req = urllib.request.Request(URL, headers={"User-Agent": "geopolitical-bot"})
    d = json.load(urllib.request.urlopen(req, timeout=120))
    def r(c): return [[round(x, 2), round(y, 2)] for x, y in c]
    out = []
    for f in d["features"]:
        p = f["properties"]
        try:
            g = shape(f["geometry"]).simplify(0.04, preserve_topology=True)
            geoms = [g] if g.geom_type == "Polygon" else list(getattr(g, "geoms", []))
            polys = [[r(x.exterior.coords)] for x in geoms if x.geom_type == "Polygon" and not x.is_empty]
            if polys:
                out.append({"a3": p.get("ADM0_A3"), "de": p.get("NAME_DE"), "name": p.get("NAME"), "p": polys})
        except Exception as e:
            log.write(f"skip {p.get('NAME')}: {e}\n")
    json.dump(out, open("pipeline/assets/welt.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    log.write(f"{len(out)} Länder\n")
except Exception:
    log.write(traceback.format_exc())
log.close()
