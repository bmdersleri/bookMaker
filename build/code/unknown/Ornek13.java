import java.util.concurrent.ThreadLocalRandom;

public class ThreadLocalRandomOrnek {
    public static void main(String[] args) {
        // Thread-safe rastgele sayı üretimi
        int sayi = ThreadLocalRandom.current().nextInt(1, 101);
        System.out.println("Thread-safe rastgele: " + sayi);
        
        // Belirli aralıkta sayı
        double ondalik = ThreadLocalRandom.current().nextDouble(0.0, 1.0);
        System.out.println("0-1 arası thread-safe: " + ondalik);
        
        // Performans karşılaştırması (tek thread'de bile avantajlı)
        long baslangic = System.nanoTime();
        for (int i = 0; i < 1000000; i++) {
            ThreadLocalRandom.current().nextInt();
        }
        long sure = System.nanoTime() - baslangic;
        System.out.println("ThreadLocalRandom süresi: " + sure + " ns");
    }
}