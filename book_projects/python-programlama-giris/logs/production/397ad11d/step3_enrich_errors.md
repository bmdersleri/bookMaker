# Fonksiyonlar ve Modüller: Yaygın Hatalar

## Hata 1: Değişken Kapsamı (Scope) Karışıklığı
**Hata:** Fonksiyon içinde tanımlanan değişkenin fonksiyon dışında da erişilebilir olduğunu sanmak.
**Neden:** Yeni başlayanlar, tüm değişkenlerin aynı düzeyde olduğunu varsayar.
**Düzeltme:** Fonksiyon içinde tanımlanan değişkenler yereldir (local scope). Fonksiyon dışında kullanmak için `return` ile değer döndürülmeli veya `global` anahtar kelimesi kullanılmalıdır.

```python
# Yanlış
def topla(a, b):
    sonuc = a + b  # sonuc yerel değişkendir

topla(3, 5)
print(sonuc)  # NameError: name 'sonuc' is not defined

# Doğru
def topla(a, b):
    return a + b

sonuc = topla(3, 5)
print(sonuc)  # 8
```

## Hata 2: Mutable Varsayılan Argüman Kullanımı
**Hata:** Varsayılan argüman olarak liste veya sözlük gibi değişebilir (mutable) nesneler kullanmak.
**Neden:** Varsayılan argümanlar fonksiyon tanımlandığında bir kez oluşturulur ve her çağrıda aynı nesne kullanılır.
**Düzeltme:** Varsayılan değer olarak `None` kullanın ve fonksiyon içinde kontrol ederek yeni bir mutable nesne oluşturun.

```python
# Yanlış
def ogrenci_ekle(isim, liste=[]):
    liste.append(isim)
    return liste

print(ogrenci_ekle("Ali"))    # ['Ali']
print(ogrenci_ekle("Veli"))   # ['Ali', 'Veli']  # Beklenmeyen!

# Doğru
def ogrenci_ekle(isim, liste=None):
    if liste is None:
        liste = []
    liste.append(isim)
    return liste

print(ogrenci_ekle("Ali"))    # ['Ali']
print(ogrenci_ekle("Veli"))   # ['Veli']
```

## Hata 3: `*args` ve `**kwargs` Sıralamasını Karıştırmak
**Hata:** Fonksiyon parametrelerini yanlış sırada tanımlamak.
**Neden:** Python'da parametre sıralaması belirli bir kurala bağlıdır: normal parametreler, `*args`, varsayılan parametreler, `**kwargs`.
**Düzeltme:** Doğru sıralamayı öğrenin ve uygulayın.

```python
# Yanlış
def hata_fonksiyon(*args, a, b=5, **kwargs):  # SyntaxError
    pass

# Doğru
def dogru_fonksiyon(a, b=5, *args, **kwargs):
    pass
```

## Hata 4: Lambda İfadelerini Aşırı Karmaşıklaştırmak
**Hata:** Lambda içinde birden fazla işlem, döngü veya koşul kullanmaya çalışmak.
**Neden:** Lambda'nın tek ifade (expression) olması gerektiğini unutmak.
**Düzeltme:** Lambda yalnızca tek bir ifade için kullanılmalıdır. Karmaşık işlemler için normal fonksiyon tanımlayın.

```python
# Yanlış
islem = lambda x: x**2 if x > 0 else x * -1 if x < 0 else 0  # Okunamaz!

# Doğru
def mutlak_deger(x):
    if x > 0:
        return x
    elif x < 0:
        return -x
    return 0

# Veya basit lambda
kare = lambda x: x**2
```

## Hata 5: Modül İçe Aktarırken `__name__ == "__main__"` Kontrolünü Atlamak
**Hata:** Modül içindeki test kodlarını doğrudan çalıştırmak ve modül içe aktarıldığında da bu kodların çalışması.
**Neden:** Modülün hem bağımsız çalıştırıldığında hem de içe aktarıldığında aynı davranışı göstereceğini varsaymak.
**Düzeltme:** Test kodlarını `if __name__ == "__main__":` bloğu içine alın.

```python
# Yanlış (hesap.py)
def topla(a, b):
    return a + b

print(topla(3, 5))  # Modül içe aktarıldığında da çalışır!

# Doğru (hesap.py)
def topla(a, b):
    return a + b

if __name__ == "__main__":
    print(topla(3, 5))  # Sadece doğrudan çalıştırıldığında çalışır
```