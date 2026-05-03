// Dosya: DosyaIslemleriHataDuzeltme2.java
public class DosyaIslemleriHataDuzeltme2 {
    public static void main(String[] args) {
        String satir = "1001;Ayşe;Yılmaz;85";

        String[] alanlar = satir.split(";");

        if (alanlar.length == 4) {
            System.out.println("Ad: " + alanlar[1]);
        } else {
            System.out.println("CSV satırı beklenen biçimde değil.");
        }
    }
}