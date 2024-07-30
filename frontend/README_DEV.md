Autor: Martin Belluš

# Úvod

Toto je dokumentácia k frontendu hry GMO šach pre developerov. Aplikácia je
napísaná v jazyku Python s použitím knižnice Tkinter na tvorbu grafického
rozhrania.

Aplikácia je zložená z niekoľkých widgetov, ktoré sú do okna ukladané pomocou
správcu geometrie `pack`.

# Hlavné widgety

## ChessboardUI

Toto je trieda, ktorá je zodpovedná za vykreslovanie stavu šachovnice,
spracovanie vstupu užívateľa a komunikáciu s backendom. Táto trieda je odvodená
od `Tkinter.Canvas`.

Všetky informácie, teda aktuálny stav, pozíciu figúrok a podobne, sú získavané
od triedy `backend.Chessboard`.

### Stav šachovnice

Šachovnica sa môže nachádzať v jednom zo stavov špecifikovaných v
`utility.enums.GameState`. V závyslosti na stave šachovnice je zobrazovaný
rôzny text a pravý a ľavý klik myši majú rôzne funkcie. Za prechody medzi
stavmi hry je zodpovedná funkcia `switch_state`.

Ak je na začiatku zmeny stavu šachovnica "zamrazená", tak sa zmena stavu
uskutoční s 5 sekundovým oneskorením. Počas tohto oneskorania sa zobrazí
obrázok `images/special/freeze.png`.

Na konci zmeny stavu sa ešte vyriešia prípadné premeny pešiakov. Ak sa niektorý
z pešiakov dokáže premeniť, tak sa zobrazí dialógové okno, v ktorom môže hráč
vybrať, na ktorú figúrku sa pešiak premení. Premenu pešiaka vykonáva funkcia
`do_promotion`.

### Vykresľovanie figúrok

Figúrky na šachovnici sú vykresľované pomocou obrázkov. Presnejšie pomocou
funkcie `create_image` triedy `Tkinter.Canvas`. Za vytvorenie a úpravu obrázka
je zodpovedná trieda `ImageSelector` popísaná nižšie.

Po každej zmene polohy figúrok sa zavolá funkcia `redraw_pieces`, ktorá najprv
vymaže všetky obrázky na šachovnici a potom vykreslí aktuálnu polohu figúrok na
šachovnici.

Na vykreslovanie ťahov sa používajú metódy:

- `draw_moves` - vykreslí možné ťahy figúrky
	- parametre:
		- `current_descriptors` - zoznam tried `MoveDescriptor`, ktoré reprezentujú políčka, na ktoré sa figúrka môže pohnúť
		- `color` - farba, ktorou sa zvýraznia políčka, na ktoré sa figúrka môže pohnúť
- `clear_selected` - zafarbí všetky políčka na pôvodnú farbu

### Pokladanie figúrok

Na pokladanie figúrok sa používajú metódy:

- `place_piece` - položí figúrku zo zadaným genómom na zadané políčko
	- pri chybe vytvorí dialógové okno s chybovou hláškou a normálne skončí
	- parametre:
		- `dna` - genóm figúrky
		- `color` - farba figúrky
		- `x` - x-ová súradnica políčka
		- `y` - y-ová súradnica políčka
- `place_piece_hash` - podobne ako `place_piece`, ale genóm je reprezentovaný kódom figúrky
	- pri chybe vytvorí dialógové okno s chybovou hláškou a normálne skončí
	- parametre:
		- `hash` - kód figúrky
		- `color` - farba figúrky
		- `x` - x-ová súradnica políčka
		- `y` - y-ová súradnica políčka
- `place_preset` - položí začiatočné rozloženie figúrok podľa kódu pre zadaného hráča
	- môže skončiť s chybou, ktorú potom vyrieši `InputPopup`
	- parametre:
		- `preset` - kód začiatočného rozloženia figúrok
		- `color` - farba figúrky

Každá z týchto metód zavolá korešpondujúcu metódu triedy `backend.Chessboard` a
následne prekreslí stav šachovnice pomocou funckie `redraw_pieces`.

Tieto funkcie sa použivajú ako callback funckie pre niektoré z tlačítok v menu
alebo v dialógových oknách `InputPopup`.

### Spracovanie vstupu užívateľa

Kliknutia sa spracovávajú priradením udalostí (kliknutí myšou) k metódam tejto
triedy pomocou funckie `bind`.

V rôznych stavoch sa používajú nasledovné metódy:

- pred hrou (`NOT_STARTED`)
	- ľavým kliknutím sa nastavuje pozícia kráľa (`set_king_click`)
- počas hry
	- ľavým kliknutím sa pohybuje figúrkou (`ingame_click`)
	- pravým kliknutím sa zobrazia možné ťahy figúrky (`preview_click`)
- v móde Lab
	- ľavým kliknutím sa pohybuje figúrkou (`ingame_click`)
	- pravým kliknutím sa zobrazia informácie o figúrke (`get_dna_click`)

## EditorUI

Trieda `EditorUI` slúži na zobrazenie editora genómov a tlačítok na
interakciu s `ChessboardUI`. Táto trieda je odvodená od triedy `Tkinter.Frame`.

`EditorUI` obsahuje nasledovné komponenty:

