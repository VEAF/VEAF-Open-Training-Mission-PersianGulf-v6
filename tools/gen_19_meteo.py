"""Lot 19 : météo de base de la mission. Pas de variantes météo dans une Open Training : le serveur VEAF fixe la
météo et l'heure de chaque session (décision de David, 12/10/2026) ; la mission doit seulement voler correctement
sans lui. Le squelette du scaffold a sa base de nuages au sol (Preset1 à 0 m) : ciel clair de mi-novembre à la place.
"""
from lib import Batch

if __name__ == "__main__":
    b = Batch()
    b.act("set_weather", temperature=28, wind_speed=4.1, wind_direction=320, visibility=9999, cloud_type="clear",
          precipitation=False, fog_enabled=False)
    b.save("19-meteo.json")
