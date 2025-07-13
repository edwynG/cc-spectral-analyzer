import numpy as np
# --- Constantes y Configuración del Proyecto ---

# Frecuencias DTMF (Hz)
fr = np.array([697, 770, 852, 941])
fc = np.array([1209, 1336, 1477])

# Mapeo de dígitos a sus frecuencias (fila, columna)
dtmf_map = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477)
}

# Parámetros de la señal
T = 0.25      # Duración del tono (segundos)
Fs = 32768    # Tasa de muestreo (Hz)
