// Dosya: DosyaIslemleriTemel.java
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class DosyaIslemleriTemel {
    public static void main(String[] args) {
        Path yol = Path.of("temel_notlar.txt");

        try (BufferedWriter writer = Files.newBufferedWriter(yol)) {
            writer.write("Java dosya işlemleri");
            writer.newLine();
            writer.write("Satır satır yazma örneği");
        } catch (IOException e) {
            System.out.println("Yazma sırasında hata oluştu.");
        }

        try (BufferedReader reader = Files.newBufferedReader(yol)) {
            String satir = reader.readLine();

            while (satir != null) {
                System.out.println(satir);
                satir = reader.readLine();
            }
        } catch (IOException e) {
            System.out.println("Okuma sırasında hata oluştu.");
        }
    }
}
