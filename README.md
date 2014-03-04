Spuštění aplikace 
========================

Kalibraci spustíme prostřednictvím souboru kalibrace2.py. Výstupem toho programu je kalibrační matice.

    python kalibrace2.py



Pro spuštění samotné aplikace slouží soubor sledovani.py s obrazovým výstupem.

    python sledovani.py
   
Spuštění kinect serveru
======

    cd projects/gerhat/src/kinectserver/build
    ./kinect_server

Získání obrázku
======

    stazene/openNI/.../samples/bin/x64-release
    ./sample
    
    m - obrací směr
    3 - zobrazí RGB kameru
    1 - hloubková mapa

Příprava video dat
==========

1)Převod videa na JPG
    Program: Free Video to JPG Converter http://www.slunecnice.cz/sw/free-video-to-jpg-converter/
    Použítí:  zvolit vstupní a výstupní adresář, volba potřebné extrakce (every frame)
  
2)Změna rozměrů obrázků
    Program: JPEG Resampler 2010 http://www.slunecnice.cz/sw/jpeg-resampler/
    Použití: zvolit zdroj a cíl, volba zmenšení na pevná šířka a výška
    
 
