# engine/turn_manager/desteden_cek.py
from core.game_state import GameState
from log import logger

@logger.log_function
def desteden_cek(game, oyuncu_index):
    """
    Sırası gelen oyuncunun desteden taş çekmesini sağlar.
    """
    if not (game.oyun_durumu == GameState.NORMAL_TUR and game.sira_kimde_index == oyuncu_index):
        return False
    oyuncu = game.oyuncular[oyuncu_index]
    tas = game.deste.tas_cek()
    if tas:
        oyuncu.tas_al(tas)
        game.turda_tas_cekildi[oyuncu_index] = True
        game.oyun_durumu = GameState.NORMAL_TAS_ATMA
        oyuncu.el_sirala()
        return True
    return False