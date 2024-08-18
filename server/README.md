Autor: Jakub Konc

## Server

Jednoduchý HTTP server, ktorý slúži na zjednodušenie prenášania DNA figúrok medzi počítačmi.

### Použitie

Server sa spúšťa príkazom `python3 server.py`. Defaultne beží na localhost:5000.

### Fungovanie

Server má zoznam povolených podadries *ALLOWED_SUBADDRESSES*. Pri requestoch na iné URL cesty server vráti *404 Not Found*.

#### POST /\<subaddress\>/\<code\>

Code môže obsahovať len písmená anglickej abecedy, číslice a mínus.

Server uloží obsah requestu do súboru `./<subaddress>/<code>`. Ak súbor už existuje, request sa ignoruje.

Vráti 200 OK.

#### GET /\<subaddress\>/\<code\>

Code môže obsahovať len písmená anglickej abecedy, číslice a mínus.

Server vráti obsah súboru `./<subaddress>/<code>` a 200 OK. Ak súbor neexistuje, vráti *404 Not Found*.
