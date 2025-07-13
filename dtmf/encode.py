import tempfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.io import wavfile
from playsound import playsound
from utils.paths import safe_remove
from . import dtmf_map, T, Fs

# La función genera la señal de audio que corresponde al tono DTMF de un dígito telefónico, combinando dos frecuencias específicas en una señal senoidal que puede ser reproducida o graficada.
def generate_tone(digit):
    if digit not in dtmf_map:
        raise ValueError(f"Dígito DTMF inválido: {digit}")
    f1, f2 = dtmf_map[digit]
    t = np.arange(0, T, 1/Fs)  # paso fijo 1/Fs
    y = 0.5 * (np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t))
    return t, y

def play_and_plot(digit):
    """Reproduce el tono y grafica la señal y su espectro."""
    t, y = generate_tone(digit)

    # Guarda en un archivo WAV temporal para reproducir
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmpfile:
        wavfile.write(tmpfile.name, Fs, np.int16(y * 32767))
        temp_path = tmpfile.name
    
    playsound(temp_path)
    safe_remove(temp_path)

    # Grafica la señal continua
    plt.figure("Señal Continua")
    plt.clf()
    plt.plot(t, y, color='#007AFF') # Color estilo iPhone
    plt.title(f"Señal continua: dígito {digit}", fontsize=14, fontweight='bold')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show(block=False)

    # Calcula la FFT
    N = len(y)
    Y = fft(y)
    xf = fftfreq(N, 1 / Fs)

    # Grafica el espectro de frecuencia
    plt.figure("Espectro de Frecuencia")
    plt.clf()
    plt.stem(xf, np.abs(Y), basefmt=" ", linefmt='#34C759', markerfmt='o') # Colores estilo iPhone
    plt.xlim(600, 1600)
    plt.title(f"Espectro discreto: dígito {digit}", fontsize=14, fontweight='bold')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show(block=False)
