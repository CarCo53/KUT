# rules/joker_manager.py
from core.tile import Tile
from rules.per_validators import seri_mu, kut_mu
from rules.rules_manager import Rules
from log import logger
from ai.strategies.cift_stratejisi._ciftleri_ve_tekleri_bul import _ciftleri_ve_tekleri_bul

class JokerManager:
    @staticmethod
    @logger.log_function
    def el_ac_joker_kontrolu(game, oyuncu, secilen_taslar):
        jokerler = [t for t in secilen_taslar if t.renk == "joker"]
        normal_taslar = [t for t in secilen_taslar if t.renk != "joker"]

        if not jokerler:
            return {"status": "no_joker"}
        
        # KRİTİK DÜZELTME: ÇİFT GÖREVİ ÖZEL MANTIĞI SADECE İLK AÇILIŞ İÇİN UYGULANMALIDIR.
        if game.mevcut_gorev == "Çift" and not game.acilmis_oyuncular[oyuncu.index]:
            
            if len(secilen_taslar) != 8:
                 return {"status": "invalid_joker_move", "message": "Çift görevi için tam olarak 8 taş seçmelisiniz."}

            ciftler, tekler = _ciftleri_ve_tekleri_bul(normal_taslar)
            
            gerekli_joker_sayisi = len(tekler)
            
            if len(jokerler) < gerekli_joker_sayisi:
                return {"status": "invalid_joker_move", "message": "Çift yapmak için yeterli Joker yok. Gereken: " + str(gerekli_joker_sayisi)}
            
            olasi_secenekler = tekler
            
            if olasi_secenekler:
                 return {"status": "joker_choice_needed", "options": olasi_secenekler, "joker": jokerler[0], "secilen_taslar": secilen_taslar}
            else:
                 tum_kalan_taslar = [t for t in oyuncu.el if t not in secilen_taslar]
                 
                 if tum_kalan_taslar:
                      # Elde kalanları sun (Kullanıcının talep ettiği esnek seçim)
                      return {"status": "joker_choice_needed", "options": tum_kalan_taslar, "joker": jokerler[0], "secilen_taslar": secilen_taslar}
                 else:
                      # Elde kalan da yoksa, sembolik bir seçim sun (UI'ı tetiklemek için)
                      return {"status": "joker_choice_needed", "options": [Tile("mavi", 1, "mavi_1.png")], "joker": jokerler[0], "secilen_taslar": secilen_taslar}

        # Eğer oyuncu elini daha önce açmışsa (acilmis_oyuncular = True), normal per kuralları uygulanır.
        # Seriler ve Kütler için orijinal mantık:
        
        is_seri_potansiyeli = len({t.renk for t in normal_taslar}) == 1
        is_kut_potansiyeli = len({t.deger for t in normal_taslar}) == 1
        
        if is_seri_potansiyeli:
            return {"status": "joker_choice_needed", "options": JokerManager.joker_icin_olasi_taslar(normal_taslar), "joker": jokerler[0], "secilen_taslar": secilen_taslar}
        if is_kut_potansiyeli and len(normal_taslar) <= 3:
            return {"status": "joker_choice_needed", "options": JokerManager.joker_icin_olasi_taslar(normal_taslar), "joker": jokerler[0], "secilen_taslar": secilen_taslar}
        
        return {"status": "invalid_joker_move"}
    
    @staticmethod
    @logger.log_function
    def joker_icin_olasi_taslar(diger_taslar):
        # ... (mevcut kod aynı kalır)
        olasi_taslar = []
        
        # Seri için
        if len({t.renk for t in diger_taslar}) == 1:
            renk = diger_taslar[0].renk
            sayilar = sorted([t.deger for t in diger_taslar])
            mevcut_sayilar_set = set(sayilar)
            min_deger, max_deger = sayilar[0], sayilar[-1]
            aday_sayilar = set()
            bosluk_sayisi = (max_deger - min_deger + 1) - len(sayilar)
            
            # İç ve dış boşlukları hesapla
            for d in range(min_deger + 1, max_deger):
                if d not in mevcut_sayilar_set: aday_sayilar.add(d)
            if bosluk_sayisi <= 1:
                is_dongusel = 1 in mevcut_sayilar_set and 13 in mevcut_sayilar_set
                if min_deger > 1 or is_dongusel: aday_sayilar.add(min_deger - 1 if min_deger > 1 else 13)
                if max_deger < 13 or is_dongusel: aday_sayilar.add(max_deger + 1 if max_deger < 13 else 1)

            for deger in sorted(list(aday_sayilar)):
                 if 1 <= deger <= 13:
                     joker_temsilci = Tile(renk, deger, f"{renk}_{deger}.png")
                     joker_mock = Tile("joker", 0, "joker.png")
                     joker_mock.joker_yerine_gecen = joker_temsilci
                     test_per = diger_taslar + [joker_mock]
                     if Rules.genel_per_dogrula(test_per): olasi_taslar.append(joker_temsilci)
        
        # Küt için
        elif len({t.deger for t in diger_taslar}) == 1 and len(diger_taslar) <= 3:
            deger = diger_taslar[0].deger
            renkler_mevcut = {t.renk for t in diger_taslar}
            tum_renkler = ["sari", "mavi", "siyah", "kirmizi"]
            for renk in tum_renkler:
                if renk not in renkler_mevcut: olasi_taslar.append(Tile(renk, deger, f"{renk}_{deger}.png"))
        
        return olasi_taslar