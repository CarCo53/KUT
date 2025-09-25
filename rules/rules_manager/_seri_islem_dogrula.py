# rules/rules_manager/_seri_islem_dogrula.py
from log import logger
from core.tile import Tile

@logger.log_function
def _seri_islem_dogrula(per, tas):
    if len(per) >= 14: return False
    
    per_tasi_listesi = [t for t in per if t.renk != "joker" or (t.renk == "joker" and t.joker_yerine_gecen is not None)]
    if not per_tasi_listesi:
        if tas.renk == "joker" and not tas.joker_yerine_gecen: return True
        return False

    per_rengi = per_tasi_listesi[0].renk
    
    if tas.renk != "joker" and tas.renk != per_rengi: return False

    sayilar = []
    for t in per:
        if t.renk == "joker" and t.joker_yerine_gecen is not None:
            sayilar.append(t.joker_yerine_gecen.deger)
        elif t.renk != "joker":
            sayilar.append(t.deger)
    
    joker_sayisi = sum(1 for t in per if t.renk == "joker" and t.joker_yerine_gecen is None)
    sayilar.sort()
    
    if tas.renk == "joker" and not tas.joker_yerine_gecen:
        if not sayilar: return True
        if sayilar[0] > 1 and sayilar[0] - 1 not in sayilar: return True
        if sayilar[-1] < 13 and sayilar[-1] + 1 not in sayilar: return True
        if 1 in sayilar and 13 in sayilar and 12 not in sayilar: return True
        return False

    tas_degeri = tas.deger

    if tas_degeri == sayilar[0] - 1 or tas_degeri == sayilar[-1] + 1:
        return True
    
    if 1 in sayilar and 13 in sayilar:
        if len(sayilar) == 2 and sayilar[0] == 1 and sayilar[-1] == 13 and tas_degeri == 12:
            return True
        if len(sayilar) >= 3 and sorted([1,2,3]) == sorted(sayilar[:3]) and tas_degeri == 13:
             return False
        if len(sayilar) >= 3 and sorted([12,13,1]) == sorted(sayilar[-3:]) and tas_degeri == 2:
            return False

    if tas_degeri == 13 and 1 in sayilar and 2 in sayilar:
        return False
    if tas_degeri == 1 and 12 in sayilar and 13 in sayilar:
         return False
    
    return False