# rules/rules_manager/__init__.py
from rules.gorevler import GOREV_LISTESI
from log import logger

# Ayırdığımız fonksiyonları içe aktar
from .per_dogrula import per_dogrula
from .genel_per_dogrula import genel_per_dogrula
from .islem_dogrula import islem_dogrula
from ._per_kut_mu import _per_kut_mu
from ._per_seri_mu import _per_seri_mu
from ._kut_islem_dogrula import _kut_islem_dogrula
from ._seri_islem_dogrula import _seri_islem_dogrula

class Rules:
    GOREVLER = GOREV_LISTESI
    @staticmethod
    def per_dogrula(taslar, gorev):
        return per_dogrula(taslar, gorev)

    @staticmethod
    #@logger.log_function
    def genel_per_dogrula(taslar):
        return genel_per_dogrula(taslar)

    @staticmethod
    @logger.log_function
    def islem_dogrula(per, tas):
        return islem_dogrula(per, tas)

    @staticmethod
    @logger.log_function
    def _per_kut_mu(per):
        return _per_kut_mu(per)

    @staticmethod
    @logger.log_function
    def _per_seri_mu(per):
        return _per_seri_mu(per)
        
    @staticmethod
    @logger.log_function
    def _kut_islem_dogrula(per, tas):
        return _kut_islem_dogrula(per, tas)

    @staticmethod
    @logger.log_function
    def _seri_islem_dogrula(per, tas):
        return _seri_islem_dogrula(per, tas)