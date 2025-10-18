# rules/rules_manager/_per_seri_mu.py
from log import logger

@logger.log_function
def _per_seri_mu(per):
    # Düzeltme: Jokerlerin temsil ettiği taşın rengini kullan.
    renkler = set()
    for t in per:
        # Gerçek taşı veya jokerin temsil ettiği taşı al
        gercek_tas = t.joker_yerine_gecen or t
        if gercek_tas.renk == "joker": 
             continue # Joker'i kendi rengiyle sayma
        renkler.add(gercek_tas.renk)
        
    return len(renkler) <= 1