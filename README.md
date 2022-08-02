
# Coral Dev Board Mini Enviro Board

This is a little package that allow the Google Coral Dev Board Mini to use the Enviro Board.


## Installation Instructions

First verify your coral date:

```
$ date
```
If the date is wrong try to set your time zone with :
```
$ sudo dpkg-reconfigure tzdata
```
then download the date from internet and apply it:
```
$ sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"
```


We can now install the packages :
```
$ sudo apt-get install libgpiod2 python3-libgpiod gpiod python3-pil
```

and then run :
```
$ sudo pip3 install smbus2
$ sudo pip3 install adafruit-circuitpython-ssd1306
$ sudo pip3 install adafruit-circuitpython-bmp280
```

You should now be all set !
## Examples

```python
import board
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
from EnviroBoard.EnviroBoard import EnviroBoard
import asyncio

async def main():
	envio = EnviroBoard()

	oled = envio.display
	# Clear display.
	oled.fill(0)
	oled.show()
	# Create blank image for drawing.
	# Make sure to create image with mode '1' for 1-bit color.
	image = Image.new('1', (oled.width, oled.height))

	# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)
	# Draw a white background
	draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
	# Draw a smaller inner rectangle
	draw.rectangle((5, 5, oled.width - 5 - 1, oled.height - 5 - 1),
				outline=0, fill=0)
	# Load default font.
	font = ImageFont.load_default()


	# Draw Some Text
	btn = DigitalInOut(board.GPIO0)
	btn.direction = Direction.INPUT
	counter = 0
	prev_state = btn.value

	while(True):
		cur_state = btn.value
		value = "None"
		if cur_state != prev_state:
			if not cur_state:
				counter = (counter + 1) % 4
		prev_state = cur_state
		
		if counter == 0:
			value = "RH : %.2f %%" % envio.humidity
		elif counter == 1:
			value = "Temp : %.2f °C" % envio.temperature
		elif counter == 2:
			value = "Press : %.2f Pa" % envio.pressure
		elif counter == 3:
			value = "Lux : %.2f nW/cm²" % await envio.luminosity

		print(value)
		# Draw a white background
		draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
		# Draw a smaller inner rectangle
		draw.rectangle((5, 5, oled.width - 5 - 1, oled.height - 5 - 1),
				outline=0, fill=0)
		text = value
		(font_width, font_height) = font.getsize(text)
		draw.text((oled.width//2 - font_width//2, oled.height//2 - font_height//2),
			text, font=font, fill=255)


		oled.image(image)
		oled.show()
		await asyncio.sleep(0.05)



asyncio.run(main())

```
## Ressources

We use [Blinka (Circuit Python)](https://learn.adafruit.com/monochrome-oled-breakouts/python-usage-2) to access the screen via SPI : 

[Circuit Python for Coral](https://learn.adafruit.com/circuitpython-on-google-coral-linux-blinka/overview)

[Coral Dev Board Mini datasheet](https://coral.ai/docs/dev-board-mini/datasheet/)

[Enviro Board datasheet](https://coral.ai/docs/enviro-board/datasheet/)
