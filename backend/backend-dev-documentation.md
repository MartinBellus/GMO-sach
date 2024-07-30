Autor: Jakub Konc

# Úvod

Toto je vývojárska dokumentácia k backendu hry GMO šach.

### Chessboard

Chessboard je jedinou triedou knižnice (mimo enumov a dátových tried), ktorá by mala byť používaná zvonka. Jej vonkajšie metódy sú opísané v [backend-user-documentation.md](backend-user-documentation.md). Stará sa o úplnú správu hry, v štandardnom móde aj sandbox móde. Medzi jej funkcie patrí:
- vkladanie figúrok na šachovnicu a ich odstraňovanie
- získavanie a vykonávanie ťahov figúrok
- správa aktuálneho stavu hry
- meranie času

Rozloženie figúrok na šachovnici sa uchováva v *dict*-e pozícia->*Piece*.
Okrem toho šachovnica vlastní:
- objekt *ChessClock* na meranie času
- zoznam pešiakov, ktorí sa môžu premeniť
- aktuálny stav hry
- zoznam platných *MoveDescriptorov*

#### Vkladanie a odstraňovanie figúrok

Na odstránenie figúrky stačí jednoducho zmazať príslušný záznam z *dict*-u.
Na vloženie figúrky musíme získať jej DNA - buď ju máme zadanú alebo ju načítať zo servera podľa hashu (viď. sekcia Network). Následne toto DNA sparsujeme a vytvoríme z neho *Genome*. Ten použijeme na vytvorenie *Piece*, ktoré vložíme do *dict*-u.

Okrem toho je vkladanie figúrok možné aj pomocou presetov. Po jeho načítaní zo servera a sparsovaní sa zadné dve rady šachovnice správne zaplnia - v poslednej rade budú figúrky z presetu a v predposlednej pešiaci.

#### Získavanie a vykonávanie ťahov figúrok

Na získanie možných ťahov figúrky si vyberieme jej *Piece* z mapy a genómu sa spýtame na zoznam *MoveDescriptor*-ov.

Pri vykonávaní ťahu treba urobiť viacej vecí:
- Spracovať niektoré debuffy (mutácia, náhodný pohyb, freeze)
- Poposúvať figúrky
- Prepnúť aktuálneho hráča na časovači
- Skontrolovať či sa niekomu neznížil počet kráľov
  - To spravíme jednoducho tak, že spočítame kráľov pred a po posunutí figúrok
  - Ak áno, hra končí

Okrem toho je ešte niekedy potrebné premeniť pešiaka - ale to je zhodné s odstránením tohoto pešiaka a vložením novej figúrky. Tu je treba si dávať pozor, aby bežal čas hráčovi, ktorého pešiak sa má zmeniť.

#### Správa stavu hry

Stav hry sa mení jedine pri jej spustení a po jej konci - teda len v rámci ťahu.

#### Meranie času

Meranie času prebieha pomocou objektu *ChessClock*.

### Piece

Piece je trieda, ktorá reprezentuje jednu figúrku. Obsahuje:
- genóm figúrky
- farbu figúrky
- či je figúrka pešiakom - teda či sa vie v poslednom rade premeniť
- či je figúrka kráľom

Mimo getterov a setterov obsahuje metódu *get_moves*, ktorá vráti všetky možné ťahy figúrky. Tá získa zoznam všetkých možných ťahov od svojho genómu a prefiltruje ich podľa svojich debuffov.

### ChessClock

Jednoduchá trieda na udržiavanie zvyšného času hráčov. Pamätá si zostávajúci čas každého hráča, hráča ktorému práve beží čas a čas posledného updatu. Pri všetky metódy potom updatne zostávajúce časy a prípadne aj hráča na ťahu. 

Na získanie aktuálneho času používa funciu *monotonic()* z štandardnej knižnice *time*.

### Preset

Trieda, ktorá opisuje jeden preset. Obsahuje pole hashov figúrok v presete. Tiež má stringovú reprezentáciu - hashe všetkých figúrok oddelené pomlčkami.
- Má metódu na získanie hashu celého presetu
  - Ten je prvých 6 hexadecimálnych znakov sha256 hashu stringovej reprezentácie
- Tiež má metódy na nahranie presetu na server a jeho získanie zo servera
  - Tie pomocou modulu Network stringovú reprezentáciu zašifrujú/dešifrujú a nahrajú/získajú ju zo servera
  - Získanie následne stringovú reprezentáciu rozdelí na hashe figúrok a vyrobí z nich *Preset*

