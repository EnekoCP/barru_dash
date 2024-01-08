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

# Inicializamos pygame
pygame.init()

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
        demo_tablero_coche(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
    except KeyboardInterrupt:
        pass