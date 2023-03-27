from datetime import datetime, timedelta
import re
from escpos.printer import Usb
import logging
from time import strftime
import time
from PyQt5.QtCore import QSettings
import variables_globales as vg
import sys

sys.path.insert(1, '/home/pi/Urban_Urbano/db')

from operadores import obtener_operador_por_UID
from ventas_queries import obtener_ultimo_folio_de_item_venta, obtener_total_de_ventas_por_folioviaje_y_fecha
from asignaciones_queries import obtener_asignacion_por_folio_de_viaje

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
            settings = QSettings('/home/pi/Urban_Urbano/ventanas/settings.ini', QSettings.IniFormat)
            fecha = str(strftime('%d-%m-%Y')).replace('/', '-')
            total_a_liquidar_bd = 0.0
            ultima_venta_bd = obtener_ultimo_folio_de_item_venta()
            total_de_boletos_db = obtener_total_de_ventas_por_folioviaje_y_fecha(settings.value('folio_de_viaje'), fecha)
            print("El tamaño de boletos en la base de datos es: "+str(len(total_de_boletos_db)))
            logging.info(f"El total de boletos en la base de datos es: {len(total_de_boletos_db)}")
            
            # Procedemos a hacer la suma de la liquidación
            if len(total_de_boletos_db) != 0:
                for p in range(len(total_de_boletos_db)):
                    total_a_liquidar_bd = total_a_liquidar_bd + float(total_de_boletos_db[p][11])
                print("BD - El total a liquidar es: "+str(total_a_liquidar_bd))
                logging.info(f"BD - El total a liquidar es: {total_a_liquidar_bd}")
            
            print("Ultima venta en la base de datos es: "+str(ultima_venta_bd))
            logging.info(f"Ultima venta en la base de datos es: {ultima_venta_bd}")
            total_de_folio_aforo_efectivo = int(settings.value('info_estudiantes').split(',')[0]) + int(settings.value('info_normales').split(',')[0]) + int(settings.value('info_chicos').split(',')[0]) + int(settings.value('info_ad_mayores').split(',')[0])
            print("El total de boletos en el aforo es: "+str(total_de_folio_aforo_efectivo))
            logging.info(f"El total de boletos en el aforo es: {total_de_folio_aforo_efectivo}")
            if ultima_venta_bd != None:
                print("Ultima folio de venta en la bd: "+str(ultima_venta_bd[1]))
                logging.info(f"Ultima folio de venta en la bd: {ultima_venta_bd[1]}")
                if len(total_de_boletos_db) != total_de_folio_aforo_efectivo:
                    print("La cantidad de boletos en la base de datos no coincide con la cantidad de boletos en el aforo.")
                    logging.info(f"La cantidad de boletos en la base de datos no coincide con la cantidad de boletos en el aforo.")
                    if len(total_de_boletos_db) != ultima_venta_bd[1]:
                        print("La cantidad de boletos en la base de datos no coincide con el folio de la ultima venta en la base de datos.")
                        logging.info(f"La cantidad de boletos en la base de datos no coincide con el folio de la ultima venta en la base de datos.")
                        total_de_folio_aforo_efectivo = ultima_venta_bd[1]
                        print("Se ha actualizado el total de boletos en el aforo a: "+str(total_de_folio_aforo_efectivo))
                        logging.info(f"Se ha actualizado el total de boletos en el aforo a: {total_de_folio_aforo_efectivo}")
                    total_de_folio_aforo_efectivo = len(total_de_boletos_db)
                    print("Se ha actualizado el total de boletos en el aforo a: "+str(total_de_folio_aforo_efectivo))
                    logging.info(f"Se ha actualizado el total de boletos en el aforo a: {total_de_folio_aforo_efectivo}")
                    
            nc='0x04c5'
            ns='0x126e'

            n_creador_hex = int(nc, 16)
            n_serie_hex = int(ns, 16)

            instancia_impresora = Usb(n_creador_hex, n_serie_hex, 0)
            hora_actual = strftime('%H:%M:%S')
            instancia_impresora.set(align='center')
            if len(settings.value('folio_de_viaje')) > 0:
                trama_dos_del_viaje = obtener_asignacion_por_folio_de_viaje(settings.value('folio_de_viaje'))
            else:
                trama_dos_del_viaje = obtener_asignacion_por_folio_de_viaje(vg.folio_asignacion)
            logging.info("Impresora encontrada")
            for i in range(2):
                instancia_impresora.text(f"Fv: {settings.value('folio_de_viaje')}  Sw: {vg.version_del_software}\n")
                if len(vg.numero_de_operador) > 0:
                    instancia_impresora.text(f"Numero de empleado: {vg.numero_de_operador}\n")
                else:
                    if len(vg.csn_chofer) > 0:
                        instancia_impresora.text(f"Numero de empleado: {vg.csn_chofer}\n")
                    else:
                        instancia_impresora.text(f"Numero de empleado: {settings.value('csn_chofer')}\n")
                instancia_impresora.text(f"Folio de liquidacion: {settings.value('folio_de_viaje_webservice')}\n")
                instancia_impresora.text(f"Inicio de viaje: {trama_dos_del_viaje[4]} {trama_dos_del_viaje[5]}\n")
                instancia_impresora.text(f"Fin de viaje: {fecha} {hora_actual}\n")
                instancia_impresora.text(f"Unidad: {idUnidad}    Serv: {settings.value('servicio')}\n")
                instancia_impresora.text(f"Estud:        {str(settings.value('info_estudiantes')).split(',')[0]}  $       {str(settings.value('info_estudiantes')).split(',')[1]}\n")
                instancia_impresora.text(f"Normal:       {str(settings.value('info_normales')).split(',')[0]}  $       {str(settings.value('info_normales')).split(',')[1]}\n")
                instancia_impresora.text(f"Menor:        {str(settings.value('info_chicos')).split(',')[0]}  $       {str(settings.value('info_chicos')).split(',')[1]}\n")
                instancia_impresora.text(f"Ad.May:       {str(settings.value('info_ad_mayores')).split(',')[0]}  $       {str(settings.value('info_ad_mayores')).split(',')[1]}\n")
                instancia_impresora.text(f"Total a liquidar: $ {total_a_liquidar_bd}\n")
                instancia_impresora.text(f"Total de folios: {total_de_folio_aforo_efectivo}\n")
                instancia_impresora.cut()
                logging.info(f"Tickets de corte impresos correctamente.")
            return True
        except Exception as e:
            print(e)
            logging.info(e)
            return False
except Exception as e:
    print("No hubo comunicacion con impresora")