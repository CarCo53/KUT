# ai/strategies/planlama_stratejisi/en_akilli_ati_bul.py
from log import logger

@logger.log_function
def en_akilli_ati_bul(el, el_analizi, atilan_taslar):
    jokersiz_el = [t for t in el if t.renk != "joker"]
    if not jokersiz_el:
        return max(el, key=lambda t: t.deger)
        
    en_kotu_tas = None
    
    tam_perler = [item for sublist in el_analizi["uc_taslilar"] for item in sublist] + \
                 [item for sublist in el_analizi["dort_taslilar"] for item in sublist] + \
                 [item for sublist in el_analizi["seriler"] for item in sublist] + \
                 [item for sublist in el_analizi["ciftler"] for item in sublist]

    tek_taslar = [t for t in jokersiz_el if t not in tam_perler]
    
    if tek_taslar:
        en_kotu_tas = max(tek_taslar, key=lambda t: t.deger)
    
    if en_kotu_tas is None:
        for tas in jokersiz_el:
            if tas.deger != 1 and tas.deger != 13:
                 if not any(tas in per for per in el_analizi["seriler"]) and \
                    not any(tas in per for per in el_analizi["uc_taslilar"]) and \
                    not any(tas in per for per in el_analizi["dort_taslilar"]):
                         en_kotu_tas = tas
                         break
    
    if en_kotu_tas is None and jokersiz_el:
        en_kotu_tas = max(jokersiz_el, key=lambda t: t.deger)

    return en_kotu_tas