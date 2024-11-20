import sys
import os
import network
import machine
import time
import ujson
import urequests  # Compatible con MicroPython
from machine import Pin, ADC
from secrets import secrets  # Archivo separado para las credenciales Wi-Fi
from Wifi_lib import wifi_init  # Librerías externas para inicializar Wi-Fi

# Inicializar Wi-Fi
wifi_init()

# Verificar conexión Wi-Fi
wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    print("Error: Wi-Fi no conectado. Verifica las credenciales.")
    sys.exit()

# Clase para detectar la placa
class Board:
    class BoardType:
        ESP32 = 'ESP32'
        UNKNOWN = 'Unknown'

    def __init__(self):
        self.type = self.detect_board_type()

    def detect_board_type(self):
        sysname = os.uname().sysname.lower()
        machine_name = os.uname().machine.lower()
        if sysname == 'esp32' and 'esp32' in machine_name:
            return self.BoardType.ESP32
        else:
            return self.BoardType.UNKNOWN

# Detectar tipo de placa
BOARD_TYPE = Board().type
print("Tarjeta Detectada: " + BOARD_TYPE)

# Configuración de los pines (usar pines ADC válidos para ESP32)
if BOARD_TYPE == Board.BoardType.ESP32:
    led = Pin(2, Pin.OUT)  # GPIO 2 para el ESP32 (LED integrado)
    sensor_pin_1 = 32  # GPIO 32 (compatible con ADC1)
    sensor_pin_2 = 33  # GPIO 33 (compatible con ADC1)
    sensor_pin_3 = 34  # GPIO 34 (compatible con ADC1, entrada solamente)
else:
    print("Placa desconocida. Terminando ejecución.")
    sys.exit()

# Configurar ADC con atenuación y resolución adecuada
adc1 = ADC(Pin(sensor_pin_1))
adc2 = ADC(Pin(sensor_pin_2))
adc3 = ADC(Pin(sensor_pin_3))

adc1.atten(ADC.ATTN_11DB)  # Rango de 0-3.9V
adc2.atten(ADC.ATTN_11DB)  # Rango de 0-3.9V
adc3.atten(ADC.ATTN_11DB)  # Rango de 0-3.9V

# URL del servidor
url = "http://192.168.0.5/insertar_datos.php"

# Umbral de decibeles para alerta 
umbral_decibelios = 70

# Función para leer valores del KY-037 y convertirlos a decibelios
def leer_ky037(adc):
    try:
        valor_analogico = adc.read()
        if valor_analogico is None or valor_analogico == 0:
            return 0
        # Convertir valor analógico a decibelios aproximados
        decibelios = valor_analogico / 4095 * 100  # Ajusta el rango según el sensor
        return decibelios
    except Exception as e:
        print(f"Error leyendo el sensor: {e}")
        return 0  # Devuelve 0 en caso de error

# Determinar el sensor con mayor nivel de decibelios
def determinar_sensor_mayor(decibelios):
    max_valor = max(decibelios)
    return decibelios.index(max_valor) + 1, max_valor  # Índice +1 (ID) y el valor

while True:
    try:
        # Leer valores de los sensores
        decibelios_1 = leer_ky037(adc1)
        decibelios_2 = leer_ky037(adc2)
        decibelios_3 = leer_ky037(adc3)

        # Crear una lista con los valores de los sensores
        valores = [decibelios_1, decibelios_2, decibelios_3]

        # Determinar el sensor con mayor nivel de decibelios
        sensor_mayor, max_decibelios = determinar_sensor_mayor(valores)
        print(f"Sensor con mayor nivel de decibelios: Sensor {sensor_mayor} ({max_decibelios:.2f} dB)")

        # Crear datos para enviar
        id_usuario = 1
        fecha_registro = "{}-{}-{} {}:{}:{}".format(*time.localtime()[:6])  # Formato de fecha
        excede_limite = max_decibelios > umbral_decibelios

        data = {
            "nivelSonido1": decibelios_1,
            "nivelSonido2": decibelios_2,
            "nivelSonido3": decibelios_3,
            "fechaRegistro": fecha_registro,
            "excedeLimite": excede_limite,
            "direcion_idDir": sensor_mayor,
            "usuario_idUsuario": id_usuario
        }

        # Enviar datos al servidor
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(url, data=ujson.dumps(data), headers=headers)
        print("Datos enviados:", data)
        print("-> Respuesta del servidor:", response.text)
        response.close()

        # Controlar el LED
        if excede_limite:
            led.on()
            print("Nivel de decibelios alto, LED encendido")
        else:
            led.off()
            print("Nivel de decibelios normal, LED apagado")

    except OSError as e:
        print(f"Error al procesar los datos o enviar al servidor: {e}")
        # Intentar reconectar Wi-Fi si la conexión falla
        if not wlan.isconnected():
            print("Reconectando a Wi-Fi...")
            wlan.connect(secrets['ssid'], secrets['password'])
            time.sleep(5)  # Esperar 5 segundos antes de reintentar

    time.sleep(2)



