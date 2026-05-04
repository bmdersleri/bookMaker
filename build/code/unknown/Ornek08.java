public class TrigonometriOrnek {
    public static void main(String[] args) {
        double aciDerece = 45;
        double aciRadyan = Math.toRadians(aciDerece);
        
        System.out.println("45° = " + aciRadyan + " radyan");
        System.out.println("Sin 45°: " + Math.sin(aciRadyan));
        System.out.println("Cos 45°: " + Math.cos(aciRadyan));
        System.out.println("Tan 45°: " + Math.tan(aciRadyan));
        
        // Ters trigonometrik fonksiyonlar
        double sinDeger = 0.5;
        double aci = Math.asin(sinDeger);
        System.out.println("Arcsin(0.5) = " + Math.toDegrees(aci) + "°");
        
        // Pratik: Dairenin alanı
        double yaricap = 5;
        double alan = Math.PI * Math.pow(yaricap, 2);
        System.out.println("Daire alanı: " + alan);
    }
}