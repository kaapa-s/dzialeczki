import json, html, os
HERE=os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE,"cent.json")))

PAGES=[("index.html","Post 1 – działka 1000–3000 m², MPZP, las"),("post2.html","Post 2 – od 3000 m², las z 3 stron")]

def render(out, *, A, AMB, NOULDK, B, D, E, title, h1, sub, amb_title, amb_sub="", amb_stat="niejednoznaczne"):
    cur=' aria-current="page"'
    nav_html='<nav class="pages" aria-label="Podstrony">'+"".join(f'<a href="{f}"{cur if f==out else ""}>{html.escape(t)}</a>' for f,t in PAGES)+"</nav>"
    e = html.escape
    def plinks(ps):
        out=[]
        for p in ps:
            lon,lat = C[p["id"]]
            g = "https://mapy.geoportal.gov.pl/imap/Imgp_2.html?identifyParcel="+p["id"]
            m = f"https://www.google.com/maps?q={lat},{lon}"
            out.append(f'<div class="parcel"><label class="seen" title="obejrzana"><input type="checkbox" data-k="{e(p["id"])}"></label>{star(p["id"])}<span class="nr">{e(p["label"])}</span> <a href="{e(g)}" target="_blank">Geoportal</a> <a class="sec" href="{m}" target="_blank">Google Maps</a> <code>{e(p["id"])}</code></div>')
        return "".join(out)
    def rk(*parts): return "r:"+"|".join(parts)
    def star(k): return f'<button type="button" class="star" data-s="{e(k)}" title="potencjalnie interesująca" aria-pressed="false">☆</button>'
    def note(k): return f'<td class="nt"><textarea data-n="{e(k)}" rows="1" placeholder="notatka…" aria-label="Notatka"></textarea></td>'
    def tr(k, cells, row_star=True): return f'<tr data-r="{e(k)}"><td>{star(k) if row_star else ""}{cells[0]}</td>' + "".join(f"<td{c[0]}>{c[1]}</td>" if isinstance(c,tuple) else f"<td>{c}</td>" for c in cells[1:]) + note(k) + "</tr>"
    def chk(*parts): return f'<label class="seen" title="obejrzane"><input type="checkbox" data-k="{e("r:"+"|".join(parts))}"></label>'
    def tel(t): return f'<a href="tel:{t.replace(" ","")}">{e(t)}</a>' if t else ""
    def src(z,lk): return e(z)+(f'<br><a href="{e(lk)}" target="_blank">ogłoszenie ↗</a>' if lk else "")
    def lnk(u,label): return f'<a href="{e(u)}" target="_blank">{label}</a>' if u else ""
    rows_a = "".join(tr(rk(a,l), [e(a), e(l), plinks(ps), e(n), tel(t), (" class=src", src(z,lk))], row_star=False) for a,l,ps,n,t,z,lk in A)
    rows_amb = "".join(tr(rk(a,l), [e(a), e(l), plinks(ps), e(n), tel(t), (" class=src", src(z,lk))], row_star=False) for a,l,ps,n,t,z,lk in AMB)
    rows_nu = "".join(tr(rk(a,l), [chk(a,l)+e(a), e(l), f"<b>{e(nr)}</b>", e(n), f"{lnk(m,'Google Maps (pinezka)')} {lnk(lk,'ogłoszenie ↗')}"]) for a,l,nr,n,m,lk in NOULDK)
    rows_b = "".join(tr(rk(a,l), [chk(a,l)+e(a), e(l), e(n), lnk(u,'otwórz ↗')]) for a,l,n,u in B)
    rows_d = "".join(tr(rk(a,l), [chk(a,l)+e(a), e(l), e(n), tel(t)]) for a,l,n,t in D)
    rows_e = "".join(tr(rk(a,n), [chk(a,n)+e(a), e(n), tel(t)]) for a,n,t in E)
    nA = sum(len(x[2]) for x in A)
    Cimg=[]
    JS = r"""
    const KEY='dzialki-obejrzane', HKEY='dzialki-ukryj';
    const load=k=>{try{return JSON.parse(localStorage.getItem(k))}catch(e){return null}};
    const save=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}};
    let seen=load(KEY)||{};
    const boxes=[...document.querySelectorAll('.seen input')];
    function refresh(){
      boxes.forEach(b=>{b.checked=!!seen[b.dataset.k]; const par=b.closest('.parcel'); if(par) par.classList.toggle('done',b.checked);});
      document.querySelectorAll('tr').forEach(tr=>{const bs=[...tr.querySelectorAll('.seen input')]; tr.classList.toggle('done',bs.length>0&&bs.every(b=>b.checked));});
      document.getElementById('cnt').textContent=new Set(boxes.filter(b=>b.checked).map(b=>b.dataset.k)).size+' / '+new Set(boxes.map(b=>b.dataset.k)).size;
    }
    boxes.forEach(b=>b.addEventListener('change',()=>{ if(b.checked) seen[b.dataset.k]=new Date().toISOString().slice(0,10); else delete seen[b.dataset.k]; save(KEY,seen); refresh(); }));
    const hide=document.getElementById('hide');
    hide.checked=!!load(HKEY); document.body.classList.toggle('hide',hide.checked);
    hide.addEventListener('change',()=>{document.body.classList.toggle('hide',hide.checked); save(HKEY,hide.checked);});
    document.getElementById('clr').addEventListener('click',()=>{ if(!Object.keys(seen).length) return; seen={}; save(KEY,seen); refresh(); });
    refresh();

    // --- ★ potencjalnie interesujące + notatki + filtr ---
    const SKEY='dzialki-ciekawe', NKEY='dzialki-notatki', FKEY='__FKEY__';
    let fav=load(SKEY)||{}, notes=load(NKEY)||{};
    const stars=[...document.querySelectorAll('.star')], areas=[...document.querySelectorAll('textarea[data-n]')];
    const rows=[...document.querySelectorAll('tr[data-r]')];
    function paintStars(){
      stars.forEach(b=>{const on=!!fav[b.dataset.s]; b.textContent=on?'★':'☆'; b.classList.toggle('on',on); b.setAttribute('aria-pressed',on); const par=b.closest('.parcel'); if(par) par.classList.toggle('fav',on);});
      document.getElementById('nfav').textContent=Object.keys(fav).length;
    }
    stars.forEach(b=>b.addEventListener('click',()=>{const k=b.dataset.s; if(fav[k]) delete fav[k]; else fav[k]=new Date().toISOString().slice(0,10); save(SKEY,fav); paintStars(); applyFilter();}));
    const fit=t=>{t.style.height='auto'; t.style.height=t.scrollHeight+2+'px';};
    let tmr;
    areas.forEach(t=>{
      t.value=notes[t.dataset.n]||''; fit(t); t.classList.toggle('has',!!t.value.trim());
      t.addEventListener('input',()=>{fit(t); const v=t.value; if(v.trim()) notes[t.dataset.n]=v; else delete notes[t.dataset.n]; t.classList.toggle('has',!!v.trim());
        clearTimeout(tmr); tmr=setTimeout(()=>{save(NKEY,notes); document.getElementById('nnote').textContent=Object.keys(notes).length;},300);});
      t.addEventListener('blur',()=>{save(NKEY,notes); applyFilter();});
    });
    document.getElementById('nnote').textContent=Object.keys(notes).length;
    const fsel=document.getElementById('fsel'), fq=document.getElementById('fq');
    const fs=load(FKEY)||{}; fsel.value=fs.mode||'all'; fq.value=fs.q||'';
    const norm=x=>x.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/ł/g,'l');
    function applyFilter(){
      const mode=fsel.value, q=norm(fq.value.trim());
      document.body.classList.toggle('only-fav',mode==='fav');
      let shown=0;
      rows.forEach(r=>{
        const isFav=[...r.querySelectorAll('.star')].some(b=>fav[b.dataset.s]);
        const ta=r.querySelector('textarea'); const hasNote=!!(ta&&ta.value.trim());
        let ok= mode==='all' || (mode==='fav'&&isFav) || (mode==='note'&&hasNote) || (mode==='any'&&(isFav||hasNote));
        if(ok&&q) ok=norm(r.innerText+' '+(ta?ta.value:'')).includes(q);
        r.hidden=!ok; if(ok) shown++;
      });
      document.querySelectorAll('section').forEach(sec=>{sec.hidden=!sec.querySelector('tr[data-r]:not([hidden])');});
      const active=mode!=='all'||q; document.getElementById('fres').textContent=active?('pasuje: '+shown+' / '+rows.length):'';
      document.getElementById('fnone').hidden=!(active&&!shown);
      save(FKEY,{mode:fsel.value,q:fq.value});
    }
    fsel.addEventListener('change',applyFilter); fq.addEventListener('input',applyFilter);
    paintStars(); applyFilter();
    """
    page = f"""<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{e(title)}</title><style>
    :root{{--bg:#fafaf8;--fg:#1d1d1b;--mut:#6b6b66;--line:#e3e2dc;--acc:#1f6f4a;--warn:#a15c00;--card:#fff;--fav:#c48a00;--favbg:#fdf7e6;--notebg:#f4f8f5}}
    @media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#161615;--fg:#ecebe6;--mut:#9a9992;--line:#2e2e2b;--acc:#5fc28f;--warn:#e0a650;--card:#1e1e1c;--fav:#f0c24b;--favbg:#2a2516;--notebg:#1b241f}}}}
    body{{background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,system-ui,sans-serif;margin:0;padding:24px 16px 64px}}
    main{{max-width:1440px;margin:auto}} h1{{margin:0 0 4px}} h2{{margin:40px 0 4px;font-size:19px}} .sub{{color:var(--mut);margin:0 0 12px}}
    .tw{{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}}
    table{{border-collapse:collapse;width:100%}} th,td{{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid var(--line)}}
    th{{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}} tr:last-child td{{border:0}}
    a{{color:var(--acc);font-weight:600}} a.sec{{font-weight:400;color:var(--mut)}} code{{font-size:11px;color:var(--mut)}}
    .parcel{{white-space:nowrap;margin:2px 0}} .nr{{display:inline-block;min-width:3.5em;font-weight:700}}
    .src{{font-size:13px;color:var(--mut)}} .warn{{color:var(--warn)}} .stats{{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}} .stats div{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 14px}} .stats b{{font-size:20px;display:block}}
    .seen{{cursor:pointer;margin-right:6px}} .seen input{{cursor:pointer;accent-color:var(--acc);vertical-align:-2px}}
    .parcel.done,tr.done{{opacity:.45}} .parcel.done .nr{{text-decoration:line-through}}
    body.hide .parcel.done,body.hide tr.done{{display:none}}
    .star{{font:inherit;font-size:17px;line-height:1;background:none;border:0;padding:0 4px 0 0;cursor:pointer;color:var(--mut);vertical-align:-1px}}
    .star.on{{color:var(--fav)}} .star:focus-visible{{outline:2px solid var(--acc);border-radius:3px}}
    .parcel.fav .nr{{color:var(--fav)}} tr:has(.star.on){{background:var(--favbg)}}
    body.only-fav .parcel:not(.fav){{display:none}}
    td.nt{{min-width:200px;width:18%}} a[href^=tel]{{white-space:nowrap}} .nt textarea{{width:100%;box-sizing:border-box;min-height:32px;resize:vertical;font-family:inherit;font-size:13px;line-height:1.4;color:var(--fg);background:transparent;border:1px dashed var(--line);border-radius:6px;padding:5px 7px}}
    .nt textarea:focus{{outline:none;border:1px solid var(--acc);background:var(--card)}} .nt textarea.has{{border-style:solid;background:var(--notebg)}}
    .bar select,.bar input[type=search]{{font:inherit;color:var(--fg);background:var(--card);border:1px solid var(--line);border-radius:6px;padding:3px 8px}}
    .bar input[type=search]{{min-width:0;width:14em;max-width:100%}} .bar .sep{{flex-basis:100%;height:0}}
    #fnone{{margin:32px 0;color:var(--mut)}}
    nav.pages{{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 18px;font-size:14px}} nav.pages a{{font-weight:500;color:var(--mut);text-decoration:none;border:1px solid var(--line);border-radius:999px;padding:3px 12px}} nav.pages a[aria-current]{{color:var(--fg);border-color:var(--acc);font-weight:600}}
    .bar{{display:flex;gap:16px;align-items:center;flex-wrap:wrap;color:var(--mut);font-size:14px}} .bar button{{font:inherit;color:var(--mut);background:none;border:1px solid var(--line);border-radius:6px;padding:3px 10px;cursor:pointer}}
    </style></head><body><main>
    {nav_html}<h1>{e(h1)}</h1><p class="sub">{sub}</p>
    <div class="stats"><div><b>{len(A)}</b>z linkami ({nA} działek)</div><div><b>{len(AMB)}</b>{e(amb_stat)}</div><div><b>{len(NOULDK)}</b>numer bez potwierdzenia</div><div><b>{len(B)}</b>ogłoszenia bez numeru</div><div><b>{len(D)+len(E)}</b>do dopytania</div></div>
    <div class="bar"><span>Obejrzane: <b id="cnt">0</b></span><label><input type="checkbox" id="hide"> ukryj obejrzane</label><button id="clr" type="button">wyczyść zaznaczenia</button>
    <span class="sep"></span><span>★ <b id="nfav">0</b> · notatek: <b id="nnote">0</b></span>
    <label>Pokaż: <select id="fsel"><option value="all">wszystkie</option><option value="fav">tylko ★</option><option value="note">z notatką</option><option value="any">★ lub notatka</option></select></label>
    <input type="search" id="fq" placeholder="szukaj (miejscowość, gmina, notatka…)" aria-label="Szukaj"><span id="fres"></span></div>
    <p id="fnone" hidden>Nic nie pasuje do filtra.</p>
    <section><h2>A. Linki do geoportalu</h2><p class="sub">Link „Geoportal” otwiera mapę z zaznaczoną działką.</p>
    <div class="tw"><table><tr><th>Autor</th><th>Lokalizacja</th><th>Działki</th><th>Szczegóły</th><th>Tel.</th><th>Źródło</th><th>Notatka</th></tr>{rows_a}</table></div>
    </section>
    <section><h2 class="warn">{e(amb_title)}</h2>{f'<p class="sub">{e(amb_sub)}</p>' if amb_sub else ""}
    <div class="tw"><table><tr><th>Autor</th><th>Lokalizacja</th><th>Kandydaci</th><th>Szczegóły</th><th>Tel.</th><th>Źródło</th><th>Notatka</th></tr>{rows_amb}</table></div>
    </section>
    <section><h2 class="warn">A″. Numer jest, ale nie ma go w ewidencji (ULDK)</h2><p class="sub">Linku do geoportalu nie da się zrobić automatycznie – sprawdź ręcznie albo dopytaj.</p>
    <div class="tw"><table><tr><th>Autor</th><th>Lokalizacja</th><th>Numery</th><th>Szczegóły</th><th>Linki</th><th>Notatka</th></tr>{rows_nu}</table></div>
    </section>
    <section><h2>B. Ogłoszenie bez numeru działki – dopytaj</h2><p class="sub">Otworzyłem każde ogłoszenie – numeru nie ma w treści.</p>
    <div class="tw"><table><tr><th>Autor</th><th>Lokalizacja</th><th>Co wiadomo</th><th>Link</th><th>Notatka</th></tr>{rows_b}</table></div>
    </section>
    <section><h2>D. Jest miejscowość, brak numeru – dopytaj</h2>
    <div class="tw"><table><tr><th>Autor</th><th>Lokalizacja</th><th>Z komentarza</th><th>Tel.</th><th>Notatka</th></tr>{rows_d}</table></div>
    </section>
    <section><h2>E. Brak konkretów – dopytaj</h2>
    <div class="tw"><table><tr><th>Autor</th><th>Treść</th><th>Tel.</th><th>Notatka</th></tr>{rows_e}</table></div>
    </section>
    </main><script>{JS}</script></body></html>"""
    page=page.replace("__FKEY__","dzialki-filtr-"+out.split(".")[0])
    open(os.path.join(HERE,"..",out),"w").write(page)
    print("ok", out, len(A)+len(AMB)+len(NOULDK)+len(B)+len(D)+len(E))
