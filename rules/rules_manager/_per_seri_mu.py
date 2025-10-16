# rules/rules_manager/_per_seri_mu.py
from log import logger

@logger.log_function
def _per_seri_mu(per):
    renkler = {t.renk for t in per if t.joker_yerine_gecen or t.renk != "joker"}
    return len(renkler) <= 1