// Dosya: CsvAyiracHatasi2.java
public class CsvAyiracHatasi2 {
    public static void main(String[] args) {
        String satir = "1001;Ayşe;Yılmaz;85";

        String[] alanlar = satir.split(";");

        if (alanlar.length == 4) {
            System.out.println("Öğrenci adı: " + alanlar[1]);
        } else {
            System.out.println("Kayıt beklenen biçimde değil.");
        }
    }
}