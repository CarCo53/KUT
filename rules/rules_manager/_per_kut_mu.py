# rules/rules_manager/_per_kut_mu.py
from log import logger

@logger.log_function
def _per_kut_mu(per):
    # Düzeltme: Jokerlerin temsil ettiği taşın değerini kullan.
    degerler = set()
    for t in per:
        # Gerçek taşı veya jokerin temsil ettiği taşı al
        gercek_tas = t.joker_yerine_gecen or t
        if gercek_tas.renk == "joker": 
             continue # Joker'i kendi değeriyle sayma
        degerler.add(gercek_tas.deger)
        
    return len(degerler) <= 1