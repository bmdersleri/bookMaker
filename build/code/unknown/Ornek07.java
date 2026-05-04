public class RoundOrnek {
    public static void main(String[] args) {
        System.out.println("3.2'nin yuvarlanmışı: " + Math.round(3.2));     // 3
        System.out.println("3.5'in yuvarlanmışı: " + Math.round(3.5));      // 4
        System.out.println("3.8'in yuvarlanmışı: " + Math.round(3.8));      // 4
        System.out.println("-3.2'nin yuvarlanmışı: " + Math.round(-3.2));   // -3
        System.out.println("-3.5'in yuvarlanmışı: " + Math.round(-3.5));    // -3
        System.out.println("-3.8'in yuvarlanmışı: " + Math.round(-3.8));    // -4
        
        // Not: round() float için int, double için long döndürür
        float f = 3.7f;
        double d = 3.7;
        System.out.println("float round: " + Math.round(f));   // 4 (int)
        System.out.println("double round: " + Math.round(d));  // 4 (long)
    }
}