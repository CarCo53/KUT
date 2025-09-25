# rules/rules_manager/_kut_islem_dogrula.py
from log import logger

@logger.log_function
def _kut_islem_dogrula(per, tas):
    if len(per) >= 4: return False
    per_degeri = next((t.deger for t in per if t.renk != "joker"), None)
    per_renkleri = {t.renk for t in per if t.renk != "joker"}
    if tas.renk == "joker": return True
    return tas.deger == per_degeri and tas.renk not in per_renkleri