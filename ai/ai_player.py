# ai/ai_player.py

from core.player import Player
from log import logger

# Ayırdığımız strateji fonksiyonlarını import et
from ai.strategies.degerlendirme_stratejisi.tas_degerlendir import tas_degerlendir
from ai.strategies.el_acma_stratejisi.el_ac_dene import el_ac_dene
from ai.strategies.islem_stratejisi.islem_yap_dene import islem_yap_dene
from ai.strategies.discard_stratejisi.karar_ver_ve_at_wrapper import karar_ver_ve_at_wrapper


class AIPlayer(Player):
    @logger.log_function
    def __init__(self, isim, index):
        super().__init__(isim, index)
        self.oyun_analizi = None

    @logger.log_function
    def atilan_tasi_degerlendir(self, game, atilan_tas):
        return tas_degerlendir(self, game, atilan_tas)

    @logger.log_function
    def ai_el_ac_dene(self, game):
        # DÜZELTME: El açmış oyuncular için kısıtlama kaldırıldı. AI her zaman hamle aramalıdır.
        return el_ac_dene(self, game)

    @logger.log_function
    def ai_islem_yap_dene(self, game):
        # DÜZELTME: El açmış oyuncular için kısıtlama kaldırıldı. AI her zaman hamle aramalıdır.
        return islem_yap_dene(self, game)

    @logger.log_function
    def karar_ver_ve_at(self, game):
        # Tüm karar verme mantığı dışarıdaki fonksiyona devredildi.
        return karar_ver_ve_at_wrapper(self, game)