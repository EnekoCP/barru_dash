import time
import argparse

import pygame

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import RPi.GPIO as GPIO

# Configuración de la biblioteca GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # Utiliza el pin GPIO17 para el LED
GPIO.setup(27, GPIO.OUT)  # Utiliza el pin GPIO27 para el LED
GPIO.setup(22, GPIO.OUT)  # Utiliza el pin GPIO22 para el LED

GPIO.setup(5, GPIO.OUT)  # Utiliza el pin GPIO5 para el LED
GPIO.setup(6, GPIO.OUT)  # Utiliza el pin GPIO6 para el LED
GPIO.setup(13, GPIO.OUT)  # Utiliza el pin GPIO13 para el LED

GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
GPIO.output(22, GPIO.LOW)

GPIO.output(5, GPIO.LOW)
GPIO.output(6, GPIO.LOW)
GPIO.output(13, GPIO.LOW)

led_green = False
led_yellow = False
led_red = False
led_white = False
led_orange = False
led_blue = False

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

draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
# Load default font.
font = ImageFont.load_default()
font1 = ImageFont.truetype('fuente1.TTF', 7)
font2 = ImageFont.truetype('fuente1.TTF', 5)
font3 = ImageFont.truetype('fuente1.TTF', 9)

# Carga una imagen desde un archivo
image_path = "subaru.bmp"  # Cambia la ruta a tu imagen
imageSubaru = Image.open(image_path).convert("1")  # Convierte a modo 1-bit (blanco y negro)

# Escala la imagen si es necesario
imageSubaru = imageSubaru.resize((32, 32), Image.ANTIALIAS)


def init_led_green():
    global led_green
    # Enciende el LED
    if not led_green:
        led_green = True
        GPIO.output(22, GPIO.HIGH)
        print("LED encendido")


def off_led_green():
    global led_green
    # Apaga el LED
    if led_green:
        GPIO.output(22, GPIO.LOW)
        led_green = False
        print("LED apagado")


def init_led_yellow():
    global led_yellow
    # Enciende el LED
    if not led_yellow:
        led_yellow = True
        GPIO.output(27, GPIO.HIGH)
        print("LED encendido")


def off_led_yellow():
    global led_yellow
    # Apaga el LED
    if led_yellow:
        GPIO.output(27, GPIO.LOW)
        led_yellow = False
        print("LED apagado")


def init_led_red():
    global led_red
    # Enciende el LED
    if not led_red:
        led_red = True
        GPIO.output(17, GPIO.HIGH)
        print("LED encendido")


def off_led_red():
    global led_red
    # Apaga el LED
    if led_red:
        GPIO.output(17, GPIO.LOW)
        led_red = False
        print("LED apagado")


def init_led_blue():
    global led_blue
    # Enciende el LED
    if not led_blue:
        led_blue = True
        GPIO.output(13, GPIO.HIGH)
        print("LED encendido")


def off_led_blue():
    global led_blue
    # Apaga el LED
    if led_blue:
        GPIO.output(13, GPIO.LOW)
        led_blue = False
        print("LED apagado")


def init_led_orange():
    global led_orange
    # Enciende el LED
    if not led_orange:
        led_orange = True
        GPIO.output(6, GPIO.HIGH)
        print("LED encendido")


def off_led_orange():
    global led_orange
    # Apaga el LED
    if led_orange:
        GPIO.output(6, GPIO.LOW)
        led_orange = False
        print("LED apagado")


def init_led_white():
    global led_white
    # Enciende el LED
    if not led_white:
        led_white = True
        GPIO.output(5, GPIO.HIGH)
        print("LED encendido")


def off_led_white():
    global led_white
    # Apaga el LED
    if led_white:
        GPIO.output(5, GPIO.LOW)
        led_white = False
        print("LED apagado")


def init_leds_oled():
    global led_red, led_yellow, led_green
    init_oled()
    init_led_red()
    init_led_blue()
    time.sleep(3)
    init_led_yellow()
    init_led_orange()
    time.sleep(2)
    init_led_green()
    init_led_white()
    time.sleep(5)
    reproducir_sonido(True)


def init_oled():
    draw.text((0, 5), "SUBARU IMPREZA", font=font1, fill=255)
    draw.text((20, 17), "SimHub by CHUME", font=font, fill=255)

    # Display updated image
    oled.image(image)
    oled.show()


def limpiar_oled():
    # Clear display.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    # Limpia la pantalla.
    oled.show()


# Function to update OLED with new data
def update_oled(rpm, tempRef, tempAir):
    limpiar_oled()
    # Crea un objeto ImageDraw para dibujar en la imagen
    draw.text((0, 0), "RPM: {}".format(rpm), font=font3, fill=255)
    draw.text((0, 15), "-TEMP Ref: {} C".format(tempRef), font=font2, fill=255)
    draw.text((0, 22), "-TEMP Air: {} C".format(tempAir), font=font2, fill=255)

    # Display updated image
    oled.image(image)
    oled.show()


def reproducir_sonido(cambio_marcha):
    if cambio_marcha:
        pygame.mixer.music.load("cambioMarcha.mp3")  # Cambia "cambio_marcha.mp3" al nombre de tu archivo de sonido
        pygame.mixer.music.play(loops=3)


def parar_sonido():
    pygame.mixer.music.stop()


def mostrar_marcha_y_rpm(device, marcha, rpm):
    parar_sonido()
    with canvas(device) as draw:
        text(draw, (1, 0), f"{marcha}", fill="white", font=proportional(CP437_FONT))

        if rpm >= 7500:
            reproducir_sonido(True)  # Reproducir sonido al cambiar de marcha
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
    tempRef = 0
    tempAir = 0

    try:
        while True:
            # Simular el aumento de RPM
            rpm += 200
            tempRef += 5
            tempAir += 5
            update_oled(rpm, tempRef, tempAir)

            if 500 <= rpm <= 3000:
                off_led_green()
            elif 3000 < rpm <= 5000:
                off_led_yellow()
            elif 5000 < rpm <= 8000:
                off_led_red()
            else:
                pass

            if tempRef < 80:
                init_led_blue()
            else:
                off_led_blue()
            if tempAir < 80:
                init_led_orange()
            else:
                off_led_orange()

            if rpm > 8000:
                rpm = 0
                init_led_red()
                init_led_green()
                init_led_yellow()
                time.sleep(1)
                marcha += 1
                if marcha > 5:
                    marcha = 1

            mostrar_marcha_y_rpm(device, marcha, rpm)
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argumentos para la demostración del tablero del coche',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Número de matrices LED MAX7219 en cascada')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90],
                        help='Corrige la orientación del bloque al estar conectado verticalmente')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3],
                        help='Rotar la pantalla 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--reverse-order', type=bool, default=False,
                        help='Establecer en verdadero si los bloques están en orden inverso')

    args = parser.parse_args()

    try:
        init_leds_oled()
        limpiar_oled()
        demo_tablero_coche(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
    except KeyboardInterrupt:
        pass
