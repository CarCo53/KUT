# engine/turn_manager/tas_at.py
from core.game_state import GameState, AtilanTasDegerlendirici
from log import logger

@logger.log_function
def tas_at(game, oyuncu_index, tas_id):
    """
    Oyuncunun elindeki bir taşı yere atmasını sağlar.
    """
    oyuncu = game.oyuncular[oyuncu_index]
    if not oyuncu.el and game.acilmis_oyuncular[oyuncu_index]:
        game.oyun_durumu = GameState.BITIS
        game.kazanan_index = oyuncu_index
        return True
    if game.oyun_durumu not in [GameState.ILK_TUR, GameState.NORMAL_TAS_ATMA]:
        return False
    if oyuncu_index != game.sira_kimde_index:
        return False
    atilan_tas = oyuncu.tas_at(tas_id)
    if atilan_tas:
        game.atilan_taslar.append(atilan_tas)
        if game.acilmis_oyuncular[oyuncu_index] and not oyuncu.el:
            game.oyun_durumu = GameState.BITIS
            game.kazanan_index = oyuncu_index
            return True

        game.oyuncu_hamle_yapti = [False] * len(game.oyuncular)

        game.oyun_durumu = GameState.ATILAN_TAS_DEGERLENDIRME
        game.atilan_tas_degerlendirici = AtilanTasDegerlendirici(oyuncu_index, len(game.oyuncular))
        game.turda_tas_cekildi[oyuncu_index] = False
        return True
    return False