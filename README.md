# 🍎​ Ruokalista

### Mikä tämän projektin tarkoitus on?
Tarkoituksena on antaa sinulle, python kehittäjälle helppo tapa hakea tietoa mistä vain ravintolasta joka käyttää Jamixin palveluita.<br>
Esimerkiksi voit helposti tehdä skriptin joka hakee päivän kouluruoan. <br>Main tiedostossa on esimerkki joka hakee Jamixin ruokalistasta Viitaniemen Gradian pääruoan.

### Miten sitä voi käyttää?
Helppoa! Tässä on esimerkki:
```py
# Esimerkki tulostaa Gradian 23.01.2024 tarjolla olleen menun JSON tiedot.
import jamixapi
pvm = "20240123"
print(jamixapi.haeRuokaLista(pvm, "96786", "10"))
```

### Muut ominaisuudet
Tällä hetkellä tästä löytyy myös ominaisuus jonka avulla voit tehdä helposti ICS-kalenteritiedoston jonka voit esim. viedä Google kalenteriisi.

### V2
Suosittelen vaihtamaan V2:een sillä se on paljon simppelimpi. Se löytyy v2 branchista.