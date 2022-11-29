##########################################
# Autor: Ernesto Lomar
# Fecha de creación: 12/04/2022
# Ultima modificación: 16/08/2022
#
# Script para la comunicación con el modem.
#
##########################################

#Librerías externas
from PyQt5.QtCore import QObject, pyqtSignal
import time
import logging
from time import strftime
import subprocess
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSettings
import sys

sys.path.insert(1, '/home/pi/Urban_Urbano/db')
sys.path.insert(1, '/home/pi/Urban_Urbano/configuraciones_iniciales/actualizacion')

#Librerias propias
from comand import Comunicacion_Minicom, Principal_Modem
import variables_globales
from queries import obtener_datos_aforo
from asignaciones_queries import guardar_actualizacion, obtener_asignaciones_no_enviadas, actualizar_asignacion_check_servidor, obtener_todas_las_asignaciones_no_enviadas
import variables_globales
from comand import Comunicacion_Minicom, Principal_Modem
import variables_globales
from folio import cargarFolioActual, actualizar_folio
from asignaciones_queries import actualizar_estado_del_viaje_check_servidor, obtener_estado_de_viajes_no_enviados, obtener_asignacion_por_folio_de_viaje, obtener_fin_de_viaje_por_folio_de_viaje
from ventas_queries import obtener_estado_de_ventas_no_enviadas, actualizar_estado_venta_check_servidor, obtener_venta_por_folio_y_foliodeviaje, obtener_estado_de_todas_las_ventas_no_enviadas
from actualizar import Actualizar

#Creamos un objeto de la clase Principal_Modem
modem = Principal_Modem()

