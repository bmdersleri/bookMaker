import java.util.Random;

public class SeedOrnek {
    public static void main(String[] args) {
        // Aynı seed ile aynı sayılar üretilir
        Random r1 = new Random(42);
        Random r2 = new Random(42);
        
        System.out.println("=== AYNI SEED ===");
        System.out.println("r1: " + r1.nextInt(100));
        System.out.println("r2: " + r2.nextInt(100));  // Aynı sayı
        System.out.println("r1: " + r1.nextInt(100));
        System.out.println("r2: " + r2.nextInt(100));  // Aynı sayı
        
        // Farklı seed ile farklı sayılar
        Random r3 = new Random(100);
        System.out.println("\n=== FARKLI SEED ===");
        System.out.println("r3: " + r3.nextInt(100));
        
        // Seed kullanım alanları:
        // 1. Testlerde tekrarlanabilirlik
        // 2. Oyunlarda harita oluşturma
        // 3. Bilimsel simülasyonlar
    }
}