import json, html, os
HERE=os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE,"cent.json")))
def P(id_, label):  # parcel
    return {"id": id_, "label": label}
OTO="https://www.otodom.pl/pl/oferta/duza-dzialka-budowlana-w-spokojnym-otoczeniu-ID4u3oj"
FRE="https://freedom.pl/oferta/dzialka-na-sprzedaz-soltykow-brzozowa-12499-3685-ogs/"
ZAL="https://www.olx.pl/d/oferta/dzialka-budowlana-1349-m-z-mpzp-przy-lesie-s7-zaluski-CID3-ID1cAkWF.html"
NIW="https://www.olx.pl/d/oferta/dzialka-735-m-wz-prad-las-dzialka-pod-warszawa-CID3-ID1bf4Gl.html"
# (autor, lokalizacja, działki, uwagi, tel, źródło, link)
A = [
 ("Hubert Górski","Niegów, gm. Zabrodzie",[P("143506_2.0014.218/7","218/7")],"2800 m², asfalt od frontu","","komentarz",""),
 ("Mateusz Postek","Łukawska Wola, gm. Głowaczów",[P("140702_5.0022.72","72"),P("140702_5.0022.63","63")],"2800 / 2900 m², WZ, 120 / 130 tys.","","komentarz",""),
 ("Anna Płochocka","Stanisławów (pow. miński), ul. Skrajna",[P("141214_4.0001.564/1","564/1"),P("141214_4.0001.564/2","564/2")],"po 1807 m², szer. 17,6 m, WZ, 120 zł/m². Pinezka z Google Maps trafia w 564/2","530 390 445","komentarz",""),
 ("Kamil Mrówa","Olszanka, gm. Wyszków, ul. Szmaragdowa",[P("143505_5.0014.337","337")],"2100 m², MPZP","","komentarz",""),
 ("Agata Słomska","Grzebowilk, gm. Siennica",[P("141213_5.0011.1249/6","1249/6"),P("141213_5.0011.1249/7","1249/7")],"po 1000 m²","","komentarz",""),
 ("Przemysław Majewski","Świniotop, gm. Wyszków",[P("143505_5.0021.170","170"),P("143505_5.0021.154","154"),P("143505_5.0021.174","174"),P("143505_5.0021.263","263")],"2100–2500 m², 140 zł/m² (263: 100 zł/m²). ⚠ Działki nr 161 nie ma w ewidencji – dopytaj","","komentarz",""),
 ("Wiesław Golba","Skłudy, gm. Obryte",[P("142402_2.0016.27/1","27/1"),P("142402_2.0016.28/1","28/1")],"razem 12000 m²","508 386 406","komentarz",""),
 ("Patryk Nowak","Nowa Pogorzel, gm. Siennica",[P("141213_5.0020.105","105")],"3000 m², media w działce","","komentarz",""),
 ("Anna Marton","Arciechów, gm. Radzymin",[P("143409_5.0001.865","865")],"9632 m², MPZP MN/ML, 160 zł/m²","728 566 338","komentarz",""),
 ("Marlena Waszczuk","Wiskitki",[P("143805_4.0001.495/9","495/9")],"1560 m², prąd i woda","","komentarz",""),
 ("Dorota Pankowska","Grabina Radziwiłłowska, gm. Puszcza Mariańska",[P("143803_2.0012.151/2","151/2")],"Puszcza Bolimowska","","komentarz",""),
 ("Anna Piękoś","Laskowiec, gm. Rzekuń",[P("141510_2.0009.442","442")],"11600 m², MPZP budowlano-leśna","","komentarz",""),
 ("Bogusia Godlewska","Nowy Lubiel, gm. Rząśnik",[P("143503_2.0011.494/34","494/34")],"1000 m², graniczy z lasem, 5 min do Narwi","667 262 710","komentarz (nowy)",""),
 ("Janina Bogucka","Aleksandria, gm. Puszcza Mariańska",[P("143803_2.0001."+n,n) for n in ["277","279","280","281","282","283","284","285"]],"Z OCR wypisu z planu: MPZP MN/RM. 277 i 279–281 ok. 1490 m² (dojazd drogą wewn. 278), 282–285 ok. 1040 m² (bezpośrednio przy drodze gminnej). Obręb ustalony po zgodności powierzchni z ewidencją","","OCR zdjęć",""),
 ("Damian Komorowski","Ołdakowizna, gm. Stanisławów",[P("141214_5.0013.59/13","59/13")],"Z OCR grafiki: 3001 m², WZ na 2 domy, prąd/woda/światłowód, udział w drodze 59/10, 104 zł/m²","535 502 200","OCR zdjęcia",""),
 ("Jakub Jastrzębski","Sołtyków, gm. Skaryszew (pow. radomski)",[P("142510_5.0026.AR_1.302/8","302/8"),P("142510_5.0026.AR_1.302/9","302/9")],"871 / 872 m², MPZP, prostokątne. ⚠ Okolice Radomia – daleko","","ogłoszenie",FRE),
 ("ZanySeahorse2548","Załuski, pow. płoński",[P("142012_2.0026.12/29","12/29"),P("142012_2.0026.12/27","12/27"),P("142012_2.0026.12/28","12/28"),P("142012_2.0026.12/30","12/30")],"12/29: 1349 m², ok. 25×54 m, MPZP, przy lesie. Sąsiednie 12/27, 12/28, 12/30 też na sprzedaż","","ogłoszenie",ZAL),
 ("Kasia Czerwińska-Sabała","Niwy Ostrołęckie, gm. Warka",[P("140611_5.0026.102/1","102/1")],"Działka matka 8000 m² w trakcie podziału (735 m², 1000 m²…), WZ","","ogłoszenie",NIW),
 ("Anna Bro","Gaj, gm. Zabrodzie (pow. wyszkowski)",[P("143506_2.0006.161","161")],"2900 m², 2,4 km do węzła S8 Mostówka, 3,4 km do Niegowa","","komentarz (nowy)",""),
 ("Sebastian Kazimierczyk","Wąsewo-Kolonia, gm. Wąsewo (pow. ostrowski)",[P("141610_2.0030.4/2","4/2")],"MPZP. ⚠ W ewidencji ok. 11 100 m² – może do podziału, dopytaj","","komentarz (nowy)",""),
 ("Emilia Wysocka (agentka)","Czachów, gm. Jasieniec (pow. grójecki)",[P("140606_2.0004.19/"+n,"19/"+n) for n in ["11","12","13","14","15","16","17","18","19","20","21","22","23","25","26"]],"Z OCR grafiki: 16 działek po ok. 1500 m² (w ewidencji 1499 m²), media w drodze, dojazd asfaltowy, 6 km do S7 (Grójec). 19/24 sprzedana, kilka z „REZERWACJA” – nie wiadomo które. Na ulotce też inne oferty (Turowice, Kocerany, Janów, Izabelin Górki…) bez numerów","512 536 830","OCR zdjęcia",""),
 ("Katarzyna Kasiek","Dziekanów Polski, gm. Łomianki",[P("143205_5.0005.653/"+n,"653/"+n) for n in ["3","4","5"]],"1606 m² łącznie (3 działki), 39×41 m, nad Jeziorem Dziekanowskim, osoba prywatna","","ogłoszenie","https://www.otodom.pl/pl/oferta/dzialka-nad-jeziorem-10km-od-warszawy-sprzedajacy-osoba-prywatna-ID4CEdB"),
 ("Norbert Popławski (Muvon)","Bednary Kolonia, gm. Nieborów (⚠ woj. łódzkie)",[P("100509_2.0002.127/7","127/7"),P("100509_2.0002.128/7","128/7"),P("100509_2.0002.128/6","128/6"),P("100509_2.0002.127/6","127/6")],"1600 / 1982 / 2631 / ok. 3130 m², 75 zł/m² (127/7: 119 900 zł), droga wewn. 127/8","","ogłoszenie","https://muvon.pl/oferta/prestizowe-dzialki-w-malowniczej-gm-nieborow/"),
 ("Syl Wek","Podgać, gm. Zabrodzie",[P("143506_2.0017.107/9","107/9")],"MPZP, prąd przy działce, wodociąg w drodze gminnej, 46 km od Warszawy (numer dosłany w drugim komentarzu)","","komentarz (nowy)",""),
 ("Robert Trojanowski","Nowa Wola, gm. Grabów n. Pilicą (26-902)",[P("140704_2.0021.96/"+n,"96/"+n) for n in ["6","7","8","9","10"]],"WZ, 3000 i 4500 m², woda i prąd w drodze gminnej, okolice Puszczy Stromieckiej. Oferta agencji AWIKOM","","komentarz (nowy)",""),
 ("Maria Janiak","Zakroczym (miasto, obręb 01-01), pow. nowodworski",[P("141406_4.0001.14","14")],"4923 m², MPZP MN + usługi nieuciążliwe, droga publiczna nr 62 (asfalt), prąd blisko, woda w drodze, 2 km do S7, 5 km do stacji Modlin","","komentarz (nowy)",""),
 ("Mikołaj Staniaszek","Olszówka, gm. Mszczonów (między Żyrardowem a Mszczonowem)",[P("143802_5.0066.135/3","135/3")],"Działka 1500 m² wydzielana z 135/3 (trójkątny narożnik przy drodze, 34 × 42 m na mapce), media w drodze, zrobiony wjazd; niedaleko Suntago. Potwierdzone w drugim komentarzu","","komentarz (nowy)",""),
 ("Anna Karpińska","Wólka Iłówiecka, gm. Mińsk Mazowiecki",[P("141211_2.0039.382","382")],"Z OCR zrzutu geoportalu: 14 429 m², bardzo wąski i długi pas, „budowlana z lasem”. ⚠ Kształt daleki od prostokąta 1000–3000 m² – pewnie tylko część do podziału, dopytaj","","OCR zdjęcia (nowy)",""),
 ("Klaudia Tywanek","Zator, gm. Puszcza Mariańska",[P("143803_2.0040.239/4","239/4")],"3115 m² (w ewidencji 3111), WZ, prąd i woda na działce, droga asfaltowa, blisko lasu","","komentarz (nowy)",""),
 ("Kamil Rek","Suchowizna, gm. Stanisławów (pow. miński)",[P("141214_5.0022.158","158")],"3258 m², ok. 142 × 23 m, 390 tys. (120 zł/m²), bez pośrednika. Wniosek o WZ na 2 domy – planowany podział na 2 × 1629 m², można kupić całość albo zarezerwować połowę. Wodociąg w działce, prąd przy drodze, dojazd z dwóch stron, 500 m od DK50","","ogłoszenie (nowy)","https://adresowo.pl/o/dzialka-budowlana-stanislawow-suchowizna-3-258-m2-v2p0k8"),
 ("Arka Diusz","Góry, gm. Jakubów (pow. miński)",[P("141208_2.0006.700","700")],"Sam numer w komentarzu. W ewidencji ok. 1540 m²","","komentarz (nowy)",""),
 ("Jola Nałęcz","Ostrowik, gm. Celestynów (pow. otwocki)",[P("141703_2.0007.242/14","242/14")],"Budowlana, woda i prąd w pobliżu, „10800 m lasu” (w ewidencji cała działka 10 880 m²) – za duża, chyba że do podziału","","komentarz (nowy)",""),
 ("Ur Bo","Karniewo, gm. Regimin (pow. ciechanowski)",[P("140208_2.0005.25/5","25/5")],"Ponad 1 ha (w ewidencji 11 386 m²), możliwy podział, reszta warunków spełniona wg autora","","komentarz (nowy)",""),
 ("Paweł Piętka","Urzut, gm. Nadarzyn (pow. pruszkowski), ul. Chabrowa 48",[P("142105_2.0015.12","12")],"Ok. 1550–1580 m², 490 tys. Prąd, gaz, woda i światłowód w drodze niedaleko. Identyfikator ze zrzutu geoportalu w ogłoszeniu","","FB Marketplace","https://www.facebook.com/marketplace/item/697292276283849/"),
 ("Krzysiek Bondyra","Wity, gm. Kałuszyn (pow. miński)",[P("141209_5.0026.280/"+n,"280/"+n+l) for n,l in [("1",""),("2",""),("4"," (rezerwacja)"),("5"," (rezerwacja)"),("6","")]],"6 działek z WZ przy lesie, kształt zbliżony do kwadratu (ok. 35 × 36 m): 280/1–280/5 po 1200 m², 280/6 – 1500 m². 280/3 sprzedana. Woda miejska i prąd do przyłączenia, droga powiatowa 2247W, 5,7 km do A2, ok. 58 km do Warszawy","","FB Marketplace","https://www.facebook.com/marketplace/item/27035754139422429/"),
]
AMB = [
 ("Piotr Miciałkiewicz","Józefów „05-52…” – kod ucięty",
  [P("140609_2.0015.21/1","21/1 · gm. Pniewy"),P("143410_2.0005.21/1","21/1 · gm. Strachówka"),P("140604_2.0004.21/1","21/1 · gm. Goszczyn"),P("140608_5.0012.21/1","21/1 · gm. Nowe Miasto n. P.")],
  "1100 m² + 800 m² lasu, „45 km od Warszawy, S7 lub S8”. 4 kandydaci z Mazowsza – dopytaj o gminę","","komentarz",""),
 ("Kszysztof Michalec","„koło Garwolina”",[P("140304_2.0006.304","304 · Jagodne, gm. Garwolin")],"Z OCR zdjęcia: działka nr 304, 4800 m², ok. 50 × 142–180 m, woda. Obręb zgadnięty po powierzchni (w ewidencji 4694 m²) – tylko gm. Garwolin sprawdzona, dopytaj","","OCR zdjęcia",""),
]
NOULDK = [
 ("Nieruchomosci_Strzegocin","Strzegocin, gm. Świercze","11/9 i 11/5","3564 m² łącznie, wielobok. Numerów nie ma w ewidencji ULDK (może stary/nowy podział)","https://www.google.com/maps?q=52.67244,20.78868",OTO),
 ("Elzbieta Szymanowska","Zalesie, gm. Błędów","13/1 – 13/13","Z odpowiedzi pod komentarzem. 3700 m², 170 tys., WZ. Obręb istnieje, ale działek 13/x brak w ULDK – pewnie świeży podział","", ""),
 ("Urszula Dula","Wierzbica, gm. Serock","ok. 1139–1142 (OCR niepewny)","Z OCR grafiki: 4 działki po ok. 1000 m², 130 zł/m² (całość) / 150 zł/m² (pojedynczo). Numery z miniatury mapy – rozmyte, brak w ULDK","",""),
]
B = [
 ("StylishRadish611","Zakrzewo Kościelne, pow. płocki","3000 m², możliwy podział","https://gratka.pl/nieruchomosci/dzialka-plocki-mala-wies-zakrzewo-koscielne/ob/43984559"),
 ("TrustyRadish5025","Boguszków, gm. Magnuszew","0,49 ha, WZ, pełne uzbrojenie","https://www.olx.pl/d/oferta/atrakcyjna-dzialka-w-boguszkowie-0-49ha-warka-8km-warszawa-50-km-wz-CID3-ID19E0VM.html"),
 ("Piotr Niedek","Kamionka, gm. Latowicz","1000 m², WZ bezterminowe","https://www.morizon.pl/oferta/sprzedaz-dzialka-minski-latowicz-1000m2-mzn2048118828"),
 ("Martyna Sobolewska","Krawcowizna, gm. Strachówka","5 działek po ok. 1150 m², WZ, 110 zł/m² (post FB)","https://www.facebook.com/share/p/1Dh8g7jj3g/"),
 ("Alicja Krawczyk-Dąbrowska","Budy Ciepielińskie","1019 m², WZ – ⚠ ogłoszenie OLX już usunięte","https://www.olx.pl/d/oferta/dzialka-1019-m-wz-asfalt-blisko-serocka-budy-ciepielinskie-CID3-ID1ckkaw.html"),
 ("Norbert Lao","Cegielnia, gm. Radzymin, ul. Bajkowa","1000 m², 590 tys., pozwolenie na budowę + projekt „W kosaćcach 44”, wylane ławy fundamentowe, wszystkie media, 4 km do S8 (FB Marketplace). Numeru brak w opisie i na zdjęciach","https://www.facebook.com/marketplace/item/1048006984633593/"),
 ("Monika Błaszczak","Ostrówek, gm. Klembów","link do strony biura, bez konkretnej oferty","https://www.blaszczak-nieruchomosci.pl"),
 ("Norbert Popławski (Muvon)","Radziejowice-Parcel, gm. Radziejowice","3 działki po ok. 2000 m² (40×50 m), MPZP 2MN/U, prąd w działce, 170 zł/m² (340 tys.). Pinezka z ogłoszenia trafia w 76/8 (4031 m²) – przybliżone","https://muvon.pl/oferta/unikat-prestizowe-dzialki-w-malowniczej-okolicy/"),
 ("Agentka Paulina (Metrohouse)","Polesie, gm. Łyszkowice (⚠ woj. łódzkie)","1100 m², 119 tys. (108 zł/m²), przy drodze asfaltowej. Pinezka z ogłoszenia trafia w dz. 61 (2,16 ha) – przybliżone","https://metrohouse.pl/nieruchomosc/SGBUPE144/nieruchomosc-na-sprzedaz-dzialka-lowicki-polesie"),
 ("Łukasz Bobrowski","Rozniszew, gm. Magnuszew","2053 m², asfalt, skrzynka energetyczna (film YouTube)","https://www.youtube.com/shorts/T1zA_zT_6kc"),
]
D = [
 ("GenuinePersimmon3300","09-100 Płońsk (okolice)","bez lasu, 1 km od S7",""),
 ("Wanda Korycka","Kalen, 09-550 Szczawin Kościelny","2× 1400 m², WZ, 120 km od Warszawy",""),
 ("Paulina Konopacka","Wola Starogrodzka, gm. Parysów","5600 m², rolno-budowlana",""),
 ("Sylwia Syga","Poschła, gm. Parysów","5× ok. 1200 m², MPZP, media",""),
 ("Czarek Andrzejewski","Jackowo Dworskie, gm. Nasielsk","3220 m², WZ, 161 tys.","666 678 112"),
 ("Paulina Sobieska","Osowiec (który?)","2500 m², 490 tys., własny las",""),
 ("Roman Strzelczyk","Strzyżyna, gm. Grabów n. Pilicą","1200 m², woda i prąd; WZ „w trakcie załatwiania”",""),
 ("PassionateElephant557","Arciechów, gm. Radzymin","",""),
 ("Piotr Kucharenko","Radzymin","Z OCR grafiki: 1106 m², MPZP jednorodzinna, prąd w drodze, woda 50 m","600 916 086"),
 ("Gosia Sikorska","Kałęczyn, gm. Stoczek","5 działek 955–1948 m², WZ, 65 zł/m², ok. 80 km. Mapka z numerami nieczytelna","510 073 295"),
 ("Hubert Kowalik","Soboklęszcz, gm. Joniec","1000 i 1500 m², WZ, prąd, 100 zł/m²",""),
 ("Katarzyna PL","Gulczewo, gm. Wyszków","1000 m², uzbrojona, 120 zł/m², zdjęcie z drona (działka „1” przy lesie)","502 916 565"),
 ("Edyta Żyśkiewicz","Całowanie, gm. Karczew","„działka budowlana” – nic więcej",""),
 ("Grażyna Piasecka (polecenie)","Wilków Polski, gm. Leoncin","Poleca Janusza Jezierskiego – „miał działkę z niewielkim laskiem”","509 166 816"),
 ("Aniela Kowalik","26-910 (gm. Magnuszew)","1500 m² z domem w stanie surowym",""),
]
E = [
 ("Kamil Jonik","„Den IS” – pewnie oznaczenie kogoś",""),
 ("Aleksandra Liszewska","„priv”",""),
 ("Kazimierz Hencz","tylko telefon","663 157 543"),
 ("Janusz Borys","4402 m², 70 zł/m², 3 km do S7, 10 km do Grójca – brak miejscowości",""),
 ("Grzegorz Pazik","4 działki po 800 m² + 1 × 1300 m², woda i kanalizacja, ok. 1 h do Warszawy; „działka 4 od ulicy sprzedana”. Brak miejscowości, numery na mapce nieczytelne (~827/x)",""),
 ("Dawid Głowacki","tylko 4 zdjęcia działki, bez opisu",""),
]
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
const SKEY='dzialki-ciekawe', NKEY='dzialki-notatki', FKEY='dzialki-filtr';
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
<title>Działki z FB</title><style>
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
.bar{{display:flex;gap:16px;align-items:center;flex-wrap:wrap;color:var(--mut);font-size:14px}} .bar button{{font:inherit;color:var(--mut);background:none;border:1px solid var(--line);border-radius:6px;padding:3px 10px;cursor:pointer}}
</style></head><body><main>
<h1>Działki z komentarzy na FB</h1><p class="sub">Identyfikatory działek z ULDK (GUGiK) · komentarze pobrane z FB, ogłoszenia otwarte, zdjęcia odczytane · stan na 2026-10-05</p>
<div class="stats"><div><b>{len(A)}</b>z linkami ({nA} działek)</div><div><b>{len(AMB)}</b>niejednoznaczne</div><div><b>{len(NOULDK)}</b>numer bez potwierdzenia</div><div><b>{len(B)}</b>ogłoszenia bez numeru</div><div><b>{len(D)+len(E)}</b>do dopytania</div></div>
<div class="bar"><span>Obejrzane: <b id="cnt">0</b></span><label><input type="checkbox" id="hide"> ukryj obejrzane</label><button id="clr" type="button">wyczyść zaznaczenia</button>
<span class="sep"></span><span>★ <b id="nfav">0</b> · notatek: <b id="nnote">0</b></span>
<label>Pokaż: <select id="fsel"><option value="all">wszystkie</option><option value="fav">tylko ★</option><option value="note">z notatką</option><option value="any">★ lub notatka</option></select></label>
<input type="search" id="fq" placeholder="szukaj (miejscowość, gmina, notatka…)" aria-label="Szukaj"><span id="fres"></span></div>
<p id="fnone" hidden>Nic nie pasuje do filtra.</p>
<section><h2>A. Linki do geoportalu</h2><p class="sub">Link „Geoportal” otwiera mapę z zaznaczoną działką.</p>
<div class="tw"><table><tr><th>Autor</th><th>Lokalizacja</th><th>Działki</th><th>Szczegóły</th><th>Tel.</th><th>Źródło</th><th>Notatka</th></tr>{rows_a}</table></div>
</section>
<section><h2 class="warn">A′. Niejednoznaczne – jest numer, ale nie wiadomo, która miejscowość</h2>
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
open(os.path.join(HERE,"..","index.html"),"w").write(page)
print("ok", len(A)+len(AMB)+len(B)+len(Cimg)+len(D)+len(E))
