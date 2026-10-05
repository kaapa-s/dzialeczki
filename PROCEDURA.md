# Aktualizacja listy działek z komentarzy FB

Post: https://www.facebook.com/groups/711943943162830/posts/1820926428931237/
Wynik: `index.html` (GitHub Pages – repo `kaapa-s/dzialeczki`) (generowany przez `scripts/gen.py`).

## Pliki

| Plik | Do czego |
|---|---|
| `komentarze.md` | pierwotny zrzut komentarzy (ucięte linki, bez zdjęć) |
| `scripts/gen.py` | **dane** (listy `A`, `AMB`, `NOULDK`, `B`, `D`, `E`) + generator HTML |
| `scripts/cent.py` | pobiera z ULDK środki działek (do linku Google Maps) i dopisuje do `cent.json` |
| `scripts/cent.json` | cache współrzędnych – `gen.py` wymaga wpisu dla każdego ID z list `A`/`AMB` |
| `scripts/area.py` | liczy powierzchnie działek w ULDK – do zgadywania obrębu po powierzchni |
| `scripts/browser-snippets.js` | fragmenty JS do odpalania w Chrome (numerowane 1–8) |

## Kroki

### 1. Pobranie komentarzy z FB (Claude in Chrome)

1. Otwórz post w nowej karcie. Zostaw sortowanie **„Most relevant”** – przy „All comments” ładowanie się wieszało.
2. Uruchom snippet **1** (udawanie widocznej karty). Bez tego FB nie doładowuje komentarzy, bo karta MCP jest w tle (`document.visibilityState === 'hidden'`).
3. Uruchom snippet **2** (kolektor `window.__collect`). FB wirtualizuje listę – komentarze poza ekranem znikają z DOM, więc trzeba zbierać na bieżąco.
4. Przewijaj okienko posta **kółkiem myszy** (`computer → scroll` w środek okienka: 3 w górę, 10 w dół, `wait 3`, `__collect()`), w `browser_batch` po kilka rund. Programowe `scrollTop` nie wyzwala doładowania. Kończ, gdy licznik przestaje rosnąć, a na dole zostają tylko szare placeholdery.
5. Snippet **3** → lista autorów. Porównaj z tym, co już jest w `gen.py`, i wybierz nowych.
6. Snippet **4** → treść nowych komentarzy (i odpowiedzi – często tam autor dopisuje numery, np. Szymanowska „13/1 do 13/13”).
7. Snippet **5** → pełne linki do ogłoszeń. W `komentarze.md` linki są ucięte „...”, tu są pełne. Query string trzeba obciąć, bo narzędzie blokuje wynik z `?...`.

### 2. OCR zdjęć

1. Snippet **6**: `__show2('Autor', indeks, obrót)` wyświetla zdjęcie na całym ekranie; potem `screenshot`, a drobne napisy `zoom` na fragment.
2. Miniatury z FB mają niską rozdzielczość (~300 px) – drobne numery na mapkach bywają nieczytelne (Dula, Sikorska). Wtedy: do grupy „dopytaj” albo „numer niepewny”.
3. Na koniec usuń overlay: `document.getElementById('__ov')?.remove()`.

### 3. Ogłoszenia

1. Każdy link otwórz w **osobnej** karcie (żeby nie stracić stanu posta) i uruchom snippet **7** – szuka „nr działki / obręb / ddd/dd” w treści i współrzędnych w HTML.
2. Gdy numeru nie ma, a są współrzędne – `GetParcelByXY` w ULDK, ale wynik oznacz jako przybliżony (pinezki otodom bywają obok, np. Strzegocin trafia w Prusinowice).
3. **FB Marketplace** – zgoda na zasady danych już udzielona (2026-10-05), ogłoszenia otwierają się normalnie. Opis: `document.querySelector('div[role="main"]').innerText` (uciąć od „Recently listed”); numery bywają w opisie albo na zrzucie geoportalu w zdjęciach. Gdyby znów wyskoczyło „You'll need to make a choice about Marketplace” – nie klikać za użytkownika.
4. Post FB z innego profilu: po snippecie 1 – snippet **8** (wyciąga tekst z JSON-a w HTML).
5. curl/WebFetch do OLX/otodom/gratka nie działa (403 / przekierowanie) – tylko przez Chrome.

