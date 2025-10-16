# ai/strategies/degerlendirme_stratejisi/tas_degerlendir.py
from log import logger
from itertools import combinations
from rules.rules_manager import Rules
from ai.strategies.planlama_stratejisi.eli_analiz_et import eli_analiz_et

@logger.log_function
def tas_degerlendir(ai_player, game, atilan_tas):
    # Kural 1: Açılmış per'e işleme
    if game.acilmis_oyuncular[ai_player.index]:
        for per_idx, per in enumerate(game.acilan_perler[ai_player.index]):
            if Rules.islem_dogrula(per, atilan_tas):
                logger.info(f"AI {ai_player.isim} açılmış perine taş eklemek için atılan taşı alıyor: {atilan_tas.renk}_{atilan_tas.deger}")
                return True
    else:
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