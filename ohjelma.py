import os
from jamixapi import haeRuoka, luoTapahtuma
from datetime import datetime, timedelta # Lisättiin datetime moduuli jotta saadaan pvm automaattisesti.

# Otettu ideaa netistä, mutta ei sentään täysin kopioitu.
tamaPaiva = datetime.now()
paiviaMaanantaihin = tamaPaiva.weekday()
maanantai = tamaPaiva - timedelta(days=paiviaMaanantaihin)
tiistai = maanantai + timedelta(days=1)
keskiviikko = maanantai + timedelta(days=2)
torstai = maanantai + timedelta(days=3)
perjantai = maanantai + timedelta(days=4)
ma = maanantai.strftime('%Y%m%d')
ti = tiistai.strftime('%Y%m%d')
ke = keskiviikko.strftime('%Y%m%d')
to = torstai.strftime('%Y%m%d')
pe = perjantai.strftime('%Y%m%d')
# -----------------------------------------------------

# Testattu Linux Mintillä ja gnome-calendar sovelluksella.
print("Käytät ohjelmaa " + os.name + " järjestelmällä.\n")
if os.name == "posix":
    print("Järjestelmäsi todennäköisesti tukee automaattista kalenteriin lisäystä.")

print("Minkä koulun ruokalistan haluat hakea?")
print("1. Gradia")
print("2. JAMK")
print("3. Poistu")

valinta = input()

koulu = ""

if valinta == "1":
    koulu = "gradia"
elif valinta == "2":
    koulu = "jamk"
elif valinta == "3":
    exit()
else:
    koulu = "gradia"

print("Kumman menun haluat hakea?")
print("1. Päämenu")
print("2. Kasvismenu")

valinta = input()

menu = ""

if valinta == "1":
    menu = "liha"
elif valinta == "2":
    menu = "kasvis"
else:
    menu = "liha"

# Luodaan kansio ruokalistoille, jos sitä ei jo ole.
if not os.path.exists("ruokalistat"):
    os.mkdir("ruokalistat")
    print("Luotu kansio ruokalistat/.")

paivaLista = []

# Lisätään kaikki päivämäärät listaan.
paivaLista.append(ma)
paivaLista.append(ti)
paivaLista.append(ke)
paivaLista.append(to)
paivaLista.append(pe)

# Ja käydään ne läpi.
for pv in paivaLista:
    ruoka = haeRuoka(pv, koulu)
    tiedosto = open(f"ruokalistat/{pv}.ics", "w")
    tiedosto.write(luoTapahtuma(ruoka, pv, menu, koulu))
    tiedosto.close()
    print(f"Tallennettu ruokalista tiedostoon: {pv}.ics kansioon ruokalistat/.")

# Sitten jos käyttäjä haluaa, lisätään ruokalista kalenteriin.
def lisaaKalenterrin():
    # Tukee vain gnome-calendar sovellusta.
    os.system("gnome-calendar ruokalistat/*.ics")

valinta = input("Haluatko lisätä viikon ruokalistan kalenteriisi? (k/e)")

if valinta == "k" or valinta == "kyllä":
    lisaaKalenterrin()
else:
    print("Kiitos ja näkemiin!")
    exit()
