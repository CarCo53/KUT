# ai/strategies/cift_stratejisi/tasi_cift_yapar_mi.py
from log import logger
from ai.strategies.cift_stratejisi._ciftleri_ve_tekleri_bul import _ciftleri_ve_tekleri_bul

@logger.log_function
def tasi_cift_yapar_mi(el, tas):
    """Verilen taşın, eldeki teklerden birini çifte dönüştürüp dönüştürmediğini kontrol eder."""
    _, tekler = _ciftleri_ve_tekleri_bul(el)
    for tek_tas in tekler:
        if tek_tas.renk == tas.renk and tek_tas.deger == tas.deger:
            return True
    return False