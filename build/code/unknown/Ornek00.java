// com/egitim/uygulama/model/Ogrenci.java
package com.egitim.uygulama.model;

public class Ogrenci {
    private String ad;
    private String soyad;
    private int ogrenciNo;
    
    public Ogrenci(String ad, String soyad, int ogrenciNo) {
        this.ad = ad;
        this.soyad = soyad;
        this.ogrenciNo = ogrenciNo;
    }
    
    public String getAd() {
        return ad;
    }
}