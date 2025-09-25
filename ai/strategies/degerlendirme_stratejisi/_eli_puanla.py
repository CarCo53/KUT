# ai/strategies/degerlendirme_stratejisi/_eli_puanla.py
from log import logger

@logger.log_function
def _eli_puanla(el):
    if not el: return 0
    puan = len([t for t in el if t.renk == 'joker']) * 25
    for tas in el:
        if tas.renk == 'joker': continue
        for diger_tas in el:
            if tas.id != diger_tas.id:
                if tas.deger == diger_tas.deger: puan += 10
                if tas.renk == diger_tas.renk:
                    fark = abs(tas.deger - diger_tas.deger)
                    if fark == 1: puan += 12
                    elif fark == 2: puan += 6
    return puan