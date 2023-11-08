# Tämä tiedosto hoitaa vuorovaikutuksen Jamixin rajapinnan kanssa.

import json
import requests
from bs4 import BeautifulSoup # Sivun sisällöstä jonkin asian (ruoan nimen) etsimistä varten. <-- "Web scraping" englanniksi.
# En tykkäisi käyttää normaalisti koska se on paljon raskaampaa "kohdesivustoa" kohtaan.

# Kopioitu esimerkki pohja wikipediasta ja muutettu joitakin osia helpomman käsitteltyn takaamiseksi.
tapahtumaPohja = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Ruoka v1.0//FI
BEGIN:VEVENT
DTSTAMP:YYYYMMDDTXXXXXXZ
ORGANIZER;CN=Veeti Simpanen:MAILTO:gr289440@gradia.fi
DTSTART:YYYYMMDDTXXXXXXZ
DTEND:YYYYMMDDTXXXXXXZ
SUMMARY:RUOKANIMI
END:VEVENT
END:VCALENDAR
"""

# Haetaan ruokalista päivämäärän ja nykyään myös koulun perusteella.
def haeRuoka(pvm, koulu):
    osoiteGradia = f"https://fi.jamix.cloud/apps/menuservice/rest/haku/menu/96786/10?lang=fi&date={pvm}&date2={pvm}"
    osoiteJamk = f"https://fi.jamix.cloud/apps/menuservice/rest/haku/menu/93077/60?lang=fi&date={pvm}&date2={pvm}"
    if koulu == "gradia":
        vastaus = requests.get(osoiteGradia)
        return vastaus.json()
    elif koulu == "jamk":
        vastaus = requests.get(osoiteJamk)
        return vastaus.json()
    else:
        vastaus = "Täh? Tälläistä koulua ei ole."
        return vastaus

# Luodaan ICS muotoinen "tapahtuma" jonka nimi on päivän ruoka. Esim "KANALASAGNE" tai mitä ikinä ruokana onkaan.
def luoTapahtuma(jsontiedot, pvm, menu, koulu):
    try:
        # Palauttaa Jamkilla automaattisesti kasvisruoan, koska se on ensimmäisenä vaihtoehtona.
        # Gradialla toisin päin.
        if menu == "liha" and koulu == "gradia": # GRADIA PÄÄ
            ruokanimi = jsontiedot[0]["menuTypes"][0]["menus"][0]["days"][0]["mealoptions"][0]["menuItems"][0]["name"]
        elif menu == "kasvis" and koulu == "gradia": # GRADIA KASVIS
            ruokanimi = jsontiedot[0]["menuTypes"][0]["menus"][0]["days"][0]["mealoptions"][1]["menuItems"][0]["name"]
        elif menu == "liha" and koulu == "jamk": # JAMK PÄÄ
            ruokanimi = jsontiedot[0]["menuTypes"][0]["menus"][0]["days"][0]["mealoptions"][1]["menuItems"][0]["name"]
        elif menu == "kasvis" and koulu == "jamk": # JAMK KASVIS
            ruokanimi = jsontiedot[0]["menuTypes"][0]["menus"][0]["days"][0]["mealoptions"][0]["menuItems"][0]["name"]
        else:
            ruokanimi = "EN TIEDÄ MITÄ RUOKAA ON."
        tapahtuma = tapahtumaPohja.replace("YYYYMMDDTXXXXXXZ", f"{pvm}T110000Z")
        tapahtuma = tapahtuma.replace("RUOKANIMI", ruokanimi)
        return tapahtuma
    except: # Periaatteessa sama asia kuin ylempi osuus, mutta "ruokanimi" onkin virhe viesti.
        virheTapahtuma = tapahtumaPohja.replace("YYYYMMDDTXXXXXXZ", f"{pvm}T110000Z")
        virheTapahtuma = virheTapahtuma.replace("RUOKANIMI", "Ruokaa haettaessa tapahtui virhe!")
        return virheTapahtuma
    finally:
        print("Luotu tapahtuma.")