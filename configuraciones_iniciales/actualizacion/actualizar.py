##########################################
# Autor: Ernesto Lomar
# Fecha de creación: 12/04/2022
# Ultima modificación: 16/08/2022
#
# Script de la ventana enviar vuelta.
#
##########################################

#Librerías externas
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import logging

#Se hacen las importaciones necesarias
from FTP import ConfigurarFTP, IniciarSesionFTP, ActualizarArchivos
import subprocess

class Actualizar(QWidget):
    
    def __init__(self):
        super().__init__()
        try:
            self.setGeometry(0, 0 , 800, 440)
            self.setWindowFlags(Qt.FramelessWindowHint)
            uic.loadUi("/home/pi/Urban_Urbano/ui/actualizacion.ui", self)
            self.settings = QSettings('/home/pi/Urban_Urbano/ventanas/settings.ini', QSettings.IniFormat)
            self.label_porcentaje.hide()
        except Exception as e:
            logging.info(e)

    def actualizar_raspberrypi(self, tamanio_esperado):
        try:
            self.label_info.setStyleSheet('font: 18pt "MS Shell Dlg 2"; color: rgb(55, 147, 72);')
            self.label_info_2.setStyleSheet('font: 18pt "MS Shell Dlg 2"; color: rgb(55, 147, 72);')
            self.label_info.setText("Recibiendo actualizaciones...")
            self.label_info_2.setText("por favor, no use la boletera")
            hacer = ConfigurarFTP()
            if hacer:
                time.sleep(.5)
                hacer = IniciarSesionFTP()
                if hacer:
                    time.sleep(.5)
                    hacer = ActualizarArchivos(tamanio_esperado)
                    if hacer:
                        self.label_info.setStyleSheet('font: 18pt "MS Shell Dlg 2"; color: rgb(55, 147, 72);')
                        self.label_info_2.setText("")
                        self.label_info.setText("Actualización correcta, reiniciando...")
                        time.sleep(8)
                        subprocess.run("sudo reboot", shell=True)
                    else:
                        self.label_info.setStyleSheet('font: 18pt "MS Shell Dlg 2"; color: rgb(255, 0, 0);')
                        self.label_info_2.setText("")
                        self.label_info.setText("Error al actualizar")
                        time.sleep(60)
                        self.close()
                else:
                    self.label_info.setStyleSheet('font: 18pt "MS Shell Dlg 2"; color: rgb(255, 0, 0);')
                    self.label_info_2.setText("")
                    self.label_info.setText("Sesión FTP no iniciada")
                    time.sleep(60)
                    self.close()
            else:
                self.label_info.setStyleSheet('font: 18pt "MS Shell Dlg 2"; color: rgb(255, 0, 0);')
                self.label_info_2.setText("")
                self.label_info.setText("No se completo la configuración de FTP")
                time.sleep(60)
                self.close()
        except Exception as e:
            print(e)
            self.label_info.setStyleSheet('font: 18pt "MS Shell Dlg 2"; color: rgb(255, 0, 0);')
            self.label_info_2.setText("")
            self.label_info.setText("No se completo la actualizacion")
            logging.info(e)