import spidev
import time
from gpiozero import LED

# --- SPI Setup ---
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# --- LCD Pins ---
RS = LED(17)
E = LED(27)
D4 = LED(22)
D5 = LED(5)
D6 = LED(6)
D7 = LED(13)

# --- pH Calibration Constants ---
V_pH7 = 1.60
V_pH4 = 2.07
Slope = (V_pH7 - V_pH4) / (7 - 4)

# --- LCD Functions ---
def pulse_enable():
    E.on()
    time.sleep(0.0001)
    E.off()
    time.sleep(0.0001)

def send_data(data, mode):
    RS.on() if mode else RS.off()
    E.off()
    for i in range(4):
        [D4, D5, D6, D7][i].value = (data >> (i + 4)) & 0x01
    pulse_enable()
    for i in range(4):
        [D4, D5, D6, D7][i].value = (data >> i) & 0x01
    pulse_enable()

def init_lcd():
    time.sleep(0.05)
    for _ in range(3):
        send_data(0x30, False)
        time.sleep(0.05)
    send_data(0x20, False)
    send_data(0x28, False)
    send_data(0x0C, False)
    send_data(0x01, False)
    send_data(0x06, False)

def write_string(message):
    for char in message:
        send_data(ord(char), True)
        time.sleep(0.001)

def set_cursor(line, position):
    addr = position + (0x40 if line == 2 else 0x00)
    send_data(0x80 | addr, False)

def clear_display():
    send_data(0x01, False)
    time.sleep(0.05)

# --- Sensor Functions ---
def read_adc(channel):
    if channel < 0 or channel > 7:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]

def convert_to_voltage(data, vref=3.3):
    return (data * vref) / 1023.0

def voltage_to_pH(voltage):
    return 7 + (voltage - V_pH7) / Slope

# --- Main Program ---
try:
    init_lcd()
    time.sleep(0.1)

    while True:
        # Read pH sensor
        ph_adc = read_adc(0)
        ph_voltage = convert_to_voltage(ph_adc)
        pH = voltage_to_pH(ph_voltage)

        # --- Display pH ---
        clear_display()
        set_cursor(1, 0)
        write_string(f"pH: {pH:.2f}")
        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting...")
    spi.close()
