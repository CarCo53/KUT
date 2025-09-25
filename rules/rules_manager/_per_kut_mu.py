# rules/rules_manager/_per_kut_mu.py
from log import logger

@logger.log_function
def _per_kut_mu(per):
    degerler = {t.deger for t in per if t.joker_yerine_gecen or t.renk != "joker"}
    return len(degerler) <= 1