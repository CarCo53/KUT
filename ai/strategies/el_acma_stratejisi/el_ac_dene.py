# ai/strategies/el_acma_stratejisi/el_ac_dene.py
from log import logger
from itertools import combinations
from rules.rules_manager import Rules
from ai.strategies.planlama_stratejisi.eli_analiz_et import eli_analiz_et
from ai.strategies.klasik_per_stratejisi.en_iyi_per_bul import en_iyi_per_bul
from ai.strategies.coklu_per_stratejisi.en_iyi_coklu_per_bul import en_iyi_coklu_per_bul
from ai.strategies.cift_stratejisi.en_iyi_ciftleri_bul import en_iyi_ciftleri_bul


@logger.log_function
def el_ac_dene(ai_player, game):
    gorev = game.mevcut_gorev
    
    if not game.acilmis_oyuncular[ai_player.index]:
        if gorev == "Çift":
            acilacak_per = en_iyi_ciftleri_bul(ai_player.el, gorev)
            if acilacak_per:
                return [t.id for t in acilacak_per]
            else:
                return None
        
        elif "2x" in gorev or "+" in gorev:
            acilacak_per = en_iyi_coklu_per_bul(ai_player.el, gorev)
            if acilacak_per:
                return [t.id for t in acilacak_per]
            else:
                return None
        
        else:
            acilacak_per = en_iyi_per_bul(ai_player.el, gorev)
            if acilacak_per:
                return [t.id for t in acilacak_per]
            else:
                return None
    
    else:
        el_analizi = eli_analiz_et(ai_player.el)
        for per in el_analizi["seriler"]:
            if Rules.genel_per_dogrula(per): return [t.id for t in per]
        for per in el_analizi["uc_taslilar"] + el_analizi["dort_taslilar"]:
            if Rules.genel_per_dogrula(per): return [t.id for t in per]
        
        # Ek per açma denemesi
        for i in range(3, len(ai_player.el) + 1):
            for kombo in combinations(ai_player.el, i):
                if Rules.genel_per_dogrula(list(kombo)):
                    return [t.id for t in kombo]
    
    return None