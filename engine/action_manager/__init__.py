# engine/action_manager/__init__.py

from rules.rules_manager import Rules
from rules.joker_manager import JokerManager
from core.game_state import GameState
from log import logger

# Ayırdığımız fonksiyonları import et
from .joker_degistir_global import joker_degistir_global 
from .el_ac import el_ac
from .islem_yap import islem_yap
from ._eli_ac_ve_isle import _eli_ac_ve_isle
from .joker_degistir import joker_degistir # YENİ İMPORT

class ActionManager:
    @staticmethod
    @logger.log_function
    def joker_degistir(game, degistiren_oyuncu_idx, per_sahibi_idx, per_idx, tas_id):
        return joker_degistir(game, degistiren_oyuncu_idx, per_sahibi_idx, per_idx, tas_id)
        
    @staticmethod
    @logger.log_function
    def joker_degistir_global(game, degistiren_oyuncu_idx, temsilci_tas):
        return joker_degistir_global(game, degistiren_oyuncu_idx, temsilci_tas)

    @staticmethod
    @logger.log_function
    def el_ac(game, oyuncu_index, tas_id_list):
        return el_ac(game, oyuncu_index, tas_id_list)
    
    @staticmethod
    @logger.log_function
    def _eli_ac_ve_isle(game, oyuncu_index, secilen_taslar):
        return _eli_ac_ve_isle(game, oyuncu_index, secilen_taslar)
    
    @staticmethod
    @logger.log_function
    def islem_yap(game, isleyen_oyuncu_idx, per_sahibi_idx, per_idx, tas_id):
        return islem_yap(game, isleyen_oyuncu_idx, per_sahibi_idx, per_idx, tas_id)