from PyQt5.QtCore import QObject, pyqtSignal
import time
import logging
import subprocess
from asignaciones_queries import obtener_asignacion_por_folio_de_viaje
from PyQt5.QtCore import QSettings
import variables_globales as vg
import datetime
from time import strftime

class DeteccionGeocercasWorker(QObject):
    try:
        finished = pyqtSignal()
        progress = pyqtSignal(dict)
        settings = QSettings('/home/pi/Urban_Urbano/ventanas/settings.ini', QSettings.IniFormat)
    except Exception as e:
        print(e)
        logging.info(e)

    def run(self):
        try:
            try:
                from abrir_ventanas import AbrirVentanas
            except Exception as e:
                print(e)
            
            while True:
                
                import variables_globales
                self.longitud = variables_globales.longitud
                self.latitud = variables_globales.latitud
                
                try:
                    fecha_actual = str(subprocess.run("date", stdout=subprocess.PIPE, shell=True).stdout.decode())
                    print("La fecha actual de la RPI es: ",fecha_actual)
                    indice = fecha_actual.find(":")
                    hora_actual = fecha_actual[(int(indice) - 2):(int(indice) + 6)]
                    print("LA HORA ACTUAL RPI ES: ", hora_actual)
                    
                    #Obtenemos el folio de viaje
                    if len(self.settings.value('folio_de_viaje')) > 0:
                        trama_dos_del_viaje = obtener_asignacion_por_folio_de_viaje(self.settings.value('folio_de_viaje'))
                    else:
                        trama_dos_del_viaje = obtener_asignacion_por_folio_de_viaje(vg.folio_asignacion)
                    
                    #Obtenemos la fecha del dia de hoys
                    hoy = datetime.datetime.now().date()
                    
                    fecha_hace_dos_dias = hoy - datetime.timedelta(days=2)
                    fecha_ayer = hoy - datetime.timedelta(days=1)
                    
                    fecha_completa_trama_dos = str(str(trama_dos_del_viaje).split(",")).replace("'","").replace('"','').replace("[","").replace("]","").replace("(","").replace(")","").replace(" ","").split(",")
                    fecha_de_trama_dos = str(fecha_completa_trama_dos[5]).replace("-","/")
                    hora_trama_dos = str(fecha_completa_trama_dos[6])
                    
                    fecha_datetime_trama_dos = datetime.datetime.strptime(fecha_de_trama_dos, "%d/%m/%Y")
                    fecha_datetime_hoy = datetime.datetime.strptime(str(hoy).replace("-","/"), "%Y/%m/%d")
                    fecha_datetime_hace_dos_dias = datetime.datetime.strptime(str(fecha_hace_dos_dias).replace("-","/"), "%Y/%m/%d")
                    fecha_datetime_ayer = datetime.datetime.strptime(str(fecha_ayer).replace("-","/"), "%Y/%m/%d")
                    
                    fecha_formateada_trama_dos = fecha_datetime_trama_dos.strftime("%d/%m/%Y")
                    fecha_formateada_hoy = fecha_datetime_hoy.strftime("%d/%m/%Y")
                    fecha_formateada_hace_dos_dias = fecha_datetime_hace_dos_dias.strftime("%d/%m/%Y")
                    fecha_formateada_ayer = fecha_datetime_ayer.strftime("%d/%m/%Y")
                    
                    print("La fecha de la trama dos formateada es: ", fecha_formateada_trama_dos)
                    print("La fecha de hoy formateada es: ", fecha_formateada_hoy)
                    print("La fecha de hace dos dias formateada es: ", fecha_formateada_hace_dos_dias)
                    print("La fecha de ayer es: ", fecha_formateada_ayer)
                    
                    if int(hora_actual[:2]) <= 2:
                        
                        if (fecha_formateada_trama_dos <= fecha_formateada_hace_dos_dias) or (fecha_formateada_trama_dos <= fecha_formateada_ayer and int(hora_trama_dos[:2]) <= 2):
                            print("El inicio de viaje es de hace dos dias o mas, o hace un dia pero antes de las 2am.")
                            AbrirVentanas.cerrar_vuelta.cargar_datos()
                            AbrirVentanas.cerrar_vuelta.show()
                            AbrirVentanas.cerrar_vuelta.terminar_vuelta(AbrirVentanas.cerrar_vuelta)
                            AbrirVentanas.cerrar_turno.cargar_datos()
                            AbrirVentanas.cerrar_turno.show()
                            AbrirVentanas.cerrar_turno.cerrar_turno(AbrirVentanas.cerrar_turno)
                    
                    elif int(hora_actual[:2]) > 2:
                        
                        if fecha_formateada_trama_dos <= fecha_formateada_ayer:
                            print("El inicio de viaje tiene de diferencia un dia o mas de estar abierto.")
                            AbrirVentanas.cerrar_vuelta.cargar_datos()
                            AbrirVentanas.cerrar_vuelta.show()
                            AbrirVentanas.cerrar_vuelta.terminar_vuelta(AbrirVentanas.cerrar_vuelta)
                            AbrirVentanas.cerrar_turno.cargar_datos()
                            AbrirVentanas.cerrar_turno.show()
                            AbrirVentanas.cerrar_turno.cerrar_turno(AbrirVentanas.cerrar_turno)
                except Exception as e:
                    print(e)
                
                self.detectando_geocercas_hilo = variables_globales.detectando_geocercas_hilo
                if self.detectando_geocercas_hilo == False:
                    variables_globales.detectando_geocercas_hilo = True
                    self.finished.emit()
                    break
                self.progress.emit({"longitud": self.longitud, "latitud": self.latitud})
                time.sleep(5)
        except Exception as e:
            print(e)
            logging.info(e)