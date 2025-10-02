# carco53/kut/KUT-cd894003f2d58f59637d6a552aa651b1e1f8e2f6/ai/strategies/degerlendirme_stratejisi/atilan_tasi_almaya_deger_mi.py

from log import logger
from core.tile import Tile
from ai.strategies.planlama_stratejisi.eli_analiz_et import eli_analiz_et
from rules.gorevler import Gorevler # Görevleri kontrol etmek için

@logger.log_function
def atilan_tasi_almaya_deger_mi(ai_oyuncu, oyun, atilan_tas):
    # Oyuncu elini açmışsa, zaten yerden taş alma hakkı yoktur, sadece Desteden çeker.
    # Bu fonksiyon sadece atan oyuncu hariç diğer 3 oyuncu için Atılan Taş Değerlendirme aşamasında çalışır.
    
    mevcut_el = ai_oyuncu.el + [atilan_tas]
    mevcut_gorev = oyun.mevcut_gorev
    
    # Yeni bir taş eklendiğinde eli analiz et
    yeni_analiz = eli_analiz_et(mevcut_el)
    
    mevcut_el_puan = ai_oyuncu.puan_el_analizi["toplam_puan"]
    yeni_el_puan = yeni_analiz["toplam_puan"]
    
    # 1. KRİTİK: ÇİFT GÖREVİ ÖNCELİĞİ
    if not oyun.acilmis_oyuncular[ai_oyuncu.index]:
        # Eğer görev Çift ise (Tekli Çift veya Çiftli Çift)
        if mevcut_gorev in [Gorevler.CIFT_3, Gorevler.CIFT_4, Gorevler.CIFT_5, Gorevler.CIFT_6, Gorevler.CIFT_7]:
            
            # Atılan taş, mevcut eldeki bir taşla çift oluşturabiliyor mu?
            cift_olusturma_potansiyeli = False
            
            # Atılan taşın id'sini geçici olarak 0 vererek çift olup olmadığını kontrol et.
            # (Tekrar eden taşları ayırt etmek için basit bir kontrol yapılır)
            atilan_tas_id = atilan_tas.id
            atilan_tas.id = 0 

            for tas in ai_oyuncu.el:
                # Normal çift
                if tas.deger == atilan_tas.deger and tas.renk == atilan_tas.renk:
                    cift_olusturma_potansiyeli = True
                    break
                # Jokerli çift (Eğer elde joker varsa ve bu joker ile bir çift oluşturulacaksa)
                if tas.renk == "joker":
                    if tas.joker_yerine_gecen:
                         if tas.joker_yerine_gecen.deger == atilan_tas.deger and tas.joker_yerine_gecen.renk == atilan_tas.renk:
                              cift_olusturma_potansiyeli = True
                              break
                    else:
                        # Joker henüz atanmamışsa, atılan taşın aynısından bir tane daha kabul edilir.
                        # Bu kuralı basitleştirelim: Atılan taşın aynısından bir tane daha elde varsa, AL!
                        # Atılan taş ile elde aynı renk ve değerde 1 taş daha varsa (çifti tamamlamak için joker yerine kullanılabilecek)
                        if sum(1 for t in ai_oyuncu.el if t.deger == atilan_tas.deger and t.renk == atilan_tas.renk) > 0:
                            cift_olusturma_potansiyeli = True
                            break
                        
            atilan_tas.id = atilan_tas_id # ID'yi geri getir
            
            if cift_olusturma_potansiyeli:
                logger.info("AI: Çift görevi önceliği nedeniyle atılan taşı alıyor.")
                return True
        
    # 2. GENEL PUANLAMA KARARI (Çift görevi dışında veya ek kontrol)
    
    # Puan artışı yeterliyse al
    if yeni_el_puan > mevcut_el_puan:
        puan_farki = yeni_el_puan - mevcut_el_puan
        
        # Eğer büyük bir puan sıçraması varsa (Örn: Per tamamlama)
        if puan_farki > 100: 
            return True
        
        # Eğer bu taşla el bitiriliyorsa kesin al
        if len(mevcut_el) == 15 and len(yeni_analiz["kullanilamayan_taslar"]) == 0:
            return True
            
        # Puan farkının eşiği (Basit eşik kuralı)
        if puan_farki > 30: 
            return True

    # Diğer durumlarda alma
    return False