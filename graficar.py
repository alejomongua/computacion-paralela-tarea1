import os
import subprocess
import sys
import time

import matplotlib.pyplot as plt

C_PROGRAM_TEMPLATE = 'pi_para_posix-thread.c'
BUILD_FOLDER = 'build'
OUTPUT_FOLDER = 'build'
THREADS = [1, 2, 4, 8, 16]
ITERATIONS = 5

def compilar(num_threads, con_gap=True):
    """
    Compila el programa con el número de hilos indicado
    """
    if con_gap:
        gap_multiplier = '8'
        salida = f"{BUILD_FOLDER}/threads{num_threads}_con_gap"
    else:
        gap_multiplier = '1'
        salida = f"{BUILD_FOLDER}/threads{num_threads}_sin_gap"

    exit_code = subprocess.call([
        "gcc",
        f"-DTHREADS={num_threads}",
        f"-DGAP_MULTIPLIER={gap_multiplier}",
        C_PROGRAM_TEMPLATE,
        "-o",
        salida,
        '-lpthread',
    ])
    if exit_code:
        print(f"Error al compilar threads{num_threads} ({exit_code})")
        sys.exit(exit_code)

def generar_ejecutables():
    """
    Compila a partir de la plantilla dependiendo del número de hilos
    retorna prematuramente si hay error al compilar
    """

    # Si no existe el directorio de salida, lo crea
    if not os.path.exists(BUILD_FOLDER):
        os.makedirs(BUILD_FOLDER)

    for num_threads in THREADS:
        # Genera ejecutable sin gap
        compilar(num_threads, con_gap=False)

        # Genera ejecutable con gap
        compilar(num_threads)

def ejecutar(num_threads, con_gap=True):
    """
    Ejecuta uno de los archivos compilados
    retorna el tiempo de ejecución
    """
    if con_gap:
        salida = f"{BUILD_FOLDER}/threads{num_threads}_con_gap"
    else:
        salida = f"{BUILD_FOLDER}/threads{num_threads}_sin_gap"

    start = time.time()
    exit_code = subprocess.call([salida])
    elapsed = time.time() - start
    if exit_code:
        print(f"Error al ejecutar threads{num_threads} ({exit_code})")
        sys.exit(exit_code)

    return elapsed

def ejecutar_todos():
    """
    Ejecuta todos los ejecutables generados
    Esta es la función que más tarda, puede tardar varios minutos
    Retorna un array con los tiempos para ser graficado
    """

    # La salida es un array de arrays con el siguiente formato
    #[ 
    #   [
    #       num_threads,
    #       tiempo_de_ejecucion_con_gap,
    #       tiempo_de_ejecucion_sin_gap,
    #   ],
    #]
    salida = []

    # Se itera por el número de threads
    for num_threads in THREADS:
        print(f'Pruebas con {num_threads} hilos')
        tiempos_con_gap = []
        tiempos_sin_gap = []
        # Se toman ITERATIONS datos para cada ejecutable
        for _ in range(ITERATIONS):
            tiempo_sin_gap = ejecutar(num_threads)
            tiempo_con_gap = ejecutar(num_threads, con_gap=False)
            tiempos_con_gap.append(tiempo_sin_gap)
            tiempos_sin_gap.append(tiempo_con_gap)

        # Se calcula el promedio de los tiempos
        promedio_con_gap = sum(tiempos_con_gap) / len(tiempos_con_gap)
        promedio_sin_gap = sum(tiempos_sin_gap) / len(tiempos_sin_gap)
        print(f'Promedio con gap: {promedio_con_gap}')
        print(f'Promedio sin gap: {promedio_sin_gap}')
        print()
        salida.append([num_threads, promedio_con_gap, promedio_sin_gap])
    
    return salida

def graficar(datos):
    """
    Se grafican los resultados de las ejecuciones
    """
    # Si no existe el directorio de salida, lo crea
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    eje_x = [item[0] for item in datos]
    con_gap = [item[1] for item in datos]
    sin_gap = [item[2] for item in datos]

    plt.title('Tiempo de ejecución vs cantidad de hilos')
    plt.xlabel('Hilos')
    plt.ylabel('Tiempo (s)')
    plt.plot(eje_x, con_gap, label='Con Gap', marker='o')
    plt.plot(eje_x, sin_gap, label='Sin Gap', marker='x')
    plt.legend(loc='upper right')
    plt.savefig(f'{OUTPUT_FOLDER}/salida.pdf')


def main():
    """Entry point"""
    generar_ejecutables()

    datos_grafica = ejecutar_todos()

    graficar(datos_grafica)

if __name__ == '__main__':
    main()
