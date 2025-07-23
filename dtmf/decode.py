import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
from scipy import signal as sig
from playsound import playsound
from tkinter import filedialog, messagebox
from . import dtmf_map, fc, fr

def signalDecode(signal, fs):
    """
    Decodifica una señal DTMF en dígitos usando:
      Segmentación por energía.
      FFT para extraer picos de frecuencia.
      
    """
    digits = ''
    window_size = int(fs * 0.02)
    energy_threshold = np.mean(signal**2) * 0.2 

    toneIn = False
    startIndex = 0

    for i in range(0, len(signal) - window_size, window_size):
        window_energy = np.mean(signal[i:i + window_size]**2)

        if not toneIn and window_energy > energy_threshold:
            toneIn = True
            startIndex = i

        elif toneIn and window_energy < energy_threshold:
            toneIn = False
            endIndex = i
            segment = signal[startIndex:endIndex]

            if len(segment) < int(fs * 0.1):
                continue

            # FFT aplicado al segmento
            Y = fft(segment)
            freqs = fftfreq(len(segment), 1 / fs)

            pos = freqs > 0
            freqs_pos = freqs[pos]
            mags = np.abs(Y[pos])

            mask = (freqs_pos > 600) & (freqs_pos < 1550)
            if not np.any(mask):
                continue

            freqs_rel = freqs_pos[mask]
            mags_rel = mags[mask]
            if len(mags_rel) < 2:
                continue

            # dos picos más grandes
            peaks = np.argsort(mags_rel)[-2:]
            f_low, f_high = sorted(freqs_rel[peaks])

            row = fr[np.argmin(np.abs(fr - f_low))]
            col = fc[np.argmin(np.abs(fc - f_high))]

            found = '?'
            for d, (r, c) in dtmf_map.items():
                if r == row and c == col:
                    found = d
                    break

            digits += found
            if len(digits) >= 11:
                break

    return digits


def plot_spectrogram(signal, fs):
    # spectograma para denotar bien las graficas
    plt.figure("Espectrograma")
    plt.clf()
    # ventana 20 ms, solapamiento 10 ms
    NFFT = int(0.02 * fs)
    noverlap = int(0.01 * fs)
    Pxx, freqs, bins, im = plt.specgram(
        signal,
        NFFT=NFFT,
        Fs=fs,
        noverlap=noverlap,
        cmap='Blues',
        scale='dB'
    )
    plt.ylim(500, 1600)
    plt.title("Espectrograma de la señal", fontsize=14, fontweight='bold', color='#0050C8')
    plt.xlabel("Tiempo (s)", color='#0050C8')
    plt.ylabel("Frecuencia (Hz)", color='#0050C8')
    cbar = plt.colorbar(im)
    cbar.set_label('Intensidad (dB)', color='#0050C8')
    cbar.ax.yaxis.set_tick_params(color='#0050C8')
    plt.grid(False)
    plt.show(block=False)


def signalLoad():
    
    path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if not path:
        return
    # arreglo para evitar errores
    try:
        fs, data = wavfile.read(path)
        if data.ndim > 1:
            data = data[:, 0]
        signal = data.astype(np.float32) / np.max(np.abs(data))

        playsound(path)

        # Dominio del tiempo
        t = np.linspace(0, len(signal) / fs, num=len(signal))
        plt.figure("Señal Cargada")
        plt.clf()
        plt.plot(t, signal, color='#5AC8FA')  # azul claro
        plt.title("Señal cargada del archivo", fontsize=14, fontweight='bold', color='#004AAB')
        plt.xlabel("Tiempo (s)", color='#004AAB')
        plt.ylabel("Amplitud Normalizada", color='#004AAB')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.show(block=False)

        # Espectrograma
        plot_spectrogram(signal, fs)

        # Decodificacion
        return signalDecode(signal, fs)
    
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo procesar el archivo:\n{e}")