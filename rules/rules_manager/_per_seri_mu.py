# rules/rules_manager/_per_seri_mu.py
from log import logger

@logger.log_function
def _per_seri_mu(per):
    renkler = set()
    for t in per:
        # Gerçek taşı (veya Joker'in temsil ettiği taşı) al
        gercek_tas = t.joker_yerine_gecen or t
        
        # Eğer hala bir joker ise (yani joker ve atanmamışsa), kontrolü atla.
        # Masadaki açılmış jokerlerin temsilcileri zaten atanmış olacağı için
        # bu kontrol, Joker'in renk alanını 'joker' olarak sete eklemesini engeller.
        if gercek_tas.renk == "joker":
             continue
             
        renkler.add(gercek_tas.renk)

    # Per sadece tek bir renk içeriyorsa geçerlidir.
    # Not: Boş perler için (olası bir hatadan korunmak için) en azından 1 renk beklenir.
    return len(renkler) <= 1