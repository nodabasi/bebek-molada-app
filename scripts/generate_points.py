#!/usr/bin/env python3
"""Generate one static page per seed spot (nokta/<id>/), the spot index,
sitemap.xml and robots.txt. Run from the repo root: python3 scripts/generate_points.py

Pages answer searches such as "<place> bebek bakım odası". Only facts present in
data/seed-*.json are used; nothing is invented.
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://nodabasi.github.io/bebek-molada-app"
APP_STORE = "https://apps.apple.com/app/id6807793408"

TAGS = {
    "bebek_bakim_odasi": "Bebek bakım odası",
    "emzirme_alani": "Emzirme alanı",
    "mama_isitma": "Mama ısıtma",
    "puset": "Puset",
    "oyun_alani": "Oyun alanı",
    "aile_tuvaleti": "Aile tuvaleti",
}
PLACE_TYPES = {
    "avm": "AVM",
    "kamu": "Kamu binası",
    "havalimani": "Havalimanı",
    "magaza": "Mağaza",
    "park": "Park",
}


def load():
    spots = []
    for name in ("seed-anadolu-yakasi.json", "seed-avrupa-yakasi.json"):
        spots += json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))
    return sorted(spots, key=lambda s: (s["district"], s["name"]))


def head(title, desc, canonical, depth):
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="{up}assets/logo.png">
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<div class="wrap">
"""


def foot(depth):
    up = "../" * depth
    return f"""
<hr>
<footer>
  <a href="{up}nokta/">Tüm noktalar</a>
  <a href="{up}support/">Destek</a>
  <a href="{up}privacy/">Gizlilik Politikası</a>
  <a href="{up}">Ana sayfa</a>
  <div class="copyright">© 2026 Mehmet Nusret Odabaşı</div>
</footer>

</div>
</body>
</html>
"""


def spot_page(s):
    tags = [TAGS[t] for t in s["tags"]]
    has_room = "bebek_bakim_odasi" in s["tags"]
    kind = "bebek bakım odası" if has_room else "bebek imkânları"
    title = f"{s['name']} {kind} ({s['district']}) | Bebek Molada"
    desc = (
        f"{s['name']}, {s['district']}: " + ", ".join(t.lower() for t in tags)
        + ". Konum, kat bilgisi ve yol tarifi Bebek Molada'da."
    )
    url = f"{SITE}/nokta/{s['id']}/"
    maps = f"https://www.google.com/maps/search/?api=1&query={s['lat']},{s['lng']}"
    chips = "\n".join(f"  <li>{escape(t)}</li>" for t in tags)
    check = ""
    if s.get("needsOnSiteCheck"):
        check = (
            "\n<p><i>Bu noktanın bilgileri yerinde teyit edilmedi. Gittiysen uygulamadan "
            "onaylayıp not bırakırsan diğer ebeveynlere yardım olur.</i></p>"
        )
    return (
        head(title, desc, url, 2)
        + f"""
<header>
  <img src="../../assets/logo.png" alt="Bebek Molada">
  <h1>{escape(s['name'])}</h1>
  <p class="tagline">{escape(s['district'])}, {escape(s['city'])} · {PLACE_TYPES.get(s['placeType'], '')}</p>
</header>

<h2>Burada neler var</h2>
<ul class="chips">
{chips}
</ul>

<h2>Nerede</h2>
<p>{escape(s['address'])}</p>
<p>{escape(s['locationNote'])}</p>
<p><a href="{escape(maps)}">Yol tarifi için haritada aç</a></p>{check}

<h2>Yakınında başka nokta var mı?</h2>
<p>Bebek Molada, İstanbul'daki bebek bakım odası, emzirme alanı ve mama ısıtma
noktalarını tek haritada gösterir. Çevrendeki en yakın noktayı görmek ve eksik
bir yeri eklemek için uygulamayı indir.</p>
<p><a href="{APP_STORE}">App Store'da Bebek Molada</a></p>
"""
        + foot(2)
    )


def index_page(spots):
    by_district = {}
    for s in spots:
        by_district.setdefault(s["district"], []).append(s)
    sections = []
    for d in sorted(by_district):
        items = "\n".join(
            f'  <li><a href="{s["id"]}/">{escape(s["name"])}</a></li>' for s in by_district[d]
        )
        sections.append(f"<h2>{escape(d)}</h2>\n<ul class=\"plain\">\n{items}\n</ul>")
    return (
        head(
            "İstanbul bebek bakım odaları ve emzirme alanları | Bebek Molada",
            "İstanbul'da bebek bakım odası, emzirme alanı ve mama ısıtma imkânı olan AVM ve mekânların ilçe ilçe listesi.",
            f"{SITE}/nokta/",
            1,
        )
        + """
<header>
  <img src="../assets/logo.png" alt="Bebek Molada">
  <h1>İstanbul'da bebek molası noktaları</h1>
  <p class="tagline">İlçeye göre bebek bakım odası ve emzirme alanları</p>
</header>

"""
        + "\n\n".join(sections)
        + foot(1)
    )


def main():
    spots = load()
    for s in spots:
        out = ROOT / "nokta" / s["id"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(spot_page(s), encoding="utf-8")
    (ROOT / "nokta" / "index.html").write_text(index_page(spots), encoding="utf-8")
    urls = [f"{SITE}/", f"{SITE}/en/", f"{SITE}/nokta/"] + [f"{SITE}/nokta/{s['id']}/" for s in spots]
    body = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n',
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"{len(spots)} spot pages generated")


if __name__ == "__main__":
    main()
