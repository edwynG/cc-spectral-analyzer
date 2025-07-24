# Transformadas de fourier - análisis espectral

El **análisis espectral** es una herramienta para entender cómo se descompone una señal en sus componentes de frecuencia. Esta descomposición se realiza mediante la transformada de Fourier, que permite transformar una señal en el dominio del tiempo a su representación en el dominio de la frecuencia. En particular, la transformada discreta de Fourier es clave para analizar señales digitales, donde la información se encuentra en muestras discretas. Cuando presionamos un dígito en un teléfono, se genera un sonido compuesto por la superposición de dos frecuencias específicas: una asociada a la fila y otra a la columna del teclado. Cada tecla produce así un tono único que puede ser codificado y decodificado mediante técnicas de procesamiento de señales. Para generar estos tonos, se combinan dos ondas senoidales con frecuencias determinadas, y se muestrea la señal en intervalos regulares definidos por la frecuencia de muestreo $F_s$. Esto implica dividir el intervalo de tiempo de duración $T$ en puntos igualmente espaciados con separación $1/F_s$ obteniendo así una señal discreta que puede ser analizada digitalmente.

## Estructura del proyecto
```
cc-spectral-analyzer/
├── dtmf/
│   ├── __init__.py        # Constantes y frecuencias DTMF
│   ├── encode.py          # Generación y visualización de tonos DTMF
│   ├── decode.py          # Decodificación y análisis de señales DTMF
├── gui/
│   ├── interface.py       # Interfaz gráfica para interactuar con el teclado 
├── test/
│   ├── generator.py       # Generador de archivos .wav para pruebas DTMF
│   ├── ...                # Casos de pruebas generados
├── utils/
│   ├── paths.py           # Funciones auxiliares para manejo de archivos
├── docs/
│   ├── ...                # Informe y enunciado del proyecto
├── main.py                # Punto de inicio del programa principal
├── README.md              # Documentación general del proyecto
├── requirements.txt       # Lista de dependencias necesarias
```

## Instalación y ejecución

1. **Crear entorno virtual:**
    ```bash
    python -m venv venv
    ```

2. **Activar entorno virtual:**
    - En Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - En Linux/Mac:
      ```bash
      source venv/bin/activate
      ```

3. **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Ejecutar:**
    ```bash
    python main.py
    ```

## Generación de casos de prueba

Para generar archivos `.wav` de tonos DTMF personalizados:

1. Ejecuta el CLI ubicado en la carpeta `test`:
    ```bash
    python test/generator.py (--num | -n) <NUMERO-DE-11-DIGITOS>
    ```
    Reemplaza `<NUMERO-DE-11-DIGITOS>` por el número o secuencia que deseas generar.

2. Los archivos `.wav` generados se guardarán en la carpeta `test` o en la raiz del proyecto (Depende de en que ubicación abras la consola) y pueden ser usados para probar el decodificador.

## Notas adicionales
- Los casos de prueba para el decodificador están en la carpeta `test`.
- Consulta el código fuente y los comentarios para más detalles sobre la implementación.

