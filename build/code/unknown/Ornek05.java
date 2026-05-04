public class CeilOrnek {
    public static void main(String[] args) {
        System.out.println("3.2'nin tavanı: " + Math.ceil(3.2));      // 4.0
        System.out.println("3.8'in tavanı: " + Math.ceil(3.8));       // 4.0
        System.out.println("-3.2'nin tavanı: " + Math.ceil(-3.2));    // -3.0
        System.out.println("-3.8'in tavanı: " + Math.ceil(-3.8));     // -3.0
        System.out.println("5.0'ın tavanı: " + Math.ceil(5.0));       // 5.0
        
        // Pratik: Bir sınavda geçme notu hesaplama
        double puan = 67.3;
        double yuvarlanmisPuan = Math.ceil(puan);
        System.out.println("Yuvarlanmış puan: " + yuvarlanmisPuan);  // 68.0
    }
}