# engine/action_manager/joker_degistir_global.py

from log import logger
from core.game_state import GameState

@logger.log_function
def joker_degistir_global(game, degistiren_oyuncu_idx, temsilci_tas):
    """
    Okey Taşı Alanı'nda gösterilen joker temsilci taşına tıklanarak global joker değişimi yapar.
    """
    if not game.acilmis_oyuncular[degistiren_oyuncu_idx]:
        return {"status": "fail", "message": "Elini açmadan joker alamazsınız."}
    
    el_acan_tur = game.ilk_el_acan_tur.get(degistiren_oyuncu_idx)
    if el_acan_tur is not None and game.tur_numarasi <= el_acan_tur:
        return {"status": "fail", "message": "El açtığınız turda joker alamazsınız."}
        
    if degistiren_oyuncu_idx != game.sira_kimde_index:
        return {"status": "fail", "message": "Joker değişimi sadece sıranızdayken yapılabilir."}

    # Kural: Joker değişimi, desteden/yerden taş çekildikten sonra yapılır.
    if game.oyun_durumu != GameState.NORMAL_TAS_ATMA:
        return {"status": "fail", "message": "Joker değişimi yapmadan önce desteden/yerden taş çekmelisiniz."}

    oyuncu = game.oyuncular[degistiren_oyuncu_idx]
    
    # 1. Oyuncunun elinde jokerin temsil ettiği taş var mı?
    degistirilecek_tas = next((t for t in oyuncu.el if t.renk == temsilci_tas.renk and t.deger == temsilci_tas.deger), None)
    if not degistirilecek_tas:
        return {"status": "fail", "message": f"Elinde, Okey taşının temsil ettiği {temsilci_tas.renk.capitalize()} {temsilci_tas.deger} taşı bulunmuyor."}

    # 2. Masadaki bu temsilciye sahip jokeri bul
    for per_sahibi_idx, perler in game.acilan_perler.items():
        for per_idx, per in enumerate(perler):
            for i, per_tasi in enumerate(per):
                # Jokerin temsil ettiği taş, tıklanan temsilci taş ile tam olarak aynı Tile nesnesi mi?
                if per_tasi.renk == "joker" and per_tasi.joker_yerine_gecen == temsilci_tas:
                    # Joker bulundu, değişim yapılıyor

                    joker = per.pop(i)
                    
                    # KRİTİK DÜZELTME: Global temsilciyi listeden KALDIR
                    if temsilci_tas in game.acik_joker_temsilcileri:
                        game.acik_joker_temsilcileri.remove(temsilci_tas)
                    
                    joker.joker_yerine_gecen = None
                    
                    # Taşları değiştir
                    oyuncu.tas_al(joker) 
                    oyuncu.el.remove(degistirilecek_tas) 
                    
                    per.append(degistirilecek_tas) 
                    
                    oyuncu.el_sirala()
                    game._per_sirala(per)
                    game.oyun_durumu = GameState.NORMAL_TAS_ATMA # Hamle yapıldı
                    return {"status": "success", "message": f"Joker başarıyla değiştirildi: {temsilci_tas.renk.capitalize()} {temsilci_tas.deger}!"}
                    
    return {"status": "fail", "message": "Masada bu temsilciye sahip aktif bir joker bulunamadı."}