# Tarea numero 1

Gráfica de tiempos de programa paralelizado

Se graficarán los tiempos que se en calcular pi con 2e9 iteraciones paralelizando el proceso en 1, 2, 4, 8 y 16 hilos

También se graficarán los tiempos quitando el gap que se deja para que las variables que se accederán de manera concurrente no queden en el mismo bloque de caché del procesador

## Setup

Crear el ambiente virtual

    python3 -m pip install virtualenv
    mkdir venv
    virtualenv -p python3 venv

Instalar requerimientos

    pip install -r requirements.txt

Activar el ambiente virtual:

    source venv/bin/activate

Ejecutar el programa

    python graficar.py

La gráfica generada queda en build/salida.pdf

