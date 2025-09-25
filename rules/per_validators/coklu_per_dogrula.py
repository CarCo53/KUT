# rules/per_validators/coklu_per_dogrula.py
from itertools import combinations
from log import logger
from rules.per_validators.kut_mu import kut_mu
from rules.per_validators.seri_mu import seri_mu

@logger.log_function
def coklu_per_dogrula(taslar, tip, min_sayi, adet):
    if len(taslar) != min_sayi * adet: return False
    kontrol_fonksiyonu = kut_mu if tip == "küt" else seri_mu
    for grup1_kombinasyonu in combinations(taslar, min_sayi):
        kalan_taslar = [t for t in taslar if t not in grup1_kombinasyonu]
        if kontrol_fonksiyonu(list(grup1_kombinasyonu), min_sayi) and kontrol_fonksiyonu(kalan_taslar, min_sayi):
            return (list(grup1_kombinasyonu), kalan_taslar)
    return False