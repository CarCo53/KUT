# gui/buttons/desteden_cek.py
from log import logger

@logger.log_function
def desteden_cek(arayuz):
    arayuz.oyun.desteden_cek(0)
    arayuz.arayuzu_guncelle()