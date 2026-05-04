// Problem: Hem java.util.Date hem java.sql.Date kullanılacak
// Çözüm: Birini import et, diğerini tam nitelikli isimle kullan

import java.util.Date;  // Birini import et

public class TarihIslemleri {
    public void tarihleriKarsilastir() {
        Date utilDate = new Date();  // java.util.Date
        
        // java.sql.Date için tam nitelikli isim
        java.sql.Date sqlDate = new java.sql.Date(System.currentTimeMillis());
        
        System.out.println("Util Date: " + utilDate);
        System.out.println("SQL Date: " + sqlDate);
    }
}