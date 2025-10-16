# engine/turn_manager/atilan_tasi_al.py
from core.game_state import GameState
from log import logger

@logger.log_function
def atilan_tasi_al(game, oyuncu_index):
    """
    Oyuncunun yere atılan son taşı almasını sağlar.
    """
    if game.oyun_durumu != GameState.ATILAN_TAS_DEGERLENDIRME:
        return
    if not game.atilan_taslar:
        return
    alici_oyuncu = game.oyuncular[oyuncu_index]
    atilan_tas = game.atilan_taslar.pop()
    alici_oyuncu.tas_al(atilan_tas)
    game.turda_tas_cekildi[oyuncu_index] = True
    asil_sira_index = game.atilan_tas_degerlendirici.asilin_sirasi()
    if oyuncu_index == asil_sira_index:
        game._sira_ilerlet(oyuncu_index)
        game.oyun_durumu = GameState.NORMAL_TAS_ATMA
    else:
        ceza_tas = game.deste.tas_cek()
        if ceza_tas:
            alici_oyuncu.tas_al(ceza_tas)
        game._sira_ilerlet(asil_sira_index)
        game.oyun_durumu = GameState.NORMAL_TUR
    alici_oyuncu.el_sirala()
    game.atilan_tas_degerlendirici = None