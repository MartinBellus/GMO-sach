Autor: Martin Belluš

# Úvod

Toto je užívateľská dokumentácia k frontendu hry GMO šach.

Aplikácia obsahuje dve hlavné časti.

## Editor genómov (Lab)

Lab je priestor, v ktorom sa dá experimentovať s genómami, ukladať si ich na
server a vytvárať úvodné rozloženia figúrok do reálnej hry. Lab obsahuje
testovaciu šachovnicu, editor genómov a menu na ukladanie a načítavanie
genómov.

## Hra

V tomto priestore sa hrajú reálne hry. Na začiatku si hráči načítajú dopredu
vytvorené rozloženia figúrok a potom začnú hrať šach. Hra obsahuje hernú
šachovnicu, menu na načítavanie rozloženia figúrok a šachové hodiny.

# Prerekvizity

Všetky potrebné knižnice sú napísané v súbore `requirements.txt`. Na ich
stiahnutie stačí zavolať príkaz `pip install -r requirements.txt`.

Obrázky pre figúrky sa nachádzajú v priečinku `images`. Všetky obrázky sú vo formáte `png` s alfa kanálom.

Na spustenie hry je potrebné, aby v priečinku `images/special` boli 2 obrázky s
názvami `king.png` a `freeeze.png`, ktoré budú použité na označenie kráľa a
zmrazenie obrazovky.

# Ovládanie a spúšťanie

Pred spustením aplikácie je potrebné aby bežal server na adrese zadefinovanej v
súbore `utility/constants.py` ako `HTTP_URL`.

## Editor genómov

Na spustenie editora stačí spustiť súbor `lab.py`. Po spustení sa zobrazí okno s editorom a testovacou šachovnicou.

### Ovládanie

Na pravej strane Labu sa nachádza editor genómov. Toto je textový editor, v ktorom sa dá upravovať genóm. Na spodku sa nachádzajú tlačitka na položenie figúrky na testovaciu šachovnicu a načítanie genómu zo súbora.

Na ukladanie a načítavanie figúrok a rozložení figúrok slúži menu v hornej časti okna. Nachádza sa v ňom zopár tlačitok.

- `Reset` - vymaže všetky figúrky z testovacej šachovnice
- `Place White Preset` - načíta prednastavené rozloženie figúrok podľa kódu alebo podľa kódu 8 figúrok v rozložení a položi ho na stranu bieleho hráča na šachovnici
- `Place Black Preset` - rovnako ako `Place White Preset`, ale položí figúrky na stranu čierneho hráča
- `Save Piece` - uloží obsah editora do súboru
- `Save Preset` - uloží na server rozloženie figúrok na prvom alebo poslednom riadku šachovnice a vráti jeho kód
- `Fetch Piece` - načíta genóm zo servera podľa kódu a vloží ho do editora
- `Help` - zobrazí nápovedu

Figúrky na šachovnici sa ovládajú myšou. Ľavým kliknutím na figúrku sa zvýraznia políčka, na ktoré táto figúrka dokáže stúpiť. Ľavým kliknutím na jedno z týchto políčok sa figúrka presunie na toto políčko. Pravým kliknutím na figúrku sa zobrazia informácie o nej, hlavne jej kód.

## Hra

Na spustenie hry stačí spustiť súbor `game.py`. Po spustení sa zobrazí okno so šachovnicou a šachovými hodinami.

Na spustenie hry je najprv potrebné, aby hráči načítali začiatočné rozloźenie figúrok pomocou tlačítok v menu. Po načítaní si každý z hráčov pravým kliknutím vyberie figúrku, ktorá bude jeho kráľ. Po tomto kroku sa môže spustiť hra tlačítkom `Start Game`.

Na pravej strane sa nachádzajú šachové hodiny. Po stlačení tlačítka `Start Game` sa spustia a začne sa odpočítavať čas aktívneho hráča. Hodiny aktívneho hráča sú vždy zvýraznené. Po uplynutí času hráč prehráva.

### Ovládanie

Figúrky na šachovnici sa ovládajú rovnako ako v Labe. Ľavým kliknutím sa zvýraznia políčka, na ktoré dokáže figúrka stúpiť a ďalším ľavím kliknutím sa figúrka presunie na toto políčko. Pravým kliknutím na protivníkovu figúrku sa zobrazia políčka, na ktoré sa táto figúrka dokáže pohnúť.
