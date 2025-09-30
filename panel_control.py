import serial

er = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

def panel_hdmi2():
    er.write(b"~0012 15\r")
    print("📺 Panel přepnut na HDMI2")

def panel_android():
    er.write(b"~0012 24\r")
    print("📱 Panel přepnut do Android módu")