#Es un QObject que emite una señal cuando está hecho.
class LeerMinicomWorker(QObject):

    def __init__(self) -> None:
        super().__init__()
        try:
            modem.abrir_puerto()
            self.settings = QSettings('/home/pi/Urban_Urbano/ventanas/settings.ini', QSettings.IniFormat)
            self.idUnidad = str(obtener_datos_aforo()[1])
        except Exception as e:
            print("\x1b[1;31;47m"+"LeerMinicom.py, linea 39: "+str(e)+'\033[0;m')
            logging.info("LeerMinicom.py, linea 39: "+str(e))
        try:
            self.intentos_envio = 0
            self.recibido_folio_webservice = 0
        except Exception as e:
            print("\x1b[1;31;47m"+"LeerMinicom.py, linea 47: "+str(e)+'\033[0;m')
            logging.info("LeerMinicom.py, linea 47: "+str(e))
    try:
        finished = pyqtSignal()
        progress = pyqtSignal(dict)
        hora_actualizada = False
    except Exception as e:
        print("\x1b[1;31;47m"+"LeerMinicom.py, linea 64: "+str(e)+'\033[0;m')
        logging.info("LeerMinicom.py, linea 64: "+str(e))

    #Crea un nuevo hilo, y en ese hilo ejecuta una función que emite una señal cada segundo
    def run(self):
        
        try:
            self.contador_servidor = 0
            respuesta = cargarFolioActual()
            self.folio = respuesta['folio']
            if self.folio != 1:
                self.folio = self.folio + 1
            id_folio = respuesta['id']
            self.reenviar = self.folio
        except Exception as e:
            logging.info("Error al actualizar folio: "+str(e))
            print("\x1b[1;31;47m"+"LeerMinicom.py, linea 66: "+str(e)+'\033[0;m')
        try:
            while True:
                
                if self.folio == self.reenviar + 30:
                    #self.reenviar_varios_datos_servidor()
                    self.reenviar = self.folio

                res = Comunicacion_Minicom()
                res['signal_3g'] = modem.signal_3g()
                res['connection_3g'] = modem.conex_3g()
                variables_globales.signal = res['signal_3g']
                variables_globales.connection_3g = res['connection_3g']
                folio_asignacion_viaje = variables_globales.folio_asignacion
                fecha_completa = strftime('%Y-%m-%d %H:%M:%S')
                fecha = strftime("%m/%d/%Y")
                hora = strftime("%H:%M:%S")
                dia = strftime("%d-%m-%Y")
                enviado = ''
                trama = ''
                
                if ("error" not in res.keys()):
                    #GPS FUNCIONA
                    variables_globales.longitud = res['longitud']
                    variables_globales.latitud = res['latitud']
                    variables_globales.velocidad = res['velocidad']
                    variables_globales.GPS = "ok"

                    actualizar_folio(id_folio, self.folio, fecha)

                    if self.contador_servidor >= 4:
                        
                        if folio_asignacion_viaje != 0:
                            trama = "3"+","+str(self.folio)+','+str(folio_asignacion_viaje)+","+hora+","+str(res['latitud'])+","+str(res['longitud'])+","+str(variables_globales.geocerca.split(",")[0])+","+str(res['velocidad'])
                            result = modem.mandar_datos(trama)
                            enviado = result['enviado']
                            if enviado == True:
                                print("\x1b[1;32m"+"#############################################")
                                print("\x1b[1;32m"+"Trama GNSS enviada: "+trama)
                                print("\x1b[1;32m"+"#############################################")
                                logging.info('Trama enviada: '+trama)
                            else:
                                logging.info('Trama no enviada: '+trama)
                                print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                                print("\x1b[1;31;47m"+"Trama GNSS no enviada: "+trama+'\033[0;m')
                                print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                            self.reeconectar_socket(enviado)
                            self.folio = self.folio + 1
                            self.realizar_accion(result)
                        else:
                            folio_de_viaje_sin_viaje = f"{''.join(fecha_completa[:10].split('-'))[3:]}{self.idUnidad}{99}"
                            trama = "3"+","+str(self.folio)+','+str(folio_de_viaje_sin_viaje)+","+hora+","+str(res['latitud'])+","+str(res['longitud'])+","+str(variables_globales.geocerca.split(",")[0])+","+str(res['velocidad'])
                            result = modem.mandar_datos(trama)
                            enviado = result['enviado']
                            if enviado == True:
                                print("\x1b[1;32m"+"#############################################")
                                print("\x1b[1;32m"+"Trama GNSS enviada: "+trama)
                                print("\x1b[1;32m"+"#############################################")
                                logging.info('Trama enviada: '+trama)
                            else:
                                logging.info('Trama no enviada: '+trama)
                                print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                                print("\x1b[1;31;47m"+"Trama GNSS no enviada: "+trama+'\033[0;m')
                                print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                            self.reeconectar_socket(enviado)
                            self.folio = self.folio + 1
                            self.realizar_accion(result)
                else:
                    variables_globales.GPS = "error"
                    logging.info('Error al obtener datos del GPS')
                    
                if self.contador_servidor >= 4:
                    try:
                        print("\x1b[1;32m"+"Verificando si hay datos en la BD por enviar...")
                        total_de_asignaciones_no_enviadas = obtener_todas_las_asignaciones_no_enviadas()
                        if len(total_de_asignaciones_no_enviadas) != 0:
                            try:
                                self.enviar_inicio_de_viaje()
                            except Exception as e:
                                print("\x1b[1;31;47m"+"LeerMinicom.py, linea 157: "+str(e)+'\033[0;m')
                        else:
                            try:
                                self.enviar_venta()
                            except Exception as e:
                                print("\x1b[1;31;47m"+"LeerMinicom.py, linea 163: "+str(e)+'\033[0;m')
                        total_de_ventas_no_enviadas = obtener_estado_de_todas_las_ventas_no_enviadas()
                        if variables_globales.folio_asignacion == 0 and len(total_de_ventas_no_enviadas) == 0:
                            try:
                                self.enviar_fin_de_viaje()
                            except Exception as e:
                                print("\x1b[1;31;47m"+"LeerMinicom.py, linea 169: "+str(e)+'\033[0;m')
                        print("\x1b[1;32m"+"Terminando de verificar si hay datos en la BD por enviar...")
                    except Exception as e:
                        logging.info('Error al enviar datos al servidor: '+str(e))
                        print("\x1b[1;31;47m"+"Error al enviar datos al servidor: "+str(e)+'\033[0;m')
                    self.contador_servidor = 0
                
                self.progress.emit(res)
                time.sleep(5)
                self.contador_servidor = self.contador_servidor + 1
        except Exception as e:
            print("\x1b[1;31;47m"+"LeerMinicom.py, linea 155: "+str(e)+'\033[0;m')
            logging.info("LeerMinicom.py, linea 155: "+str(e))

    def realizar_accion(self, result):
        """
        Si la clave "accion" esta en el diccionario de resultados del servidor, entonces el valor de la clave
        "accion" se asigna a la variable accion. Si accion es igual a "APAGAR", entonces la raspberrry se
        apaga. Si accion es igual a "REINICIAR", entonces se reinicia la raspberry. Si accion es igual a
        "ACTUALIZAR", entonces se actualiza el raspberry
        """
        try:
            if "accion" in result.keys():
                accion = result['accion']
                print("La accion a realizar es: " + accion)
                logging.info('La accion a realizar es: '+accion)
                fecha = strftime("%m/%d/%Y")
                if "A" in accion:
                    try:
                        print("Entro a A")
                        logging.info('Entro a A')
                        datos = accion.split(',')
                        if len(datos) == 2:
                            if self.recibido_folio_webservice <= 3:
                                self.recibido_folio_webservice +=1
                                self.settings.setValue("folio_de_viaje_webservice",datos[1])
                                print("Folio de web service recibido correctamente")
                                logging.info('Folio de web service recibido correctamente')
                            else:
                                if variables_globales.folio_asignacion == 0:
                                    self.recibido_folio_webservice = 0
                                    print("Reiniciando folio de web service")
                                    logging.info('Reiniciando folio de web service')
                    except Exception as e:
                        logging.info('Error al hacer accion A: '+str(e))
                        print("LeerMinicom.py, linea 138: "+str(e))
                if "B" in accion:
                    try:
                        logging.info('Entro a B')
                        total_de_ventas_no_enviadas = obtener_estado_de_ventas_no_enviadas()
                        total_de_inicio_de_viajes_no_enviados = obtener_asignaciones_no_enviadas()
                        total_de_fin_de_viajes_no_enviados = obtener_estado_de_viajes_no_enviados()
                        if len(total_de_ventas_no_enviadas) == 0 and len(total_de_inicio_de_viajes_no_enviados) == 0 and len(total_de_fin_de_viajes_no_enviados) == 0:
                            guardar_actualizacion('REINICIAR', fecha, 1)    
                            modem.cerrar_socket()
                            print("REINICIAR")
                            logging.info("Reinicio de raspberry por petición del servidor")
                            subprocess.run("sudo reboot", shell=True)
                        else:
                            while True:
                                if len(total_de_ventas_no_enviadas) == 0 and len(total_de_inicio_de_viajes_no_enviados) == 0 and len(total_de_fin_de_viajes_no_enviados) == 0:
                                    break
                                else:
                                    self.enviar_venta()
                                    self.enviar_inicio_de_viaje()
                                    self.enviar_fin_de_viaje()
                                    time.sleep(1)
                                    total_de_ventas_no_enviadas = obtener_estado_de_ventas_no_enviadas()
                                    total_de_inicio_de_viajes_no_enviados = obtener_asignaciones_no_enviadas()
                                    total_de_fin_de_viajes_no_enviados = obtener_estado_de_viajes_no_enviados()
                                    time.sleep(2)
                            guardar_actualizacion('REINICIAR', fecha, 1)    
                            modem.cerrar_socket()
                            print("REINICIAR")
                            logging.info("Reinicio de raspberry por petición del servidor")
                            subprocess.run("sudo reboot", shell=True)
                    except Exception as e:
                        print("LeerMinicom.py, linea 225: "+str(e))
                elif "C" in accion:
                    try:
                        logging.info('Entro a C')
                        datos = accion.split(',')
                        if len(datos) == 2:
                            try:
                                total_de_ventas_no_enviadas = obtener_estado_de_ventas_no_enviadas()
                                total_de_inicio_de_viajes_no_enviados = obtener_asignaciones_no_enviadas()
                                total_de_fin_de_viajes_no_enviados = obtener_estado_de_viajes_no_enviados()
                                if len(total_de_ventas_no_enviadas) == 0 and len(total_de_inicio_de_viajes_no_enviados) == 0 and len(total_de_fin_de_viajes_no_enviados) == 0:
                                    guardar_actualizacion('ACTUALIZAR', fecha, 1)
                                    logging.info("Actualizando raspberry por petición del servidor")
                                    ventana_actualzar = Actualizar()
                                    ventana_actualzar.show()
                                    ventana_actualzar.actualizar_raspberrypi(int(datos[1]))
                                else:
                                    while True:
                                        if len(total_de_ventas_no_enviadas) == 0 and len(total_de_inicio_de_viajes_no_enviados) == 0 and len(total_de_fin_de_viajes_no_enviados) == 0:
                                            break
                                        else:
                                            self.enviar_venta()
                                            self.enviar_inicio_de_viaje()
                                            self.enviar_fin_de_viaje()
                                            time.sleep(1)
                                            total_de_ventas_no_enviadas = obtener_estado_de_ventas_no_enviadas()
                                            total_de_inicio_de_viajes_no_enviados = obtener_asignaciones_no_enviadas()
                                            total_de_fin_de_viajes_no_enviados = obtener_estado_de_viajes_no_enviados()
                                            time.sleep(2)
                                    guardar_actualizacion('ACTUALIZAR', fecha, 1)
                                    logging.info("Actualizando raspberry por petición del servidor")
                                    ventana_actualzar = Actualizar()
                                    ventana_actualzar.show()
                                    ventana_actualzar.actualizar_raspberrypi(int(datos[1]))
                            except Exception as e:
                                print("LeerMinicom.py, linea 258: "+str(e))
                    except Exception as e:
                        print("LeerMinicom.py, linea 239: "+str(e))
                elif "D," in accion:
                    try:
                        logging.info('Entro a D')
                        datos = accion.split(',')
                        if datos[1] == "5":
                            try:
                                print("El servidor requiere una trama 5")
                                print(f"el servidor pide el folio {datos[2]} de los ventas")
                                print(f"del folio_de_viaje {datos[3]}")
                                folio = datos[2]
                                if folio != "99":
                                    folio_viaje = datos[3]
                                    if folio_viaje == "0":
                                        print("Se pide el folio de viaje actual")
                                        folio_viaje_competo = variables_globales.folio_asignacion
                                        venta_db = obtener_venta_por_folio_y_foliodeviaje(folio, folio_viaje_competo)
                                        print("La venta encontrada es: ",str(venta_db))
                                    else:
                                        print("Se pide un folio de viaje diferente al actual")
                                        fecha_viaje_pedido = folio_viaje[:6]
                                        folio_viaje_pedido = folio_viaje[6:]
                                        folio_viaje_competo = f"{fecha_viaje_pedido}{self.idUnidad}{folio_viaje_pedido}"
                                        venta_db = obtener_venta_por_folio_y_foliodeviaje(folio, folio_viaje_competo)
                                        print("La venta encontrada es: ",str(venta_db))
                                    try:
                                        if venta_db != None:
                                            id = venta_db[0]
                                            folio_aforo_venta = venta_db[1]
                                            folio_de_viaje = venta_db[2]
                                            hora_db = venta_db[4]
                                            id_del_servicio_o_transbordo = venta_db[5]
                                            id_geocerca = venta_db[6]
                                            id_tipo_de_pasajero = venta_db[7]
                                            transbordo_o_no = venta_db[8]

                                            trama = '5'+","+str(folio_aforo_venta)+","+str(folio_de_viaje)+","+str(hora_db)+","+str(id_del_servicio_o_transbordo)+","+str(id_geocerca)+","+str(id_tipo_de_pasajero)+","+str(transbordo_o_no)
                                            print("\x1b[1;32m"+"Reenviando venta: "+trama)
                                            logging.info("Reenviando venta: "+trama)
                                            result = modem.mandar_datos(trama)
                                            enviado = result['enviado']

                                            if enviado == True:
                                                try:
                                                    actualizar_estado_venta_check_servidor(id)
                                                    print("\x1b[1;32m"+"#############################################")
                                                    print("\x1b[1;32m"+"Trama de venta reenviada")
                                                    print("\x1b[1;32m"+"#############################################")
                                                    logging.info("Trama de venta reenviada")
                                                except Exception as e:
                                                    print("LeerMinicom.py, linea 376: "+str(e))
                                            else:
                                                print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                                                print("\x1b[1;31;47m"+"Trama de venta no reenviada"+'\033[0;m')
                                                print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                                                logging.info("No se pudo reenviar la trama de venta")
                                                self.reeconectar_socket(enviado)
                                                self.realizar_accion(result)
                                        else:
                                            print("\x1b[1;33m"+"No existe en la BD la venta solicitada.")
                                    except Exception as e:
                                        print("LeerMinicom.py, linea 378: "+str(e))
                                else:
                                    print("El servidor pide folio de venta 99")
                            except Exception as e:
                                print("LeerMinicom.py, linea 316: "+str(e))
                        elif datos[1] == "2":
                            try:
                                print("Se requiere una trama 2")
                                print(f"el servidor pide el folio de inicio de viaje {datos[2]} de los inicio de viajes")
                                folio_de_viaje_pedido = datos[2]
                                if folio_de_viaje_pedido == "0":
                                    folio_viaje_competo = variables_globales.folio_asignacion
                                    inicio_de_viaje_db = obtener_asignacion_por_folio_de_viaje(folio_viaje_competo)
                                else:
                                    fecha_viaje_pedido = folio_viaje[:6]
                                    folio_viaje_pedido = folio_viaje[6:]
                                    if folio_viaje_pedido != "99":
                                        folio_viaje_competo = f"{fecha_viaje_pedido}{self.idUnidad}{folio_viaje_pedido}"
                                        inicio_de_viaje_db = obtener_asignacion_por_folio_de_viaje(folio_viaje_competo)
                                    else:
                                        print("El servidor pide folio de inicio de viaje 99")
                                        return
                                print("inicio_de_viaje_db: "+str(inicio_de_viaje_db))
                                try:
                                    if inicio_de_viaje_db != None:
                                        id = inicio_de_viaje_db[0]
                                        csn_chofer = inicio_de_viaje_db[2]
                                        servicio_pension = str(inicio_de_viaje_db[3]).replace("-", ",").split(",")[0]
                                        hora_inicio = inicio_de_viaje_db[5]
                                        folio_de_viaje = inicio_de_viaje_db[6]

                                        trama = '2'+","+str(folio_de_viaje)+","+str(hora_inicio)+","+str(csn_chofer)+","+servicio_pension
                                        print("\x1b[1;32m"+"Reenviando inicio de viaje: "+trama)
                                        logging.info("Reenviando inicio de viaje: "+trama)
                                        result = modem.mandar_datos(trama)
                                        enviado = result['enviado']

                                        if enviado == True:
                                            try:
                                                actualizar_asignacion_check_servidor(id)
                                                print("\x1b[1;32m"+"#############################################")
                                                print("\x1b[1;32m"+"Trama de inicio de viaje reenviada")
                                                print("\x1b[1;32m"+"#############################################")
                                                logging.info("Trama de inicio de viaje reenviada")
                                            except Exception as e:
                                                print("LeerMinicom.py, linea 376: "+str(e))
                                        else:
                                            logging.info("No se pudo reenviar la trama de inicio de viaje")
                                            print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                                            print("\x1b[1;31;47m"+"Trama de inicio de viaje no reenviada"+'\033[0;m')
                                            print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                                            self.reeconectar_socket(enviado)
                                            self.realizar_accion(result)
                                    else:
                                        print("\x1b[1;33m"+"No existe en la BD inicio de viaje solicitado.")
                                except Exception as e:
                                    print("LeerMinicom.py, linea 378: "+str(e))
                            except Exception as e:
                                print("LeerMinicom.py, linea 370: "+str(e))
                        elif datos[1] == "4":
                            try:
                                print("Se requiere una trama 4")
                                print(f"el servidor pide el folio de fin {datos[2]} de los fin de viajes")
                                folio_de_fin_de_viaje_pedido = datos[2]
                                if folio_de_fin_de_viaje_pedido == "0":
                                    folio_viaje_competo = variables_globales.folio_asignacion
                                    fin_de_viaje_db = obtener_fin_de_viaje_por_folio_de_viaje(folio_viaje_competo)
                                else:
                                    fecha_viaje_pedido = folio_viaje[:6]
                                    folio_viaje_pedido = folio_viaje[6:]
                                    if folio_viaje_pedido != "99":
                                        folio_viaje_competo = f"{fecha_viaje_pedido}{self.idUnidad}{folio_viaje_pedido}"
                                        fin_de_viaje_db = obtener_fin_de_viaje_por_folio_de_viaje(folio_viaje_competo)
                                    else:
                                        print("El servidor pide folio de fin de viaje 99")
                                        return
                                print("Final de viaje_db es: ", fin_de_viaje_db)
                                try:
                                    if fin_de_viaje_db != None:
                                        id = fin_de_viaje_db[0]
                                        csn_chofer = fin_de_viaje_db[1]
                                        hora_inicio = fin_de_viaje_db[3]
                                        total_de_folio_aforo_efectivo = fin_de_viaje_db[4]
                                        total_de_folio_aforo_tarjeta = fin_de_viaje_db[5]
                                        folio_de_viaje = fin_de_viaje_db[6]

                                        trama = '4'+","+str(folio_de_viaje)+","+str(hora_inicio)+","+str(csn_chofer)+","+str(total_de_folio_aforo_efectivo)+","+str(total_de_folio_aforo_tarjeta)
                                        print("\x1b[1;32m"+"Reenviando cierre de viaje: "+trama)
                                        logging.info("Reenviando cierre de viaje: "+trama)
                                        result = modem.mandar_datos(trama)
                                        enviado = result['enviado']

                                        if enviado == True:
                                            try:
                                                actualizar_estado_del_viaje_check_servidor(id)
                                                print("\x1b[1;32m"+"#############################################")
                                                print("\x1b[1;32m"+"Trama de fin de viaje reenviada")
                                                print("\x1b[1;32m"+"#############################################")
                                                logging.info("Trama de fin de viaje reenviada")
                                            except Exception as e:
                                                print("LeerMinicom.py, linea 376: "+str(e))
                                        else:
                                            print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                                            print("\x1b[1;31;47m"+"Trama de fin de viaje no reenviada"+'\033[0;m')
                                            print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                                            logging.info("No se pudo reenviar la trama de fin de viaje")
                                            self.reeconectar_socket(enviado)
                                            self.realizar_accion(result)
                                    else:
                                        print("\x1b[1;33m"+"No existe en la BD fin de viaje solicitado.")
                                except Exception as e:
                                    print("LeerMinicom.py, linea 378: "+str(e))
                            except Exception as e:
                                print("LeerMinicom.py, linea 370: "+str(e))
                    except Exception as e:
                        print("LeerMinicom.py, linea 253: "+str(e))
        except Exception as e:
            print("LeerMinicom.py, linea 255: "+str(e))

    def reeconectar_socket(self, enviado: bool):
        # Si el número de intentos de enviar un mensaje a través de tcp es 10, el socket se cierra y
        # se abre uno nuevo.
        try: 
            print("\x1b[1;32m"+'numero de intentos'+ str(int(self.intentos_envio) + 1))
            if enviado != True:
                self.intentos_envio = self.intentos_envio + 1
                if self.intentos_envio == 4:
                    try:
                        logging.info('Creando una nueva conexion con el socket')
                        print("\x1b[1;33m"+"Creando un nuevo socket......")
                        modem.cerrar_socket()
                        modem.abrir_puerto()
                    except Exception as e:
                        print("\x1b[1;31;47m"+"LeerMinicom.py, linea 176: "+str(e)+'\033[0;m')
                    """
                    elif self.intentos_envio == 4:
                        try:
                            logging.info('Creando una nueva maquina de estado')
                            print("\x1b[1;33m"+"Creando una nueva maquina de estado......")
                            modem.cerrar_socket()
                            modem.reiniciar_configuracion_quectel()
                            modem.abrir_puerto()
                        except Exception as e:
                            print("\x1b[1;31;47m"+"LeerMinicom.py, linea 186: "+str(e)+'\033[0;m')"""
                elif self.intentos_envio == 6:
                    try:
                        logging.info('Reiniciando el quectel')
                        print("\x1b[1;33m"+"Reiniciando el quectel......")
                        modem.cerrar_socket()
                        modem.reiniciar_QUEQTEL()
                        modem.reiniciar_configuracion_quectel()
                        modem.abrir_puerto()
                    except Exception as e:
                        print("\x1b[1;31;47m"+"LeerMinicom.py, linea 196: "+str(e)+'\033[0;m')
                    """
                    elif self.intentos_envio == 8:
                        try:
                            logging.info('Reiniciando la RASPBERRY')
                            print("\x1b[1;31;47m"+"Reiniciando la RASPBERRY......"+'\033[0;m')
                            resultado = "REINICIANDO"
                            time.sleep(5)
                            mensaje = QMessageBox()
                            mensaje.setIcon(QMessageBox.Info)
                            mensaje.about(self, "AVISO", f"AVISO: {resultado}")
                            time.sleep(5)
                            subprocess.run("sudo reboot", shell=True)
                            modem.cerrar_socket()
                            print("REINICIAR")
                            subprocess.run("sudo reboot", shell=True)
                        except Exception as e:
                            print("\x1b[1;31;47m"+"LeerMinicom.py, linea 196: "+str(e)+'\033[0;m')"""
                elif self.intentos_envio == 10:
                    self.intentos_envio = 0
            else:
                self.intentos_envio = 0
        except Exception as e:
            print("\x1b[1;31;47m"+"LeerMinicom.py, linea 178: "+str(e)+'\033[0;m')
    
    def enviar_inicio_de_viaje(self):
        try:
            asignaciones = obtener_asignaciones_no_enviadas()

            if len(asignaciones) > 0:
                for asignacion in asignaciones:
                    try:
                        id = asignacion[0]
                        csn_chofer = asignacion[2]
                        servicio_pension = str(asignacion[3]).replace("-", ",").split(",")[0]
                        hora_inicio = asignacion[5]
                        folio_de_viaje = asignacion[6]

                        trama = '2'+","+str(folio_de_viaje)+","+str(hora_inicio)+","+str(csn_chofer)+","+servicio_pension
                        print("\x1b[1;32m"+"Enviando inicio de viaje: "+trama)
                        logging.info("Enviando inicio de viaje: "+trama)
                        result = modem.mandar_datos(trama)
                        enviado = result['enviado']

                        if enviado == True:
                            try:
                                actualizar_asignacion_check_servidor(id)
                                print("\x1b[1;32m"+"#############################################")
                                print("\x1b[1;32m"+"Trama de inicio de viaje enviada")
                                print("\x1b[1;32m"+"#############################################")
                                logging.info("Trama de inicio de viaje enviada")
                            except Exception as e:
                                print("LeerMinicom.py, linea 376: "+str(e))
                        else:
                            logging.info("No se pudo enviar la trama de inicio de viaje")
                            print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                            print("\x1b[1;31;47m"+"Trama de inicio de viaje no enviada"+'\033[0;m')
                            print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                            self.reeconectar_socket(enviado)
                            self.realizar_accion(result)
                    except Exception as e:
                        print("LeerMinicom.py, linea 378: "+str(e))
        except Exception as e:
            print("LeerMinicom.py, linea 380: "+str(e))

    def enviar_fin_de_viaje(self):
        try:
            viajes = obtener_estado_de_viajes_no_enviados()

            if len(viajes) > 0:
                for viaje in viajes:
                    try:
                        id = viaje[0]
                        csn_chofer = viaje[1]
                        hora_inicio = viaje[3]
                        total_de_folio_aforo_efectivo = viaje[4]
                        total_de_folio_aforo_tarjeta = viaje[5]
                        folio_de_viaje = viaje[6]

                        trama = '4'+","+str(folio_de_viaje)+","+str(hora_inicio)+","+str(csn_chofer)+","+str(total_de_folio_aforo_efectivo)+","+str(total_de_folio_aforo_tarjeta)
                        print("\x1b[1;32m"+"Enviando cierre de viaje: "+trama)
                        logging.info("Enviando cierre de viaje: "+trama)
                        result = modem.mandar_datos(trama)
                        enviado = result['enviado']

                        if enviado == True:
                            try:
                                actualizar_estado_del_viaje_check_servidor(id)
                                print("\x1b[1;32m"+"#############################################")
                                print("\x1b[1;32m"+"Trama de fin de viaje enviada")
                                print("\x1b[1;32m"+"#############################################")
                                logging.info("Trama de fin de viaje enviada")
                            except Exception as e:
                                print("LeerMinicom.py, linea 376: "+str(e))
                        else:
                            print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                            print("\x1b[1;31;47m"+"Trama de fin de viaje no enviada"+'\033[0;m')
                            print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                            logging.info("No se pudo enviar la trama de fin de viaje")
                            self.reeconectar_socket(enviado)
                            self.realizar_accion(result)
                    except Exception as e:
                        print("LeerMinicom.py, linea 378: "+str(e))
        except Exception as e:
            print("LeerMinicom.py, linea 380: "+str(e))
    
    def enviar_venta(self):
        try:
            ventas = obtener_estado_de_ventas_no_enviadas()

            if len(ventas) > 0:
                for venta in ventas:
                    try:
                        id = venta[0]
                        folio_aforo_venta = venta[1]
                        folio_de_viaje = venta[2]
                        hora_db = venta[4]
                        id_del_servicio_o_transbordo = venta[5]
                        id_geocerca = venta[6]
                        id_tipo_de_pasajero = venta[7]
                        transbordo_o_no = venta[8]

                        trama = '5'+","+str(folio_aforo_venta)+","+str(folio_de_viaje)+","+str(hora_db)+","+str(id_del_servicio_o_transbordo)+","+str(id_geocerca)+","+str(id_tipo_de_pasajero)+","+str(transbordo_o_no)
                        print("\x1b[1;32m"+"Enviando venta: "+trama)
                        logging.info("Enviando venta: "+trama)
                        result = modem.mandar_datos(trama)
                        enviado = result['enviado']

                        if enviado == True:
                            try:
                                actualizar_estado_venta_check_servidor(id)
                                print("\x1b[1;32m"+"#############################################")
                                print("\x1b[1;32m"+"Trama de venta enviada")
                                print("\x1b[1;32m"+"#############################################")
                                logging.info("Trama de venta enviada")
                            except Exception as e:
                                print("LeerMinicom.py, linea 376: "+str(e))
                        else:
                            print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                            print("\x1b[1;31;47m"+"Trama de venta no enviada"+'\033[0;m')
                            print("\x1b[1;31;47m"+"#############################################"+'\033[0;m')
                            logging.info("No se pudo enviar la trama de venta")
                            self.reeconectar_socket(enviado)
                            self.realizar_accion(result)
                    except Exception as e:
                        print("LeerMinicom.py, linea 378: "+str(e))
        except Exception as e:
            print("LeerMinicom.py, linea 380: "+str(e))