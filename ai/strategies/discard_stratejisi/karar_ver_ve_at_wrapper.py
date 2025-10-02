# ai/strategies/discard_stratejisi/karar_ver_ve_at_wrapper.py
from log import logger
from ai.strategies.planlama_stratejisi.eli_analiz_et import eli_analiz_et
from ai.strategies.planlama_stratejisi.en_akilli_ati_bul import en_akilli_ati_bul

@logger.log_function
def karar_ver_ve_at_wrapper(ai_player, game):
    if not ai_player.el: return None
    oyun_analizi = eli_analiz_et(ai_player.el)
    
    # NOTE: en_akilli_ati_bul fonksiyonu, el, oyun_analizi ve atilan_taslar (veya None) bekler.
    atilan_tas = en_akilli_ati_bul(ai_player.el, oyun_analizi, game.atilan_taslar)
    return atilan_tas