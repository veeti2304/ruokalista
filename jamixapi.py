"""
Jamix API Wrapper V2
--------------------

Käyttö: Etsi päivän ateria Jamixin API:n kautta ja luo siitä halutessasi ICS tiedosto.
Tekijä / Author: github.com/veeti2304
Jamix: https://jamix.com

Toivottavasti tästä on edes jollekin hyötyä ja seuraa ainakin melkein best-practice mindsettiä :D
"""

from __future__ import annotations

import requests
from datetime import datetime, timedelta
from typing import Any

class JamixClient:
    """Asiakasohejlma Jamixin API:lle."""

    BASE_URL = "https://fi.jamix.cloud/apps/menuservice/rest/haku/menu"

    def __init__(self, customer_id: int, kitchen_id: int, language: str = "fi"):
        self.customer_id = customer_id
        self.kitchen_id = kitchen_id
        self.language = language

    def fetch_menu(self, date: str) -> list[dict[str, Any]]:
        """
        Hae menu JSON tietylle päivälle API:sta.
        Aika formaatti: YYYYMMDD (esimerkkinä: 20240614 jossa 14 on päivä ja 06 on kuukausi)
        """
        url = (
            f"{self.BASE_URL}/{self.customer_id}/{self.kitchen_id}"
            f"?lang={self.language}&date={date}&date2={date}"
        )

        response = requests.get(url, timeout=10, verify=False) # Huom: verify=False poistaa SSL varmistuksen, eli vähän getto ratkaisu.
        response.raise_for_status()
        return response.json()

    @staticmethod
    def extract_meal_name(menu_json: list[dict[str, Any]]) -> str:
        """
        Hae pääruoan nimi JSON datasta.
        """
        try:
            return (
                menu_json[0]["menuTypes"][0]["menus"][0]
                ["days"][0]["mealoptions"][0]
                ["menuItems"][0]["name"]
            )
        except (KeyError, IndexError, TypeError):
            return "Ei ruokaa :( [Joku todnäk. joko meni pieleen tai sitten ruokalan määrärahoja leikattiin, (tai on viikonloppu)]"

class ICSBuilder:
    """ICS kalenteritiedoston rakentaja. Kätevä kun halutaan lisätä ruoka kalenteriin."""

    @staticmethod
    def build_event(
        date: str,
        summary: str,
        organizer_name: str,
        organizer_email: str,
        start_time: str = "120000",
        duration_minutes: int = 30,
    ) -> str:
        """
        Luo ICS kalenteritiedosto annetulla tiedolla.

        date: YYYYMMDD
        start_time: HHMMSS
        """

        start_dt = datetime.strptime(f"{date}{start_time}", "%Y%m%d%H%M%S")
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        now_utc = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

        return f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Ruoka v2.0//FI
BEGIN:VEVENT
DTSTAMP:{now_utc}
ORGANIZER;CN={organizer_name}:MAILTO:{organizer_email}
DTSTART:{start_dt.strftime("%Y%m%dT%H%M%SZ")}
DTEND:{end_dt.strftime("%Y%m%dT%H%M%SZ")}
SUMMARY:{summary}
END:VEVENT
END:VCALENDAR
"""

def get_daily_meal_ics(
    date: str,
    customer_id: int,
    kitchen_id: int,
    organizer_name: str,
    organizer_email: str,
) -> str:
    """
    Hae päivän ateria ja palauta se ICS kalenteritiedostona.
    """
    client = JamixClient(customer_id, kitchen_id)
    menu_json = client.fetch_menu(date)
    meal_name = client.extract_meal_name(menu_json)

    return ICSBuilder.build_event(
        date=date,
        summary=meal_name,
        organizer_name=organizer_name,
        organizer_email=organizer_email,
    )