# ai/strategies/klasik_per_stratejisi/en_iyi_per_bul.py
from itertools import combinations
from rules.rules_manager import Rules
from collections import defaultdict
from log import logger
from ai.strategies.cift_stratejisi.en_iyi_ciftleri_bul import en_iyi_ciftleri_bul

@logger.log_function
def en_iyi_per_bul(el, gorev):
    gorev_tipi, min_sayi = gorev.split(' ') if ' ' in gorev else (gorev, 0)
    min_sayi = int(min_sayi) if min_sayi else 0
    
    jokerler = [t for t in el if t.renk == 'joker']
    normal_taslar = [t for t in el if t.renk != 'joker']
    
    if "Seri" in gorev:
        renk_gruplari = defaultdict(list)
        for tas in normal_taslar:
            renk_gruplari[tas.renk].append(tas)
        
        for renk in renk_gruplari:
            tas_listesi = sorted(renk_gruplari[renk], key=lambda t: t.deger)
            benzersiz_degerler = sorted(list(set(t.deger for t in tas_listesi)))
            
            for i in range(len(benzersiz_degerler) - min_sayi + 1):
                for j in range(i + min_sayi - 1, len(benzersiz_degerler)):
                    aday_degerler = benzersiz_degerler[i:j+1]
                    bosluk = (aday_degerler[-1] - aday_degerler[0] + 1) - len(aday_degerler)
                    if bosluk <= len(jokerler):
                        aday_per = [t for t in tas_listesi if t.deger in aday_degerler] + jokerler[:bosluk]
                        if Rules.per_dogrula(aday_per, gorev):
                            return aday_per
    
    elif "Küt" in gorev:
        deger_gruplari = defaultdict(list)
        for tas in normal_taslar:
            deger_gruplari[tas.deger].append(tas)

        for deger in deger_gruplari:
            if len(deger_gruplari[deger]) + len(jokerler) >= min_sayi:
                aday_per = deger_gruplari[deger] + jokerler[:min_sayi - len(deger_gruplari[deger])]
                if Rules.per_dogrula(aday_per, gorev):
                    return aday_per
    
    elif gorev == "Çift":
        acilacak_per = en_iyi_ciftleri_bul(el, gorev)
        if acilacak_per:
            return acilacak_per

    for boyut in range(min_sayi, len(el) + 1):
        for kombo in combinations(el, boyut):
            if Rules.per_dogrula(list(kombo), gorev):
                return list(kombo)
    
    return None