import time
from smartcard.System import readers
from smartcard.Exceptions import NoCardException
from esp_bridge import esp
from panel_control import panel_hdmi2, panel_android
import card_manager

MASTER_CARD_UID = "FFFFFFFF"

def card_loop():
    r = readers()
    if not r:
        print("❌ Žádná čtečka karet nenalezena!")
        return
    reader = r[0]
    print(f"✅ Používám čtečku: {reader}")
    connection = reader.createConnection()

    while True:
        try:
            connection.connect()
        except NoCardException:
            time.sleep(0.5)
            continue

        GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
        try:
            data, sw1, sw2 = connection.transmit(GET_UID)
        except Exception as e:
            print(f⚠️ Chyba čtení karty: {e}")
            time.sleep(0.5)
            continue

        if sw1 == 0x90 and sw2 == 0x00:
            uid = "".join([f"{x:02X}" for x in data])
            print(f"🎯 Detekována karta UID: {uid}")

            if uid == MASTER_CARD_UID:
                handle_master_card()
            else:
                role = card_manager.is_authorized(uid)
                if role:
                    print(f"✅ Karta autorizována, role: {role}")
                else:
                    print("❌ Nepovolená karta")
        time.sleep(1)

def handle_master_card():
    panel_hdmi2()
    esp.receive_menu_input(duration=60)
    panel_android()
    esp.set_tx_mode()
    print("🔵 Návrat do běžného režimu: Android + TX ESP")
