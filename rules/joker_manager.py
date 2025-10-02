# carco53/kut/KUT-cd894003f2d58f59637d6a552aa651b1e1f8e2f6/rules/joker_manager.py

from core.tile import Tile
from rules.per_validators import seri_mu, kut_mu
from rules.rules_manager import Rules # Rules modülünü import et
from log import logger

class JokerManager:
    @staticmethod
    @logger.log_function
    def el_ac_joker_kontrolu(game, oyuncu, secilen_taslar):
        joker = next((t for t in secilen_taslar if t.renk == "joker"), None)
        if not joker:
            return {"status": "no_joker"}
        
        diger_taslar = [t for t in secilen_taslar if t.id != joker.id]
        
        if not diger_taslar or len(diger_taslar) < 2:
            return {"status": "invalid_joker_move", "message": "Jokerle per açmak için en az iki taş daha seçmelisiniz."}
        
        is_seri_potansiyeli = len({t.renk for t in diger_taslar}) == 1
        is_kut_potansiyeli = len({t.deger for t in diger_taslar}) == 1
        
        if is_seri_potansiyeli or (is_kut_potansiyeli and len(diger_taslar) <= 3):
            return {"status": "joker_choice_needed", "options": JokerManager.joker_icin_olasi_taslar(diger_taslar), "joker": joker, "secilen_taslar": secilen_taslar}
        
        return {"status": "invalid_joker_move"}
    
    @staticmethod
    @logger.log_function
    def joker_icin_olasi_taslar(diger_taslar):
        olasi_taslar = []
        
        # Küt için (Aynı)
        if len({t.deger for t in diger_taslar}) == 1 and len(diger_taslar) <= 3:
            deger = diger_taslar[0].deger
            renkler_mevcut = {t.renk for t in diger_taslar}
            tum_renkler = ["sari", "mavi", "siyah", "kirmizi"]
            for renk in tum_renkler:
                if renk not in renkler_mevcut:
                    olasi_taslar.append(Tile(renk, deger, f"{renk}_{deger}.png"))
            return olasi_taslar

        # Seri için (Yalnızca per'i GEÇERLİ yapacak seçenekler sunulur)
        if len({t.renk for t in diger_taslar}) == 1:
            renk = diger_taslar[0].renk
            sayilar = sorted([t.deger for t in diger_taslar])
            mevcut_sayilar_set = set(sayilar)
            
            min_deger = sayilar[0]
            max_deger = sayilar[-1]
            aday_sayilar = set()
            
            # 1. ZORUNLU EKSİK TAŞLARI DOLDURMA (Min ve Max arasındaki boşluklar)
            for d in range(min_deger + 1, max_deger):
                if d not in mevcut_sayilar_set:
                    aday_sayilar.add(d)

            # 2. UÇ NOKTALARI VE DÖNGÜSEL BOŞLUKLARI EKLE (Per'i uzatma)
            bosluk_sayisi = (max_deger - min_deger + 1) - len(sayilar)
            
            # Ardışık ve tek boşluk varsa (bosluk_sayisi=1) veya tam ardışıksa (bosluk_sayisi=0)
            if bosluk_sayisi <= 1:
                
                # Döngüsel Seriyi de modifiye 1-13 olarak kontrol etmek için
                is_dongusel = 1 in mevcut_sayilar_set and 13 in mevcut_sayilar_set
                
                # Minimumdan bir önceki (1'e atlamak için 13'ü ekler)
                if min_deger > 1 or is_dongusel: 
                    aday_sayilar.add(min_deger - 1 if min_deger > 1 else 13)

                # Maksimumdan bir sonraki (13'ten sonra 1'i ekler)
                if max_deger < 13 or is_dongusel:
                    aday_sayilar.add(max_deger + 1 if max_deger < 13 else 1)
            
            # Final kontrol: Joker'in temsilci olarak seçilmesiyle oluşan per, genel kurala uymalı.
            joker_test_listesi = []
            for deger in sorted(list(aday_sayilar)):
                if 1 <= deger <= 13:
                    joker_temsilci = Tile(renk, deger, f"{renk}_{deger}.png")
                    joker_mock = Tile("joker", 0, "joker.png")
                    joker_mock.joker_yerine_gecen = joker_temsilci
                    test_per = diger_taslar + [joker_mock]
                    
                    if Rules.genel_per_dogrula(test_per):
                        joker_test_listesi.append(joker_temsilci)
            
            return joker_test_listesi

        return []