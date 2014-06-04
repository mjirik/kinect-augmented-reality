
   
Spuštění kinect serveru
======

    cd projects/gerhat/src/kinectserver/build
    ./kinect_server

Konfigurace
===========

Pro konfiguraci aplikace je ve skriptu config.py potřeba nastavit následující parametry:

* Pro kalibraci zvolit příslušné vstupní obrázky (např: obp2.jpg a obk8.jpg)
* Nastavení ip adresy pro kinect server
* Optimální LOOP_TIME
* Požadované rozměry okna pro promítání
* Složku vykreslovaných obrázků
* Adresář se složkami pro gif
* Režim aplikace (MODE = "demo" použití fakeserveru při absenci dat z kinectu, při zadání čehokoliv jiného jsou použita data z kinectu)
* Volba vykreslení dalších bodů (hlava,krk)
* Při nastavení rotate_and_scale_of_image = "yes" 
* Při nastavení spacebar_to_toggle_images == "yes" vykreslování obrázků ze složky, přepínání pomocí mezerníku
* Při nastavení spacebar_to_toggle_directory == "yes" vykreslování sekvence obrázků, přepínání mezi adresáři s obrázky pomocí mezerníku

Kalibrace
=========

* Promítnutí kalibračního obrazce na projektor (obp2.jpg) zoom 100%
* Získání obrázku z kinectu
    * Otevření ve webovém proohlížeči wsclient.html
    * Zadat ip adresu
    * Stisknout Connect
    * Zadat rgb
    * Odeslat zprávu
    * Uložit obrázek (uložit s názvem obk8.jpg)
* Spuštění skriptu automotic_calibration


Spuštění 
========

Pro spuštění samotné aplikace slouží soubor sledovani.py s obrazovým výstupem.

    python sledovani.py
    
    



Příprava video dat
==========

1) Převod videa na JPG

    Program: Free Video to JPG Converter http://www.slunecnice.cz/sw/free-video-to-jpg-converter/
    Použítí:  zvolit vstupní a výstupní adresář, volba potřebné extrakce (every frame)
  
2) Změna rozměrů obrázků

    Program: JPEG Resampler 2010 http://www.slunecnice.cz/sw/jpeg-resampler/
    Použití: zvolit zdroj a cíl, volba zmenšení na pevná šířka a výška
    
 
