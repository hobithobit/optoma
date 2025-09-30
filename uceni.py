import time
from smartcard.System import readers
from smartcard.Exceptions import NoCardException
import card_manager

def learn_master_cards():
    r = readers()
    if not r:
        print("❌ Žádná čtečka karet nenalezena!")
        return

    reader = r[0]
    print(f"✅ Používám čtečku: {reader}")
    connection = reader.createConnection()

    cards_to_learn = ["Master Card", "Super Card"]
    learned_cards = {}

    for card_name in cards_to_learn:
        print(f"📌 Přiložte kartu: {card_name}")
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
                print(f"⚠️ Chyba čtení karty: {e}")
                time.sleep(0.5)
                continue

            if sw1 == 0x90 and sw2 == 0x00:
                uid = "".join([f"{x:02X}" for x in data])
                print(f"🟢 Detekována karta UID: {uid} ({card_name})")
                
                # uložíme kartu do databáze
                card_manager.set_master_card(uid) if card_name == "Master Card" else card_manager.set_super_card(uid)
                learned_cards[card_name] = uid
                print(f"✅ {card_name} byla nastavena: {uid}")
                break

            time.sleep(0.5)

    print("🎉 Všechny hlavní karty byly naučeny:")
    for name, uid in learned_cards.items():
        print(f"{name}: {uid}")

if __name__ == "__main__":
    learn_master_cards()
