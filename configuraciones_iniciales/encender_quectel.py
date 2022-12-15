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
            
        print("################################################")
        print("Verificando bases de datos...")
        fecha_ahora = datetime.datetime.utcnow()
        print("Hoy es "+str(fecha_ahora))
        fecha_antigua = fecha_ahora - datetime.timedelta(days=15)
        print("Hace 15 días fue "+str(fecha_antigua))
        año_hace_15_dias = str(fecha_antigua)[:4]
        mes_hace_15_dias = str(fecha_antigua)[5:7]
        dia_hace_15_dias = str(fecha_antigua)[8:10]
        fecha_hace_15_dias = año_hace_15_dias+mes_hace_15_dias+dia_hace_15_dias
        print("La fecha hace 15 días es "+str(fecha_hace_15_dias))
        eliminado_inicio_viaje_db = False
        eliminado_fin_de_viaje_db = False
        eliminado_tickets_db = False
        eliminado_ventas_db = False
        
        # Procedemos a hacer el chequeo de los registros de auto_asignaciones en la base de datos
        todos_los_auto_asignaciones_antiguas = seleccionar_auto_asignaciones_antiguas()
        print("Todas las auto asignaciones antiguas: ", todos_los_auto_asignaciones_antiguas)
        if len(todos_los_auto_asignaciones_antiguas) > 0:
            contador_de_auto_asignaciones_eliminadas = 0
            for i in range(len(todos_los_auto_asignaciones_antiguas)):
                lista_fecha = str(todos_los_auto_asignaciones_antiguas[i][1]).split("-")
                cadena_fecha = lista_fecha[2]+lista_fecha[1]+lista_fecha[0]
                if int(cadena_fecha) <= int(fecha_hace_15_dias):
                    eliminado_inicio_viaje_db = eliminar_auto_asignaciones_antiguas(todos_los_auto_asignaciones_antiguas[i][0])
                    if eliminado_inicio_viaje_db:
                        contador_de_auto_asignaciones_eliminadas+=1
            if contador_de_auto_asignaciones_eliminadas > 0:
                print("Auto asignaciones verificadas, se eliminaron "+str(contador_de_auto_asignaciones_eliminadas)+" registros")
            else:
                print("No se eliminaron registros de auto asignaciones")
                
        time.sleep(1)
        print("\n")
        
        # Procedemos a hacer el chequeo de los registros de fin_de_viaje en la base de datos
        todas_los_de_fin_de_viaje_antiguas = seleccionar_fin_de_viaje_antiguos()
        print("Todas los fin de viaje antiguos: ", todas_los_de_fin_de_viaje_antiguas)
        if len(todas_los_de_fin_de_viaje_antiguas) > 0:
            contador_de_fin_viaje_eliminadas = 0
            for i in range(len(todas_los_de_fin_de_viaje_antiguas)):
                lista_fecha_fin = str(todas_los_de_fin_de_viaje_antiguas[i][1]).split("-")
                cadena_fecha_fin = lista_fecha_fin[2]+lista_fecha_fin[1]+lista_fecha_fin[0]
                if int(cadena_fecha_fin) <= int(fecha_hace_15_dias):
                    eliminado_fin_de_viaje_db = eliminar_fin_de_viaje_antiguos(todas_los_de_fin_de_viaje_antiguas[i][0])
                    if eliminado_fin_de_viaje_db:
                        contador_de_fin_viaje_eliminadas+=1
            if contador_de_fin_viaje_eliminadas > 0:
                print("Fin de viaje verificados, se eliminaron "+str(contador_de_fin_viaje_eliminadas)+" registros")
            else:
                print("No se eliminaron registros de fin de viaje")
                
        time.sleep(1)
        print("\n")
        
        # Procedemos a hacer el chequeo de los registros de tickets en la base de datos
        todas_los_tickets_antiguos = seleccionar_tickets_antiguos()
        print("Todas las tickets antiguos: ", todas_los_tickets_antiguos)
        if len(todas_los_tickets_antiguos) > 0:
            contador_de_tickets_eliminadas = 0
            for i in range(len(todas_los_tickets_antiguos)):
                lista_fecha_ticket = str(todas_los_tickets_antiguos[i][1]).split("-")
                cadena_fecha_ticket = lista_fecha_ticket[2]+lista_fecha_ticket[1]+lista_fecha_ticket[0]
                if int(cadena_fecha_ticket) <= int(fecha_hace_15_dias):
                    eliminado_tickets_db = eliminar_tickets_antiguos(todas_los_tickets_antiguos[i][0])
                    if eliminado_tickets_db:
                        contador_de_tickets_eliminadas+=1
            if contador_de_tickets_eliminadas > 0:
                print("Tickets verificados, se eliminaron "+str(contador_de_tickets_eliminadas)+" registros")
            else:
                print("No se eliminaron registros de tickets")
                
        time.sleep(1)
        print("\n")
        
        # Procedemos a hacer el chequeo de los registros de ventas en la base de datos
        todas_las_ventas_antiguas = seleccionar_ventas_antiguas()
        print("Todas las ventas antiguas: ", todas_las_ventas_antiguas)
        if len(todas_las_ventas_antiguas) > 0:
            contador_de_ventas_eliminadas = 0
            for i in range(len(todas_las_ventas_antiguas)):
                lista_fecha_ventas = str(todas_las_ventas_antiguas[i][1]).split("-")
                cadena_fecha_venta = lista_fecha_ventas[2]+lista_fecha_ventas[1]+lista_fecha_ventas[0]
                if int(cadena_fecha_venta) <= int(fecha_hace_15_dias):
                    eliminado_ventas_db = eliminar_ventas_antiguas(todas_las_ventas_antiguas[i][0])
                    if eliminado_ventas_db:
                        contador_de_ventas_eliminadas+=1
            if contador_de_ventas_eliminadas > 0:
                print("Ventas verificadas, se eliminaron "+str(contador_de_ventas_eliminadas)+" registros")
            else:
                print("No se eliminaron registros de ventas")
                
        time.sleep(1)
        
        print("Se terminó de verificar las bases de datos")
        print("################################################")
        
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