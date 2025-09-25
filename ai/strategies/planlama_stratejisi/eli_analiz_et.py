# ai/strategies/planlama_stratejisi/eli_analiz_et.py
from collections import defaultdict
from log import logger
from rules.per_validators.kut_mu import kut_mu
from rules.per_validators.seri_mu import seri_mu

@logger.log_function
def eli_analiz_et(el):
    el_analizi = {
        "ciftler": [],
        "uc_taslilar": [],
        "dort_taslilar": [],
        "seriler": [],
        "ikili_potansiyeller": {"seri": [], "kut": []}
    }
    
    renk_gruplari = defaultdict(list)
    for tas in el:
        if tas.renk != 'joker':
            renk_gruplari[tas.renk].append(tas)
    
    for renk in renk_gruplari:
        renk_gruplari[renk].sort(key=lambda t: t.deger)

    for renk, tas_listesi in renk_gruplari.items():
        if len(tas_listesi) >= 3:
            for i in range(len(tas_listesi) - 2):
                if tas_listesi[i+1].deger == tas_listesi[i].deger + 1 and tas_listesi[i+2].deger == tas_listesi[i+1].deger + 1:
                    seri = [tas_listesi[i], tas_listesi[i+1], tas_listesi[i+2]]
                    el_analizi["seriler"].append(seri)
    
    renk_deger_gruplari = defaultdict(list)
    deger_gruplari = defaultdict(list)
    for tas in el:
        if tas.renk != 'joker':
            anahtar = (tas.renk, tas.deger)
            renk_deger_gruplari[anahtar].append(tas)
            deger_gruplari[tas.deger].append(tas)
            
    for tas_listesi in renk_deger_gruplari.values():
        if len(tas_listesi) == 2:
             el_analizi["ciftler"].append(tas_listesi)
    
    for deger, tas_listesi in deger_gruplari.items():
        if len(tas_listesi) >= 3:
            renkler_seti = {t.renk for t in tas_listesi}
            if len(renkler_seti) >= 3:
                if len(tas_listesi) == 3:
                    el_analizi["uc_taslilar"].append(tas_listesi)
                elif len(tas_listesi) == 4:
                    el_analizi["dort_taslilar"].append(tas_listesi)

    for renk, tas_listesi in renk_gruplari.items():
        for i in range(len(tas_listesi) - 1):
            if tas_listesi[i+1].deger - tas_listesi[i].deger <= 2:
                el_analizi["ikili_potansiyeller"]["seri"].append((tas_listesi[i], tas_listesi[i+1]))
                
    for deger, tas_listesi in deger_gruplari.items():
        if len(tas_listesi) == 2:
            el_analizi["ikili_potansiyeller"]["kut"].append(tuple(tas_listesi))
            
    return el_analizi