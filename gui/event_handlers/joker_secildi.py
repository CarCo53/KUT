# gui/event_handlers/joker_secildi.py
from log import logger

@logger.log_function
def joker_secildi(arayuz, secilen_deger, joker, secilen_taslar, pencere):
    pencere.destroy()
    arayuz.oyun.el_ac_joker_ile(0, secilen_taslar, joker, secilen_deger)
    arayuz.secili_tas_idler = []
    arayuz.arayuzu_guncelle()