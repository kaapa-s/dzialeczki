import urllib.request, urllib.parse, re, sys
def area(i):
    q=urllib.parse.urlencode({"request":"GetParcelById","id":i,"result":"geom_wkt","srid":"2180"})
    t=urllib.request.urlopen("https://uldk.gugik.gov.pl/?"+q,timeout=30).read().decode()
    if not t.startswith("0"): return None
    pts=[tuple(map(float,p.split())) for p in re.findall(r"[\d.]+ [\d.]+", t.split("\n",1)[1])]
    return abs(sum(pts[k][0]*pts[k+1][1]-pts[k+1][0]*pts[k][1] for k in range(len(pts)-1)))/2
for o in sys.argv[1:]:
    print(o, [ (n, round(area(f"{o}.{n}") or 0)) for n in ["277","278","279","285"]])
