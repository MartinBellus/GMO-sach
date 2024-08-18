# GMO šach
GMO šach bola hra na jesenné sústredenie KSP 2023.
Počas tejto aktivity družinky proti sebe hrali duely v GMO šachu. Na to potrebovali zistiť systém fungovania genómov figúrok a vyrobiť čo najlepšie figúrky.

## Idea hry
GMO šach je založený na šachu, a teda sa s ním v mnohých smeroch zhoduje. Hlavným rozdielom je, že každá figúrka má genóm, ktorý popisuje jej možné ťahy. Hráči na začiatku poznajú genómy štandardných šachových figúrok a experimentovaním sa z nich snažia odvodiť princíp fungovania genómov.

## Implementácia hry
Aplikácia sa skladá z niekoľkých základných blokov:
- Backend - Zodpovedný za spracovávanie genómu figúrok, stavu hry. Viď [README backendu](backend/README.md).
- Frontend - Zobrazovanie hry, spracovanie užívateľských vstupov. Viď [README frontendu](frontend/README.md)
- Server - Beží nezávisle, slúži na ukladanie genómov. Viď [README servera](server/README.md)

Backend a frontend sú skompilované do aplikácie, ktorá je distribuovaná účastníkom. Samozrejme, keďže zdrojové kódy prezrádzajú fungovanie genómu, musia byť nejakým spôsobom obfuskované. Tu sme sa rozhodli ísť cestou kompilovania celej aplikácie do jednej binárky pomocou nástroja [PyInstaller](https://pyinstaller.org). Tento spôsob nie je dokonalý, ale vzhľadom na podmienky hry (4 hodiny v kontrolovanom prostredí) je dostatočný.

## Spustenie
Aplikácia sa spúšťa príkazmi `python3 game.py`, resp. `python3 lab.py`. Špecifiká sa nachádzajú v [README frontendu](frontend/README.md).

# Credits

- Nápad na hru
    - Viktor Balan
    - Martin Belluš
    - Jakub Konc
- Vývoj aplikácie
    - Martin Belluš
        - Frontend modul
        - Utility sekcia
    - Jakub Konc
        - Backend a server moduly
        - Utility sekcia
- Obrázky
    - [Macrune12](https://macrune12.itch.io/)
        - Pod **creative commons BY-ND 4.0**
    
