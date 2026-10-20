"""Einmalig: Ländergrenzen (Natural Earth 1:50 Mio., gemeinfrei) laden, vereinfachen, kompakt speichern."""
import json, urllib.request
from shapely.geometry import shape, mapping
URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson"
d = json.load(urllib.request.urlopen(URL))
out = []
for f in d["features"]:
    p = f["properties"]
    g = shape(f["geometry"]).simplify(0.04, preserve_topology=True)
    m = mapping(g)
    def r(c): return [[round(x, 2), round(y, 2)] for x, y in c]
    polys = [m["coordinates"]] if m["type"] == "Polygon" else list(m["coordinates"])
    out.append({"a3": p.get("ADM0_A3"), "de": p.get("NAME_DE"), "name": p.get("NAME"),
                "p": [[r(ring) for ring in poly] for poly in polys]})
json.dump(out, open("pipeline/assets/welt.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(len(out), "Länder")
