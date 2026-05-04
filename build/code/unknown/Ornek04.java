// KÖTÜ ÖRNEK: Aşırı static import kullanımı
import static java.lang.Math.*;
import static java.lang.System.*;
import static java.lang.Integer.*;

public class KotuOrnek {
    public void kotuKullanim() {
        // Hangi sınıftan geldiği belli değil
        out.println(MAX_VALUE);  // System.out mi? Integer.MAX_VALUE mi?
        out.println(PI);         // Açık, Math.PI olduğu belli
        out.println(parseInt("123")); // Integer.parseInt
        
        // Okunabilirlik sorunu: Kodun kaynağı belirsiz
        double sonuc = sqrt(pow(abs(-5), 2) + pow(abs(3), 2));
    }
}

// İYİ ÖRNEK: Dengeli kullanım
import static java.lang.Math.PI;
import static java.lang.Math.sqrt;
import static java.lang.Math.pow;

public class IyiOrnek {
    public void dengeliKullanim() {
        double alan = PI * pow(5, 2);  // Açık ve okunabilir
        double kok = sqrt(25);          // Matematiksel ifade doğal
        
        // System.out için static import kullanma
        System.out.println("Alan: " + alan);
        
        // Integer.parseInt için static import kullanma
        int sayi = Integer.parseInt("123");
    }
}