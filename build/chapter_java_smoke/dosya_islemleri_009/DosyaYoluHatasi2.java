// Dosya: DosyaYoluHatasi2.java
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class DosyaYoluHatasi2 {
    public static void main(String[] args) {
        Path yol = Path.of("veriler", "ogrenciler.csv");

        if (!Files.exists(yol)) {
            System.out.println("Dosya bulunamadı: " + yol);
            System.out.println("Çalışma klasörünü ve dosya yolunu kontrol edin.");
            return;
        }

        try (BufferedReader reader = Files.newBufferedReader(yol)) {
            String satir = reader.readLine();

            if (satir == null) {
                System.out.println("Dosya boş.");
            } else {
                System.out.println(satir);
            }
        } catch (IOException e) {
            System.out.println("Dosya okunurken hata oluştu.");
        }
    }
}
