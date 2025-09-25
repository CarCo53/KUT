# gui/buttons/tas_at.py
from log import logger

@logger.log_function
def tas_at(arayuz):
    secili = arayuz.secili_tas_idler
    if len(secili) == 1:
        arayuz.oyun.tas_at(0, secili[0])
        arayuz.secili_tas_idler = []
    else:
        arayuz.statusbar.guncelle("Lütfen atmak için sadece 1 taş seçin.")
    arayuz.arayuzu_guncelle()