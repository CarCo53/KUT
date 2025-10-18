# gui/arayuzguncelle/arayuzu_guncelle.py

import tkinter as tk
from core.game_state import GameState
from log import logger
import scoring # YENİ İMPORT

def arayuzu_guncelle(arayuz):
    oyun = arayuz.oyun
    oyuncu_index = 0 # İnsan oyuncu (Oyuncu 1)
    
    for i, oyuncu in enumerate(oyun.oyuncular):
        key = f"oyuncu_{i+1}"
        frame = arayuz.alanlar[key]
        
        # OYUNCU BİLGİSİNİN GÜNCELLENMESİ
        frame.config(text=f"{oyuncu.isim} ({len(oyuncu.el)} taş)") 
        
        for widget in frame.winfo_children():
            widget.destroy()
            
        # TAŞLARIN ÇİZİLMESİ
        for tas in oyuncu.el:
            img = arayuz.visuals.tas_resimleri.get(tas.imaj_adi)
            if img:
                label = tk.Label(frame, image=img, borderwidth=0)
                if tas.id in arayuz.secili_tas_idler and i == 0:
                    label.config(highlightthickness=3, highlightbackground="black")
                label.pack(side=tk.LEFT, padx=1, pady=1)
                if i == 0:
                    label.bind("<Button-1>", lambda e, t_id=tas.id: arayuz.tas_sec(t_id))

    # MASA VE PER ÇİZİMİ (Önceki düzeltmelerimizdeki gibi, Joker'i altın çerçeveli çiziyor)
    for widget in arayuz.masa_frame.winfo_children():
        widget.destroy()

    for oyuncu_idx, per_listesi in oyun.acilan_perler.items():
        if not per_listesi: continue
        oyuncu_adi = oyun.oyuncular[oyun.oyuncular[oyuncu_idx].index].isim 
        oyuncu_per_cercevesi = tk.Frame(arayuz.masa_frame)
        oyuncu_per_cercevesi.pack(anchor="w", pady=2)
        tk.Label(oyuncu_per_cercevesi, text=f"{oyuncu_adi}:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        for per_idx, per in enumerate(per_listesi):
            per_cerceve_dis = tk.Frame(oyuncu_per_cercevesi, borderwidth=1, relief="sunken", padx=2, pady=2)
            per_cerceve_dis.pack(side=tk.LEFT, padx=5)
            per_cerceve_dis.bind("<Button-1>", lambda e, o_idx=oyuncu_idx, p_idx=per_idx: arayuz.per_sec(o_idx, p_idx))

            for tas in per:
                if tas.joker_yerine_gecen:
                    img_adi = tas.joker_yerine_gecen.imaj_adi
                    img = arayuz.visuals.tas_resimleri.get(img_adi)
                    
                    tas_cerceve = tk.Frame(per_cerceve_dis, bg="gold", borderwidth=2, relief="groove")
                    tas_cerceve.pack(side=tk.LEFT, padx=1, pady=1)
                    
                    if img:
                        label = tk.Label(tas_cerceve, image=img, borderwidth=0)
                        label.pack()
                        label.bind("<Button-1>", lambda e, o_idx=oyuncu_idx, p_idx=per_idx: arayuz.per_sec(o_idx, p_idx))

                else:
                    img = arayuz.visuals.tas_resimleri.get(tas.imaj_adi)
                    if img:
                        label = tk.Label(per_cerceve_dis, image=img, borderwidth=0)
                        label.pack(side=tk.LEFT, padx=1, pady=1)
                        label.bind("<Button-1>", lambda e, o_idx=oyuncu_idx, p_idx=per_idx: arayuz.per_sec(o_idx, p_idx))


    # DESTE/ATILAN TAŞLARIN GÜNCELLENMESİ
    for widget in arayuz.deste_frame.winfo_children():
         if widget != arayuz.deste_sayisi_label:
            widget.destroy()
    arayuz.deste_sayisi_label.config(text=f"Kalan: {len(oyun.deste.taslar)}")
    if oyun.deste.taslar:
         img_kapali = arayuz.visuals.tas_resimleri.get("kapali.png")
         if img_kapali:
             tk.Label(arayuz.deste_frame, image=img_kapali).pack()

    arayuz.atilan_frame.config(text="Atılan Taşlar")
    if oyun.atilan_tas_degerlendirici:
        atan_oyuncu_adi = oyun.oyuncular[oyun.atilan_tas_degerlendirici.tasi_atan_index].isim
        arayuz.atilan_frame.config(text=f"Atan Oyuncu: {atan_oyuncu_adi}")
        
    for widget in arayuz.atilan_frame.winfo_children():
        widget.destroy()
    for tas in oyun.atilan_taslar:
         img = arayuz.visuals.tas_resimleri.get(tas.imaj_adi)
         if img:
             tk.Label(arayuz.atilan_frame, image=img).pack(side=tk.LEFT)

    # BUTON VE STATUS BAR GÜNCELLEMESİ
    # Normal buton durumları GameState'e göre ayarlanır.
    arayuz.button_manager.butonlari_guncelle(oyun.oyun_durumu)
    
    # -------------------------------------------------------------------------
    # KRİTİK DÜZELTME: İLK EL AÇILIŞI SONRASI ZORUNLU TAŞ ATMA KURALI
    # -------------------------------------------------------------------------
    # Oyuncu 1'in sırası ve NORMAL_TAS_ATMA durumunda (yani taş çekilmiş/alınmış, şimdi hamle sırası)
    if oyun.sira_kimde_index == oyuncu_index and oyun.oyun_durumu == GameState.NORMAL_TAS_ATMA:
        
        # Oyuncu bu turda ilk ana hamlesini yaptı mı? (oyuncu_hamle_yapti=True sadece ilk el açılışı turunda ayarlanır)
        if oyun.oyuncu_hamle_yapti[oyuncu_index]:
            # KURAL: İlk el açılışından sonra sadece taş atılabilir.
            
            # El Aç, İşleme ve Joker Değiştirme Butonlarını Kapat
            # Bu, butonlari_guncelle'nin yaptığı ayarlamayı geçersiz kılar ve taş atmayı zorlar.
            # Buton referanslarının ButtonManager içinde tanımlı olduğu varsayılmıştır.
            if hasattr(arayuz.button_manager, 'el_ac_btn'):
                arayuz.button_manager.el_ac_btn.config(state="disabled")
            if hasattr(arayuz.button_manager, 'islem_yap_btn'):
                arayuz.button_manager.islem_yap_btn.config(state="disabled")
            # Joker değiştirme butonu da kapatılmalı
            if hasattr(arayuz.button_manager, 'joker_degistir_btn'):
                arayuz.button_manager.joker_degistir_btn.config(state="disabled")
                
            # Taş At Butonunu Açık Tut
            if hasattr(arayuz.button_manager, 'tas_at_btn'):
                 arayuz.button_manager.tas_at_btn.config(state="normal")
            
            # Status Bar'ı özel olarak güncelle
            oyuncu_durum = "Görevi başarıyla açtınız. Lütfen sırayı bitirmek için bir taş atın."
            arayuz.statusbar.guncelle(f"Sıra: {oyun.oyuncular[oyun.sira_kimde_index].isim} | {oyuncu_durum}")


    if oyun.oyun_durumu == GameState.BITIS:
        # PUAN HESAPLAMA VE GÖSTERİMİ
        puanlar = scoring.puan_hesapla(oyun.oyuncular)
        
        kazanan_isim = "Bilinmiyor"
        if oyun.kazanan_index is not None:
            kazanan_isim = oyun.oyuncular[oyun.kazanan_index].isim
        
        # Sadece kaybedenlerin puanlarını göster
        puan_mesaji = ", ".join([f"{oyun.oyuncular[i].isim}: {puanlar[i]}" 
                                 for i in range(len(oyun.oyuncular)) 
                                 if oyun.kazanan_index is None or i != oyun.kazanan_index])
        
        if oyun.kazanan_index is None:
             final_mesaj = "Deste bittiği için oyun sonlandı."
        else:
             final_mesaj = f"Oyun Bitti! Kazanan: {kazanan_isim}."

        arayuz.statusbar.guncelle(f"{final_mesaj} Kalan Puanlar: {puan_mesaji}. Yeni oyuna başlayabilirsiniz.")
        # AI döngüsü durdurulur.
    else:
        # Genel Status Bar Güncellemesi (Özel durumlar hariç)
        # Eğer özel kısıtlama durumu yoksa, normal durumu göster.
        if not (oyun.sira_kimde_index == oyuncu_index and oyun.oyun_durumu == GameState.NORMAL_TAS_ATMA and oyun.oyuncu_hamle_yapti[oyuncu_index]):
            oyuncu_durum = "Açılmış" if oyun.acilmis_oyuncular[0] else f"Görev: {oyun.mevcut_gorev}"
            sira_bilgi = f"Sıra: {oyun.oyuncular[oyun.sira_kimde_index].isim}"
            if oyun.oyun_durumu == GameState.ATILAN_TAS_DEGERLENDIRME and oyun.atilan_tas_degerlendirici:
                degerlendiren_idx = oyun.atilan_tas_degerlendirici.siradaki()
                degerlendiren = oyun.oyuncular[degerlendiren_idx].isim
                sira_bilgi = f"Değerlendiren: {degerlendiren}"
            elif oyun.oyun_durumu == GameState.ILK_TUR:
                sira_bilgi += " (Taş atarak başlayın)"
            arayuz.statusbar.guncelle(f"{sira_bilgi} | {oyuncu_durum}")
        
        # OYUN BİTMEDİYSE AI DÖNGÜSÜNÜ DEVAM ETTİR
        arayuz.pencere.after(750, arayuz.ai_oynat)