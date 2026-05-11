import numpy as np

class FiltroFIR:
    def __init__(self, _coeficientes):
        self.coeficientes_fir = _coeficientes
        self.num_taps = len(_coeficientes)
        self.buffer_circular = np.zeros(self.num_taps)
        self.indice_buffer = 0
    
    def procesar_filtro(self, valor_entrada):
        self.buffer_circular[self.indice_buffer] = valor_entrada
        
        offset = self.indice_buffer
        offset_coef = 0
        salida = 0
        
        while(offset >= 0):
            salida += self.buffer_circular[offset] * self.coeficientes_fir[offset_coef]
            offset -= 1
            offset_coef += 1
            
        offset = self.num_taps - 1
        while(self.indice_buffer < offset):
            salida += self.buffer_circular[offset] * self.coeficientes_fir[offset_coef]
            offset -= 1
            offset_coef += 1
            

        if((self.indice_buffer + 1) >= self.num_taps):
            self.indice_buffer = 0
        else:
            self.indice_buffer += 1
            
        return salida