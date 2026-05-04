public class MathRandomTemel {
    public static void main(String[] args) {
        // Temel kullanım
        double rastgele = Math.random();
        System.out.println("0-1 arası rastgele: " + rastgele);
        
        // Belirli aralıkta sayı üretme formülü:
        // (int)(Math.random() * (max - min + 1)) + min
        
        // 1-10 arası tamsayı
        int birOn = (int)(Math.random() * 10) + 1;
        System.out.println("1-10 arası: " + birOn);
        
        // 50-100 arası tamsayı
        int elliYuz = (int)(Math.random() * 51) + 50;
        System.out.println("50-100 arası: " + elliYuz);
        
        // 0-100 arası çift sayı
        int ciftSayi = (int)(Math.random() * 51) * 2;
        System.out.println("0-100 arası çift: " + ciftSayi);
    }
}