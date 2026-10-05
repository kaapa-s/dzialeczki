// Fragmenty JS wykonywane w karcie Chrome (javascript_tool) – patrz PROCEDURA.md.
// Każdy blok uruchamiać osobno. Pętle trzymać krótkie: wywołanie ma limit 45 s,
// a timery w karcie w tle są mocno spowalniane.

// --- 1. Udawaj widoczną kartę (bez tego FB nie doładowuje komentarzy w tle) ---
Object.defineProperty(document, 'visibilityState', { get: () => 'visible', configurable: true });
Object.defineProperty(document, 'hidden', { get: () => false, configurable: true });
window.requestAnimationFrame = cb => setTimeout(() => cb(performance.now()), 16);
window.cancelAnimationFrame = id => clearTimeout(id);
document.dispatchEvent(new Event('visibilitychange'));

// --- 2. Kolektor komentarzy (FB usuwa z DOM komentarze poza ekranem, więc zbieramy na bieżąco) ---
window.__c = window.__c || {};
window.__collect = function () {
  // cały dokument – FB potrafi mieć 2 dialogi, a pierwszy bywa nieaktualną kopią z kilkunastoma komentarzami
  const dlg = document;
  for (const a of dlg.querySelectorAll('div[role="article"]')) {
    const lab = a.getAttribute('aria-label') || '';
    if (!/^(Comment|Reply) by/.test(lab)) continue;
    const txt = a.innerText;
    const links = [...a.querySelectorAll('a[href]')].map(x => x.href);
    const imgs = [...a.querySelectorAll('img')].filter(i => i.naturalWidth > 150).map(i => i.src);
    const old = window.__c[lab];
    window.__c[lab] = {
      lab,
      txt: (old && old.txt.length > txt.length) ? old.txt : txt,
      links: [...new Set([...(old?.links || []), ...links])],
      imgs: [...new Set([...(old?.imgs || []), ...imgs])],
    };
  }
  // rozwiń "See more" / "View N replies"
  [...dlg.querySelectorAll('div[role="button"],span[role="button"]')]
    .filter(b => /^(View more comments|View \d+ more comments?|View (all )?\d+ repl(y|ies)|See more)$/i.test(b.innerText.trim()))
    .forEach(b => b.click());
  return Object.keys(window.__c).length;
};
window.__collect();
// Potem: na przemian scroll kółkiem myszy w okienku posta (computer → scroll, 3 w górę + 10 w dół),
// wait 3 s, window.__collect() – aż liczba przestanie rosnąć.

// --- 3. Lista autorów ---
[...new Set(Object.keys(window.__c).map(k => k.replace(/^(Comment|Reply) by /, '').replace(/ (a few seconds|\d+ \w+|about an? \w+|an? \w+) ago$/, '')))].join('; ');

// --- 4. Teksty nowych komentarzy (podmień listę nazwisk) ---
Object.values(window.__c).filter(v => /Nazwisko1|Nazwisko2/.test(v.lab))
  .map(v => '### ' + v.lab + ' (img:' + v.imgs.length + ')\n' + v.txt.slice(0, 900)).join('\n');

// --- 5. Linki zewnętrzne (rozpakowane z l.facebook.com, bez query stringa – inaczej narzędzie blokuje wynik) ---
Object.values(window.__c).map(v => {
  const ls = [...new Set(v.links.map(h => {
    try { const u = new URL(h); return u.hostname.startsWith('l.facebook.com') ? decodeURIComponent(u.searchParams.get('u')) : h; } catch (e) { return h; }
  }).filter(h => !/facebook\.com\/(groups|profile|hashtag)|comment_id=/.test(h)).map(h => h.split('?')[0]))];
  return ls.length ? v.lab.replace(/^(Comment|Reply) by /, '').slice(0, 30) + ' => ' + ls.join(' , ') : null;
}).filter(Boolean).join('\n');

// --- 6. Podgląd zdjęcia z komentarza na pełnym ekranie (do OCR przez screenshot/zoom) ---
// __show2('Janina Bogucka', 0, -90)  → autor, indeks zdjęcia, obrót w stopniach (0 = bez obrotu)
window.__show2 = function (name, idx, rot) {
  document.getElementById('__ov')?.remove();
  const srcs = [...new Set(Object.values(window.__c).filter(v => v.lab.includes(name)).flatMap(v => v.imgs))];
  const src = srcs[idx || 0]; if (!src) return 'brak, zdjęć: ' + srcs.length;
  const d = document.createElement('div'); d.id = '__ov';
  d.style.cssText = 'position:fixed;inset:0;z-index:999999;background:#fff;display:flex;align-items:center;justify-content:center';
  const im = document.createElement('img'); im.src = src;
  im.style.cssText = rot ? 'height:95vw;width:auto;max-width:none;max-height:none;transform:rotate(' + rot + 'deg)'
                         : 'height:96vh;width:auto;max-width:none;max-height:none';
  d.appendChild(im); d.onclick = () => d.remove(); document.body.appendChild(d);
  return 'ok, zdjęć: ' + srcs.length;
};
// sprzątanie: document.getElementById('__ov')?.remove()

// --- 7. Ekstraktor numerów działek z ogłoszenia (otodom / olx / gratka / freedom / morizon) ---
(() => {
  const t = document.body.innerText;
  const html = document.documentElement.innerHTML.replace(/\\"/g, '"');
  const snip = [...t.matchAll(/.{0,100}(nr\.? ?dz|numer dz|działk[ai] nr|ewid|obręb|obreb|\b\d{1,4}\/\d{1,3}\b).{0,100}/gi)].map(m => m[0]).slice(0, 15);
  const ll = [...html.matchAll(/"(lat|latitude)"\s*:\s*(5[0-4]\.\d+)[^}]{0,80}"(lon|lng|longitude)"\s*:\s*(1[4-9]\.\d+|2[0-4]\.\d+)/g)].map(m => m[2] + ',' + m[4]).slice(0, 2);
  return JSON.stringify({ url: location.href.split('?')[0], title: document.title, snip, ll });
})();

// --- 8. Treść posta FB z innego profilu (gdy karta w tle nie renderuje) – po kroku 1 ---
(() => {
  const html = document.documentElement.innerHTML;
  const seg = [...html.matchAll(/"text":"([^"]{20,4000})"/g)].map(m => m[1]).sort((a, b) => b.length - a.length)[0] || '';
  return seg.replace(/\\n/g, '\n').replace(/\\u([0-9a-f]{4})/gi, (_, h) => String.fromCharCode(parseInt(h, 16))).slice(0, 2500);
})();
