# rules/per_validators/karma_per_dogrula.py
from itertools import combinations
from log import logger
from rules.per_validators.kut_mu import kut_mu
from rules.per_validators.seri_mu import seri_mu

@logger.log_function
def karma_per_dogrula(taslar, min_sayi):
    if len(taslar) != min_sayi * 2: return False
    for kut_kombinasyonu in combinations(taslar, min_sayi):
        seri_taslar = [t for t in taslar if t not in kut_kombinasyonu]
        if kut_mu(list(kut_kombinasyonu), min_sayi) and seri_mu(seri_taslar, min_sayi):
            return (list(kut_kombinasyonu), seri_taslar)
    for seri_kombinasyonu in combinations(taslar, min_sayi):
        kut_taslar = [t for t in taslar if t not in seri_kombinasyonu]
        if seri_mu(list(seri_kombinasyonu), min_sayi) and kut_mu(kut_taslar, min_sayi):
            return (list(seri_kombinasyonu), kut_taslar)
    return False