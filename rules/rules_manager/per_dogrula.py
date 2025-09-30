# rules/rules_manager/per_dogrula.py
from rules.gorevler import GOREV_LISTESI
from rules.per_validators.kut_mu import kut_mu
from rules.per_validators.seri_mu import seri_mu
from rules.per_validators.coklu_per_dogrula import coklu_per_dogrula
from rules.per_validators.karma_per_dogrula import karma_per_dogrula
from rules.per_validators.cift_per_mu import cift_per_mu
from log import logger

#@logger.log_function
def per_dogrula(taslar, gorev):
    if gorev == "Küt 3": return len(taslar) == 3 and kut_mu(taslar, 3)
    if gorev == "Seri 3": return len(taslar) == 3 and seri_mu(taslar, 3)
    if gorev == "Küt 4": return len(taslar) == 4 and kut_mu(taslar, 4)
    if gorev == "Seri 4": return len(taslar) == 4 and seri_mu(taslar, 4)
    if gorev == "Seri 5": return len(taslar) == 5 and seri_mu(taslar, 5)
    if gorev == "2x Küt 3": return len(taslar) == 6 and coklu_per_dogrula(taslar, "küt", 3, 2)
    if gorev == "2x Seri 3": return len(taslar) == 6 and coklu_per_dogrula(taslar, "seri", 3, 2)
    if gorev == "Küt 3 + Seri 3": return len(taslar) == 6 and karma_per_dogrula(taslar, 3)
    if gorev == "2x Küt 4": return len(taslar) == 8 and coklu_per_dogrula(taslar, "küt", 4, 2)
    if gorev == "2x Seri 4": return len(taslar) == 8 and coklu_per_dogrula(taslar, "seri", 4, 2)
    if gorev == "Küt 4 + Seri 4": return len(taslar) == 8 and karma_per_dogrula(taslar, 4)
    if gorev == "Çift": return cift_per_mu(taslar)
    return False