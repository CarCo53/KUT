# rules/rules_manager/islem_dogrula.py
from log import logger
from rules.rules_manager._per_seri_mu import _per_seri_mu
from rules.rules_manager._per_kut_mu import _per_kut_mu
from rules.rules_manager._kut_islem_dogrula import _kut_islem_dogrula
from rules.rules_manager._seri_islem_dogrula import _seri_islem_dogrula


#@logger.log_function
def islem_dogrula(per, tas):
    if not per or not tas: return False
    
    # Kural Düzeltmesi: Jokerin işlenebilir olup olmadığı, per yapısını kontrol eden
    # alt fonksiyonlar tarafından belirlenmelidir. Jokerin sadece açılmış pere 
    # işlenmesini tamamen engellemek, eli bitirme senaryolarını kısıtlamaktadır.
    if tas.renk == "joker":
        logger.info(f"Kural Kısıtlaması Kaldırıldı: Joker ({tas.id}) ile işleme denemesi yapılıyor.")
    
    # Eğer taş bir joker ise, kontrol akışı normal şekilde devam etmeli ve 
    # aşağıdaki işlevler jokerin o perde geçerli bir taş yerine geçip geçmediğini 
    # kontrol etmelidir.
    
    if _per_seri_mu(per): return _seri_islem_dogrula(per, tas)
    elif _per_kut_mu(per): return _kut_islem_dogrula(per, tas)
    return False