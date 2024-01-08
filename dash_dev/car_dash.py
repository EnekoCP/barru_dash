import obd
import time
import argparse
import pygame
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text

# Inicializar pygame
pygame.init()

pygame.mixer.music.load("cambioMarcha.mp3")  # Cambia "cambio_marcha.mp3" al nombre de tu archivo de sonido

def verificar_conexion_bluetooth():
    # Especifica el puerto serial Bluetooth de tu adaptador OBD-II
    puerto_bluetooth = "/dev/rfcomm0"  # Cambia esto al puerto Bluetooth correcto en tu sistema
    try:
        # Intenta establecer la conexión OBD-II
        connection = obd.OBD(portstr=puerto_bluetooth, fast=False, timeout=30)

        # Verifica si la conexión fue exitosa
        if connection.is_connected():
            print("Conexión Bluetooth exitosa")
            pygame.mixer.music.play()
        else:
            print("No se pudo establecer la conexión Bluetooth")

    except Exception as e:
        print(f"Error: {e}")

def reproducir_sonido(device, pitido_activado):
    if pitido_activado:
        corte(device)
        pygame.mixer.music.play(loops=-1)  # Reproducir el sonido en bucle
    else:
        pygame.mixer.music.stop()

def mostrar_marcha(device, marcha):
    with canvas(device) as draw:
        text(draw, (1, 0), f"{marcha}", fill="white")

def corte(device):
    try:
        while True:
            with canvas(device) as draw:
                draw.rectangle((0, 0, device.width, device.height), outline="red", fill="red")
            time.sleep(0.1)  # Ajusta el retardo según sea necesario
    except KeyboardInterrupt:
        pass

def obtener_rpm():
    cmd = obd.commands.RPM
    response = connection.query(cmd)

    if response.is_null():
        return 0
    else:
        return response.value.magnitude

def obtener_speed():
    cmd = obd.commands.SPEED
    response = connection.query(cmd)

    if response.is_null():
        return 0
    else:
        return response.value.magnitude

def obtener_engine_load():
    cmd = obd.commands.ENGINE_LOAD
    response = connection.query(cmd)

    if response.is_null():
        return 0
    else:
        return response.value.magnitude

def obtener_coolant_temp():
    cmd = obd.commands.COOLANT_TEMP
    response = connection.query(cmd)

    if response.is_null():
        return 0
    else:
        return response.value.magnitude

def obtener_intake_temp():
    cmd = obd.commands.INTAKE_TEMP
    response = connection.query(cmd)

    if response.is_null():
        return 0
    else:
        return response.value.magnitude

def demo_tablero_coche(n, block_orientation, rotate, inreverse):
    # Crear el dispositivo de la matriz
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation,
                     rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)
    print("Dispositivo creado")

    # Iniciar la demostración
    marcha = 1
    rpm_anterior = 0

    try:
        while True:
            # Obtener datos de RPM desde OBD-II
            rpm = obtener_rpm()

            # Obtener datos de TEMP COOLANT desde OBD-II
            temp = obtener_coolant_temp()
            if temp < 80:
                revoluciones_corte = 3000
            elif 80 < temp < 90:
                revoluciones_corte = 4000
            else:
                revoluciones_corte = 5000

            cambio_marcha = rpm_anterior > 4000 and rpm <= 4000

            # Activar el pitido
            pitido_activado = rpm >= revoluciones_corte

            reproducir_sonido(device, pitido_activado)  # Reproducir sonido al cambiar de marcha o detener el pitido
            if cambio_marcha:
                mostrar_marcha_y_rpm(device, marcha)
            time.sleep(0.1)

            # Actualizar la variable de revoluciones anteriores
            rpm_anterior = rpm

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argumentos para la demostración del tablero del coche', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Número de matrices LED MAX7219 en cascada')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrige la orientación del bloque al estar conectado verticalmente')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotar la pantalla 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Establecer en verdadero si los bloques están en orden inverso')

    args = parser.parse_args()

    try:
        verificar_conexion_bluetooth()
        demo_tablero_coche(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
    except KeyboardInterrupt:
        pass