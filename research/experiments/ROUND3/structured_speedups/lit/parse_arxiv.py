"""Parse arXiv API Atom XML files -> compact listing (id, date, title, authors, abstract head)."""
import sys, re, json, xml.etree.ElementTree as ET
ns = {"a": "http://www.w3.org/2005/Atom"}
out = []
for fn in sys.argv[1:]:
    try:
        root = ET.parse(fn).getroot()
    except Exception as e:
        print("PARSE FAIL", fn, e); continue
    for e in root.findall("a:entry", ns):
        aid = e.find("a:id", ns).text.rsplit("/", 1)[-1]
        t = " ".join(e.find("a:title", ns).text.split())
        d = e.find("a:published", ns).text[:10]
        au = [x.find("a:name", ns).text for x in e.findall("a:author", ns)]
        ab = " ".join(e.find("a:summary", ns).text.split())
        out.append(dict(id=aid, date=d, title=t, authors=au, abstract=ab, src=fn))
seen = set()
for r in out:
    if r["id"] in seen: continue
    seen.add(r["id"])
    n = int(sys.argv[0] and 0) or 0
    print(f"[{r['id']}] {r['date']} | {r['title']} | {', '.join(r['authors'][:4])}{' et al.' if len(r['authors'])>4 else ''}")
json.dump(out, open("_last_parse.json", "w", encoding="utf-8"), indent=1)
