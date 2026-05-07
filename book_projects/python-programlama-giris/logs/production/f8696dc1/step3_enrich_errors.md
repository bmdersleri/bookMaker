# Bölüm 5: Dosya İşlemleri ve Hata Yönetimi - Sık Yapılan Hatalar

## Hata 1: Dosyayı Kapamayı Unutmak
**Hata:** `FileInputStream` veya `FileOutputStream` kullanıldıktan sonra `close()` metodu çağrılmaz.

**Neden yapılır:** Programcılar dosya işlemi bittiğinde kaynakların otomatik temizleneceğini varsayar. Java'da garbage collector bellek temizler ama dosya tanıtıcıları (file handles) gibi sistem kaynaklarını temizlemez.

**Düzeltme:** Try-with-resources kullanın:
```java
// Yanlış
FileInputStream fis = new FileInputStream("veri.txt");
// ... işlemler ...
// fis.close() unutuldu!

// Doğru
try (FileInputStream fis = new FileInputStream("veri.txt")) {
    // ... işlemler ...
} // Otomatik kapanır
```

## Hata 2: IOException'ı Genel Exception ile Yakalamak
**Hata:** `catch (Exception e)` kullanarak tüm hataları tek bir blokta yakalamak.

**Neden yapılır:** Programcılar hata türlerini ayırt etmek istemez veya "nasıl olsa yakalarım" düşüncesiyle genel yakalama yapar.

**Düzeltme:** Spesifik exception türlerini ayrı ayrı yakalayın:
```java
// Yanlış
try {
    // dosya işlemleri
} catch (Exception e) {
    System.out.println("Hata: " + e.getMessage());
}

// Doğru
try {
    // dosya işlemleri
} catch (FileNotFoundException e) {
    System.out.println("Dosya bulunamadı: " + e.getMessage());
} catch (IOException e) {
    System.out.println("Okuma/yazma hatası: " + e.getMessage());
}
```

## Hata 3: Dosya Yolunda Platform Farklılığını Göz Ardı Etmek
**Hata:** Dosya yolunda sabit ayraç (`\` veya `/`) kullanmak.

**Neden yapılır:** Windows'ta `\`, Linux/macOS'te `/` kullanılır. Programcılar kendi platformlarına göre yazıp diğer platformlarda çalışmayacağını düşünmez.

**Düzeltme:** `File.separator` veya `Paths.get()` kullanın:
```java
// Yanlış
String yol = "C:\\Kullanıcılar\\veri.txt"; // Sadece Windows

// Doğru
String yol = "kaynaklar" + File.separator + "veri.txt";
// veya
Path yol = Paths.get("kaynaklar", "veri.txt");
```

## Hata 4: Try Bloğunda Return Kullanıp Finally'i Atlamak
**Hata:** Try bloğunda `return` kullanıldığında finally bloğunun çalışmayacağını düşünmek.

**Neden yapılır:** Programcılar `return` ifadesinin hemen metottan çıkacağını bilir ama finally'in her durumda çalıştığını unutur.

**Düzeltme:** Finally bloğunun her zaman çalıştığını hatırlayın:
```java
public int dosyaOku(String dosyaAdi) {
    try {
        FileInputStream fis = new FileInputStream(dosyaAdi);
        return fis.read(); // Burada return olsa bile
    } catch (IOException e) {
        return -1;
    } finally {
        // Bu blok her zaman çalışır
        System.out.println("Temizlik yapıldı");
    }
}
```

## Hata 5: Checked Exception'ı Görmezden Gelmek
**Hata:** Checked exception'ı boş catch bloğuyla yakalayıp hiçbir şey yapmamak.

**Neden yapılır:** Programcılar hatayı "şimdilik" görmezden gelir, sonra düzeltmeyi unutur. Veya "bu hata hiç olmaz" diye düşünür.

**Düzeltme:** En azından hatayı loglayın veya kullanıcıya bildirin:
```java
// Yanlış
try {
    FileReader fr = new FileReader("veri.txt");
} catch (FileNotFoundException e) {
    // Boş, hiçbir şey yapılmadı
}

// Doğru
try {
    FileReader fr = new FileReader("veri.txt");
} catch (FileNotFoundException e) {
    System.err.println("Dosya bulunamadı: " + e.getMessage());
    // Veya kullanıcıya bildir
    throw new RuntimeException("Kritik dosya eksik", e);
}
```