### Network

Vždy po vytvorení nového genómu alebo presetu prebieha jeho upload na server. Genóm/Preset sa zahashuje a jeho zašifrovaná reprezentácia sa nahrá na server pod kľúčom tohoto hashu. Pri fetchovaní podľa hashu sa hash použije ako kľúč, dáta pod týmto kľúčom si vypýtame od servera a dešifrujeme ich.

Upload má formu **POST** requestu na `SERVER_URL/genome/<hash>`, resp. `SERVER_URL/preset/<hash>`.

Fetchuje sa **GET** requestom na rovnaké adresy.

#### Šifrovanie

Šifrovanie zabezpečuje, aby pri prenose DNA figúrok medzi serverom a klientom neboli voľne čitateľné na sieti.
Zároveň však z princípu hry jej kód nemôže byť čitateľný hráčmi. Taktiež má hra pomerne krátke trvanie - zopár hodín a preto nie je nutné používať veľmi silné šifrovanie. 

Rozhodol som sa použiť jednoduchý algoritmus, ktorý na šifrovanom stringu spraví prefixové sumy zmodulované 64. Následne ešte každý znak posunie o konštantu. Tento algoritmus je jednoduchý ale vďaka tomu, že kód je skrytý pomerne ťažko uhádnuteľný. Evidentne je aj jednoducho invertovateľný na dešifrovanie.

Zašifrovaný reťazec je v base64.

#### NetworkQuery

Trieda *NetworkQuery* opisuje sieťový request na adresu `SERVER_URL/<subaddress>/<file>`. Request obsiahnutý v takomto objekte sa dá poslať ako POST alebo GET.
Pri zlyhaní spojenia sa pokusy opakujú, s exponeciálne sa zvyšujúcimi rozostupmi medzi pokusmi. Ak sa ani po niekoľkých pokusoch nepodarí spojenie, hádže výnimku.

### Genome

Hlavná trieda na prácu s genómom figúrky. Genóm figúrky sa skladá z niekoľkých spirulaterálov, teda hlavnou činnosťou tejto triedy je držanie všetkých spirulaterálov genómu. Okrem toho si pamätá aj debuffy genómu, keďže tie sa aplikujú globálne na všetky jej spirulaterály.

##### Parsing DNA

Vďaka pomerne priamočiarej a lienárnej štruktúre DNA je parsovanie pomerne jednoduché. Máme štruktúru *DnaStream*, z ktorej postupne vyberám kodóny. Na začiatku parsingu a vždy po spracovaní spirulaterálu sa pozrieme, či ešte nejaké kodóny v streame zostaly. Ak áno, začneme parsovať ďaľší spirulaterál - najprv načítame 7 kodónov oddeľovača a potom berieme pohybové kodóny až kým nenarazíme na začiatočný kodón (ďaľšieho) oddeľovača alebo DNA neskončí. 

Počas celého procesu kontrolujeme platnosť DNA a v prípade akejkoľvek nezhody hádžeme *InvalidGenomeException*.

##### Generovanie ťahov

Druhou zaujímavou funkciou genómu je generovanie možných ťahov. Toto prebieha pre každý spirulaterál samostatne - jediný zdieľaný stav sú debuffy. Presne podľa špecifikácie, každý spirulaterál vo všetkých ôsmich kombinácia začiatočného smeru a smeru otáčania vygeneruje možné pohyby. V každej takejto možnosti postupne simuluje pohyby a pre tie, ktoré sú ofarbovacie generuje *MoveDescriptor*y. Tento proces sa končí keď;
- Pri ofarbovacom ťahu narazíme na políčko, kde už stojí figúrka
- Dostaneme sa mimo šachovnicu
- Zacyklíme sa - dostaneme sa na políčko, kde sme už boli, v rovnakom smere aj fáze pohybu

Počas toho ešte musíme dávať pozor na debuffy - niektoré, ako napríklad *NO_TELEPORTING_BETWEEN_SIDES* musíme spracovávať už počas generovania ťahov, a iné, napríklad tie obmedzujúce farby políčok na ktoré sa vieme hýbať na konci funkcie prefiltrujeme.

#### Hash

Podobne ako *Preset*, aj *Genome* má hash na jednoduchšie presúvanie medzi počítačmi. Je to prvých 6 znakov sha256 hashu DNA.