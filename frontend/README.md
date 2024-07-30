Autor: Martin Belluš

# Úvod

Toto je užívateľská dokumentácia k frontendu hry GMO šach. GMO šach je šachová
hra, v ktorej sa ale hrá so špeciálnymi figúrkami, ktorých vlastnosti sú dané
ich genómom.

Pre užívateľov sú pripravené 2 aplikácie, v ktorých sa táto hra odohráva:

## Lab

Lab je aplikácia, v ktorej sa dá experimentovať s genómamy, ukladať si ich na
server a vytvárať úvodné rozloženia figúrok do reálnej hry. Lab obsahuje
testovaciu šachovnicu, editor genómov a menu na ukladanie a načítavanie
genómov.

## Hra

Hra je aplikácia, v ktorej sa hrajú reálne hry. Na začiatku si hráči načítajú
dopredu vytvorené rozloženia figúrok a potom začnú hrať šach. Hra obsahuje hernú
šachovnicu, menu na načítavanie rozloženia figúrok a šachové hodiny.

# Prerekvizity

Na spustenie aplikácie je potrebná verzia pythonu 3.9 alebo vyššia.

Všetky potrebné knižnice sú vypísané v súbore `requirements.txt`. Na ich
stiahnutie stačí zavolať príkaz `pip install -r requirements.txt`.

Na spustenie hry sú taktiež potrebné obrázky pre figúrky. Tieto obrázky sa
nachádzajú v priečinku `images`. Všetky obrázky sú vo formáte `png` s alfa
kanálom. Ak je obrázkov príliš málo, môže sa stať, že rôzne figúrky budú v hre
vyzerať rovnako.

Navyše je potrebné, aby v priečinku `images/special` boli 2 obrázky s názvami
`king.png` a `freeeze.png`, ktoré budú použité na označenie kráľa a efekt
zmrazenia obrazovky.

# Figúrky

Každá figúrka má svoj genóm, ktorého formát je na začiatku hry tajný a hráči sa
ho pokúšajú zistiť prostredníctvom experimentovania v labe.

Na jednoduchšie prenášanie figúrok medzi počítačmi sa používa takzvaný *kód*
figúrky. Tento kód je spravidla 6-miestny reťazec alfanumerických znakov.
Rozloženia figúrok majú podobný kód.

# Ovládanie a spúšťanie

Pred spustením aplikácie je potrebné aby bežal server na adrese zadefinovanej v
súbore `utility/constants.py` ako `HTTP_URL`. Server sa nachádza v priečinku
`server` a jeho funguvanie je popísané v súbore
`server/server-documentation.md`.

## Lab

Na spustenie labu stačí spustiť súbor `lab.py`. Po spustení sa zobrazí okno
s editorom a testovacou šachovnicou.

### Ovládanie

Na pravej strane Labu sa nachádza editor genómov. Toto je textový editor, v
ktorom sa dá upravovať genóm. Na spodku sa nachádzajú tlačitka na položenie
figúrky na testovaciu šachovnicu a načítanie genómu zo súboru.

Na ukladanie a načítavanie figúrok a rozložení figúrok slúži menu v hornej
časti okna. Nachádzajú sa v ňom nasledujúce tlačidlá:

- `Reset` - vymaže všetky figúrky z testovacej šachovnice
- `Place White Preset` - načíta prednastavené rozloženie figúrok podľa jeho kódu a položí ho na stranu bieleho hráča na šachovnici
- `Place Black Preset` - rovnako ako `Place White Preset`, ale položí figúrky na stranu čierneho hráča
- `Save Piece` - uloží obsah editora do súboru
- `Save Preset` - uloží na server rozloženie figúrok na prvom alebo poslednom riadku šachovnice a zobrazí dialógové okno s jeho kódom
- `Fetch Piece` - načíta figúrku zo servera podľa jej kódu a vloží jej genóm do editora
- `Help` - zobrazí nápovedu

Figúrky na šachovnici sa ovládajú myšou. Ľavým kliknutím na figúrku sa
zvýraznia políčka, na ktoré táto figúrka dokáže stúpiť. Ľavým kliknutím na
jedno z týchto políčok sa figúrka presunie na toto políčko. Pravým kliknutím na
figúrku sa zobrazia informácie o nej, hlavne jej kód.

## Hra

Na spustenie hry stačí spustiť súbor `game.py`. Po spustení sa zobrazí okno so
šachovnicou a šachovými hodinami.

Na spustenie hry je najprv potrebné, aby hráči načítali začiatočné rozloženie
figúrok pomocou tlačítok `Place White Preset` a `Place Black Preset` v menu. Po
načítaní si každý z hráčov pravým kliknutím vyberie figúrku, ktorá bude jeho
kráľ. Po tomto kroku sa môže spustiť hra tlačítkom `Start Game`.

Na pravej strane sa nachádzajú šachové hodiny. Po stlačení tlačítka `Start
Game` sa spustia a začne sa odpočítavať čas aktívneho hráča. Hodiny aktívneho
hráča sú vždy zvýraznené. Po uplynutí času alebo vyhodení jedného z jeho kráľov
hráč prehráva.

### Ovládanie

Figúrky na šachovnici sa ovládajú rovnako ako v Labe. Ľavým kliknutím sa
zvýraznia políčka, na ktoré dokáže figúrka stúpiť a ďalším ľavím kliknutím sa
figúrka presunie na toto políčko. Pravým kliknutím na protivníkovu figúrku sa
zobrazia políčka, na ktoré sa táto figúrka dokáže pohnúť.