### 4. Zamiana „miejscowość + numer” na identyfikator działki (ULDK)

API: `https://uldk.gugik.gov.pl/`

```bash
# po nazwie obrębu i numerze – zwraca wszystkie obręby o tej nazwie w Polsce
curl -s -G https://uldk.gugik.gov.pl/ --data-urlencode request=GetParcelByIdOrNr \
  --data-urlencode "id=Niegów 218/7" --data-urlencode result=teryt,voivodeship,county,commune,region,parcel

# obręby o danej nazwie (gdy numer nie wychodzi) → np. 140602_2.0052|Zalesie|Błędów
curl -s -G https://uldk.gugik.gov.pl/ --data-urlencode request=GetRegionByNameOrId \
  --data-urlencode id=Zalesie --data-urlencode result=teryt,region,commune,county

# czy działka istnieje (pierwsza linia "0" = tak, "-1 brak wyników" = nie)
curl -s -G https://uldk.gugik.gov.pl/ --data-urlencode request=GetParcelById \
  --data-urlencode id=143803_2.0001.285 --data-urlencode result=teryt

# działka pod współrzędnymi (lon,lat)
curl -s -G https://uldk.gugik.gov.pl/ --data-urlencode request=GetParcelByXY \
  --data-urlencode xy=21.5661779,52.2910409,4326 --data-urlencode result=teryt,commune,region,parcel
```

Zasady:
- Filtruj po `mazowieckie`, a przy kilku trafieniach – po gminie / kodzie pocztowym z komentarza. Gdy dalej niejednoznaczne → sekcja `AMB` (wszyscy kandydaci).
- Link do Google Maps (`maps.app.goo.gl/...`) rozwiń `curl -sI` (nagłówek `location` ma `q=lat,lon`) i sprawdź `GetParcelByXY`.
- Brak obrębu w komentarzu, ale znana gmina i numery → przeleć obręby gminy (`<teryt_gminy>.0001`…`.0045`) przez `GetParcelById`, a kandydatów porównaj powierzchnią: `python3 scripts/area.py 143803_2.0001 143803_2.0009 ...` (tak ustalona Aleksandria u Boguckiej).
- Numer z ogłoszenia nieobecny w ULDK (świeży podział, literówka) → sekcja `NOULDK`.

### 5. Aktualizacja strony

1. Dopisz wpisy do list w `scripts/gen.py`:
   - `A` – `(autor, lokalizacja, [P(id, etykieta), ...], szczegóły, telefon, źródło, link_ogłoszenia)`
   - `AMB` – jw., kilku kandydatów
   - `NOULDK` – `(autor, lokalizacja, numery, szczegóły, link_google_maps, link_ogłoszenia)`
   - `B` – ogłoszenie bez numeru: `(autor, lokalizacja, co_wiadomo, link)`
   - `D` – miejscowość bez numeru: `(autor, lokalizacja, co_wiadomo, telefon)`
   - `E` – brak konkretów: `(autor, treść, telefon)`
   Gdy ktoś z `B`/`D`/`E` dośle numer – przenieś go do `A`.
   ⚠ Zaznaczenia w przeglądarce (obejrzane, ★, notatki – localStorage) są przypięte do kluczy: działki z `A`/`AMB` – do ID działki, wpisy – do `"autor|lokalizacja"` (w `E`: `"autor|treść"`). Zmiana autora/lokalizacji istniejącego wpisu (albo przeniesienie z `D` do `A` ze zmienioną lokalizacją) gubi jego notatkę – wtedy trzymaj tekst bez zmian albo uprzedź użytkownika.
2. Współrzędne nowych działek: `python3 scripts/cent.py <id> <id> ...` (dopisuje do `cent.json`).
3. `python3 scripts/gen.py && open index.html`
4. Zamknij karty Chrome otwarte przez Claude.

Link do geoportalu: `https://mapy.geoportal.gov.pl/imap/Imgp_2.html?identifyParcel=<ID>`
