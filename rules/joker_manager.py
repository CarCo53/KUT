# rules/joker_manager.py

from core.tile import Tile
from rules.per_validators import seri_mu, kut_mu
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
        
        if is_seri_potansiyeli:
            return {"status": "joker_choice_needed", "options": JokerManager.joker_icin_olasi_taslar(diger_taslar), "joker": joker, "secilen_taslar": secilen_taslar}
        if is_kut_potansiyeli and len(diger_taslar) <= 3:
            return {"status": "joker_choice_needed", "options": JokerManager.joker_icin_olasi_taslar(diger_taslar), "joker": joker, "secilen_taslar": secilen_taslar}
        
        return {"status": "invalid_joker_move"}
    
    @staticmethod
    @logger.log_function
    def joker_icin_olasi_taslar(diger_taslar):
        olasi_taslar = []
        
        # Seri için (İç ve Dış Boşluk Kontrolü)
        if len({t.renk for t in diger_taslar}) == 1:
            renk = diger_taslar[0].renk
            sayilar = sorted([t.deger for t in diger_taslar])
            mevcut_sayilar_set = set(sayilar)
            
            min_deger = sayilar[0]
            max_deger = sayilar[-1]
            
            aday_sayilar = set()
            
            # 1. İç boşlukları bul (Örn: 1, 3, 4, 5'teki 2)
            for d in range(min_deger + 1, max_deger):
                if d not in mevcut_sayilar_set:
                    aday_sayilar.add(d)
            
            # 2. Endpoint'leri kontrol et (Hemen önü ve hemen arkası)
            # Min değerden bir önceki (Örn: 3, 4, 5'in 2'si)
            if min_deger > 1 and min_deger - 1 not in mevcut_sayilar_set:
                aday_sayilar.add(min_deger - 1)

            # Max değerden bir sonraki (Örn: 3, 4, 5'in 6'sı)
            if max_deger < 13 and max_deger + 1 not in mevcut_sayilar_set:
                aday_sayilar.add(max_deger + 1)
            
            # 3. Döngüsel Seri (12-13-1) için özel kontrol
            if 1 in mevcut_sayilar_set and 13 in mevcut_sayilar_set:
                # 12'nin eksik olduğu durum (1-13 arasına tamamlamak için)
                if 12 not in mevcut_sayilar_set:
                    aday_sayilar.add(12)
            
            
            for deger in aday_sayilar:
                 # Taşın zaten elde olmadığını varsayarak Tile oluştur
                 olasi_taslar.append(Tile(renk, deger, f"{renk}_{deger}.png"))


        # Küt için (Bu kısım zaten doğru çalışıyor)
        elif len({t.deger for t in diger_taslar}) == 1 and len(diger_taslar) <= 3:
            deger = diger_taslar[0].deger
            renkler_mevcut = {t.renk for t in diger_taslar}
            tum_renkler = ["sari", "mavi", "siyah", "kirmizi"]
            for renk in tum_renkler:
                if renk not in renkler_mevcut:
                    olasi_taslar.append(Tile(renk, deger, f"{renk}_{deger}.png"))
        
        return olasi_taslar