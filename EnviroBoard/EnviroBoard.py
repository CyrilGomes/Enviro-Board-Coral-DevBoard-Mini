import busio
import board
from smbus2 import SMBus
import adafruit_bmp280
import busio
import adafruit_ssd1306
import digitalio
import asyncio
class EnviroBoard:

    def __init__(self):
#        self.temperature = 0
#        self.humidity = 0
#        self.luminosity = 0
#        self.pressure = 0
        spi = board.SPI()
        reset_pin = digitalio.DigitalInOut(board.GPIO7)
        cs_pin = digitalio.DigitalInOut(board.SPI_CSB)
        dc_pin = digitalio.DigitalInOut(board.GPIO1)

        self.display = adafruit_ssd1306.SSD1306_SPI(128, 32, spi, dc_pin, reset_pin, cs_pin)

    def get_temperature(self):
        bus = SMBus(3)
        bus.write_byte_data(0x40, 0x0F, 1)

        temp_low = bus.read_byte_data(0x40, 0x00)
        temp_high = bus.read_byte_data(0x40, 0x01)
        temp_res = (temp_high << 8) | temp_low
        temp_res = temp_res / (65536)
        temp_res *= 165
        temp_res -= 40
        return temp_res

    def get_humidity(self):
        bus = SMBus(3)
        bus.write_byte_data(0x40, 0x0F, 1)

        humi_low = bus.read_byte_data(0x40, 0x02)
        humi_high = bus.read_byte_data(0x40, 0x03)

        humi_res = (humi_high << 8) | humi_low
        humi_res = humi_res / (65536)
        humi_res *= 100
        return humi_res


    async def get_luminosity(self):
        bus = SMBus(3)
        bus.write_word_data(0x45, 0x01, 0x10CA)
        await asyncio.sleep(0.88)
        data = bus.read_word_data(0x45, 0x00)
        left = data >> 8
        right = data&255
        expo = right>>4
        fractio = (right&15<<8) | (left)
        bus.read_word_data(0x45,0x01)
        return (2**expo)*fractio*1.2

    def get_pressure(self):
        i2c = busio.I2C(board.I2C1_SCL, board.I2C1_SDA)
        bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)
        return bmp280.pressure


    temperature = property(get_temperature)
    humidity = property(get_humidity)
    luminosity = property(get_luminosity)
    pressure = property(get_pressure)

