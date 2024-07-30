#### Formát:

Bloky tvaru _oddeľovač spirulaterál_ popisujúce ťahy, ktoré vie figúrka vykonať.
    - môže ich byť ľubovoľne veľa po sebe opakovaných
    - biele znaky sa ignorujú
    - hráč vie pri ťahu použiť ľubovoľný z blokov(ale nemôže ich kombinovať)
    - ak sa na dané políčko dá dostať viacerými spirulaterálmi, použije sa ten z nich, ktorý je v DNA ako prvý

DNA sa skladá len zo znakov SACH
DNA sa delí na trojice znakov(kodóny)

### Oddeľovač:

popisuje vlastnosti nasledujúceho spirulaterálu

Tvar **ST¹T²O¹O²O³Z**

S="AHH" a Z="HHA" sú fixné - indikujú začiatok a koniec oddeľovača

T¹, T² - ktorej farby budú figúrky na pôvodnom a novom políčku
    - buď nepriateľský kodón (HSH), alebo debuff kodón pre vlastné figúrky -- aby sme potresatli kopírovanie vlastných figúrok

O¹, O², O³ - ktorá figúrka bude po ťahu na pôvodnom a novom políčku, ak sa pohnem na políčko s mojou figúrkou(O¹), nepriateľovou(O²) alebo prázdne(O³)
    - HHH - ťah nepovolený
    - alebo tvar xHy
        - x označuje figúrku na políčku z ktorého sa pohybujem
        - y je figúrka na cieľovom políčku
        - x, y môžu byť A, S, C
            - A - figúrka z pôvodného políčka - tá, ktorá sa pohybuje
            - S - figúrka z cieľového políčka
            - C - políčko bude prázdne

## Debuffy

HAS - spirulateral sa vykoná len dopredu
HAC - spirulateral sa vykoná len raz
HAA - nedá sa teleportovať medzi bočnými hranami (defaultne vedia figúrky prechádzať cez ľavý/pravý okraj)
HCA - ofarbiť sa dá len políčko opačnej farby, na akej figúrka stojí
HCS - ofarbiť sa dá len políčko rovnakej farby, na akej figúrka stojí
HSS - ofarbiť políčko s figúrkou sa dá len ak s ňou susedí
HSC - keď sa touto figúrkou hýbe, hra zamrzne na 5s
HCC - figúrke po pohybe náhodne zmutuje genóm
HSA - figúrka sa pohne na náhodné políčko susediace s tým, kam hráč klikne


Debuffy sa nemôžu opakovať globálne v celej DNA figúrky
Tiež platia globálne aj pre ostatné bloky


### Spirulaterál: 

Skladá sa z viacerých (maximálne 4) kodónov, z ktorých každý opisuje pohyb figúrky v jednom smere
Figúrka sa posunie dopredu podľa prvého kodónu, otočí sa o 90° v ľubovoľnom smere, posunie sa podľa druhého kodónu, opäť sa otočí v rovnakom smere... a takto ďalej až po posledný kodón, odkiaľ sa opäť pokračuje prvým
Tento proces sa opakuje dovtedy, kým figúrka neofarbí políčko s figúrkou alebo opustí hraciu plochu
Začiatočný smer figuľky je ľubovoľný

Prvé písmeno: určuje či je ťah ofarbovací alebo nie - či sa dá na políčko, kde po tomto pohybe figúrka stojí, pohnúť
A - krok je nulový a neofarbovací bez ohľadu na zvyšok kodónu
S - ofarbovacie
C - neofarbovacie

Zvyšné dve: vzdialenosť, o koľko sa figúrka pohne - číslo v ternárnej sústave, moduluje sa piatimi(neofarbovacie) alebo troma(ofarbovacie)
A - 0
S - 1
C - 2

# Veža:
AHH HSH HAA CHA CHA CHA HHA SAS AAA AAA AAA

Vysvetlenie:
    - AHH - začiatok oddeľovača
        - HSH - figúrku na pôvodnom políčku bude vlastniť protihráč - nepodstatné keďže tam žiadna nebude
        - HAA - figúrka na cieľovom políčku bude moja - figúrka sa nevie teleportovať medzi bočnými hranami
        - CHA - po pohybe na políčko s vlastnou figúrkou bude pôvodné políčko prázdne (C) a cieľové políčko bude obsadené mojou figúrkou (A)
        - CHA - po pohybe na políčko s protihráčovou figúrkou bude pôvodné políčko prázdne (C) a cieľové políčko bude obsadené mojou figúrkou (A)
        - CHA - po pohybe na prázdne políčko bude pôvodné políčko prázdne (C) a cieľové políčko bude obsadené mojou figúrkou (A)
    - HHA - koniec oddeľovača
    - SAS - figúrka sa pohne dopredu o jedno políčko
    - 3x AAA ostatnými smermi sa nehýbe

# Pešiak:
AHH HAC HAS HHH HHH CHA HHA SAS
AHH HSH HAA HHH CHA HHH HHA CAS SAS

# Strelec:
AHH HCS HAA HHH CHA CHA HHA CAS SAS ASS ACS

# Kráľ:
AHH HAC HAA HHH CHA CHA HHA SAS SAS ACS AAC

# Kôň:
AHH HAA HAC HHH CHA CHA HHA CAC SAS AAC ACA

# Kráľovná:
AHH HSH HAA HHH CHA CHA HHA CAS SAS ASS ACS
AHH HSH HSC CHA CHA CHA HHA SAS AAA AAA AAA

(Tu sa minuli debuffy takže pri pohybe aj zmrazuje hru)
