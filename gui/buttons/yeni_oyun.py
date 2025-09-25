# gui/buttons/yeni_oyun.py
from log import logger

@logger.log_function
def yeni_oyun(arayuz):
    arayuz.oyun.baslat()
    arayuz.arayuzu_guncelle()