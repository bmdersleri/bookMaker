// Dosya: com/egitim/uygulama/api/KullaniciApi.java
package com.egitim.uygulama.api;

import com.egitim.uygulama.model.Kullanici;
import java.util.List;

public interface KullaniciApi {
    Kullanici kullaniciBul(Long id);
    List<Kullanici> tumKullanicilariGetir();
    Kullanici kullaniciKaydet(Kullanici kullanici);
    void kullaniciSil(Long id);
}