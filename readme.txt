# Smart Panel - Raspberry Pi

## Popis
Tento projekt umožňuje ovládání dotykového panelu přes RPi, PIR senzor, ESP modul a čtečku karet OMNIKEY.  
Funkce zahrnují:

- Automatické zapnutí a vypnutí panelu podle pohybu (PIR)
- Čtení UID karet a odemčení systému
- Přidávání a odebírání karet přes webové rozhraní (Flask)
- ESP komunikace pro IR ovladač a zamykání/odemčení panelu
- Přepínání panelu mezi Android a HDMI2
- Bezobslužný start po bootu RPi přes systemd

---

## Instalace

1. Nahraj `smart_panel.zip` na Raspberry Pi.
2. Rozbal:

```bash
unzip smart_panel.zip -d ~/smart_panel


sudo apt update
sudo apt install python3-pip pcsc-tools pcscd python3-serial python3-rpi.gpio
sudo pip3 install flask pyscard

sudo cp ~/smart_panel/smart_panel.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable smart_panel.service
sudo systemctl start smart_panel.service

sudo apt update
sudo apt install -y chromium-browser

chmod +x ~/smart_panel/kiosk.sh

Spuštění skriptu po startu (autostart)

Otevři autostart soubor:

mkdir -p ~/.config/lxsession/LXDE-pi
nano ~/.config/lxsession/LXDE-pi/autostart


Přidej řádek na konec:

@/home/pi/smart_panel/kiosk.sh



