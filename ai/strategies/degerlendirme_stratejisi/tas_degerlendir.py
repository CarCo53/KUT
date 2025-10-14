# ai/strategies/degerlendirme_stratejisi/tas_degerlendir.py

from log import logger
from itertools import combinations
from rules.rules_manager import Rules
from ai.strategies.planlama_stratejisi.eli_analiz_et import eli_analiz_et
from ai.strategies.cift_stratejisi.tasi_cift_yapar_mi import tasi_cift_yapar_mi # Yeni Kural İçin Import

@logger.log_function
def tas_degerlendir(ai_player, game, atilan_tas):
    # Oyuncu el açmışsa (acilmis_oyuncular = True), sadece işleme kuralı uygulanır.
    if game.acilmis_oyuncular[ai_player.index]:
        # Kural 1: Açılmış per'e işleme
        for per_idx, per in enumerate(game.acilan_perler[ai_player.index]):
            if Rules.islem_dogrula(per, atilan_tas):
                logger.info(f"AI {ai_player.isim} açılmış perine taş eklemek için atılan taşı alıyor: {atilan_tas.renk}_{atilan_tas.deger}")
                return True
    
    # --- YENİ KURAL: ÇİFT GÖREVİNDE ÇİFT TAMAMLAMA ÖNCELİĞİ ---
    if game.mevcut_gorev == "Çift" and not game.acilmis_oyuncular[ai_player.index]:
        # Tasi_cift_yapar_mi fonksiyonu, atılan taşın eldeki tek bir taşı çift yapıp yapmadığını kontrol eder.
        if tasi_cift_yapar_mi(ai_player.el, atilan_tas):
            logger.info(f"AI {ai_player.isim} ÇİFT GÖREVİ için çift tamamlamak üzere atılan taşı alıyor: {atilan_tas.renk}_{atilan_tas.deger}")
            return True
    # --- KURAL SONU ---
    
    # El henüz açılmamışsa (ve Çift kuralı uygulanmadıysa veya başarısız olduysa)
    if not game.acilmis_oyuncular[ai_player.index]:
        gecici_el = ai_player.el + [atilan_tas]
        gecici_el_analizi = eli_analiz_et(gecici_el)
        
        # Kural 2: GÖREVİ TAMAMLAMA (Oyun bitirme veya el açma)
        if any(Rules.per_dogrula(list(kombo), game.mevcut_gorev) for kombo in gecici_el_analizi['seriler'] + gecici_el_analizi['uc_taslilar'] + gecici_el_analizi['dort_taslilar'] + gecici_el_analizi['ciftler']):
            logger.info(f"AI {ai_player.isim} görevi tamamlamak için atılan taşı alıyor: {atilan_tas.renk}_{atilan_tas.deger}")
            return True
        
        # Kural 3: ATILAN TAŞ, HEMEN 3'LÜ VEYA 4'LÜ GEÇERLİ BİR PER OLUŞTURMALI
        yeni_per_bulundu = False
        for boyut in [3, 4]:
            for kombo in combinations(gecici_el, boyut):
                if atilan_tas in kombo:
                    if Rules.genel_per_dogrula(list(kombo)):
                        logger.info(f"AI {ai_player.isim} en az {boyut}'lu geçerli per oluşturduğu için atılan taşı alıyor: {atilan_tas.renk}_{atilan_tas.deger}")
                        yeni_per_bulundu = True
                        break 
            if yeni_per_bulundu:
                return True

    logger.info(f"AI {ai_player.isim} atılan taşı değerlendiriyor. Almadı.")
    return False