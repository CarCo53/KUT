# ai/strategies/cift_stratejisi/atilacak_en_kotu_tas.py
from log import logger
from ai.strategies.cift_stratejisi._ciftleri_ve_tekleri_bul import _ciftleri_ve_tekleri_bul

@logger.log_function
def atilacak_en_kotu_tas(el):
    _ , tekler = _ciftleri_ve_tekleri_bul(el)
    joker_olmayan_tekler = [t for t in tekler if t.renk != 'joker']
    if joker_olmayan_tekler:
        return max(joker_olmayan_tekler, key=lambda t: t.deger or 0)
    
    ciftler, _ = _ciftleri_ve_tekleri_bul(el)
    if ciftler:
        en_dusuk_degerli_cift = min(ciftler, key=lambda c: c[0].deger)
        return en_dusuk_degerli_cift[0]
            
    return el[0] if el else None