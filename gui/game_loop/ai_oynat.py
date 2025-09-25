# gui/game_loop/ai_oynat.py

from core.game_state import GameState
from ai.ai_player import AIPlayer
from log import logger

def ai_oynat(arayuz):
    oyun = arayuz.oyun
    if oyun.oyun_bitti_mi():
        arayuz.arayuzu_guncelle()
        return

    if oyun.oyun_durumu == GameState.ATILAN_TAS_DEGERLENDIRME:
        degerlendiren_idx = oyun.atilan_tas_degerlendirici.siradaki()
        if isinstance(oyun.oyuncular[degerlendiren_idx], AIPlayer):
            ai_oyuncu = oyun.oyuncular[degerlendiren_idx]
            atilan_tas = oyun.atilan_taslar[-1]
            if ai_oyuncu.atilan_tasi_degerlendir(oyun, atilan_tas):
                oyun.atilan_tasi_al(degerlendiren_idx)
            else:
                oyun.atilan_tasi_gecti()
            arayuz.arayuzu_guncelle()

    elif oyun.oyun_durumu in [GameState.NORMAL_TUR, GameState.NORMAL_TAS_ATMA]:
        sira_index = oyun.sira_kimde_index
        if sira_index != 0 and isinstance(oyun.oyuncular[sira_index], AIPlayer):
            ai_oyuncu = oyun.oyuncular[sira_index]

            if oyun.oyun_durumu == GameState.NORMAL_TUR:
                oyun.desteden_cek(sira_index)
                if oyun.oyun_bitti_mi(): return
                arayuz.arayuzu_guncelle()

            elini_acti_mi = oyun.acilmis_oyuncular[sira_index]

            # --- YENİ BİRLEŞTİRİLMİŞ İKİNCİL HAMLE DÖNGÜSÜ ---
            # AI, bir hamle yaptığı sürece (el açma, işleme, yeni el açma) döngü devam eder.
            action_performed_in_loop = True
            while action_performed_in_loop:
                action_performed_in_loop = False

                # 1. GÖREVİ AÇMA (İlk kez el açma, en yüksek öncelik)
                if not elini_acti_mi:
                    ac_kombo = ai_oyuncu.ai_el_ac_dene(oyun)
                    if ac_kombo:
                        oyun.el_ac(sira_index, ac_kombo)
                        arayuz.arayuzu_guncelle()
                        elini_acti_mi = True # Durumu güncelle
                        action_performed_in_loop = True
                        continue # Tekrar döngünün başına dön (işleme ve yeni el açma kontrolü için)
                
                # 2. İŞLEME / JOKER DEĞİŞTİRME (Eli açık oyuncu için, yüksek öncelik)
                # Kural: İlk el açma hamlesinin yapıldığı turda işleme yapılamaz.
                if elini_acti_mi and oyun.ilk_el_acan_tur.get(sira_index, -1) < oyun.tur_numarasi:
                    islem_hamlesi = ai_oyuncu.ai_islem_yap_dene(oyun)
                    if islem_hamlesi:
                        if islem_hamlesi.get("action_type") == "joker_degistir":
                            oyun.joker_degistir(sira_index, islem_hamlesi['sahip_idx'], islem_hamlesi['per_idx'], islem_hamlesi['tas_id'])
                        elif islem_hamlesi.get("action_type") == "islem_yap":
                            oyun.islem_yap(sira_index, islem_hamlesi['sahip_idx'], islem_hamlesi['per_idx'], islem_hamlesi['tas_id'])
                        
                        if oyun.oyun_bitti_mi(): return
                        arayuz.arayuzu_guncelle()
                        action_performed_in_loop = True
                        continue # İşleme yapıldı, döngüyü tekrarla (belki yeni bir işleme yapılabilir)

                # 3. YENİ EL AÇMA (Eli açık oyuncu için, işleme yapılmadıysa ve görev tamamlandıysa)
                # Bu kontrol, sadece önceki adımlarda bir aksiyon yapılmadıysa (action_performed_in_loop == False) ve eli açıksa çalışır.
                if elini_acti_mi and oyun.ilk_el_acan_tur.get(sira_index, -1) < oyun.tur_numarasi:
                    ac_kombo = ai_oyuncu.ai_el_ac_dene(oyun)
                    if ac_kombo:
                        oyun.el_ac(sira_index, ac_kombo)
                        if oyun.oyun_bitti_mi(): return
                        arayuz.arayuzu_guncelle()
                        action_performed_in_loop = True
                        # Yeni per açıldı, joker işleme fırsatı doğabilir, bu yüzden döngü tekrar etmeli.
                        continue
                        
            # --- DÖNGÜ SONU ---
            
            # 4. TAŞ ATMA
            if ai_oyuncu.el and oyun.oyun_durumu == GameState.NORMAL_TAS_ATMA:
                tas_to_discard = ai_oyuncu.karar_ver_ve_at(oyun)
                if tas_to_discard:
                    oyun.tas_at(sira_index, tas_to_discard.id)
                else:
                    # Atacak taş yoksa ve el açık/görev tamamlandıysa oyunu bitir
                    oyun.oyun_durumu = GameState.BITIS
                    oyun.kazanan_index = sira_index
            arayuz.arayuzu_guncelle()

    arayuz.pencere.after(750, arayuz.ai_oynat)