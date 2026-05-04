public class LogaritmaOrnek {
    public static void main(String[] args) {
        System.out.println("ln(e): " + Math.log(Math.E));           // 1.0
        System.out.println("ln(10): " + Math.log(10));              // 2.302...
        System.out.println("log10(100): " + Math.log10(100));       // 2.0
        System.out.println("log10(1000): " + Math.log10(1000));     // 3.0
        
        // Pratik: Bir sayının kaç basamaklı olduğunu bulma
        int sayi = 12345;
        int basamakSayisi = (int)Math.log10(sayi) + 1;
        System.out.println(sayi + " sayısı " + basamakSayisi + " basamaklı");
    }
}