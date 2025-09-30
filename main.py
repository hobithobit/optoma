import threading
import time
from config import MASTER_ENABLED, MASTER_URL
import requests

import card_manager
from card_reader import card_loop
from pir_monitor import pir_loop
from esp_bridge import esp_loop
from ui_server import app as flask_app

print("Inicializuji databázi...")
card_manager.init_db()

# spuštění lokálních modulů
pir_thread = threading.Thread(target=pir_loop, daemon=True)
pir_thread.start()

card_thread = threading.Thread(target=card_loop, daemon=True)
card_thread.start()

esp_thread = threading.Thread(target=esp_loop, daemon=True)
esp_thread.start()

def run_flask():
    print("Spouštím Flask server...")
    flask_app.run(host="0.0.0.0", port=5000)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# příprava skeletonu vzdálené správy
def remote_sync_loop():
    while True:
        if MASTER_ENABLED:
            try:
                # zde přijde kód pro odesílání stavu a přijímání příkazů
                # např. requests.get(f"{MASTER_URL}/status")
                pass
            except Exception as e:
                print(f"❌ Remote sync error: {e}")
        time.sleep(30)

sync_thread = threading.Thread(target=remote_sync_loop, daemon=True)
sync_thread.start()

print("Systém spuštěn. Všechny moduly běží...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Ukončuji systém...")
