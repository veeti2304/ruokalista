# Tekijä: github.com/veeti2304
# Käyttö: Etsi päivän ateria Jamixin API:n kautta ja luo siitä halutessasi ICS tiedosto.
# Jamix API: https://fi.jamix.cloud/apps/menuservice/rest/haku/menu/<customer>/<kitchen>?lang=fi

import json
import requests

# ICS kalenteritiedoston pohja
tapahtumaPohja = f"""
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Ruoka v1.0//FI
BEGIN:VEVENT
DTSTAMP:YYYYMMDDTXXXXXXZ
ORGANIZER;CN=XYZNIMI:MAILTO:MEILI
DTSTART:YYYYMMDDTXXXXXXZ
DTEND:YYYYMMDDTXXXXXXZ
SUMMARY:RUOKANIMI
END:VEVENT
END:VCALENDAR
"""

# Funktio jolla haetaan ruokalistan JSON tiedot Jamixin API:sta
# Päivämäärän muoto: YYYYMMDD (Esim: 20240125)
def haeRuokaLista(pvm, asiakas, keittio):
    # Gradia Viitaniemi: Asiakas = 96786, Keittiö = 10
    apiOsoite = f"https://fi.jamix.cloud/apps/menuservice/rest/haku/menu/{asiakas}/{keittio}?lang=fi&date={pvm}&date2={pvm}"
    try:
        # Haetaan JSON tiedot API:sta
        jsontiedot = requests.get(apiOsoite).json()
        print("[+] JSON tiedot haettu.")
        return jsontiedot
    except:
        print("[-] JSON tietojen haku epäonnistui!")
        return False

# Parsetaan JSON tiedot ja etsitään siitä ruoan nimi
def haeRuoanNimi(jsontiedot):
    try:
        ruoanNimi = jsontiedot[0]["menuTypes"][0]["menus"][0]["days"][0]["mealoptions"][0]["menuItems"][0]["name"]
        return ruoanNimi
    except:
        return "Ei ruokaa."
    finally:
        print("[+] Ruoan nimi haettu.")

# Palauta ICS tiedoston sisältö
def luoKalenteriKutsu(pvm, ruoanNimi, koulu, nimi, email):
    tapahtuma = tapahtumaPohja
    tapahtuma = tapahtuma.replace("RUOKANIMI", ruoanNimi)
    tapahtuma = tapahtuma.replace("YYYYMMDD", pvm)
    tapahtuma = tapahtuma.replace("XXXXXX", "120000")
    tapahtuma = tapahtuma.replace("XYZNIMI", nimi)
    tapahtuma = tapahtuma.replace("MEILI", email)
    print("[+] Kalenterikutsu luotu.")
    return tapahtuma