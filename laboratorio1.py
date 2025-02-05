import wfdb
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import random

ECG = "datos_signal/22"

lecturasignal = wfdb.rdrecord(ECG)
signal = lecturasignal.p_signal[:,0]  
fs = lecturasignal.fs  
numero_datos = len(signal) 
muestreo=int(5*fs)

time = [i / fs for i in range(numero_datos)]  
signal = signal[:muestreo]
time = time[:muestreo]
plt.figure(figsize=(12,4))
plt.plot(time, signal, color="violet")

plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mv)")
plt.title("Señal Biomédica ECG bases de datos physionet")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(8, 4))
plt.hist(signal, bins=50, color='orange', alpha=0.7, edgecolor='black', density=True)
plt.xlabel("Amplitud de la señal")
plt.ylabel("Frecuencia normalizada")
plt.title("Histograma de la señal (5s)")
plt.grid()
plt.show()


suma=0
for i in range(len(signal)):
    suma += signal[i]
media = suma/ len(signal)
print(f"Media de la señal: {media:.4f}")

longitud_vector = 0
for _ in signal:
    longitud_vector +=1
print(f"Longitud del vector: {longitud_vector}")

desviacion = 0
for i in range(len(signal)):
    desviacion += (signal[i] - media) ** 2
desviacion_estandar = (desviacion/len(signal)) ** 0.5
print(f"Desviación estándar: {desviacion_estandar:.4f}")

coeficiente_de_variacion = desviacion_estandar/ media if media != 0 else float ('nan')
print(f"Coeficiente de variación: {coeficiente_de_variacion:.4f}")



media_librerias = np.mean(signal)
longitud_vector_librerias = len(signal)
desviacion_librerias = np.std(signal)
coeficiente_variacion_librerias = desviacion_librerias / media_librerias if media_librerias != 0 else np.nan

print(f"Media de la señal con librerias: {media_librerias:.4f}")
print(f"Longitud del vector con librerias: {longitud_vector_librerias}")
print(f"Desviación estándar con librerias: {desviacion_librerias:.4f}")
print(f"Coeficiente de variación con librerias: {coeficiente_variacion_librerias:.4f}")

kde = gaussian_kde(signal)
x_vals = np.linspace(min(signal), max(signal), 1000)
pdf_vals = kde(x_vals)
plt.figure(figsize=(8, 4))
plt.plot(x_vals, pdf_vals, color='brown', label="")
plt.xlabel("Amplitud de la señal")
plt.ylabel("Densidad de probabilidad")
plt.title("Función de Probabilidad de la Señal")
plt.legend()
plt.grid()
plt.show()

# Ruido Gaussiano
ruido_gauss = [random.gauss(0, 0.1) for _ in range(len(signal))]
signal_gauss = [signal[i] + ruido_gauss[i] for i in range(len(signal))]
# Grafica señal contaminada Gauss
plt.figure(figsize=(12,4))
plt.plot(time, signal_gauss, color="red")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mv)")
plt.title("Señal Contaminada con Gauss")
plt.legend()
plt.grid()
plt.show()

# Ruido Impulsivo (Saltos aleatorios grandes)
ruido_impulso = [random.uniform(-1, 1) if random.random() < 0.05 else 0 for _ in range(len(signal))]
signal_impulso = [signal[i] + ruido_impulso[i] for i in range(len(signal))]
# Grafica señal contaminada Impulso
plt.figure(figsize=(12,4))
plt.plot(time, signal_impulso, color="blue")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mv)")
plt.title("Señal Contaminada con Impulso")
plt.legend()
plt.grid()
plt.show()

# Ruido de artefacto (Picos grandes en zonas específicas)
ruido_artefacto = signal[:]
for _ in range(30):  # Introducimos 30 picos aleatorios
    idx = random.randint(0, len(signal) - 1)
    ruido_artefacto[idx] += random.uniform(-2, 2)
signal_artefacto = ruido_artefacto
# Grafica señal contaminada artfecto
plt.figure(figsize=(12,4))
plt.plot(time, signal_artefacto, color="green")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mv)")
plt.title("Señal Contaminada con Artefacto")
plt.legend()
plt.grid()
plt.show()

# SNR
def calcular_potencia(senal):
    suma_cuadrados = 0
    for i in range(len(senal)):
        suma_cuadrados += senal[i] ** 2
    return suma_cuadrados / len(senal)

potencia_senal = calcular_potencia(signal)
potencia_ruido_gauss = calcular_potencia(ruido_gauss)
potencia_ruido_impulso = calcular_potencia(ruido_impulso)
potencia_ruido_artefacto = calcular_potencia([signal_artefacto[i] - signal[i] for i in range(len(signal))])

SNR_gauss = 10 * (potencia_senal / potencia_ruido_gauss)
SNR_impulso = 10 * (potencia_senal / potencia_ruido_impulso)
SNR_artefacto = 10 * (potencia_senal / potencia_ruido_artefacto)

print(f"SNR con ruido Gaussiano: {SNR_gauss:.4f}")
print(f"SNR con ruido Impulsivo: {SNR_impulso:.4f}")
print(f"SNR con ruido de Artefacto: {SNR_artefacto:.4f}")


plt.figure(figsize=(12, 8))
plt.subplot(4, 1, 1)
plt.plot(signal, label="Señal Original", color="violet")
plt.title("Señal Original")
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(signal_gauss, label="Ruido Gaussiano", color="red")
plt.title("Señal con Ruido Gaussiano")
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(signal_impulso, label="Ruido Impulsivo", color="blue")
plt.title("Señal con Ruido Impulsivo")
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(signal_artefacto, label="Ruido de Artefacto", color="green")
plt.title("Señal con Ruido de Artefacto")
plt.legend()

plt.tight_layout()
plt.show()
