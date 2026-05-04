import java.security.SecureRandom;

public class SecureRandomOrnek {
    public static void main(String[] args) {
        SecureRandom guvenli = new SecureRandom();
        
        System.out.println("=== GÜVENLİ RASTGELE SAYILAR ===");
        System.out.println("Güvenli tamsayı: " + guvenli.nextInt());
        System.out.println("0-100 arası güvenli: " + guvenli.nextInt(100));
        
        // Rastgele byte dizisi
        byte[] rastgeleBytes = new byte[16];
        guvenli.nextBytes(rastgeleBytes);
        System.out.print("Rastgele byte dizisi: ");
        for (byte b : rastgeleBytes) {
            System.out.printf("%02X ", b);
        }
        System.out.println();
        
        // Güvenli şifre oluşturma
        String sifre = guvenliSifreUret(12);
        System.out.println("Güvenli şifre: " + sifre);
    }
    
    public static String guvenliSifreUret(int uzunluk) {
        SecureRandom rastgele = new SecureRandom();
        String karakterler = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
                           "abcdefghijklmnopqrstuvwxyz" +
                           "0123456789!@#$%^&*()_+-=[]{}|;:,.<>?";
        StringBuilder sifre = new StringBuilder();
        
        for (int i = 0; i < uzunluk; i++) {
            int index = rastgele.nextInt(karakterler.length());
            sifre.append(karakterler.charAt(index));
        }
        
        return sifre.toString();
    }
}