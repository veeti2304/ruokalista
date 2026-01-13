"""
Uusi & päivitetty Jamix API Wrapper V2
---------------------------------------

Tämän tiedoston tarkoitus on toimia esimerkkinöä siitä, miten tätä versiota käytetään.
Tekijä / Author: github.com/veeti2304
Jamix: https://jamix.com
"""

from jamixapi import get_daily_meal_ics

ics_data = get_daily_meal_ics(
    date="20260120", # Päivä formaatti: YYYYMMDD
    customer_id=96786, # Esimerkki asiakastunnus (nyt Gradia)
    kitchen_id=10, # Ruokalan tunnus (pääkampus tms.)
    organizer_name="Jamix Ruoka API v2",
    organizer_email="veeti2304@example.com",
)

with open("ruoka.ics", "w", encoding="utf-8") as f:
    f.write(ics_data)