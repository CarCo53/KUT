# engine/turn_manager/atilan_tasi_gecti.py
from core.game_state import GameState
from log import logger

@logger.log_function
def atilan_tasi_gecti(game):
    """
    Oyuncunun yere atılan taşı pas geçmesini sağlar.
    """
    if game.oyun_durumu != GameState.ATILAN_TAS_DEGERLENDIRME:
        return
    game.atilan_tas_degerlendirici.bir_sonraki()
    if game.atilan_tas_degerlendirici.herkes_gecti_mi():
        yeni_sira_index = game.atilan_tas_degerlendirici.asilin_sirasi()
        game._sira_ilerlet(yeni_sira_index)
        game.oyun_durumu = GameState.NORMAL_TUR
        game.atilan_tas_degerlendirici = None