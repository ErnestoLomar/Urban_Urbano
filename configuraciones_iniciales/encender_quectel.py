import time
import subprocess
import sys
import os
import datetime
from time import strftime

sys.path.insert(1, '/home/pi/Urban_Urbano/configuraciones_iniciales/actualizacion')
sys.path.insert(1, '/home/pi/Urban_Urbano/utils')
sys.path.insert(1, '/home/pi/Urban_Urbano/db')

from asignaciones_queries import seleccionar_auto_asignaciones_antiguas, eliminar_auto_asignaciones_antiguas, seleccionar_fin_de_viaje_antiguos, eliminar_fin_de_viaje_antiguos
from tickets_usados import seleccionar_tickets_antiguos, eliminar_tickets_antiguos
from ventas_queries import seleccionar_ventas_antiguas, eliminar_ventas_antiguas
from queries import insertar_estadisticas_boletera, crear_tablas, obtener_datos_aforo
import variables_globales as vg
from eeprom_num_serie import cargar_num_serie
'''
from asignaciones_queries import eliminar_auto_asignaciones_antiguas, eliminar_fin_de_viaje_antiguos
from tickets_usados import eliminar_tickets_antiguos
from ventas_queries import eliminar_ventas_antiguas
'''

try:
    print("#############################################")
    print(f"Ernesto Lomar - Urban Urbano {vg.version_del_software}")
except Exception as e:
    print("Error al imprimir el nombre del sistema: "+str(e))

from FTP import Principal_Modem
import actualizar_hora

intentos = 0

