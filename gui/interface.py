from scipy.fft import fft, fftfreq
import tkinter as tk
from tkinter import ttk # Importar ttk para estilos más avanzados
from dtmf.decode import load_signal
from dtmf.encode import play_and_plot

class Interface:
    def __init__(self, master):
        self.master = master
        master.title("DTMF Marcador y Decodificador")
        master.geometry("500x500") # Tamaño de ventana más estilizado
        master.resizable(False, False) # No redimensionable para mantener el estilo
        master.configure(bg='#1C1C1E') # Fondo oscuro para el tema

        # Configuración de estilos para ttk (tema oscuro)
        style = ttk.Style()
        style.theme_use('clam') # Un tema más moderno y personalizable
        
        # Estilo para los botones del teclado
        style.configure('TButton', 
                        font=('SF Pro Display', 18, 'bold'), # Fuente similar a iOS
                        foreground='white',
                        background='#3A3A3C', # Gris oscuro para botones
                        relief='flat', # Sin relieve
                        padding=[10, 10], # Relleno para hacerlos más grandes
                        borderwidth=0,
                        focuscolor='#3A3A3C') # Eliminar el borde de enfoque predeterminado
        style.map('TButton', 
                  background=[('active', '#5A5A5C')]) # Cambio de color al presionar

        # Estilo para el botón de cargar
        style.configure('Load.TButton',
                        font=('SF Pro Display', 14),
                        foreground='white',
                        background='#0A84FF', # Azul más vibrante para el botón de cargar
                        relief='flat',
                        padding=[10, 10],
                        borderwidth=0,
                        focuscolor='#0A84FF')
        style.map('Load.TButton',
                  background=[('active', '#007AFF')])

        # Estilo para la etiqueta de resultado
        style.configure('TLabel',
                        font=('SF Pro Display', 14),
                        background='#1C1C1E', # Fondo oscuro
                        foreground='white') # Texto blanco

        # Frame para los botones del teclado
        btn_frame = tk.Frame(master, bg='#1C1C1E') # Fondo del frame igual al de la ventana
        btn_frame.pack(pady=20) # Más espacio vertical

        digit_keys = ['1','2','3','4','5','6','7','8','9','*','0','#']
        
        # Disposición de botones como un teclado telefónico
        key_layout = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['*', '0', '#']
        ]

        for r_idx, row_keys in enumerate(key_layout):
            for c_idx, d in enumerate(row_keys):
                btn = ttk.Button(btn_frame, text=d, 
                                 command=lambda digit=d: play_and_plot(digit),
                                 width=4, style='TButton') # Ancho fijo para consistencia
                btn.grid(row=r_idx, column=c_idx, padx=10, pady=10) # Espaciado generoso

        # Botón para cargar y decodificar
        load_btn = ttk.Button(master, text="Cargar y Decodificar Señal", command= self.eventSignal,
                              style='Load.TButton')
        load_btn.pack(pady=20, padx=20, fill='x') # Rellenar horizontalmente

        # Etiqueta de resultado
        self.result_label = ttk.Label(master, text="Dígitos decodificados: ", style='TLabel')
        self.result_label.pack(pady=10)

    def eventSignal(self):
        self.result_label.config(text=f"Dígitos decodificados: {load_signal()}")


