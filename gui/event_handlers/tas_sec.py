# gui/event_handlers/tas_sec.py
from log import logger

@logger.log_function
def tas_sec(arayuz, tas_id):
    if tas_id in arayuz.secili_tas_idler: 
        arayuz.secili_tas_idler.remove(tas_id)
    else: 
        arayuz.secili_tas_idler.append(tas_id)
    arayuz.arayuzu_guncelle()