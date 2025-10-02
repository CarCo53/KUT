# rules/rules_manager/_seri_islem_dogrula.py

from log import logger
from core.tile import Tile

@logger.log_function
def _seri_islem_dogrula(per, tas):
    if len(per) >= 14: return False
    
    # 1. Per rengi ve sayılarının çıkarılması
    per_tasi_listesi = [t for t in per if t.renk != "joker" or (t.renk == "joker" and t.joker_yerine_gecen is not None)]
    if not per_tasi_listesi:
        if tas.renk == "joker" and not tas.joker_yerine_gecen: return True
        return False

    per_rengi = per_tasi_listesi[0].renk
    if tas.renk != "joker" and tas.renk != per_rengi: return False

    sayilar = []
    for t in per:
        deger = (t.joker_yerine_gecen or t).deger if t.renk != "joker" or t.joker_yerine_gecen is not None else None
        if deger is not None:
            sayilar.append(deger)
    
    sayilar.sort()
    
    # 2. Joker Ekleme Kontrolü (Taşın kendisi joker ise)
    if tas.renk == "joker" and not tas.joker_yerine_gecen:
        if not sayilar: return True 
        
        is_dongusel = 1 in sayilar and 13 in sayilar
        
        # 1'i 14 olarak ele alarak uç noktalara ve boşluklara joker eklenebilir mi kontrolü
        sayilar_temp = [14 if s == 1 and is_dongusel else s for s in sayilar]
        sayilar_temp.sort()

        if sayilar_temp[0] > 1 or sayilar_temp[-1] < 14: 
            return True
        
        for i in range(len(sayilar_temp) - 1):
             if sayilar_temp[i+1] - sayilar_temp[i] > 1: return True
             
        return False
        
    tas_degeri = tas.deger

    # 3. TAŞ İŞLEME KONTROLÜ (1=14 Modeli ile)
    
    is_dongusel = 1 in sayilar and 13 in sayilar
    sayilar_modifiye = list(sayilar)
    tas_degeri_modifiye = tas_degeri

    if is_dongusel:
        # Döngüsel serilerde 1'i 14 olarak kabul et
        sayilar_modifiye = [14 if s == 1 else s for s in sayilar]
        sayilar_modifiye.sort()
        
        if tas_degeri == 1:
            tas_degeri_modifiye = 14
            
        # Kısıtlamalar: Serinin iki ucundan aynı anda genişletilmesi kuralını uygula.
        # Bu, serinin '13-1-2-3' gibi dairesel olarak devam etmesini engeller.
        if len(sayilar) >= 3:
            # 1-2-3 serisine 13 eklenemez:
            if sayilar_modifiye[:3] == [1, 2, 3] and tas_degeri == 13: return False
            # 12-13-1 serisine 2 eklenemez:
            if sayilar_modifiye[-3:] == [12, 13, 14] and tas_degeri == 2: return False
        
        # MODİFİYE EDİLMİŞ SERİYE UYUM KONTROLÜ (Uç noktalara eklenebilir mi?)
        if tas_degeri_modifiye == sayilar_modifiye[0] - 1 or tas_degeri_modifiye == sayilar_modifiye[-1] + 1:
            return True
            
        return False

    # Normal Seriler (Döngüsel olmayan)
    if tas_degeri == sayilar[0] - 1 or tas_degeri == sayilar[-1] + 1:
        return True
    
    return False