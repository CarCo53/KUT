# carco53/kut/KUT-cd894003f2d58f59637d6a552aa651b1e1f8e2f6/ai/strategies/discard_stratejisi/en_akilli_ati_bul.py

from log import logger

@logger.log_function
def en_akilli_ati_bul(el, el_analizi, atilan_taslar):
    
    jokersiz_el = [t for t in el if t.renk != "joker"]
    if not jokersiz_el:
        return el[0] if el else None
        
    en_dusuk_puan = float('inf')
    en_kotu_tas = None

    # KORUMA LİSTESİ: El açmak için kullanılan potansiyel tüm taşları korur.
    koruma_listesi_idler = set()
    for per_list in [el_analizi["seriler"], el_analizi["uc_taslilar"], el_analizi["dort_taslilar"]]:
        for per in per_list:
            for tas in per:
                koruma_listesi_idler.add(tas.id)
                
    joker_sayisi = sum(1 for t in el if t.renk == 'joker')

    for tas in jokersiz_el:
        puan = 0
        
        # 1. KRİTİK KORUMA KURALI (Joker'li veya Jokersiz Potansiyel Per Koruma)
        if tas.id in koruma_listesi_idler:
            puan += 100
        
        # 2. YANLIŞLIKLA JOKER YERİNE GEÇECEK TAŞI ATMAMAK (Kullanıcı Hatası Çözümü)
        potansiyel_seri_kut_taslari = set()
        for per_cifti in el_analizi["ikili_potansiyeller"]["seri"] + el_analizi["ikili_potansiyeller"]["kut"]:
             for t in per_cifti:
                  potansiyel_seri_kut_taslari.add(t.id)

        if tas.id in potansiyel_seri_kut_taslari and joker_sayisi > 0:
            # Maksimum koruma puanı (AI bu taşı asla atmamalı)
            puan += 5000 
            logger.debug(f"Taş {tas.renk}_{tas.deger} Joker'le tamamlanabilir potansiyel nedeniyle YÜKSEK PUAN aldı.")
        
        # 3. MEVCUT BASİT PUANLAMA (Yakınlık ve eşleşme)
        for diger_tas in el:
            if tas.id != diger_tas.id:
                if tas.deger == diger_tas.deger: puan += 10
                if tas.renk == diger_tas.renk:
                    fark = abs(tas.deger - diger_tas.deger)
                    if fark == 1: puan += 12
                    elif fark == 2: puan += 6
        
        # 4. KENAR DEĞERLER (Atma eğilimi, puanı düşür)
        if tas.deger in [1, 13]: 
            puan -= 3

        # En düşük puana sahip taşı bul
        if puan < en_dusuk_puan:
            en_dusuk_puan, en_kotu_tas = puan, tas
            
    # Güvenli joker olmayan tek taş bulunamazsa, joker olmayan taşlardan en kötüsünü at.
    return en_kotu_tas or jokersiz_el[0]