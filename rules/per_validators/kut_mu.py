# rules/per_validators/kut_mu.py
from log import logger

#@logger.log_function
def kut_mu(taslar, min_sayi=3):
    if len(taslar) < min_sayi: return False
    degerler = set()
    renkler = set()
    for t in taslar:
        gercek_tas = t.joker_yerine_gecen or t
        if gercek_tas.renk == "joker": continue
        degerler.add(gercek_tas.deger)
        renkler.add(gercek_tas.renk)
    if len(renkler) != len([t for t in taslar if (t.joker_yerine_gecen or t.renk != "joker")]):
        return False
    return len(degerler) <= 1 and min_sayi <= len(taslar) <= 4