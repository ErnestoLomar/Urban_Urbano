from PyQt5.QtCore import QObject, pyqtSignal
import time
import logging

class DeteccionGeocercasWorker(QObject):
    try:
        finished = pyqtSignal()
        progress = pyqtSignal(dict)
    except Exception as e:
        print(e)
        logging.info(e)

    def run(self):
        try:
            while True:
                import variables_globales
                self.longitud = variables_globales.longitud
                self.latitud = variables_globales.latitud
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