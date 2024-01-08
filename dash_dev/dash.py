import re
import time
import argparse

import pygame

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Inicializamos pygame
pygame.init()

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 32  # Change to 64 if needed
BORDER = 5

# Use for I2C.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=0)
# Load default font.
font = ImageFont.load_default()

# Carga una imagen desde un archivo
image_path = "subaru.bmp"  # Cambia la ruta a tu imagen
imageSubaru = Image.open(image_path).convert("1")  # Convierte a modo 1-bit (blanco y negro)

# Escala la imagen si es necesario
imageSubaru = imageSubaru.resize((32, 32), Image.ANTIALIAS)


def init_oled():
    draw.text((0, 0), "SUBARU IMPREZA", font=font, fill=255)
    draw.text((0, 12), "SIMHUB by CHUME", font=font, fill=255)

    # Display updated image
    oled.image(image)
    oled.show()

    time.sleep(3)


def limpiar_oled():
    # Limpia la pantalla.
    oled.fill(0)
    oled.show()


# Function to update OLED with new data
def update_oled(rpm):

    draw.text((0, 0), "RMP: " + str(rpm), font=font, fill=255)
    draw.text((0, 12), "TEMP: 50º", font=font, fill=255)

    # Display updated image
    oled.image(image)
    oled.show()

def reproducir_sonido(cambio_marcha):
    if cambio_marcha:
        pygame.mixer.music.load("cambioMarcha.mp3")  # Cambia "cambio_marcha.mp3" al nombre de tu archivo de sonido
        pygame.mixer.music.play()
def mostrar_marcha_y_rpm(device, marcha, rpm):
    with canvas(device) as draw:
        text(draw, (1, 0), f"{marcha}", fill="white", font=proportional(CP437_FONT))
        #text(draw, (0, 10), f"RPM: {rpm}", fill="white", font=proportional(CP437_FONT))
        if rpm >= 9000:
            draw.rectangle((0, 0, device.width, device.height), outline="red", fill="red")

def demo_tablero_coche(n, block_orientation, rotate, inreverse):
    # crear el dispositivo de la matriz
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation,
                     rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)
    print("Dispositivo creado")

    # iniciar la demostración
    marcha = 1
    rpm = 0

    try:
        while True:
            # Simular el aumento de RPM
            rpm += 100
            update_oled(rpm)
            if rpm > 10000:
                rpm = 0
                cambio_marcha = True
                marcha += 1
                if marcha > 6:
                    marcha = 1
            else:
                cambio_marcha = False

            reproducir_sonido(cambio_marcha)  # Reproducir sonido al cambiar de marcha
            mostrar_marcha_y_rpm(device, marcha, rpm)
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argumentos para la demostración del tablero del coche',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Número de matrices LED MAX7219 en cascada')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrige la orientación del bloque al estar conectado verticalmente')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotar la pantalla 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Establecer en verdadero si los bloques están en orden inverso')

    args = parser.parse_args()

    try:
        init_oled()
        limpiar_oled()
        demo_tablero_coche(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
    except KeyboardInterrupt:
        pass