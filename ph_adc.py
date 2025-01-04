import spidev
import time


spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, CE0
spi.max_speed_hz = 1350000


def read_channel(channel):
    assert 0 <= channel <= 7, "Channel must be between 0 and 7"
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) | adc[2]
    return data

# Convert ADC value to voltage
def convert_to_voltage(data, vref=3.3):
    return (data * vref) / 1023.0

# Convert voltage to pH
def calculate_ph(voltage, neutral_voltage=2.5, sensitivity=0.17):
    
    neutral_voltage=0.03
    sensitivity=0.18
    return 7.0 - ((voltage - neutral_voltage) / sensitivity)


try:
    while True:
        # Read pH sensor from channel 2
        raw_value = read_channel(2)
        voltage = convert_to_voltage(raw_value)
        ph = calculate_ph(voltage)

       
        print(f"Raw ADC Value: {raw_value}")
        print(f"Voltage: {voltage:.2f}V")
        print(f"pH: {ph:.2f}")

        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
