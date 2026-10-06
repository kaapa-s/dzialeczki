import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import render
def P(id_, label):  # parcel
    return {"id": id_, "label": label}
POST="https://www.facebook.com/groups/dzialkinasprzedazmazowieckie/permalink/2198601570722806/"
# (autor, lokalizacja, działki, uwagi, tel, źródło, link)
A = [
 ("Agnieszka Piesak","Jarnice, gm. Liw (pow. węgrowski)",[P("143304_2.0003.834","834"),P("143304_2.0003.835","835")],"Dwie działki z WZ, „cena za całość razem z lasem” 320 tys. do małej negocjacji, 6 km od Węgrowa. W ewidencji 6152 + 5820 m²","","komentarz (odpowiedź)",""),
 ("Agnieszka Skowrońska","Adamów Wieś, gm. Radziejowice, ul. Brzozokalska",[P("143804_2.0002.187/6","187/6")],"6000 m² (w ewidencji 6047), 210 zł/m², media (woda, prąd, gaz, internet) w drodze gminnej, domek do remontu. Można dokupić sąsiednią działkę 1500 m²","459 118 691","komentarz + ogłoszenie","https://www.otodom.pl/pl/oferta/adamow-wies-6000m2-bezposrednio-ID4xIxn"),
 ("Ania Dudek","Prabuty, gm. Długosiodło (pow. wyszkowski)",[P("143502_2.0027.431","431")],"4014 m², 230 tys., MPZP (zabudowa do ok. 49%), w sosnowym lesie Puszczy Białej, najbliższe domy 100–200 m, dojazd gruntówką od asfaltu","","ogłoszenie","https://www.olx.pl/d/oferta/dzialka-z-mozliwoscia-zabudowy-CID3-ID1b2tcf.html"),
 ("Marcin Grubas","Piaski Duchowne, gm. Brochów (pow. sochaczewski)",[P("142802_2.0022.66/2","66/2")],"3011 m², 125 tys. (41,5 zł/m²), prąd doprowadzony, częściowo zadrzewiona, pierwsza działka od ściany lasu, otulina Kampinoskiego PN, ok. 40 min od Warszawy. ⚠ Rolna/rekreacyjna – brak info o WZ. Pinezka z ogłoszenia trafia w tę samą działkę","","komentarz + ogłoszenie","https://piaski-duchowne.nieruchomosci-online.pl/dzialka,rekreacyjna,zalesiona/26901966.html"),
 ("Marcin Manowski","Prusocin, gm. Strzegowo (pow. mławski)",[P("141305_2.0036.149/7","149/7"),P("141305_2.0036.149/10","149/10")],"3044 + 3163 m² (z ogłoszenia; 149/7 ze zrzutu geoportalu, 149/10 dopasowana po powierzchni – sąsiaduje od południa). Osobne prawomocne WZ na każdą, w otoczeniu lasów sosnowych. 67 900 zł – nie wiadomo, czy za jedną","","FB Marketplace","https://www.facebook.com/marketplace/item/1746926656439118/"),
 ("Piotr Malinowski","Wydmusy k. Myszyńca (pow. ostrołęcki)",[P("141508_5.0015.1720/3","1720/3"),P("141508_5.0015.1720/4","1720/4")],"3894 / 3900 m², leśno-rekreacyjne z możliwością zabudowy (MPZP), 65 zł/m² (253 tys. za 1720/3), prąd w drodze przy sąsiednich działkach, woda ze studni, droga gminna nieutwardzona. ⚠ Kurpie – ok. 2 h od Warszawy","","ogłoszenie","https://adresowo.pl/o/dzialka-rekreacyjna-myszyniec-wydmusy-3-894-m2-a1k5e7"),
 ("Kasia Górska Nieruchomości","Ojrzanów, gm. Żabia Wola (pow. grodziski)",[P("140506_2.0018.81/26","81/26")],"Z OCR grafiki: 1800 m² (w ewidencji 1839), prąd i światłowód w działce, 260 zł/m², 30 min od Warszawy, las od północy. Biuro Nieruchomości 360°","500 360 103","OCR zdjęcia",""),
 ("Kamil Rek","Suchowizna, gm. Stanisławów (pow. miński)",[P("141214_5.0022.158","158")],"Też w poście 1. 3258 m², 390 tys., planowany podział na 2 × 1629 m², wodociąg w działce","","ogłoszenie","https://adresowo.pl/o/dzialka-budowlana-stanislawow-suchowizna-3-258-m2-v2p0k8"),
 ("Anna Piękoś","Laskowiec, gm. Rzekuń",[P("141510_2.0009.442","442")],"Też w poście 1. 11 600 m², zadrzewiona, prąd i media w pobliżu, ok. 1,5 h od Warszawy","","komentarz",""),
 ("Mikołaj Staniaszek","Olszówka, gm. Mszczonów (między Żyrardowem a Mszczonowem)",[P("143802_5.0066.135/3","135/3")],"Też w poście 1. 1500 m² wydzielane z 135/3, media w drodze, zrobiony wjazd, niedaleko Suntago","","komentarz",""),
 ("Marcin Manowski","Grzybowo, gm. Raciąż (pow. płoński)",[P("142010_2.0015.233/"+n,"233/"+n) for n in ["2","3","4","5","6","7","8","9","10","11"]],"10 działek 1000–1391 m² (233/1 to droga wewnętrzna), bezterminowe WZ, prąd i woda w drodze asfaltowej, grunt RVI, blisko lasów sosnowych, 3 km do S7, ok. 75 km od Warszawy, 55 tys. ⚠ Za małe na kryteria postu. Numery z mapy podziału w ogłoszeniu","","FB Marketplace","https://www.facebook.com/marketplace/item/1815744756505606/"),
 ("Małgorzata Karlikowska","Ćmiszew-Parcel, gm. Rybno (pow. sochaczewski)",[P("142806_2.0005.12/12","12/12")],"12 000 m² (w ewidencji 11 984), prąd, WZ, wjazd + pozwolenie na oficjalny zjazd z drogi, okolona drzewami i starodrzewiem, można odtworzyć staw","","komentarz (nowy)",""),
 ("Paweł EM","Krze Duże, gm. Radziejowice (obręb „Krze”)",[P("143804_2.0009.67","67")],"1,36 ha (w ewidencji 13 536 m²), w tym ok. 3000 m² lasu, szer. ok. 26 m, dojazd z obu końców, 560 tys., ok. 40 km od Warszawy. ⚠ MPZP A.RP – zabudowa siedliskowa (zwykle trzeba być rolnikiem)","","ogłoszenie (nowy)","https://www.olx.pl/d/oferta/dzialka-1-36-ha-z-lasem-mpzp-a-rp-krze-duze-mozliwosc-budowy-domu-ok-40-km-od-warszawy-CID3-ID1bXPxm.html"),
]
AMB = [
 ("Damian Tolak","Pokrzywnica, gm. Pokrzywnica (pow. pułtuski)",[P("142403_2.0028.471/11","471/11 · pod pinezką")],"„Mam takie” + mapka: pas pola wcięty w las przy drodze. Pinezkę podał w odpowiedzi innej osobie – trafia w 471/11 (1068 m²), pewnie skraj tego pasa; sama działka wygląda na większą. Szczegóły na priv","","komentarz (nowy pin)",""),
 ("Henryk Anczykowski / Weronika Mikołajewska","Kąck, gm. Wiązowna (pow. otwocki)",[P("141708_2.0011.634","634 · pod pinezką")],"Ta sama oferta w dwóch komentarzach. 4150 m², prostokąt 38 × 112 m, bezterminowe WZ na 2 domy jednorodzinne lub 2 dwulokalowe (900 m² PUM), prąd i woda, 8 min do A2/S17, 1,35 mln zł. Pinezka otodom trafia w 634, ale ta ma 5725 m² – przybliżone","664 090 447","komentarz + ogłoszenie (nowy)","https://www.otodom.pl/pl/oferta/dzialka-w-atrakcyjnej-lokalizacji-4150-m2wz-na-2-domy8-min-do-a2-s17-ID4D1EN"),
 ("Jarosław Kda","Cisse, gm. Szczutowo (pow. sierpecki)",[P("142706_2.0006.5/2","5/2 · z kursora na zrzucie")],"„Działki zalesione”, WZ, ponad 3000 m², 80 tys., prąd i woda w działce, OChK doliny Skrwy, przy Jeziorach Szczutowskich. Współrzędne z paska zrzutu geoportalu (pozycja kursora) trafiają w 5/2 (2915 m²) w obrębie Cisse – zgadza się z miejscowością, ale konkretny numer niepewny. ⚠ ok. 90 min+","504 004 440","OCR zdjęcia",""),
 ("Bartek Bednarczyk","Bujały-Gniewosze, gm. Jabłonna Lacka (pow. sokołowski)",[P("142904_2.0001.167/1","167/1 · pod pinezką")],"Z ogłoszenia: 3600 m² z własnym lasem, WZ na 2 domki rekreacyjne do 70 m² (zabudowa na ok. 1700 m²), obok staw strażacki, 250 tys., 1,5 h od Warszawy, pozwolenie na 2 domki. Pinezka z Google Maps trafia w 167/1, ale ta ma tylko ok. 1880 m² – możliwe, że działek jest więcej","","komentarz + ogłoszenie","https://www.olx.pl/d/oferta/sliczna-dzialka-z-lasem-wz-na-dwa-domki-spokojne-i-ciche-otoczenie-CID3-ID1coZxB.html"),
]
NOULDK = []
B = [
 ("Magdalena Wielgos","Olszynki, gm. Młodzieszyn (pow. sochaczewski)","1,81 ha w środku lasu (starodrzew, 100-letni dąb, kapliczka w narożniku), WZ na dom, 506 800 zł (28 zł/m²), OChK + Natura 2000, ok. 1 h od Warszawy. Numeru brak (FB Marketplace)","https://www.facebook.com/marketplace/item/1801322590841544/"),
 ("Patrycja Ilasz-Kłoda","Strzyżyna, gm. Grabów n. Pilicą (pow. kozienicki)","1715 m², działka leśna z pozwoleniem na budowę, prąd podłączony, wodociąg w drodze, asfalt, skraj Puszczy Stromieckiej. Pinezka otodom trafia w wielki kompleks 345/2 – bezużyteczna","https://www.otodom.pl/pl/oferta/piekna-dzialka-lesna-z-pnb-i-mediami-1h-jazdy-z-warszawy-ID4CCNV"),
]
D = [
 ("Agnieszka Radzio Romańczuk","Pogorzelec, gm. Łochów","Blisko rzeka Liwiec","798 566 004"),
 ("Małgorzata Wieczorek","Ludwików, gm. Jedlińsk","Działki ok. 12 ar i 16 ar (?), sąsiadują z lasem, w pobliżu rzeka Radomka. Zdjęcie: pole przy ścianie lasu",""),
 ("Paulina Konopacka","Wola Starogrodzka, gm. Parysów","5600 m², rolno-budowlana",""),
 ("Agnieszka Lewandowska","Gilówka Górna, gm. Iłów (pow. sochaczewski)","5700 m², uzbrojona (prąd, woda), z pozwoleniem na budowę domu",""),
 ("Anna Malinowska","gm. Sierpc, nad rzeką Skrwą","0,7 ha bezpośrednio nad rzeką, WZ, prąd doprowadzony, blisko DK10, ok. 120 km od Warszawy – reszta na priv",""),
 ("Justyna Erkan","Pieczyska (łowickie?)","Tylko nazwa + zdjęcie lasu",""),
]
E = [
 ("Maksymilian Gerej","3068 m², 50 min od Warszawy w stronę Białegostoku, zdjęcie łąki przy lesie – reszta na priv",""),
 ("Andrzej Dymowski","Zrzut ogłoszenia z otodom (łąka przy lesie) – na priv",""),
 ("Agnieszka Dmowska","Tylko zdjęcie: pole przy asfalcie, ściana lasu",""),
 ("Piotr Mikulski","„Spełnia warunki, media w działce” – na priv",""),
 ("Bartek Nowogrodzki","„Napisałem wiadomość prywatną”",""),
 ("Beata Krystyna","„Priv”",""),
]
render("post2.html", A=A, AMB=AMB, NOULDK=NOULDK, B=B, D=D, E=E,
       title="Działki z FB – post 2", h1="Działki z komentarzy – post 2 (nie mój)",
       sub=f'Post: <a href="{POST}" target="_blank">„Szukam działki od 3000 m², max 1,5 h od Warszawy, odgrodzona lasem z trzech stron”</a> (Krzysztof Borkowski, grupa „Działki na sprzedaż mazowieckie”) · większość autorów odsyła na priv – numery wyciągnięte z ogłoszeń, mapek i pinezek · identyfikatory z ULDK · stan na 2026-10-06',
       amb_title="A′. Z pinezki / współrzędnych – przybliżone",
       amb_sub="Numer ustalony z pinezki albo współrzędnych na zrzucie – działka pod punktem, niekoniecznie ta sprzedawana. Sprawdź na geoportalu sąsiednie.",
       amb_stat="z pinezki (przybliżone)")
