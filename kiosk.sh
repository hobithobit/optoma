#!/bin/bash
# Počkej, než se spustí desktop a Flask server
sleep 20

# Zakázat screensaver a blanking
xset s off
xset -dpms
xset s noblank

# Spuštění Chromium v kiosk módu
/usr/bin/chromium-browser --noerrdialogs --kiosk http://127.0.0.1:5000 --incognito --disable-translate --no-first-run
