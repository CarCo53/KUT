# rules/per_validators/cift_per_mu.py
from log import logger

@logger.log_function
def cift_per_mu(taslar):
    if len(taslar) < 8 or len(taslar) % 2 != 0: return False
    tas_gruplari, joker_sayisi = {}, 0
    for tas in taslar:
        if tas.renk == "joker": joker_sayisi += 1
        else:
            anahtar = (tas.renk, tas.deger)
            tas_gruplari[anahtar] = tas_gruplari.get(anahtar, 0) + 1
    tek_kalan_sayisi = sum(1 for sayi in tas_gruplari.values() if sayi % 2 != 0)
    return joker_sayisi >= tek_kalan_sayisi