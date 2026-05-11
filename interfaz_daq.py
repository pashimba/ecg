import serial 
import time

class ConexionDAQ:
    def __init__(self, puerto='COM3', velocidad=115200):
        try:
            self.arduino = serial.Serial(puerto, velocidad, timeout=1)
            time.sleep(2) 
            print(f"Conectado exitosamente al Arduino en el puerto {puerto}")
        except Exception as e:
            print(f"Error al conectar con el DAQ: {e}")
            self.arduino = None

    def leer_muestra(self):
        """Lee una sola línea de voltaje enviada por el Arduino"""
        if self.arduino and self.arduino.in_waiting > 0:
            try:
                linea = self.arduino.readline().decode('utf-8').strip()
                return float(linea)
            except:
                return None
        return None

    def cerrar(self):
        if self.arduino:
            self.arduino.close()