# gui/buttons/gec.py
from log import logger

@logger.log_function
def gec(arayuz):
    arayuz.oyun.atilan_tasi_gecti()
    arayuz.arayuzu_guncelle()