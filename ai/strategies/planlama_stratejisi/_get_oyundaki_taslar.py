# ai/strategies/planlama_stratejisi/_get_oyundaki_taslar.py
from collections import Counter
from log import logger

@logger.log_function
def _get_oyundaki_taslar(perler):
    oyundaki_taslar = Counter()
    for per in perler:
        for tas in per:
            gercek_tas = tas.joker_yerine_gecen if tas.renk == 'joker' else tas
            if gercek_tas:
                oyundaki_taslar[(gercek_tas.tas_rengi, gercek_tas.deger)] += 1
    return oyundaki_taslar