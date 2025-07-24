# Transformadas de fourier - análisis espectral

El **análisis espectral** es una herramienta para entender cómo se descompone una señal en sus componentes de frecuencia. Esta descomposición se realiza mediante la transformada de Fourier, que permite transformar una señal en el dominio del tiempo a su representación en el dominio de la frecuencia. En particular, la transformada discreta de Fourier es clave para analizar señales digitales, donde la información se encuentra en muestras discretas. Cuando presionamos un dígito en un teléfono, se genera un sonido compuesto por la superposición de dos frecuencias específicas: una asociada a la fila y otra a la columna del teclado. Cada tecla produce así un tono único que puede ser codificado y decodificado mediante técnicas de procesamiento de señales. Para generar estos tonos, se combinan dos ondas senoidales con frecuencias determinadas, y se muestrea la señal en intervalos regulares definidos por la frecuencia de muestreo $F_s$. Esto implica dividir el intervalo de tiempo de duración $T$ en puntos igualmente espaciados con separación $1/F_s$ obteniendo así una señal discreta que puede ser analizada digitalmente.

## Comandos necesarios

python -m venv venv
.\venv\Scripts\activate

## Primera vez sin tener las dependencias ejecutar

pip install numpy matplotlib scipy
pip install playsound==1.2.2

## ejecutar proyecto

python main.py

## (En caso de querer probar el generador de tonos) 
## ejecutar generador de tonos, modificar la linea 58 para cambiar los numeros en caso de ser necesario

python test/generator.py

## Casos de prueba para decodificador de tonos estan ubicados en la carpeta "test" con sus respectivos numeros

