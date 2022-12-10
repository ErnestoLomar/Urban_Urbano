import time
import subprocess
import sys
import os
import datetime

sys.path.insert(1, '/home/pi/Urban_Urbano/configuraciones_iniciales/actualizacion')
sys.path.insert(1, '/home/pi/Urban_Urbano/utils')
sys.path.insert(1, '/home/pi/Urban_Urbano/db')

from asignaciones_queries import seleccionar_auto_asignaciones_antiguas, eliminar_auto_asignaciones_antiguas, seleccionar_fin_de_viaje_antiguos, eliminar_fin_de_viaje_antiguos
from tickets_usados import seleccionar_tickets_antiguos, eliminar_tickets_antiguos
from ventas_queries import seleccionar_ventas_antiguas, eliminar_ventas_antiguas
from variables_globales import version_del_software
'''
from asignaciones_queries import eliminar_auto_asignaciones_antiguas, eliminar_fin_de_viaje_antiguos
from tickets_usados import eliminar_tickets_antiguos
from ventas_queries import eliminar_ventas_antiguas
'''

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
        """
        print("################################################")
        print("Verificando bases de datos...")
        fecha_ahora = datetime.datetime.utcnow()
        print("Hoy es "+str(fecha_ahora))
        fecha_antigua = fecha_ahora - datetime.timedelta(days=15)
        print("Hace 15 días fue "+str(fecha_antigua))
        año_hace_15_dias = str(fecha_antigua)[:4]
        mes_hace_15_dias = str(fecha_antigua)[5:7]
        dia_hace_15_dias = str(fecha_antigua)[8:10]
        fecha_hace_15_dias = dia_hace_15_dias+"-"+mes_hace_15_dias+"-"+año_hace_15_dias
        print("La fecha hace 15 días es "+str(fecha_hace_15_dias))
        eliminado_inicio_viaje_db = False
        eliminado_fin_de_viaje_db = False
        eliminado_tickets_db = False
        eliminado_ventas_db = False
        todos_los_auto_asignaciones_antiguas = seleccionar_auto_asignaciones_antiguas(fecha_hace_15_dias)
        print("Todas las auto asignaciones antiguas: ", todos_los_auto_asignaciones_antiguas)
        eliminado_inicio_viaje_db = eliminar_auto_asignaciones_antiguas(fecha_hace_15_dias)
        if eliminado_inicio_viaje_db:
            print("Auto asignaciones verificadas")
        else:
            print("Ocurrió un problema al verificar las auto asignaciones")
        time.sleep(1)
        todas_los_de_fin_de_viaje_antiguas = seleccionar_fin_de_viaje_antiguos(fecha_hace_15_dias)
        print("Todas las ventas de fin de viaje antiguas: ", todas_los_de_fin_de_viaje_antiguas)
        eliminado_fin_de_viaje_db = eliminar_fin_de_viaje_antiguos(fecha_hace_15_dias)
        if eliminado_fin_de_viaje_db:
            print("Fin de viajes verificados")
        else:
            print("Ocurrió un problema al verificar los fin de viajes")
        time.sleep(1)
        todas_los_tickets_antiguos = seleccionar_tickets_antiguos(fecha_hace_15_dias)
        print("Todos los tickets antiguos: ", todas_los_tickets_antiguos)
        eliminado_tickets_db = eliminar_tickets_antiguos(fecha_hace_15_dias)
        if eliminado_tickets_db:
            print("Tickets verificados")
        else:
            print("Ocurrió un problema al verificar los tickets")
        time.sleep(1)
        todas_las_ventas_antiguas = seleccionar_ventas_antiguas(fecha_hace_15_dias)
        print("Todas las ventas antiguas: ", todas_las_ventas_antiguas)
        eliminado_ventas_db = eliminar_ventas_antiguas(fecha_hace_15_dias)
        if eliminado_ventas_db:
            print("Ventas verificadas")
        else:
            print("Ocurrió un problema al verificar las ventas")
        time.sleep(1)
        print("Se terminó de verificar las bases de datos")
        print("################################################")"""
        if os.path.exists("/home/pi/Urban_Urbano/ventanas/inicio.py"):
            subprocess.run("sudo python3 /home/pi/Urban_Urbano/ventanas/inicio.py",shell=True)
        else:
            print("No se encontró el archivo inicio.py")
    except Exception as e:
        print("ALGO OCURRIO AL INICIAR EL SISTEMA: ", e)
        intentos = intentos + 1
        if intentos < 5:
            Encender_QUECTEL()
        else:
            subprocess.run("sudo reboot",shell=True)
        print(e)

Encender_QUECTEL()