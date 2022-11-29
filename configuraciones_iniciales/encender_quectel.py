import time
import subprocess
import sys
import os

sys.path.insert(1, '/home/pi/Urban_Urbano/configuraciones_iniciales/actualizacion')
sys.path.insert(1, '/home/pi/Urban_Urbano/utils')

from variables_globales import version_del_software

try:
    print("#############################################")
    print(f"Ernesto Lomar - Urban Urbano {version_del_software}")
except Exception as e:
    print("Error al imprimir el nombre del sistema: "+str(e))

from FTP import Principal_Modem
import actualizar_hora

intentos = 0

def Encender_QUECTEL():
    global intentos
    try:
        print('Cargando sistema ...')
        time.sleep(20)
        modem = Principal_Modem()
        modem.inicializar_configuraciones_quectel()
        while True:
            if actualizar_hora.actualizar_hora():
                break
            print("################################################")
            time.sleep(3)
        if os.path.exists("/home/pi/Urban_Urbano/ventanas/inicio.py"):
            subprocess.run("sudo python3 /home/pi/Urban_Urbano/ventanas/inicio.py",shell=True)
        else:
            print("No se encontró el archivo inicio.py")
    except Exception as e:
        print("ALGO OCURRIO AL INICIAR EL QUECTEL")
        intentos = intentos + 1
        if intentos < 5:
            Encender_QUECTEL()
        else:
            subprocess.run("sudo reboot",shell=True)
        print(e)

Encender_QUECTEL()