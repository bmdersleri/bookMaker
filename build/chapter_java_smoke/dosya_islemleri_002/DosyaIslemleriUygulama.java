// Dosya: DosyaIslemleriUygulama.java
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class DosyaIslemleriUygulama {
    public static void main(String[] args) {
        Path yol = Path.of("ogrenciler.csv");

        try (BufferedWriter writer = Files.newBufferedWriter(yol)) {
            writer.write("1001,Ayşe,Yılmaz,85");
            writer.newLine();
            writer.write("1002,Mehmet,Demir,72");
            writer.newLine();
            writer.write("1003,Zeynep,Kaya,90");
        } catch (IOException e) {
            System.out.println("CSV yazma sırasında hata oluştu.");
        }

        try (BufferedReader reader = Files.newBufferedReader(yol)) {
            String satir = reader.readLine();

            while (satir != null) {
                String[] alanlar = satir.split(",");

                if (alanlar.length == 4) {
                    System.out.println("No: " + alanlar[0]);
                    System.out.println("Ad Soyad: "
                            + alanlar[1] + " " + alanlar[2]);
                    System.out.println("Not: " + alanlar[3]);
                    System.out.println("---");
                }

                satir = reader.readLine();
            }
        } catch (IOException e) {
            System.out.println("CSV okuma sırasında hata oluştu.");
        }
    }
}
