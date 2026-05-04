import java.util.Random;

public class RandomSinifiOrnek {
    public static void main(String[] args) {
        Random rastgele = new Random();
        
        // Farklı türlerde rastgele değerler
        System.out.println("Rastgele tamsayı: " + rastgele.nextInt());
        System.out.println("0-100 arası: " + rastgele.nextInt(101));
        System.out.println("Rastgele ondalık: " + rastgele.nextDouble());
        System.out.println("Rastgele boolean: " + rastgele.nextBoolean());
        System.out.println("Rastgele float: " + rastgele.nextFloat());
        System.out.println("Rastgele long: " + rastgele.nextLong());
        
        // Belirli aralıkta sayı üretme
        int min = 10, max = 20;
        int aralik = rastgele.nextInt(max - min + 1) + min;
        System.out.println(min + "-" + max + " arası: " + aralik);
    }
}