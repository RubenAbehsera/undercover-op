"""Extrait les fiches personnages du One Piece Wiki (onepiece.fandom.com).

Usage:
    python wiki_extract.py            # extrait toutes les pages de seeds/pages.txt
    python wiki_extract.py "Nami" ... # extrait les pages données

Sortie: seeds/personnages.brut.yml (régénéré intégralement à chaque passage).
Cache: cache/<slug>.html — relire le wiki uniquement si absent.

Les valeurs sont brutes, issues de l'infobox rendue (repli: {{Char Box}}
en wikitext). La relecture humaine est obligatoire avant usage.
"""

import html
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://onepiece.fandom.com/api.php"
ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache"
PAGES = ROOT / "seeds" / "pages.txt"
OUT = ROOT / "seeds" / "personnages.brut.yml"
PAUSE = 0.4  # politesse entre requêtes

SECTION_RE = re.compile(
    r'<div class="pi-item pi-data[^"]*"\s+data-source="([^"]+)"[^>]*>.*?'
    r'<div class="pi-data-value[^"]*">(.*?)</div>',
    re.S,
)
TITLE_RE = re.compile(r'<h2[^>]*pi-title[^>]*>(.*?)</h2>', re.S)
SMALL_RE = re.compile(r"<small\b.*?</small>", re.S)
IGNORED_SOURCES = {"image", "tabs"}
CHARBOX_RE = re.compile(r"\{\{Char Box(.*?)\n\}\}", re.S)
CHARBOX_FIELD_RE = re.compile(r"^\|\s*(\w+)\s*=\s*(.+?)\s*$", re.M)


def slug(title: str) -> str:
    s = re.sub(r"[^\w\s-]", "", title.lower().strip())
    return re.sub(r"[\s_-]+", "_", s)


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "undercover-op-fabrication/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8")
    except urllib.error.URLError:
        # OpenSSL (Python) rejette la chaîne du proxy local ; curl (Schannel) l'accepte.
        return subprocess.run(
            ["curl", "-s", "--max-time", "30", url],
            capture_output=True,
            check=True,
        ).stdout.decode("utf-8")


def page_html(title: str) -> str:
    path = CACHE / f"{slug(title)}.html"
    if path.exists():
        return path.read_text(encoding="utf-8")
    params = urllib.parse.urlencode(
        {"action": "parse", "page": title, "prop": "text", "redirects": "1", "format": "json"}
    )
    data = json.loads(fetch(f"{API}?{params}"))
    wikitext = data["parse"]["text"]["*"]
    CACHE.mkdir(parents=True, exist_ok=True)
    path.write_text(wikitext, encoding="utf-8")
    time.sleep(PAUSE)
    return wikitext


def page_wikitext(title: str) -> str:
    params = urllib.parse.urlencode(
        {"action": "parse", "page": title, "prop": "wikitext", "redirects": "1", "format": "json"}
    )
    return json.loads(fetch(f"{API}?{params}"))["parse"]["wikitext"]["*"]


def clean(text: str) -> str:
    text = re.sub(r"<sup\b.*?</sup>", " ", text, flags=re.S)  # références
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def strip_wikilinks(text: str) -> str:
    def visible(m):
        return m.group(1).split("|")[-1]

    return re.sub(r"\[\[([^\]]+)\]\]", visible, text)


def from_infobox_html(html_text: str) -> dict:
    title_m = TITLE_RE.search(html_text)
    fields = {}
    for src, body in SECTION_RE.findall(html_text):
        if src and src not in fields and src not in IGNORED_SOURCES:
            fields[src] = clean(body)
    titre = SMALL_RE.sub(" ", title_m.group(1)) if title_m else ""
    return {"titre": clean(titre), "champs": fields}


def from_charbox_wikitext(wikitext: str) -> dict:
    m = CHARBOX_RE.search(wikitext)
    if not m:
        return {"titre": "", "champs": {}}
    fields = {k: clean(strip_wikilinks(v)) for k, v in CHARBOX_FIELD_RE.findall(m.group(1))}
    return {"titre": fields.get("name", ""), "champs": fields}


def extract(title: str) -> dict:
    html_doc = page_html(title)
    result = from_infobox_html(html_doc)
    if not result["champs"]:
        result = from_charbox_wikitext(page_wikitext(title))
        result["source"] = "wikitext"
    else:
        result["source"] = "infobox"
    return result


def yaml_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)  # JSON est du YAML valide


def emit(entries: list[tuple[str, dict]]) -> str:
    lines = ["# Généré par wiki_extract.py — brut, à relire avant usage.", ""]
    for title, data in entries:
        lines.append(f"{slug(title)}:")
        lines.append(f"  page: {yaml_str(title)}")
        lines.append(f"  source: {yaml_str(data['source'])}")
        if data["titre"]:
            lines.append(f"  titre: {yaml_str(data['titre'])}")
        for k, v in data["champs"].items():
            lines.append(f"  {k}: {yaml_str(v)}")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> None:
    titles = argv or [l.strip() for l in PAGES.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    entries = []
    for t in titles:
        data = extract(t)
        entries.append((t, data))
        n = len(data["champs"])
        print(f"{t}: {data['source']}, {n} champs")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(emit(entries), encoding="utf-8")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main(sys.argv[1:])
