import java.util.Random;

public class RastgeleKarakterOrnek {
    public static void main(String[] args) {
        Random rastgele = new Random();
        
        // Rastgele büyük harf
        char buyukHarf = (char)('A' + rastgele.nextInt(26));
        System.out.println("Rastgele büyük harf: " + buyukHarf);
        
        // Rastgele küçük harf
        char kucukHarf = (char)('a' + rastgele.nextInt(26));
        System.out.println("Rastgele küçük harf: " + kucukHarf);
        
        // Rastgele rakam
        char rakam = (char)('0' + rastgele.nextInt(10));
        System.out.println("Rastgele rakam: " + rakam);
        
        // Rastgele string oluşturma
        String rastgeleString = rastgeleStringUret(8);
        System.out.println("Rastgele string: " + rastgeleString);
        
        // Rastgele isim oluşturma (basit)
        String[] isimler = {"Ali", "Ayşe", "Mehmet", "Zeynep", "Ahmet"};
        String[] soyisimler = {"Yılmaz", "Demir", "Çelik", "Kaya", "Öztürk"};
        String tamIsim = isimler[rastgele.nextInt(isimler.length)] + " " + 
                        soyisimler[rastgele.nextInt(soyisimler.length)];
        System.out.println("Rastgele isim: " + tamIsim);
    }
    
    public static String rastgeleStringUret(int uzunluk) {
        Random rastgele = new Random();
        String karakterler = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        StringBuilder sb = new StringBuilder();
        
        for (int i = 0; i < uzunluk; i++) {
            int index = rastgele.nextInt(karakterler.length());
            sb.append(karakterler.charAt(index));
        }
        
        return sb.toString();
    }
}