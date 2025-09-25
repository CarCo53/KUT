# ai/strategies/cift_stratejisi/en_iyi_ciftleri_bul.py
from log import logger
from rules.per_validators.cift_per_mu import cift_per_mu
from ai.strategies.cift_stratejisi._ciftleri_ve_tekleri_bul import _ciftleri_ve_tekleri_bul

@logger.log_function
def en_iyi_ciftleri_bul(el, gorev):
    if gorev != "Çift":
        return None
    
    jokerler = [t for t in el if t.renk == 'joker']
    ciftler, tekler = _ciftleri_ve_tekleri_bul(el)

    potansiyel_cift_sayisi = len(ciftler) + len(jokerler) // 2
    
    if potansiyel_cift_sayisi >= 4:
        acilacak_taslar = []
        
        for cift_grup in ciftler:
            acilacak_taslar.extend(cift_grup)

        for i in range(min(len(tekler), len(jokerler))):
            acilacak_taslar.append(tekler[i])
            jokerler[i].joker_yerine_gecen = tekler[i]
            acilacak_taslar.append(jokerler[i])
            
        kalan_jokerler = jokerler[min(len(tekler), len(jokerler)):]
        if len(kalan_jokerler) >= 2:
            acilacak_taslar.extend(kalan_jokerler)

        if cift_per_mu(acilacak_taslar):
            return acilacak_taslar
            
    return None