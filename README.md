# Název projektu - ELECTION SCRAPER

## Popis

Projekt slouží k extrahování výsledků parlamentních voleb z roku 2017. 

## Instalace knihoven

Knihovny, které jsou použity v kódu jsou uložené v souboru requirements.txt. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:
pip3 --version  #ověření verze manažeru
pip3 install -r requirements.txt   #nainstalování knihoven

## Spuštění projektu

Spuštění souboru election_scraper.py v rámci příkazového řádku požaduje dva povinné argumenty.
python election_scraper <odkaz-uzemniho-celku> <nazev-vysledneho-souboru>
Následně se vám stáhnou výsledky jsko soubor s pčíponou .csv

## Ukázka projektu

Výsledky hlasování pro okres Žďár nad Sázavou:
1. argument: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6105
2. argument: vysledky_zdar.csv

Spuštění programu:
python election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6105" "volby_zdar.csv"

Průběh stahování:
STAHUJI DATA Z VYBRANÉHO URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6105
UKLÁDÁM DO SOUBORU:  volby_zdar.csv
UKONČUJI ELECTION SCRAPER

Částečný výstup:
code,location:,registered,envelopes,valid, ....
595217,Baliny,102,71,71,8,0,0,6,0,3,8,2,1,0,0,0,8,0,6,12,0,8,0,0,0,1,5,3
595241,Blažkov,229,162,161,7,0,0,15,0,9,26,2,3,4,1,1,13,0,3,36,0,16,0,0,0,0,25,0
595250,Blízkov,272,191,191,5,0,0,14,0,4,19,3,1,3,0,0,21,0,11,42,0,50,0,1,0,0,14,3
595268,Bobrová,706,430,425,53,1,0,66,0,12,36,4,5,4,0,0,28,0,20,112,1,46,0,4,0,0,31,2
....

