
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from filtro_fir import FiltroFIR
from interfaz_daq import ConexionDAQ

FRECUENCIA_MUESTREO = 250          
NUM_COEFICIENTES = 100        
PUERTO_SERIAL = 'COM3'

def generar_coeficientes_filtro(f_inicio, f_fin, fs, n):
    """Crea coeficientes para eliminar el ruido de 50Hz (hum eléctrico)"""
    k1 = int((f_inicio / fs) * n)
    k2 = int((f_fin / fs) * n)
    
    coef_fft = np.ones(n)
    coef_fft[k1 : k2+1] = 0 
    coef_fft[n-k2 : n-k1+1] = 0
    
  
    ifft_res = np.fft.ifft(coef_fft)
    respuesta_impulso = np.real(ifft_res)
    respuesta_impulso = np.roll(respuesta_impulso, n // 2)
    
    return respuesta_impulso * np.hanning(n)


coeficientes = generar_coeficientes_filtro(45, 55, FRECUENCIA_MUESTREO, NUM_COEFICIENTES)
motor_filtro = FiltroFIR(coeficientes)
daq = ConexionDAQ(puerto=PUERTO_SERIAL)


muestras_a_mostrar = FRECUENCIA_MUESTREO * 4
datos_crudos = [0.0] * muestras_a_mostrar
datos_filtrados = [0.0] * muestras_a_mostrar


fig, (ax_arriba, ax_abajo) = plt.subplots(2, 1, figsize=(10, 7))
linea_cruda, = ax_arriba.plot(datos_crudos, color='red', label='Señal Cruda (Arduino)')
linea_filtrada, = ax_abajo.plot(datos_filtrados, color='blue', label='Señal ECG Filtrada')

ax_arriba.set_title("Visualización ECG en Tiempo Real")
ax_arriba.set_ylim(0, 5) 
ax_abajo.set_ylim(-1, 1) 
ax_arriba.legend(loc='upper right')
ax_abajo.legend(loc='upper right')

def actualizar_grafica(frame):
    valor_daq = daq.leer_muestra()
    
    if valor_daq is not None:
       
        valor_filtrado = motor_filtro.procesar_filtro(valor_daq)
        
        datos_crudos.append(valor_daq)
        datos_filtrados.append(valor_filtrado)
        datos_crudos.pop(0)
        datos_filtrados.pop(0)
        
        linea_cruda.set_ydata(datos_crudos)
        linea_filtrada.set_ydata(datos_filtrados)
        
    return linea_cruda, linea_filtrada


animacion = FuncAnimation(fig, actualizar_grafica, interval=20, blit=True)
plt.tight_layout()
plt.show()


daq.cerrar()