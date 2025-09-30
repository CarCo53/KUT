# rules/rules_manager/islem_dogrula.py
from log import logger
from rules.rules_manager._per_seri_mu import _per_seri_mu
from rules.rules_manager._per_kut_mu import _per_kut_mu
from rules.rules_manager._kut_islem_dogrula import _kut_islem_dogrula
from rules.rules_manager._seri_islem_dogrula import _seri_islem_dogrula


#@logger.log_function
def islem_dogrula(per, tas):
    if not per or not tas: return False
    
    # ÖNEMLİ KURAL DÜZELTMESİ: Joker/Okey sadece el açma veya oyun bitirme amacıyla kullanılabilir.
    # Açılmış pere işlenemez.
    if tas.renk == "joker":
        logger.info(f"Kural İhlali Engellendi: Joker ({tas.id}) açılmış pere işlenemez.")
        return False
    
    if _per_seri_mu(per): return _seri_islem_dogrula(per, tas)
    elif _per_kut_mu(per): return _kut_islem_dogrula(per, tas)
    return False