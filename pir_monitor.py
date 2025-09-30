import RPi.GPIO as GPIO
import time
from panel_control import panel_hdmi2, panel_android

PIR_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

def pir_loop():
    panel_on = False
    last_motion = time.time()
    timeout = 300  # 5 minut

    while True:
        if GPIO.input(PIR_PIN):
            if not panel_on:
                print("💡 Pohyb detekován, zapínám panel...")
                panel_hdmi2()
                panel_on = True
            last_motion = time.time()
        else:
            if panel_on and time.time() - last_motion > timeout:
                print("⏱ Timeout, vypínám panel...")
                panel_android()
                panel_on = False
        time.sleep(0.5)
