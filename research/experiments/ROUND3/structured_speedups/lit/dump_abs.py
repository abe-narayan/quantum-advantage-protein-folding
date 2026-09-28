"""Dump full abstracts from arXiv API XML files into a UTF-8 text file (verbatim abstracts, for citation checks)."""
import sys, xml.etree.ElementTree as ET
ns = {"a": "http://www.w3.org/2005/Atom"}
out = open(sys.argv[1], "a", encoding="utf-8")
for fn in sys.argv[2:]:
    r = ET.parse(fn).getroot()
    for e in r.findall("a:entry", ns):
        aid = e.find("a:id", ns).text.rsplit("/", 1)[-1]
        t = " ".join(e.find("a:title", ns).text.split())
        au = ", ".join(x.find("a:name", ns).text for x in e.findall("a:author", ns))
        d = e.find("a:published", ns).text[:10]
        jr = e.find("{http://arxiv.org/schemas/atom}journal_ref")
        ab = " ".join(e.find("a:summary", ns).text.split())
        out.write(f"### arXiv:{aid} ({d}) {t}\nAuthors: {au}\n" + (f"Journal-ref: {jr.text}\n" if jr is not None else "") + f"{ab}\n\n")
