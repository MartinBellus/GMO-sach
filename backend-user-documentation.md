Autor: Jakub Konc

## Úvod

Toto je dokumentácia k API backendu hry GMO šach. 

GMO šach sa podobá na štandardný šach, avšak každá figúrka má priradený reťazec (DNA), ktorý určuje jej ťahy. Štruktúra DNA je popísaná [tu](genome_format.md).

Hra sa hrá na 8x8 šachovnici. Do zadnej rady si hráč môže dať ľubovoľné figúrky (samozrejme musí poznať ich DNA). Figúrky sa môžu opakovať, kľudne môže byť všetkých 8 rovnakých. Avšak celý zadný rad musí byť naplnený.

V predposlednom rade sa nachádza 8 pešiakov - figúrok ktoré sa vedia hýbať o jedno políčko dopredu a vyhadzujú diagonálne. Okrem toho keď sa pešiak dostane do poslednej rady šachovnice, zmení sa na ľubovoľnú figúrku.

Pred začiatkom hry si každý z hráčov označí aspoň jednu zo svojich figúrok za kráľa.

Ťahy hráčov sa striedajú, začínajúc bielym. Každý hráč má na svoje ťahy dokopy maximálne 5 minút, hráč, ktorému sa minie čas prehráva.

Počas každého ťahu hráč pohne jednou figúrkou, pričom:
- Možné ťahy každej figúrky sú špecifikované jej DNA
- Hráč nevidí DNA protihráčových figúrok, avšak vie si prezrieť ich aktuálne možné ťahy
- GMO šach narozdiel od štandardného šachu nemá rošádu, prvý pohyb pešiaka o 2 políčka, En passant
- Ľavá a pravá hrana šachovnice sú prepojené -- teda po pohybe o jedno políčko doľava z ľavej hrany skončí figúrka na pravej

Hra sa končí buď keď jednému z hráčov vyprší čas, alebo keď je zahraný ťah, ktorým sa aspoň jednému z hráčov zníži počet kráľov. Ak sa znížil počet kráľov obom hráčom, hra končí remízou, inak ten kto prišiel o kráľa prehráva.

## Použitie

API má primárne formu volania metód inštancie triedy *backend.chessboard.Chessboard*. Tá môže existovať v dvoch režimoch:
    - štandardnom, použitom pri hrách
    - sandbox móde, ktorý je použitý pri skúšaní genómov v labe
      - neplatia v ňom všetky pravidlá hry, dajú sa do neho ľubovoľne vkladať a mazať figúrky na vyskúšanie pohybov
      - nemá časovač a hra nekončí - proste prostredie na skúšanie

**Na správne fungovanie musí byť spustený server.**

## Čo je preset a genome/preset hash?

Na zjednodušenie prenášania DNA figúrok medzi počítačmi má každý genóm hash - 6 znakový reťazec tvorený číslicami a malými písmenami anglickej abecedy. Tento kód sa vždy pri vytvorení novej figúrky uloží na server a následne sa figúrka dá pokladať pomocou neho.

Preset podobne umožňuje pomocou jedného kódu uložiť celý zadný rad figúrok. Tento kód má rovnaký formát.

### backend.chessboard.Chessboard

- *__init__(sandbox=False)*
    - Vytvorí nový objekt triedy *backend.Chessboard*
    - *sandbox* - *bool*, určuje, či je šachovnica v sandbox móde

- *insert_piece(genome_hash, color, position, is_pawn=False, is_king=False) -> None*
    - Vloží novú figúrku na šachovnicu
    - Ak je políčko obsadené, prepíše ho
    - **Dostupné len v sandbox móde**
    - **Ak figúrka s daným hashom na serveri neexistuje, hádže RemoteFileNotFound**
    - *genome_hash* - *str*, hash DNA figúrky
    - *color* - *Colors*(enum), farba figúrky
    - *position* - *Vector*, políčko na šachovnci, kde sa má figúrka nachádzať
    - *is_pawn* - *bool*, určuje, či je figúrka pešiak - či sa vie v poslednom rade premeniť
    - *is_king* - *bool*, určuje, či je figúrka kráľ

- *insert_piece_by_dna(dna, color, position, is_pawn=False, is_king=False) -> None*
    - Rovnaké ako insert_piece, ale namiesto hashu DNA sa používa priamo DNA
    - **Dostupné len v sandbox móde**
    - **V prípade neplatného genómu hádže InvalidGenomeException**

- *erase_piece(position) -> None*
    - Odstráni figúrku z danej pozície
    - Ak je políčko prázdne, raisuje *IndexError*
    - **Dostupné len v sandbox móde**
    - *position* - *Vector*, políčko na šachovnci, kde sa figúrka nachádza

- *toggle_king(position) -> None*
    - Zmení, či má figúrka na danej pozícií status kráľa
    - Ak je políčko prázdne, raisuje *IndexError*
    - **Mimo sandboxu može byť volané len pred začiatkom hry**
    - *position* - *Vector*, políčko na šachovnci, kde sa figúrka nachádza

- *get_moves(position, allow_getting_opponents_moves=False) -> list[MoveDescriptor]*
    - Vráti všetky možné ťahy figúrky na danej pozícií
      - Ak je políčko prázdne, vráti prázdne pole
      - Ak figúrka na danom políčku patrí hráčovi, ktorý nie je na ťahu
        - Ak *allow_getting_opponents_moves* je *False*, vráti prázdne pole
        - Ak *allow_getting_opponents_moves* je *True*, vráti všetky možné ťahy figúrky

    - *position* - Vector, políčko na šachovnci, kde sa figúrka nachádza
    - return - zoznam objektov *MoveDescriptor* popisujúcich možné ťahy