- `GenomeEditor` - editor genómov
	- odvodený od triedy `Tkinter.Text` s pridanou funkciou `set_text`
	- `set_text(content)` - nastaví obsah editora na `content`
- `FileSelector` - tlačítko na otvorenie dialógového okna pre výber súborov
	- odvodené od triedy `Tkinter.Button` s pridanou funkciou `select_files`
	- `select_files()` - otvorí dialógové okno `Tkinter.filedialog.askopenfilenames` a nastaví obsah editora na obsah vybraného súboru
- `PlaceButton` - panel na výber farby a políčka, na ktoré bude položená figúrka
	- `__init__(parent, callback, **kwargs)` - konštruktor triedy
		- `parent` - rodičovský widget
		- `callback` - callback funkcia, ktorá sa zavolá po `place_button`
		- `**kwargs` - ďalšie argumenty pre konštruktor triedy `Tkinter.Frame`
	- odvodený od triedy `Tkinter.Frame` s pridanými komponentami
	- `place_button` - tlačítko na pokladanie figúrky
		- po stlačení sa zavolá funckia `callback` s parametrami `color` a `x`, `y` zadanými v `form`
	- `color_button` - tlačítko na výber farby figúrky
	- `form` - `Tkinter.Entry` na výber políčka, na ktoré sa uloží figúrka

`EditorUI` komunikuje s `ChessboardUI` pomocou funkcie
`ChessboardUI.place_piece`.

## Popups

Aplikácia taktiež obsahuje jednoduché triedy pre dialógové okná. Tieto okná sú
dvoch typov, `TextPopup` a `InputPopup`. Obe triedy sú odvodené od triedy
`Tkinter.Toplevel`.

### TextPopup

Trieda `TextPopup` slúži na zobrazenie textu v dialógovom okne. Po nejakom čase
sa okno zavrie.

Konštruktor triedy má parametre:

- `title` - názov okna
- `text` - zoznam riadkov textu na zobrazenie
- `ttl` - čas, po ktorom sa okno zavrie v milisekundách (základná hodnota je 5000)
- voliteľné parametre pre triedu `Tkinter.Toplevel`

### InputPopup

Trieda `InputPopup` slúži na textu, vstupného poľa a tlačidla na odoslanie
vstupu. Po stlačení tlačidla sa zavolá funkcia `callback`, ktorá má jeden
parameter - text vstupného poľa. V prípade chyby pri vykonávaní `callback`
funkcie sa chyba zobrazí užívateľovi.

Konštruktor triedy má parametre:

- `title` - názov okna
- `text` - text, ktorý sa zobrazí nad vstupným poľom
- `callback` - funkcia, ktorá sa zavolá po stlačení tlačidla
- voliteľné parametre pre triedu `Tkinter.Toplevel`

## ChessClockUI

Trieda `ChessClockUI` je trieda odvodená od triedy `Tkinter.Frame`. Táto trieda
slúži na zobrazenie dvoch časovačov pre hráčov vo formáte `mm:ss`. Tento čas
získava od triedy `backend.Chessboard` pomocou metódy `get_remaining_time`. Po
vytvorení tejto triedy sa každých `500` milisekúnd zavolá jej funkcia `update`,
ktorá aktualizuje zobrazenie časovačov a zvýrazní časovač aktívneho hráča.

Konštruktor triedy má nasledovné parametre:

- `parent` - widget, v ktorom sa časovače nachádzajú
- `controller` - odkaz na triedu `backend.Chessboard`
- voliteľné parametre pre triedu `Tkinter.Frame`

## Menu

`Menu` je jednoduchá trieda odvodená od `Tkinter.Frame`, ktorá obsahuje
variabilný počet tlačítok s textom a predpísanou funkciou. Tlačítka sú zoradené
podľa poradia, v akom boli v konštruktore triedy a sú usporiadané horizontálne
vedla seba.

Konštruktor triedy má nasledovné parametre:

- `parent` - widget, v ktorom sa menu nachádza
- `buttons` - zoznam dvojíc `(text, callback)`, kde `text` je text tlačítka a `callback` je funkcia, ktorá sa zavolá po stlačení tlačítka
- voliteľné parametre pre triedu `Tkinter.Frame`

## Pomocné triedy

### ImageSelector

`ImageSelector` je trieda, ktorá má na starosti vyberanie obrázkov pre figúrky
a zmenu týchto obrázkov na základe farby a typu figúrky. Na manipuláciu s
obrázkami sa používa knižnica `Pillow`.

Metódy:

- `__init__(width = 50, height = 50)`
	- konštruktor triedy
	- otvorí priečinok s obrázkami figúrok a uloží ich do zoznamu obrázkov
	- parametre:
		- `width` - šírka obrázku
		- `height` - výška obrázku
- `get_image(piece_info) -> ImageTk.PhotoImage`
	- prevedie hash genómu na index obrázku, ktorý potom upraví podľa farby figúrky a vráti
	- ak je figúrka kráľ, tak sa k obrázku pridá obrázok `images/special/king.png` pomocou metódy `paste`
- `adjust(px, color)`
	- zmení farbu pixelu podľa farby figúrky
	- ak je figúrka biela, tak zvýši jas pixelu o 50%, v opačnom prípade zníži jas o 50%
