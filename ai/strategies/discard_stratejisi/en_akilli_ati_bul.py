# ai/strategies/discard_stratejisi/en_akilli_ati_bul.py
from log import logger

@logger.log_function
def en_akilli_ati_bul(el, el_analizi, atilabilecek_taslar):
    # NOT: Fonksiyon imzası, AIPlayer.karar_ver_ve_at'in gerektirdiği gibi el_analizi'ni içerecek şekilde güncellendi.
    
    if not atilabilecek_taslar:
        return el[0] if el else None
    
    guvenli_liste = [t for t in atilabilecek_taslar if t.renk != 'joker']
    if not guvenli_liste:
        for t in atilabilecek_taslar:
            # Sadece yerini almamış (boş) jokerler atılabilir, ancak bu nadir ve tehlikeli bir durumdur.
            if t.renk == 'joker' and not hasattr(t, 'joker_yerine_gecen') or not t.joker_yerine_gecen:
                return t
        return atilabilecek_taslar[0]

    en_dusuk_puan = float('inf')
    en_kotu_tas = None
    
    # El analizi yapılmış olmalı (AIPlayer.karar_ver_ve_at'ten geliyor)
    if not el_analizi:
        # Analiz yoksa bile basit puanlama ile devam et (Hata durumunda geriye dönüş)
        logger.warning("en_akilli_ati_bul: el_analizi boş geldi. Basit puanlama kullanılıyor.")
        # Bu durumda kodun geri kalanı zaten basit puanlamayı yapar.

    for tas in guvenli_liste:
        puan = 0
        
        # 1. KRİTİK JOKER KORUMA KURALI (HATANIN DÜZELTİLDİĞİ KISIM)
        # Eğer taş, Joker içeren tamamlanmış bir per'in parçasıysa, atma cezası ver (puanı yükselt).
        if el_analizi:
            tum_perler = el_analizi.get('seriler', []) + el_analizi.get('uc_taslilar', []) + el_analizi.get('dort_taslilar', [])
            for per in tum_perler:
                if tas in per:
                    puan += 100  # Temel per koruması
                    
                    # Eğer per içinde Joker varsa, bu taşı atmayı engelle (Çok yüksek puan ver)
                    if any(t.renk == 'joker' for t in per):
                        puan += 5000 # Maksimum koruma puanı
                        logger.debug(f"Taş {tas.renk}_{tas.deger} Joker içeren per nedeniyle YÜKSEK PUAN aldı.")
        
        # 2. MEVCUT BASİT PUANLAMA (Yakınlık ve eşleşme)
        for diger_tas in el:
            if tas.id != diger_tas.id:
                # Aynı değer/küt (puanı yükselt - tut)
                if tas.deger == diger_tas.deger: 
                    puan += 10
                
                # Aynı renk/seri (puanı yükselt - tut)
                if tas.renk == diger_tas.renk:
                    fark = abs(tas.deger - diger_tas.deger)
                    if fark == 1: 
                        puan += 12
                    elif fark == 2: 
                        puan += 6
        
        # 3. KENAR DEĞERLER (Atma eğilimi, puanı düşür)
        if tas.deger in [1, 13]: 
            puan -= 3

        # En düşük puana sahip taşı bul (en az potansiyel/korumaya sahip taş)
        if puan < en_dusuk_puan:
            en_dusuk_puan, en_kotu_tas = puan, tas
            
    return en_kotu_tas or guvenli_liste[0]