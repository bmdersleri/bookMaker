// Dosya: CsvOgrenciKayitSistemi.java
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.Scanner;

public class CsvOgrenciKayitSistemi {
    private static final Path DOSYA_YOLU = Path.of("ogrenciler.csv");

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        boolean devam = true;

        while (devam) {
            menuYazdir();
            System.out.print("Seçiminiz: ");
            String secim = scanner.nextLine();

            if (secim.equals("1")) {
                ogrenciEkle(scanner);
            } else if (secim.equals("2")) {
                ogrencileriListele();
            } else if (secim.equals("0")) {
                devam = false;
            } else {
                System.out.println("Geçersiz seçim.");
            }
        }

        System.out.println("Program sonlandırıldı.");
        scanner.close();
    }

    public static void menuYazdir() {
        System.out.println();
        System.out.println("=== CSV Öğrenci Kayıt Sistemi ===");
        System.out.println("1 - Öğrenci ekle");
        System.out.println("2 - Öğrencileri listele");
        System.out.println("0 - Çıkış");
    }

    public static void ogrenciEkle(Scanner scanner) {
        System.out.print("Öğrenci no: ");
        String no = scanner.nextLine().trim();

        System.out.print("Ad: ");
        String ad = scanner.nextLine().trim();

        System.out.print("Soyad: ");
        String soyad = scanner.nextLine().trim();

        System.out.print("Not: ");
        String not = scanner.nextLine().trim();

        String csvSatiri = no + "," + ad + "," + soyad + "," + not;

        try (BufferedWriter writer = Files.newBufferedWriter(
                DOSYA_YOLU,
                StandardOpenOption.CREATE,
                StandardOpenOption.APPEND)) {
            writer.write(csvSatiri);
            writer.newLine();
            System.out.println("Öğrenci kaydı eklendi.");
        } catch (IOException e) {
            System.out.println("Hata: Dosyaya yazılamadı.");
        }
    }

    public static void ogrencileriListele() {
        if (!Files.exists(DOSYA_YOLU)) {
            System.out.println("Henüz kayıt dosyası yok.");
            return;
        }

        try (BufferedReader reader = Files.newBufferedReader(DOSYA_YOLU)) {
            String satir = reader.readLine();
            int sayac = 1;

            while (satir != null) {
                yazdirCsvKaydi(satir, sayac);
                sayac++;
                satir = reader.readLine();
            }
        } catch (IOException e) {
            System.out.println("Hata: Dosya okunamadı.");
        }
    }

    public static void yazdirCsvKaydi(String satir, int sira) {
        String[] alanlar = satir.split(",");

        if (alanlar.length != 4) {
            System.out.println(sira + ". kayıt beklenen biçimde değil.");
            return;
        }

        System.out.println(sira + ". öğrenci");
        System.out.println("No: " + alanlar[0]);
        System.out.println("Ad Soyad: " + alanlar[1] + " " + alanlar[2]);
        System.out.println("Not: " + alanlar[3]);
        System.out.println("---");
    }
}
