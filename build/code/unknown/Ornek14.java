import java.util.Random;

public class GaussianOrnek {
    public static void main(String[] args) {
        Random rastgele = new Random();
        
        // Normal dağılım (ortalama=0, std=1)
        System.out.println("Normal dağılım örnekleri:");
        for (int i = 0; i < 10; i++) {
            double gaussian = rastgele.nextGaussian();
            System.out.printf("%.3f ", gaussian);
        }
        System.out.println();
        
        // Belirli ortalama ve standart sapma için dönüşüm
        double ortalama = 75.0;  // Sınav notu ortalaması
        double stdSapma = 10.0;  // Standart sapma
        
        System.out.println("\nSınav notu simülasyonu (ort=75, std=10):");
        for (int i = 0; i < 5; i++) {
            double not = ortalama + stdSapma * rastgele.nextGaussian();
            // Notu 0-100 arasında sınırla
            not = Math.max(0, Math.min(100, not));
            System.out.printf("%.1f ", not);
        }
        System.out.println();
    }
}