def Encender_QUECTEL():
    global intentos
    try:
        
        try:
            print('Cargando sistema ...')
            time.sleep(20)
            modem = Principal_Modem()
            modem.inicializar_configuraciones_quectel()
        except Exception as e:
            print("Error al inicializar el modem: "+str(e))
            
        while True:
            if actualizar_hora.actualizar_hora():
                break
            print("################################################")
            time.sleep(2)
        
        
        try:
            # Verificamos que todas las tablas necesarias estén creadas.
            crear_tablas()
            
            datos_en_memoria_eeprom = cargar_num_serie()
            mac = subprocess.run("cat /sys/class/net/eth0/address", stdout=subprocess.PIPE, shell=True)
            fecha = strftime('%Y/%m/%d').replace('/', '')[2:]
            
            # Procedemos a obtener la hora de la boletera
            fecha_actual = str(subprocess.run("date", stdout=subprocess.PIPE, shell=True))
            indice = fecha_actual.find(":")
            hora = str(fecha_actual[(int(indice) - 2):(int(indice) + 6)]).replace(":","")
            
            print("Version del software: ", vg.version_del_software)
            print("Numero de version de la tablilla: ", datos_en_memoria_eeprom['state_num_version'])
            print("MAC: ", str(mac.stdout).replace("b","").replace("'","").replace("\r","").replace("\n",""))
            print("SIM: ", vg.sim_id)
            print("Numero de serie de la tablilla: ", datos_en_memoria_eeprom['state_num_serie'])
            print("Fecha: ", fecha)
            print("Hora: ", hora)
            
            version_raspberry = ""
            
            with open('/proc/device-tree/model', 'r') as f:
                model = f.read().strip()
                if 'Raspberry Pi' in model:
                    version_raspberry = model.split('Raspberry Pi')[1].strip()
                    print('Versión de la Raspberry Pi:', version_raspberry)
                else:
                    print('Este programa sólo funciona en una Raspberry Pi.')

            # Leer el archivo /proc/meminfo para obtener información sobre la memoria RAM
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()

            # Extraer la cantidad de memoria RAM total y usada
            total_ram = int(meminfo.split('MemTotal:')[1].split('kB')[0].strip()) * 1024
            usada_ram = int(meminfo.split('MemAvailable:')[1].split('kB')[0].strip()) * 1024

            # Ejecutar el comando 'df -h' y capturar la salida
            df_output = subprocess.check_output(['df', '-h'])

            # Convertir la salida a una lista de líneas de texto
            df_lines = df_output.decode('utf-8').split('\n')

            # Buscar la línea que contiene la información del sistema de archivos /
            root_fs_line = None
            for line in df_lines:
                if line.startswith('/dev/root'):
                    root_fs_line = line
                    break

            # Obtener los campos de espacio total y usado de la línea del sistema de archivos /
            if root_fs_line is not None:
                root_fs_fields = root_fs_line.split()
                total_rom = root_fs_fields[1]
                usada_rom = root_fs_fields[2]
            else:
                total_rom = 'Unknown'
                usada_rom = 'Unknown'

            # Imprimir los resultados
            print(f'Total ROM: {total_rom}')
            print(f'Used ROM: {usada_rom}')

            # Convertir bytes a megabytes
            total_ram_mb = total_ram / (1024 * 1024)
            usada_ram_mb = usada_ram / (1024 * 1024)

            # Imprimir la información
            print('Memoria RAM total:', str(total_ram_mb)[:6], 'MB')
            print('Memoria RAM usada:', str(usada_ram_mb)[:6], 'MB')
            print('Memoria ROM total:', total_rom)
            print('Memoria ROM usada:', usada_rom)
            
            # Procedemos a guardar las tramas 9
            datos_de_la_unidad = obtener_datos_aforo()
            insertar_estadisticas_boletera(str(datos_de_la_unidad[1]), fecha, hora, "Columna_VSW", vg.version_del_software) # Version del software
            insertar_estadisticas_boletera(str(datos_de_la_unidad[1]), fecha, hora, "Columna_VT", datos_en_memoria_eeprom['state_num_version']) # Version de la tablilla
            insertar_estadisticas_boletera(str(datos_de_la_unidad[1]), fecha, hora, "Columna_NST", datos_en_memoria_eeprom['state_num_serie']) # Numero de serie de tablilla
            insertar_estadisticas_boletera(str(datos_de_la_unidad[1]), fecha, hora, "Columna_MACRPI", str(mac.stdout).replace("b","").replace("'","").replace("\r","").replace("\n","")) # MAC de raspberry
            insertar_estadisticas_boletera(str(datos_de_la_unidad[1]), fecha, hora, "Columna_IDSIM", str(vg.sim_id)) # ID SIM
            insertar_estadisticas_boletera(str(datos_de_la_unidad[1]), fecha, hora, "Columna_APNSIM", "internet.itelcel.com") # ID SIM
            insertar_estadisticas_boletera(str(datos_de_la_unidad[1]), fecha, hora, "Columna_Socket", str(datos_de_la_unidad[2])) # Socket
            insertar_estadisticas_boletera(str(datos_de_la_unidad[1]), fecha, hora, "Columna_MT", vg.version_de_MT) # Matriz tarifaría
            insertar_estadisticas_boletera(str(datos_de_la_unidad[1]), fecha, hora, "Columna_VRPI", version_raspberry) # Version raspberry
            insertar_estadisticas_boletera(str(datos_de_la_unidad[1]), fecha, hora, "Columna_RAMRPI", f"{str(usada_ram_mb)[:6]}/{str(total_ram_mb)[:6]}MB") # RAM raspberry
            insertar_estadisticas_boletera(str(datos_de_la_unidad[1]), fecha, hora, "Columna_ROMRPI", f"{usada_rom}/{total_rom}") # ROM raspberry
            
        except Exception as e:
            print(e)
            
        print("################################################")
        try:
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
            
            try:
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
            except Exception as e:
                print("Error al verificar las auto asignaciones: "+str(e))
                    
            time.sleep(0.10)
            print("\n")
            
            try:
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
            except Exception as e:
                print("Error al verificar los fin de viaje: "+str(e))
                    
            time.sleep(0.10)
            print("\n")
            
            try:
                # Procedemos a hacer el chequeo de los registros de tickets en la base de datos
                todas_los_tickets_antiguos = seleccionar_tickets_antiguos()
                print("Todas las tickets antiguos: ", todas_los_tickets_antiguos)
                if len(todas_los_tickets_antiguos) > 0:
                    contador_de_tickets_eliminadas = 0
                    for i in range(len(todas_los_tickets_antiguos)):
                        qr_completo = str(todas_los_tickets_antiguos[i][1]).split("-")
                        print("QR completo: ", qr_completo)
                        cadena_fecha_ticket = str(str(qr_completo[2]).split(",")[0])+qr_completo[1]+qr_completo[0]
                        if int(cadena_fecha_ticket) <= int(fecha_hace_15_dias):
                            eliminado_tickets_db = eliminar_tickets_antiguos(todas_los_tickets_antiguos[i][0])
                            if eliminado_tickets_db:
                                contador_de_tickets_eliminadas+=1
                    if contador_de_tickets_eliminadas > 0:
                        print("Tickets verificados, se eliminaron "+str(contador_de_tickets_eliminadas)+" registros")
                    else:
                        print("No se eliminaron registros de tickets")
            except Exception as e:
                print("Error al verificar los tickets: "+str(e))
                    
            time.sleep(0.10)
            print("\n")
            
            try:
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
            except Exception as e:
                print("Error al verificar las ventas: "+str(e))
                    
            time.sleep(0.10)
            
            print("Se terminó de verificar las bases de datos")
            print("################################################")
        except Exception as e:
            print("Ocurrió un error al verificar las bases de datos: ", e)
            time.sleep(0.10)
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