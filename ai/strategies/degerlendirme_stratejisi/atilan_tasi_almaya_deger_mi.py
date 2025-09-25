# ai/strategies/degerlendirme_stratejisi/atilan_tasi_almaya_deger_mi.py
from log import logger
from ai.strategies.discard_stratejisi import en_akilli_ati_bul
from ai.strategies.degerlendirme_stratejisi._eli_puanla import _eli_puanla

@logger.log_function
def atilan_tasi_almaya_deger_mi(mevcut_el, atilan_tas, gorev_tamamlaniyor_mu):
    if gorev_tamamlaniyor_mu: return True
    mevcut_puan = _eli_puanla(mevcut_el)
    olasi_el = mevcut_el + [atilan_tas]
    yeni_puan = _eli_puanla(olasi_el)
    fayda = yeni_puan - mevcut_puan
    
    atilabilecekler = [t for t in olasi_el if t.id != atilan_tas.id]
    atılacak_tas = en_akilli_ati_bul(olasi_el, atilabilecekler)
    if not atılacak_tas: return False

    el_den_sonra = [t for t in olasi_el if t.id != atılacak_tas.id]
    son_puan = _eli_puanla(el_den_sonra)
    
    net_kazanc = son_puan - mevcut_puan
    return net_kazanc > 20