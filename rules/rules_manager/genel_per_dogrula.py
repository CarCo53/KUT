# rules/rules_manager/genel_per_dogrula.py
from log import logger
from rules.per_validators.kut_mu import kut_mu
from rules.per_validators.seri_mu import seri_mu

#@logger.log_function
def genel_per_dogrula(taslar):
    if len(taslar) < 3: return False
    return kut_mu(taslar, len(taslar)) or seri_mu(taslar, len(taslar))