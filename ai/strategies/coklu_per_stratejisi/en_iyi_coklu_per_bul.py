# ai/strategies/coklu_per_stratejisi/en_iyi_coklu_per_bul.py
from itertools import combinations
from log import logger
from rules.per_validators.kut_mu import kut_mu
from rules.per_validators.seri_mu import seri_mu


@logger.log_function
def en_iyi_coklu_per_bul(el, gorev):
    try:
        if "2x" in gorev:
            parcalar = gorev.split(' ')
            tip_str = parcalar[1].lower()
            min_sayi = int(parcalar[2])
            toplam_tas_sayisi = min_sayi * 2
            
            if len(el) < toplam_tas_sayisi:
                return None

            kontrol_fonksiyonu = kut_mu if tip_str == "küt" else seri_mu
            
            for grup1_kombinasyonu in combinations(el, min_sayi):
                if kontrol_fonksiyonu(list(grup1_kombinasyonu), min_sayi):
                    kalan_taslar = [t for t in el if t not in grup1_kombinasyonu]
                    if len(kalan_taslar) >= min_sayi:
                        for grup2_kombinasyonu in combinations(kalan_taslar, min_sayi):
                            if kontrol_fonksiyonu(list(grup2_kombinasyonu), min_sayi):
                                return list(grup1_kombinasyonu) + list(grup2_kombinasyonu)

        elif "+" in gorev:
            parcalar = gorev.split(' ')
            tip1_str = parcalar[0].lower()
            min_sayi1 = int(parcalar[1])
            tip2_str = parcalar[3].lower()
            min_sayi2 = int(parcalar[4])
            toplam_tas_sayisi = min_sayi1 + min_sayi2

            if len(el) < toplam_tas_sayisi:
                return None

            kontrol1 = kut_mu if tip1_str == "küt" else seri_mu
            kontrol2 = seri_mu if tip2_str == "seri" else kut_mu

            for grup1_kombinasyonu in combinations(el, min_sayi1):
                if kontrol1(list(grup1_kombinasyonu), min_sayi1):
                    kalan_taslar = [t for t in el if t not in grup1_kombinasyonu]
                    if len(kalan_taslar) >= min_sayi2:
                        for grup2_kombinasyonu in combinations(kalan_taslar, min_sayi2):
                            if kontrol2(list(grup2_kombinasyonu), min_sayi2):
                                return list(grup1_kombinasyonu) + list(grup2_kombinasyonu)
    
    except (ValueError, IndexError):
        return None
            
    return None