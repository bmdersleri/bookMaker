public class FloorOrnek {
    public static void main(String[] args) {
        System.out.println("3.2'nin tabanı: " + Math.floor(3.2));     // 3.0
        System.out.println("3.8'in tabanı: " + Math.floor(3.8));      // 3.0
        System.out.println("-3.2'nin tabanı: " + Math.floor(-3.2));   // -4.0
        System.out.println("-3.8'in tabanı: " + Math.floor(-3.8));    // -4.0
        System.out.println("5.0'ın tabanı: " + Math.floor(5.0));      // 5.0
        
        // Pratik: KDV hesaplama
        double fiyat = 99.99;
        double kdvOrani = 0.18;
        double kdvliFiyat = fiyat * (1 + kdvOrani);
        double yuvarlanmisFiyat = Math.floor(kdvliFiyat * 100) / 100;
        System.out.println("KDV'li fiyat: " + yuvarlanmisFiyat);
    }
}