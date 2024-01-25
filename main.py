# ESIMERKKI KÄYTTÖ

import jamixapi
import datetime

pvm = datetime.datetime.now().strftime("%Y%m%d")
paivanRuokalista = jamixapi.haeRuokaLista(pvm, "96786", "10")
ruoanNimi = jamixapi.haeRuoanNimi(paivanRuokalista)

print(f"Tänään syötäisiin Viitaniemen Gradialla herkullista: {ruoanNimi}.")