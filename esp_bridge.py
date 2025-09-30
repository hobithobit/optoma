import serial
import serial.tools.list_ports
import time

class ESPBridge:
    def __init__(self):
        self.port = self.find_esp_port()
        if not self.port:
            print("❌ ESP nenalezeno!")
            self.ser = None
        else:
            self.ser = serial.Serial(self.port, 115200, timeout=1)
            print(f"✅ ESP připojeno na {self.port}")
            self.set_tx_mode()

    def find_esp_port(self):
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if "USB" in p.device:
                return p.device
        return None

    def send_command(self, cmd):
        if self.ser:
            self.ser.write((cmd + "\r").encode())
            print(f"ESP >> {cmd}")

    def set_tx_mode(self):
        self.send_command("MODE TX")
        print("📡 Režim TX aktivní")

    def set_rx_mode(self):
        self.send_command("MODE RX")
        print("📡 Režim RX aktivní")

    def send_sc_lock(self):
        self.send_command("SEND SC_LOCK")

    def receive_menu_input(self, duration=30):
        if not self.ser:
            return
        self.set_rx_mode()
        start = time.time()
        try:
            while time.time() - start < duration:
                if self.ser.in_waiting > 0:
                    data = self.ser.readline().decode().strip()
                    print(f"IR tlačítko >> {data}")
        finally:
            self.set_tx_mode()

esp = ESPBridge()

def esp_loop():
    while True:
        time.sleep(1)
