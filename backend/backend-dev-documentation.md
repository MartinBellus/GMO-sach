Autor: Jakub Konc

# Úvod

Toto je vývojárska dokumentácia k backendu hry GMO šach.

## Chessboard

Chessboard je jedinou triedou knižnice (mimo enumov a dátových tried), ktorá by mala byť používaná zvonka. Jej vonkajšie metódy sú opísané v [backend-user-documentation.md](backend-user-documentation.md). Stará sa o úplnú správu hry, v štandardnom móde aj sandbox móde. Medzi jej funkcie patrí:
- vkladanie figúrok na šachovnicu a ich odstraňovanie
- získavanie a vykonávanie ťahov figúrok
- správa aktuálneho stavu hry
- parsovanie DNA figúrok
- meranie času
- nahrávanie a načítavanie DNA a figúrok zo servera

### Vkladanie a odstraňovanie figúrok

Rozloženie figúrok na šachovnici sa uchováva v *dict*-e pozícia->*Piece*.

#### Piece

Piece je trieda, ktorá reprezentuje jednu figúrku. Obsahuje:
- genóm figúrky
- farbu figúrky
- či je figúrka pešiakom - teda či sa vie v poslednom rade premeniť
- či je figúrka kráľom

Mimo getterov a setterov obsahuje metódu *get_moves*, ktorá vráti všetky možné ťahy figúrky. Tá získa zoznam všetkých možných ťahov od svojho genómu a prefiltruje ich podľa svojich debuffov.

#### ChessClock

Jednoduchá trieda na udržiavanie zvyšného času hráčov. Pamätá si zostávajúci čas každého hráča, hráča ktorému práve beží čas a čas posledného updatu. Pri všetky metódy potom updatne zostávajúce časy a prípadne aj hráča na ťahu. 

Na získanie aktuálneho času používa funciu *monotonic()* z štandardnej knižnice *time*.

#### Preset

Trieda, ktorá opisuje jeden preset. Obsahuje pole hashov figúrok v presete. Tiež má stringovú reprezentáciu - hashe všetkých figúrok oddelené pomlčkami.
- Má metódu na získanie hashu celého presetu
  - Ten je prvých 6 hexadecimálnych znakov sha256 hashu stringovej reprezentácie
- Tiež má metódy na nahranie presetu na server a jeho získanie zo servera
  - Tie pomocou modulu Network stringovú reprezentáciu zašifrujú/dešifrujú a nahrajú/získajú ju zo servera
  - Získanie následne stringovú reprezentáciu rozdelí na hashe figúrok a vyrobí z nich *Preset*

#### Šifrovanie

Šifrovanie zabezpečuje, aby pri prenose DNA figúrok medzi serverom a klientom neboli voľne čitateľné na sieti.
Zároveň však z princípu hry jej kód nemôže byť čitateľný hráčmi. Taktiež má hra pomerne krátke trvanie - zopár hodín a preto nie je nutné používať veľmi silné šifrovanie. 

Rozhodol som sa použiť jednoduchý algoritmus, ktorý na šifrovanom stringu spraví prefixové sumy zmodulované 64. Následne ešte každý znak posunie o konštantu. Tento algoritmus je jednoduchý ale vďaka tomu, že kód je skrytý pomerne ťažko uhádnuteľný. Evidentne je aj jednoducho invertovateľný na dešifrovanie.

Zašifrovaný reťazec je v base64.


#### Network

Obsahuje triedu *NetworkQuery* ktorá opisuje sieťový request na adresu `SERVER_URL/<subaddress>/<file>`. Request obsiahnutý v takomto objekte sa dá poslať ako POST alebo GET.
Pri zlyhaní spojenia sa pokusy opakujú, s exponeciálne sa zvyšujúcimi rozostupmi medzi pokusmi. Ak sa ani po niekoľkých pokusoch nepodarí spojenie, hádže výnimku.


#### Genome

Hlavná trieda na prácu s genómom figúrky. Genóm figúrky sa skladá z niekoľkých spirulaterálov, teda hlavnou činnosťou tejto triedy je držanie všetkých spirulaterálov genómu. Okrem toho si pamätá aj debuffy genómu, keďže tie sa aplikujú globálne na všetky jej spirulaterály.

##### Parsing DNA

Vďaka pomerne priamočiarej a lienárnej štruktúre DNA je parsovanie pomerne jednoduché. Máme štruktúru *DnaStream*, z ktorej postupne vyberám kodóny. Na začiatku parsingu a vždy po spracovaní spirulaterálu sa pozrieme, či ešte nejaké kodóny v streame zostaly. Ak áno, začneme parsovať ďaľší spirulaterál - najprv načítame 7 kodónov oddeľovača a potom berieme pohybové kodóny až kým nenarazíme na začiatočný kodón (ďaľšieho) oddeľovača alebo DNA neskončí. 

Počas celého procesu kontrolujeme platnosť DNA a v prípade akejkoľvek nezhody hádžeme *InvalidGenomeException*.