# ai/strategies/cift_stratejisi/_ciftleri_ve_tekleri_bul.py
from collections import defaultdict
from log import logger

@logger.log_function
def _ciftleri_ve_tekleri_bul(el):
    tas_gruplari = defaultdict(list)
    for tas in el:
        if tas.renk != 'joker':
            anahtar = (tas.renk, tas.deger)
            tas_gruplari[anahtar].append(tas)
            
    ciftler, tekler = [], []
    for tas_listesi in tas_gruplari.values():
        cift_sayisi = len(tas_listesi) // 2
        for i in range(cift_sayisi):
            ciftler.append(tas_listesi[i*2 : i*2+2])
        if len(tas_listesi) % 2 != 0:
            tekler.append(tas_listesi[-1])
            
    return ciftler, tekler