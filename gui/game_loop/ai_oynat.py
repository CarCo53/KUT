# gui/game_loop/ai_oynat.py

from core.game_state import GameState
from ai.ai_player import AIPlayer
from log import logger
from rules.rules_manager import Rules # Kural kontrolü için eklendi

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
            action_performed_in_loop = True
            while action_performed_in_loop:
                action_performed_in_loop = False

                # 1. GÖREVİ AÇMA (İlk kez el açma, en yüksek öncelik)
                if not elini_acti_mi:
                    ac_kombo = ai_oyuncu.ai_el_ac_dene(oyun)
                    if ac_kombo:
                        result = oyun.el_ac(sira_index, ac_kombo)

                        # KRİTİK DÜZELTME: JOKER SEÇİMİ OTOMATİKLEŞTİRME
                        if result and result.get('status') == 'joker_choice_needed':
                            
                            # YENİ AKILLI MANTIK: Olası joker seçeneklerini test ederek GEÇERLİ bir per oluşturanı seç.
                            secilen_taslar = result["secilen_taslar"]
                            joker = result["joker"]
                            secilen_deger = None
                            
                            # 1. Olası tüm seçenekleri dene
                            for option in result["options"]:
                                # Olası per kombinasyonunu oluştur (Joker'i temsilci olarak ayarla)
                                joker.joker_yerine_gecen = option 
                                
                                # Per'in geçerliliğini test et (Oyun kuralına uygun mu?)
                                if Rules.per_dogrula(secilen_taslar, oyun.mevcut_gorev):
                                    secilen_deger = option
                                    break
                                
                                # Joker temsil bilgisini temizle (Eğer geçerli değilse)
                                joker.joker_yerine_gecen = None
                            
                            # 2. Geçerli bir değer bulunduysa devam et
                            if secilen_deger:
                                logger.info(f"AI Otomatik Joker Seçimi: El açmak için jokerin yerine {secilen_deger.renk}_{secilen_deger.deger} seçildi.")
                                # Joker'in değeri ayarlanmış olmalı.
                                # Not: el_ac_joker_ile bu atamayı zaten yaptığı için, burada tekrar yapmak teknik olarak gerekli değil 
                                # ancak hata durumlarını yönetmek için bırakılabilir.
                                joker.joker_yerine_gecen = secilen_deger 
                                oyun.el_ac_joker_ile(sira_index, secilen_taslar, joker, secilen_deger)
                                result = None # Başarıyı göster
                            else:
                                # Hiçbir seçenek geçerli bir per oluşturmadıysa, başarısız say.
                                logger.error("AI Otomatik Joker Seçimi Başarısız: Geçerli joker seçeneği bulunamadı.")
                                result['status'] = 'fail'
                        
                        # Başarılı El Açma Durumu
                        # Bu if bloğu, hem manuel el açmayı hem de başarılı joker seçimini kapsar.
                        if result is None or (result and result.get('status') != 'fail'):
                            if oyun.oyun_bitti_mi(): return
                            arayuz.arayuzu_guncelle()
                            elini_acti_mi = True
                            action_performed_in_loop = True
                            continue 
                       
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
                        continue 

                # 3. YENİ EL AÇMA (Eli açık oyuncu için, işleme yapılmadıysa ve görev tamamlandıysa)
                if elini_acti_mi and oyun.ilk_el_acan_tur.get(sira_index, -1) < oyun.tur_numarasi:
                    ac_kombo = ai_oyuncu.ai_el_ac_dene(oyun)
                    if ac_kombo:
                        result = oyun.el_ac(sira_index, ac_kombo)

                        # KRİTİK DÜZELTME: JOKER SEÇİMİ OTOMATİKLEŞTİRME
                        if result and result.get('status') == 'joker_choice_needed':
                            try:
                                secilen_deger = result["options"][0] 
                                joker = result["joker"]
                                secilen_taslar = result["secilen_taslar"]
                                
                                logger.info(f"AI Otomatik Joker Seçimi: Yeni el açmak için jokerin yerine {secilen_deger.renk}_{secilen_deger.deger} seçildi.")
                                oyun.el_ac_joker_ile(sira_index, secilen_taslar, joker, secilen_deger)
                                result = None # Başarıyı göster
                            except IndexError:
                                logger.error("AI Otomatik Joker Seçimi Başarısız: Geçerli joker seçeneği bulunamadı.")
                                result['status'] = 'fail'
                                
                        if oyun.oyun_bitti_mi(): return
                        arayuz.arayuzu_guncelle()
                        action_performed_in_loop = True
                        continue
                        
            # --- DÖNGÜ SONU ---
            
            # 4. TAŞ ATMA (Döngüden çıkış her zaman buraya ulaşmalı)
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