from datetime import datetime, timedelta
import re
from escpos.printer import Usb
import logging
from time import strftime
import time
from PyQt5.QtCore import QSettings
from variables_globales import version_del_software
import sys

sys.path.insert(1, '/home/pi/Urban_Urbano/db')

from operadores import obtener_operador_por_UID

try:

    def sumar_dos_horas(hora1, hora2):
        try:
            formato = "%H:%M:%S"
            lista = hora2.split(":")
            hora=int(lista[0])
            minuto=int(lista[1])
            segundo=int(lista[2])
            h1 = datetime.strptime(hora1, formato)
            dh = timedelta(hours=hora) 
            dm = timedelta(minutes=minuto)          
            ds = timedelta(seconds=segundo) 
            resultado1 =h1 + ds
            resultado2 = resultado1 + dm
            resultado = resultado2 + dh
            resultado=resultado.strftime(formato)
            return str(resultado)
        except Exception as e:
            print("pasaje.py, linea 151: "+str(e))
        
    def imprimir_boleto_normal_con_servicio(ultimo_folio_de_venta, fecha, hora, idUnidad, servicio, tramo, qr):
        try:
            nc='0x04c5'
            ns='0x126e'

            n_creador_hex = int(nc, 16)
            n_serie_hex = int(ns, 16)

            instancia_impresora = Usb(n_creador_hex, n_serie_hex, 0)
            fecha = str(strftime('%d-%m-%Y')).replace('/', '-')
            settings = QSettings('/home/pi/Urban_Urbano/ventanas/settings.ini', QSettings.IniFormat)
            instancia_impresora.set(align='center')
            logging.info("Impresora encontrada")
            instancia_impresora.set(align='center')                                                                    
            instancia_impresora.text(f"Folio: {(ultimo_folio_de_venta)}            {fecha} {hora}\n")
            instancia_impresora.text(f"Unidad: {idUnidad}       IMPORTE {qr[6]}:  $ {0}\n")
            instancia_impresora.text(f"Servicio: {servicio}\n")
            tramo_servicio_actual = str(str(tramo).split("-")[0]) + "-" + str(str(servicio).split("-")[2])
            instancia_impresora.text(f"Tramo: {tramo_servicio_actual}\n")
            tipo_de_pasajero = str(qr[6]).lower()
            # Actualizamos el total de folios en el resumen (ticket) de liquidación dependiendo del tipo de pasajero                                      
            if tipo_de_pasajero != "normal":
                
                if tipo_de_pasajero == "estudiante":
                    # Si el pasajero es estudiante actualizamos los datos del settings de info_estudiantes
                    incremento_pasajero = float(settings.value('info_estudiantes').split(",")[0]) + 1
                    incremento_cantidad = float(settings.value('info_estudiantes').split(",")[1])
                    settings.setValue('info_estudiantes', f"{int(incremento_pasajero)},{incremento_cantidad}")
                    
                elif tipo_de_pasajero == "menor":
                    # Si el pasajero es menor actualizamos los datos del settings de info_chicos
                    incremento_pasajero = float(settings.value('info_chicos').split(",")[0]) + 1
                    incremento_cantidad = float(settings.value('info_chicos').split(",")[1])
                    settings.setValue('info_chicos', f"{int(incremento_pasajero)},{incremento_cantidad}")
                    
                elif tipo_de_pasajero == "mayor":
                    # Si el pasajero es mayor actualizamos los datos del settings de info_ad_mayores
                    incremento_pasajero = float(settings.value('info_ad_mayores').split(",")[0]) + 1
                    incremento_cantidad = float(settings.value('info_ad_mayores').split(",")[1])
                    settings.setValue('info_ad_mayores', f"{int(incremento_pasajero)},{incremento_cantidad}")
            else:
                incremento_pasajero = float(settings.value('info_normales').split(",")[0]) + 1
                incremento_cantidad = float(settings.value('info_normales').split(",")[1])
                settings.setValue('info_normales', f"{int(incremento_pasajero)},{incremento_cantidad}")
            instancia_impresora.cut()
            time.sleep(1)
            return True
        except Exception as e:
            print("Sucedio algo al imprimir ticket normal con servicio: "+str(e))
            logging.info(e)
            return False
        
    def imprimir_boleto_normal_sin_servicio(ultimo_folio_de_venta, fecha, hora, idUnidad, tramo, qr):
        try:
            nc='0x04c5'
            ns='0x126e'

            n_creador_hex = int(nc, 16)
            n_serie_hex = int(ns, 16)

            instancia_impresora = Usb(n_creador_hex, n_serie_hex, 0)
            fecha = str(strftime('%d-%m-%Y')).replace('/', '-')
            hora_actual = strftime('%H:%M:%S')
            settings = QSettings('/home/pi/Urban_Urbano/ventanas/settings.ini', QSettings.IniFormat)
            instancia_impresora.set(align='center')                                                                    
            instancia_impresora.text(f"Folio: {(ultimo_folio_de_venta)}            {fecha} {hora}\n")
            instancia_impresora.text(f"Unidad: {idUnidad}       IMPORTE {qr[6]}:  $ {0}\n")
            instancia_impresora.text(f"Aparentemente no estas en el servicio correcto\n")
            destino_del_qr = str(str(tramo).split("-")[1])
            instancia_impresora.text(f"No se encontro el destino {destino_del_qr}\n")
            tipo_de_pasajero = str(qr[6]).lower()
            # Actualizamos el total de folios en el resumen (ticket) de liquidación dependiendo del tipo de pasajero                                      
            if tipo_de_pasajero != "normal":
                
                if tipo_de_pasajero == "estudiante":
                    # Si el pasajero es estudiante actualizamos los datos del settings de info_estudiantes
                    incremento_pasajero = float(settings.value('info_estudiantes').split(",")[0]) + 1
                    incremento_cantidad = float(settings.value('info_estudiantes').split(",")[1])
                    settings.setValue('info_estudiantes', f"{int(incremento_pasajero)},{incremento_cantidad}")
                    
                elif tipo_de_pasajero == "menor":
                    # Si el pasajero es menor actualizamos los datos del settings de info_chicos
                    incremento_pasajero = float(settings.value('info_chicos').split(",")[0]) + 1
                    incremento_cantidad = float(settings.value('info_chicos').split(",")[1])
                    settings.setValue('info_chicos', f"{int(incremento_pasajero)},{incremento_cantidad}")
                    
                elif tipo_de_pasajero == "mayor":
                    # Si el pasajero es mayor actualizamos los datos del settings de info_ad_mayores
                    incremento_pasajero = float(settings.value('info_ad_mayores').split(",")[0]) + 1
                    incremento_cantidad = float(settings.value('info_ad_mayores').split(",")[1])
                    settings.setValue('info_ad_mayores', f"{int(incremento_pasajero)},{incremento_cantidad}")
            else:
                incremento_pasajero = float(settings.value('info_normales').split(",")[0]) + 1
                incremento_cantidad = float(settings.value('info_normales').split(",")[1])
                settings.setValue('info_normales', f"{int(incremento_pasajero)},{incremento_cantidad}")
            instancia_impresora.cut()
            time.sleep(1)
            return True
        except Exception as e:
            print("Sucedio algo al imprimir ticket normal sin servicio: "+str(e))
            logging.info(e)
            return False

    def imprimir_boleto_normal_pasaje(folio, fecha, hora, unidad, tipo_pasajero, importe, servicio, tramo):
        try:
            nc='0x04c5'
            ns='0x126e'

            n_creador_hex = int(nc, 16)
            n_serie_hex = int(ns, 16)

            instancia_impresora = Usb(n_creador_hex, n_serie_hex, 0)
            fecha = str(strftime('%d-%m-%Y')).replace('/', '-')
            instancia_impresora.set(align='center')
            logging.info("Impresora encontrada")
            instancia_impresora.text(f"Folio: {folio}            {fecha} {hora}\n")
            instancia_impresora.text(f"Unidad: {unidad}       IMPORTE {tipo_pasajero}:  $ {importe}\n")
            instancia_impresora.text(f"Servicio: {servicio}\n")
            instancia_impresora.text(f"Tramo: {tramo}\n")
            instancia_impresora.cut()
            time.sleep(1)
            return True
        except Exception as e:
            print(e)
            logging.info(e)
            return False
    
    def imprimir_boleto_con_qr_pasaje(folio, fecha, hora, unidad, tipo_pasajero, importe, servicio, tramo, servicio_o_transbordo):
        try:
            nc='0x04c5'
            ns='0x126e'

            n_creador_hex = int(nc, 16)
            n_serie_hex = int(ns, 16)

            instancia_impresora = Usb(n_creador_hex, n_serie_hex, 0)
            fecha = str(strftime('%d-%m-%Y')).replace('/', '-')
            instancia_impresora.set(align='center')
            logging.info("Impresora encontrada")
            instancia_impresora.text(f"Folio: {folio}            {fecha} {hora}\n")
            instancia_impresora.text(f"Unidad: {unidad}       IMPORTE {tipo_pasajero}:  $ {importe}\n")
            instancia_impresora.text(f"Servicio: {servicio}\n")
            instancia_impresora.text(f"Tramo: {tramo}\n")
            if 'NE' in servicio_o_transbordo[8]:
                unidad_a_transbordar = str(str(servicio_o_transbordo[7]).split("_")[0]).replace("'", "")
                instancia_impresora.text(f"Transbordar unidad en: {unidad_a_transbordar}\n")
                estimado = "02:00:00"
                hora_antes_de = sumar_dos_horas(hora, estimado)
                instancia_impresora.text(f"Antes de {fecha} {hora_antes_de}\n")
                instancia_impresora.qr(f"{fecha},{hora_antes_de},{unidad},{importe},{servicio},{tramo},{tipo_pasajero},{'st'},{unidad_a_transbordar}",0, 5)
                instancia_impresora.cut()
                time.sleep(1)
                return True
            else:
                unidad_a_transbordar1 = str(str(servicio_o_transbordo[7]).split("_")[0]).replace("'", "")
                unidad_a_transbordar2 = str(str(servicio_o_transbordo[8]).split("_")[0]).replace("'", "")
                instancia_impresora.text(f"Transbordar unidad en: {unidad_a_transbordar1}\n")
                instancia_impresora.text(f"Luego transbordar unidad en: {unidad_a_transbordar2}\n")
                estimado = "02:00:00"
                hora_antes_de = sumar_dos_horas(hora, estimado)
                instancia_impresora.text(f"Antes de {fecha} {hora_antes_de}\n")
                instancia_impresora.qr(f"{fecha},{hora_antes_de},{unidad},{importe},{servicio},{tramo},{tipo_pasajero},{'ct'},{unidad_a_transbordar1},{unidad_a_transbordar2}",0, 5)
                instancia_impresora.cut()
                time.sleep(1)
                return True
        except Exception as e:
            print(e)
            logging.info(e)
            return False
        
    def imprimir_ticket_de_corte(idUnidad):
        try:
            nc='0x04c5'
            ns='0x126e'

            n_creador_hex = int(nc, 16)
            n_serie_hex = int(ns, 16)

            instancia_impresora = Usb(n_creador_hex, n_serie_hex, 0)
            fecha = str(strftime('%d-%m-%Y')).replace('/', '-')
            hora_actual = strftime('%H:%M:%S')
            settings = QSettings('/home/pi/Urban_Urbano/ventanas/settings.ini', QSettings.IniFormat)
            instancia_impresora.set(align='center')
            operador = obtener_operador_por_UID(settings.value('csn_chofer'))
            logging.info("Impresora encontrada")
            for i in range(2):
                instancia_impresora.text(f"{fecha} {hora_actual}\n")
                instancia_impresora.text(f"Fv: {settings.value('folio_de_viaje')}  Sw: {version_del_software}\n")
                if operador != None:
                    instancia_impresora.text(f"Operador: {operador[2]}\n")
                    instancia_impresora.text(f"Numero de empleado: {operador[1]}\n")
                else:
                    instancia_impresora.text(f"Operador de Reciente Ingreso\n")
                instancia_impresora.text(f"Folio de liquidacion: {settings.value('folio_de_viaje_webservice')}\n")
                instancia_impresora.text(f"Unidad: {idUnidad}    Serv: {settings.value('servicio')}\n")
                instancia_impresora.text(f"Vuelta: {settings.value('vuelta')}\n")
                instancia_impresora.text(f"Estud:        {str(settings.value('info_estudiantes')).split(',')[0]}  $       {str(settings.value('info_estudiantes')).split(',')[1]}\n")
                instancia_impresora.text(f"Normal:       {str(settings.value('info_normales')).split(',')[0]}  $       {str(settings.value('info_normales')).split(',')[1]}\n")
                instancia_impresora.text(f"Menor:        {str(settings.value('info_chicos')).split(',')[0]}  $       {str(settings.value('info_chicos')).split(',')[1]}\n")
                instancia_impresora.text(f"Ad.May:       {str(settings.value('info_ad_mayores')).split(',')[0]}  $       {str(settings.value('info_ad_mayores')).split(',')[1]}\n")
                instancia_impresora.text("\n")
                instancia_impresora.text(f"Total a liquidar: $ {settings.value('total_a_liquidar')}\n")
                instancia_impresora.text(f"Total de folios: {settings.value('total_de_folios')}\n")
                instancia_impresora.cut()
                logging.info(f"Tickets de corte impresos correctamente.")
            return True
        except Exception as e:
            print(e)
            logging.info(e)
            return False
except Exception as e:
    print("No hubo comunicacion con impresora")