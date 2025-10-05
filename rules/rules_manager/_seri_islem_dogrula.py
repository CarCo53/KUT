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
    
    # Eğer eklenecek taş Joker ise, eski mantık doğru kabul edilir (değiştirilmedi)
    if tas.renk == "joker" and not tas.joker_yerine_gecen:
        if not sayilar: return True
        if sayilar[0] > 1 and sayilar[0] - 1 not in sayilar: return True
        if sayilar[-1] < 13 and sayilar[-1] + 1 not in sayilar: return True
        if 1 in sayilar and 13 in sayilar and 12 not in sayilar: return True
        return False

    tas_degeri = tas.deger

    # YENİ MANTIK: DÖNGÜSEL SERİ UZATMA KONTROLÜ (1=14 Modeli)
    
    # Döngüsel bir per'e (1 ve 13 içeren) ekleme yapılıyor mu kontrolü, 
    # ya da 13'e 1 ya da 1'e 13 eklenerek döngü başlatılıyor mu kontrolü.
    is_dongusel = 1 in sayilar and 13 in sayilar
    
    sayilar_modifiye = list(sayilar)
    tas_degeri_modifiye = tas_degeri

    if is_dongusel or (tas_degeri == 1 and sayilar[-1] == 13) or (tas_degeri == 13 and sayilar[0] == 1):
        
        # Sayıları 14'e dönüştür (Eğer 13 varsa veya 1'e 13 ekleniyorsa)
        if 13 in sayilar or tas_degeri == 13:
             sayilar_modifiye = [14 if s == 1 else s for s in sayilar]
             sayilar_modifiye.sort()
             if tas_degeri == 1:
                 tas_degeri_modifiye = 14
        
        # Uç Kontrolü (Modifiye edilmiş sayılarla +1/-1 kontrolü)
        if tas_degeri_modifiye == sayilar_modifiye[0] - 1 or tas_degeri_modifiye == sayilar_modifiye[-1] + 1:
            
            # Kısıtlama: 12-13-1'e 2 eklenemez kuralını koru (Eski kural)
            if tas_degeri == 2 and sayilar_modifiye[-3:] == [12, 13, 14]: return False
            # Kısıtlama: 1-2-3'e 13 eklenemez kuralını koru (Eski kural)
            if tas_degeri == 13 and sayilar_modifiye[:3] == [1, 2, 3]: return False
            
            return True

    # Normal Serilere Ekleme (Orijinal check, döngüsel olmayanlar için)
    if tas_degeri == sayilar[0] - 1 or tas_degeri == sayilar[-1] + 1:
        return True
    
    # Orijinal kodda bu noktadan sonra kalan tüm karmaşık ring check'leri kaldırılmıştır.
    return False