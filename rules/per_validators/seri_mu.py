# rules/per_validators/seri_mu.py
from log import logger

#@logger.log_function
def seri_mu(taslar, min_sayi=3):
    if len(taslar) < min_sayi: return False
    renk, sayilar, joker_sayisi = None, [], 0
    for t in taslar:
        gercek_tas = t.joker_yerine_gecen or t
        if t.renk == "joker" and not t.joker_yerine_gecen:
            joker_sayisi += 1
            continue
        if renk is None: renk = gercek_tas.renk
        elif gercek_tas.renk != renk: return False
        sayilar.append(gercek_tas.deger)
    if not sayilar: return joker_sayisi >= min_sayi
    if len(set(sayilar)) != len(sayilar): return False
    sayilar.sort()
    
    # DÖNGÜSEL SERİ KONTROLÜ
    is_dongusel = 1 in sayilar and 13 in sayilar
    if is_dongusel:
        # 1'leri 14'e dönüştürerek sürekli bir dizi olup olmadığını kontrol et.
        dongusel_kopya = sorted([14 if s == 1 else s for s in sayilar])
        
        # Gereken boşluk: (Maksimum Değer - Minimum Değer + 1) - Gerçek Taş Sayısı
        # Bu, dizideki ardışık olmayan boşlukların sayısını verir.
        gereken_bosluk = (dongusel_kopya[-1] - dongusel_kopya[0] + 1) - len(dongusel_kopya)
        
        # Eğer joker sayısı gereken boşluğu kapatmaya yetiyorsa, geçerlidir.
        # Örn: [12, 13, 1] -> [12, 13, 14]. Boşluk = 0.
        # Örn: [1, 13] -> [13, 14]. Boşluk = 0. (Bu, 2 taşla seri olmaz, ancak JokerManager'da 2 taşla per açmak zaten kısıtlıdır.)
        # Örn: [1, 2, 13] -> [2, 13, 14]. Boşluk = 10. Çok fazla.
        if joker_sayisi >= gereken_bosluk: 
             return True

    # NORMAL SERİ KONTROLÜ
    gereken_bosluk_normal = (sayilar[-1] - sayilar[0] + 1) - len(sayilar)
    return joker_sayisi >= gereken_bosluk_normal