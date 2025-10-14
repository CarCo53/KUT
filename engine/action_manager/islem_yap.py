# engine/action_manager/islem_yap.py
from log import logger
from core.game_state import GameState
from rules.rules_manager import Rules

@logger.log_function
def islem_yap(game, isleyen_oyuncu_idx, per_sahibi_idx, per_idx, tas_id):
    el_acan_tur = game.ilk_el_acan_tur.get(isleyen_oyuncu_idx)
    if el_acan_tur is not None and game.tur_numarasi <= el_acan_tur:
        # Kural Güçlendirmesi
        logger.warning(f"Oyuncu {isleyen_oyuncu_idx} elini açtığı turda işleme yapamaz. Sadece taş atabilir.")
        return False

    if not game.acilmis_oyuncular[isleyen_oyuncu_idx] or isleyen_oyuncu_idx != game.sira_kimde_index:
        return False
        
    oyuncu = game.oyuncular[isleyen_oyuncu_idx]
    tas = next((t for t in oyuncu.el if t.id == tas_id), None)
    if not tas: return False
    
    per = game.acilan_perler[per_sahibi_idx][per_idx]
    
    if Rules.islem_dogrula(per, tas):
        oyuncu.tas_at(tas.id)
        per.append(tas)
        game._per_sirala(per)
        game.oyun_durumu = GameState.NORMAL_TAS_ATMA
        if not oyuncu.el:
            game.oyun_durumu = GameState.BITIS
            game.kazanan_index = isleyen_oyuncu_idx
        return True
    return False