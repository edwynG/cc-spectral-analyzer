import tempfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
from playsound import playsound
from utils.paths import safe_remove
from . import dtmf_map, T, Fs

def generate_tone(digit):
    
    if digit not in dtmf_map:
        raise ValueError(f"Dígito DTMF inválido: {digit}")
    f1, f2 = dtmf_map[digit]

    # vector de tiempo
    t = np.arange(0, T, 1/Fs)

    # síntesis directa: suma de dos senoidales
    y = 0.5 * (np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t))

    # poner fundido de 5 ms para eliminar clicks
    fade_len = int(0.005 * Fs)
    if fade_len * 2 < len(y):
        fade = np.ones_like(y)
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = fade_in[::-1]
        fade[:fade_len]    = fade_in
        fade[-fade_len:]   = fade_out
        y *= fade

    return t, y

def play_and_plot(digit):
    
    t, y = generate_tone(digit)

    # wav temporal y reproducir
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
        wavfile.write(tmp.name, Fs, np.int16(y * 32767))
        path = tmp.name
    playsound(path)
    safe_remove(path)

    plt.figure("Señal Continua")
    plt.clf()
    plt.plot(t, y, color='#007AFF')
    plt.title(f"Señal continua: dígito {digit}", fontsize=14, fontweight='bold')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show(block=False)

    N = len(y)
    Y = fft(y)
    xf = fftfreq(N, 1/Fs)

    pos = xf > 0
    xf_pos = xf[pos]
    Y_mag  = np.abs(Y[pos])

    plt.figure("Espectro de Frecuencia")
    plt.clf()
    plt.plot(xf_pos, Y_mag, color='#3443C7')
    plt.xlim(600, 1550)
    plt.title(f"Espectro discreto: dígito {digit}", fontsize=14, fontweight='bold')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show(block=False)