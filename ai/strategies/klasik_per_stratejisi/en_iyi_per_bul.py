# ai/strategies/klasik_per_stratejisi/en_iyi_per_bul.py
from itertools import combinations
from rules.rules_manager import Rules
from collections import defaultdict
from log import logger
from ai.strategies.cift_stratejisi.en_iyi_ciftleri_bul import en_iyi_ciftleri_bul

def _per_deger_hesapla(per):
    # Jokerlerin değeri 0 kabul edilir, sadece gerçek taşların sayı değeri toplanır.
    # Bu, eldeki en yüksek değerli taşları açma stratejisini destekler.
    return sum(t.deger for t in per if t.renk != 'joker')

@logger.log_function
def en_iyi_per_bul(el, gorev):
    gorev_tipi, min_sayi_str = gorev.split(' ') if ' ' in gorev else (gorev, 0)
    min_sayi = int(min_sayi_str) if min_sayi_str else 0
    
    jokerler = [t for t in el if t.renk == 'joker']
    normal_taslar = [t for t in el if t.renk != 'joker']
    
    # KRİTİK KURAL: KOLAY GÖREVLERDE (Seri 5'e kadar) MAX 1 JOKER KULLAN
    max_joker_kullanimi = 1 
    joker_limiti = min(len(jokerler), max_joker_kullanimi)
    
    aday_perler = [] # Tüm geçerli adayları tutmak için liste
    
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
                    
                    # Joker kontrolü: min(Joker limiti, bu per için gereken boşluk)
                    joker_kullan = min(joker_limiti, bosluk) 

                    if joker_kullan == bosluk:
                        aday_per = [t for t in tas_listesi if t.deger in aday_degerler] + jokerler[:joker_kullan]
                        if Rules.per_dogrula(aday_per, gorev):
                            aday_perler.append(aday_per)
    
    elif "Küt" in gorev:
        deger_gruplari = defaultdict(list)
        for tas in normal_taslar:
            deger_gruplari[tas.deger].append(tas)

        for deger in deger_gruplari:
            kalan_yer = 4 - len(deger_gruplari[deger])
            
            # Joker kullanımı: min(Joker limiti, kalan yer)
            joker_kullan = min(joker_limiti, kalan_yer) 

            if len(deger_gruplari[deger]) + joker_kullan >= min_sayi:
                aday_per = deger_gruplari[deger] + jokerler[:joker_kullan]
                if Rules.per_dogrula(aday_per, gorev):
                    aday_perler.append(aday_per)
    
    elif gorev == "Çift":
        # Çift görevi için mevcut strateji kullanılır, sonuçlar aday listesine eklenir.
        acilacak_per = en_iyi_ciftleri_bul(el, gorev)
        if acilacak_per:
            aday_perler.append(acilacak_per)


    # Geri kalan kombinasyonlar da kontrol edilir (Joker limiti burada da uygulanmalı)
    for boyut in range(min_sayi, len(el) + 1):
        for kombo in combinations(el, boyut):
            kombo_jokerler = [t for t in kombo if t.renk == 'joker']
            if len(kombo_jokerler) <= joker_limiti: # Tekrar joker limitini uygula
                 if Rules.per_dogrula(list(kombo), gorev):
                    aday_perler.append(list(kombo))
    
    
    # Tüm adaylar arasından en yüksek değere sahip olanı seç (Stratejik gereksinim)
    if aday_perler:
        # En yüksek değere sahip adayı bul
        en_iyi_per = max(aday_perler, key=_per_deger_hesapla)
        return en_iyi_per
        
    return None