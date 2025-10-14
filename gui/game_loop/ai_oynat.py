# gui/game_loop/ai_oynat.py

from core.game_state import GameState
from ai.ai_player import AIPlayer
from log import logger
from rules.rules_manager import Rules 

@logger.log_function
def ai_oynat(arayuz):
    oyun = arayuz.oyun
    
    if oyun.oyun_bitti_mi():
        arayuz.arayuzu_guncelle()
        return

    sira_index = oyun.sira_kimde_index
    
    # SIRA KULLANICIDA KONTROLÜ
    if sira_index == 0 and oyun.oyun_durumu not in [GameState.ATILAN_TAS_DEGERLENDIRME]:
        return

    # --- 1. ATILAN TAŞ DEĞERLENDİRME AŞAMASI ---
    if oyun.oyun_durumu == GameState.ATILAN_TAS_DEGERLENDIRME:
        
        # HATA DÜZELTİLDİ: 'atilan_tas_değerlendirici' yerine 'atilan_tas_degerlendirici' kullanılmalı.
        degerlendiren_idx = oyun.atilan_tas_degerlendirici.siradaki()

        if degerlendiren_idx == 0:
            return
        
        if isinstance(oyun.oyuncular[degerlendiren_idx], AIPlayer):
            ai_oyuncu = oyun.oyuncular[degerlendiren_idx]
            atilan_tas = oyun.atilan_taslar[-1]
            
            if ai_oyuncu.atilan_tasi_degerlendir(oyun, atilan_tas):
                oyun.atilan_tasi_al(degerlendiren_idx)
            else:
                oyun.atilan_tasi_gecti()
            
            arayuz.arayuzu_guncelle()
            arayuz.pencere.after(750, arayuz.ai_oynat)
            return
        
        return


    # --- 2. NORMAL TUR ve NORMAL TAŞ ATMA AŞAMALARI (AI'ın Hamlesi) ---
    if oyun.oyun_durumu in [GameState.NORMAL_TUR, GameState.NORMAL_TAS_ATMA]:
        if isinstance(oyun.oyuncular[sira_index], AIPlayer):
            ai_oyuncu = oyun.oyuncular[sira_index]

            # 2a. NORMAL TUR'da İse: Desteden Çek
            if oyun.oyun_durumu == GameState.NORMAL_TUR:
                oyun.desteden_cek(sira_index)
                if oyun.oyun_bitti_mi(): return
                arayuz.arayuzu_guncelle()

            elini_acti_mi = oyun.acilmis_oyuncular[sira_index]

            # 2b. İKİNCİL HAMLE DÖNGÜSÜ (Joker/İşleme/El Açma)
            action_performed_in_loop = True
            while action_performed_in_loop:
                action_performed_in_loop = False
                
                # 1. GÖREVİ AÇMA (İlk kez el açma) - EN YÜKSEK ÖNCELİK
                if not elini_acti_mi:
                    ac_kombo = ai_oyuncu.ai_el_ac_dene(oyun)
                    if ac_kombo:
                        result = oyun.el_ac(sira_index, ac_kombo)

                        # JOKER SEÇİMİ OTOMATİKLEŞTİRME
                        if result and result.get('status') == 'joker_choice_needed':
                            secilen_taslar = result["secilen_taslar"]
                            joker = result["joker"]
                            secilen_deger = None
                            
                            for option in result["options"]:
                                joker.joker_yerine_gecen = option 
                                if Rules.per_dogrula(secilen_taslar, oyun.mevcut_gorev):
                                    secilen_deger = option
                                    break
                                joker.joker_yerine_gecen = None
                            
                            if secilen_deger:
                                oyun.el_ac_joker_ile(sira_index, secilen_taslar, joker, secilen_deger)
                                result = None 
                            else:
                                result['status'] = 'fail' 

                        if result is None or (result and result.get('status') != 'fail'):
                            # GÖREV BAŞARIYLA TAMAMLANDI.
                            if oyun.oyun_bitti_mi(): return
                            arayuz.arayuzu_guncelle()
                            elini_acti_mi = True
                            break 
                
                # 2. İŞLEME / JOKER DEĞİŞTİRME (Eli açık ve ilk tur bitti)
                if elini_acti_mi and oyun.ilk_el_acan_tur.get(sira_index, -1) < oyun.tur_numarasi:
                    islem_hamlesi = ai_oyuncu.ai_islem_yap_dene(oyun)
                    if islem_hamlesi:
                        
                        if islem_hamlesi.get("action_type") == "joker_degistir_global": 
                            temsilci_tas = islem_hamlesi['temsilci_tas']
                            oyun.joker_degistir_global(sira_index, temsilci_tas)
                            action_performed_in_loop = True
                            
                        elif islem_hamlesi.get("action_type") == "islem_yap":
                            oyun.islem_yap(sira_index, islem_hamlesi['sahip_idx'], islem_hamlesi['per_idx'], islem_hamlesi['tas_id'])
                            action_performed_in_loop = True
                        
                        if oyun.oyun_bitti_mi(): return
                        if action_performed_in_loop:
                            arayuz.arayuzu_guncelle()
                            continue 
                
                # 3. YENİ EL AÇMA (Eli açık oyuncu için)
                if elini_acti_mi and oyun.ilk_el_acan_tur.get(sira_index, -1) < oyun.tur_numarasi:
                    ac_kombo = ai_oyuncu.ai_el_ac_dene(oyun)
                    if ac_kombo:
                        result = oyun.el_ac(sira_index, ac_kombo)

                        if result and result.get('status') == 'joker_choice_needed':
                             try:
                                 secilen_deger = result["options"][0] 
                                 joker = result["joker"]
                                 secilen_taslar = result["secilen_taslar"]
                                 oyun.el_ac_joker_ile(sira_index, secilen_taslar, joker, secilen_deger)
                                 result = None
                             except IndexError:
                                 result['status'] = 'fail'

                        if result is None or (result and result.get('status') != 'fail'):
                             if oyun.oyun_bitti_mi(): return
                             action_performed_in_loop = True
                             arayuz.arayuzu_guncelle()
                             continue

            # --- DÖNGÜ SONU ---
            
            # 2c. TAŞ ATMA (Oyun durumu NORMAL_TAS_ATMA olmalı)
            if ai_oyuncu.el and oyun.oyun_durumu == GameState.NORMAL_TAS_ATMA:
                tas_to_discard = ai_oyuncu.karar_ver_ve_at(oyun)
                if tas_to_discard:
                    oyun.tas_at(sira_index, tas_to_discard.id)
                else:
                    oyun.oyun_durumu = GameState.BITIS
                    oyun.kazanan_index = sira_index
            
            arayuz.arayuzu_guncelle()
            arayuz.pencere.after(750, arayuz.ai_oynat)
            return
    
    return