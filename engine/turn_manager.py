# engine/turn_manager.py

from core.game_state import GameState, AtilanTasDegerlendirici
from log import logger

# Ayırdığımız fonksiyonları import et
from engine.turn_manager.tas_at import tas_at
from engine.turn_manager.desteden_cek import desteden_cek
from engine.turn_manager.atilan_tasi_al import atilan_tasi_al
from engine.turn_manager.atilan_tasi_gecti import atilan_tasi_gecti

class TurnManager:
    @staticmethod
    def tas_at(game, oyuncu_index, tas_id):
        return tas_at(game, oyuncu_index, tas_id)

    @staticmethod
    def desteden_cek(game, oyuncu_index):
        return desteden_cek(game, oyuncu_index)

    @staticmethod
    def atilan_tasi_al(game, oyuncu_index):
        return atilan_tasi_al(game, oyuncu_index)

    @staticmethod
    def atilan_tasi_gecti(game):
        return atilan_tasi_gecti(game)