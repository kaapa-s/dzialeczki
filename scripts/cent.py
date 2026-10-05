import urllib.request, urllib.parse, re, json, sys
ids = sys.argv[1:]
out = {}
for i in ids:
    q = urllib.parse.urlencode({"request":"GetParcelById","id":i,"result":"geom_wkt","srid":"4326"})
    t = urllib.request.urlopen("https://uldk.gugik.gov.pl/?"+q, timeout=30).read().decode()
    pts = [tuple(map(float,p.split())) for p in re.findall(r"[\d.]+ [\d.]+", t.split("\n",1)[1])]
    x = sum(p[0] for p in pts)/len(pts); y = sum(p[1] for p in pts)/len(pts)
    out[i] = [round(y,6), round(x,6)] if x>y else [round(x,6), round(y,6)]
import os
p=os.path.join(os.path.dirname(os.path.abspath(__file__)),"cent.json")
allc=json.load(open(p)) if os.path.exists(p) else {}
allc.update(out); json.dump(allc,open(p,"w"),ensure_ascii=False,indent=0)
print(json.dumps(out))