- *start_game() -> None*
    - Začne hru
    - Môže byť volané len raz
    - V sandboxe nemá efekt

- *do_move(move_descriptor) -> GameStatus*
    - Vykoná ťah
    - *move_descriptor* - *MoveDescriptor*, ťah, ktorý sa má vykonať
        - musí byť jedným z descriptorov vrátených *get_moves* v aktuálnom kole
    - **Nesmie existovať pešiak, ktorý sa môže premeniť**
        - Pred volaním je vhodné zavolať *get_promotion* a prípadne *promote*

    
    - return - *GameStatus*, stav hry po ťahu

- *get_promotion() -> (Vector, Colors)|None*
  - Získa pešiaka, ktorý sa má premeniť
  - **Pravidlá hry nevylučujú možnosť, že tento pešiak nepatrí hráčovi na ťahu**
  - return - pozícia a farba pešiaka na premenenie alebo *None* ak taký pešiak neexistuje

- *promote(position, dna_hash) -> None*
  - Premení pešiaka na danej pozícií na figúrku s daným genomom
  - **Ak figúrka s daným hashom na serveri neexistuje, hádže RemoteFileNotFound a zlyhá**
  - *position* - *Vector*, políčko na šachovnci, kde sa pešiak nachádza
  - *dna_hash* - *str*, hash DNA figúrky

- *is_frozen() -> bool*
  - Vráti, či posledný ťah zmrazil hru
  - return - *bool*

- *get_remaining_time(color) -> float*
  - Vráti zostávajúci čas daného hráča
  - *color* - *Colors*, farba hráča
  - return - zostávajúci čas v sekundách

- *get_status() -> GameStatus*
  - Vráti aktuálny stav hry
  - return - *GameStatus*

- *load_preset(preset_hash, color) -> None*
  - Použije preset figúriek
    - Do posledného radu šachovnice z pohľadu danej farby sa umiestnia figúrky z presetu
    - Predposledný rad zaplnia pešiaci
  - **Môže byť volané len pred začiatkom hry a iba raz pre každú farbu**
  - **Ak preset s daným hashom na serveri neexistuje, hádže RemoteFileNotFound**
  - *preset_hash* - *str*, hash presetu
  - *color* - *Colors*, hráč, ktorý používa daný preset
  
- *save_preset(color) -> str|None*
  - Uloží zadný rad figúrok danej farby ako preset
  - *color* - *Colors*, farba, ktorej figúrky sa majú uložiť
  - return - *str*, hash presetu alebo *None* ak daný hráč nemá plný zadný rad

- *get_board_for_reading() -> [[PieceInfo | None]]*
  - Vráti obsah šachovnice
  - return - 2D pole veľkosti šachovnice, kde každý prvok je buď *None* alebo *PieceInfo*

- *get_current_player() -> Colors*
  - Vráti farbu hráča na ťahu
  - return - *Colors*, farba hráča na ťahu
  

### utility.enums.Colors

Enum reprezentujúci farby figúrok:
- *WHITE*
- *BLACK*

### utility.enums.GameStatus

Enum obsahujúci možné stavy hry:
- *BLACK_WON* - hra skončila, čierny vyhral
- *WHITE_WON* - hra skončila, biely vyhral
- *DRAW* - hra skončila remízou
- *IN_PROGRESS* - hra prebieha
- *NOT_STARTED* - hra ešte nezačala
- *LAB* - hra je v sandbox móde

### backend.chessboard.PieceInfo

Dátová trieda obsahjúca informácie o figúrke:
- *genome_hash* - *str*, hash DNA figúrky
- *color* - *Colors*, farba figúrky
- *is_pawn* - *bool*, či je figúrka pešiak
- *is_king* - *bool*, či je figúrka kráľ

### backend.move_descriptor.MoveDescriptor

Dátová trieda popisujúca možný ťah:
- *from_position* - *Vector*, pozícia figúrky, ktorou sa hýbe
- *to_position* - *Vector*, pozícia, na ktorú sa figúrka hýbe
- *square_from* - *(WhosePiece, Colors)* - kópia koho figúrky na *from_position* zostane a komu bude patriť
- *square_to* - *(WhosePiece, Colors)* - kópia koho figúrky na *to_position* zostane a komu bude patriť

### utility.enums.WhosePiece

Enum reprezentujúci majiteľa figúrky, používaný v *MoveDescriptor*:
- *MINE* - kopíruje sa moja figúrka
- *OPPONENTS* - kopíruje sa súperova figúrka
- *NONE* - políčko je prázdne

### utility.enums.Players

Enum reprezentujúci hráča relatívne k aktuálnemu:
- *ME* - hráč na ťahu
- *OPPONENT* - súper
- *NONE* - žiadny z hráčov

### utility.vector.Vector

Dátová trieda reprezentujúca pozíciu na šachovnici:
- *x* - *int*, x-ová súradnica
- *y* - *int*, y-ová súradnica

Sú na nej definované základné operácie - sčítanie, očítanie, násobenie skalárom, porovnávanie, hash.
