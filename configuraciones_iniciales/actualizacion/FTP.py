from glob import glob
import RPi.GPIO as GPIO
import serial
import time
import os
import subprocess
import time
import base64 

##########################################################################################################################################
#INICIAMOS COMUNICACIoN POR LOS PUERTOS Y ACTIVAMOS LOS GPIO NECESARIOS
try:
    ser = serial.Serial('/dev/serial0',115200,timeout=1)
    time.sleep(0.3)
    ser.flushInput()
    ser.flushOutput()
    time.sleep(0.3)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(12, GPIO.OUT)
    time.sleep(2)
    GPIO.setup(31, GPIO.OUT)
    GPIO.setup(35, GPIO.OUT)
    GPIO.output(31, False)
    GPIO.output(35, True)
    print("QUECTEL INICIADO CORRECTAMENTE")
except:
    print("No se pudo comunicar con el minicom")
    
#configuracion FTP
Account = "\"account\""
UserFTP = "\"Abraham\""
PassFTP = "\"May0admin2022*\""
HostFTP = "\"20.106.77.209\""
ConfConexionFTP = "AT+QFTPCFG="+Account+","+UserFTP+","+PassFTP
ConexionFTP = "AT+QFTPOPEN="+HostFTP+",21"
contador = 1

##########################################################################################################################################
class Principal_Modem: 

        def reiniciar_SIM(self):
            try:
                print("\n#####################################")
                ser.readline()
                ser.readline()
                ser.flushInput()
                ser.flushOutput()
                comando = "AT+QFUN=5\r\n"
                ser.write(comando.encode())
                print(ser.readline())
                time.sleep(5)
                respuesta = ser.readline()
                if 'OK' in respuesta.decode():
                    print("Apagando SIM...")
                    print(respuesta)
                    ser.flushInput()
                    ser.flushOutput()
                else:
                    print("No se pudo inicializar AT+QFUN=5")
                    print(respuesta)
                    time.sleep(2)
                    #self.reiniciar_SIM()
                print("#####################################\n")

                time.sleep(5)

                ser.flushInput()
                ser.flushOutput()
                comando = "AT+QFUN=6\r\n"
                ser.readline()
                ser.write(comando.encode())
                print(ser.readline())
                time.sleep(5)
                respuesta = ser.readline()
                if 'OK' in respuesta.decode():
                    print("Encendiendo SIM...")
                    print(respuesta)
                    ser.flushInput()
                    ser.flushOutput()
                else:
                    print("No se pudo inicializar AT+QFUN=6")
                    print(respuesta)
                    time.sleep(2)
                    #self.reiniciar_SIM()

                time.sleep(5)
                print("#####################################\n")
            except Exception as e:
                print("comand.py, linea 311: "+str(e))

        def inicializar_configuraciones_quectel(self):
            try:

                print("#####################################")
                ser.readline()
                ser.readline()
                ser.flushInput()
                ser.flushOutput()
                comando = "AT+CPIN?\r\n"
                ser.write(comando.encode())
                print(ser.readline())
                time.sleep(5)
                respuesta = ser.readline()
                if 'READY' in respuesta.decode():
                    print(respuesta)
                    ser.flushInput()
                    ser.flushOutput()
                else:
                    print("No se pudo inicializar AT+CPIN")
                    print(respuesta)
                    time.sleep(2)
                    #self.reiniciar_SIM()
                print("#####################################\n")

                ser.flushInput()
                ser.flushOutput()
                comando = "AT+CREG?\r\n"
                ser.readline()
                ser.write(comando.encode())
                print(ser.readline())
                time.sleep(5)
                respuesta = ser.readline()
                if ',1' in respuesta.decode() or ',5' in respuesta.decode():
                    print(respuesta)
                    ser.flushInput()
                    ser.flushOutput()
                else:
                    print("No se pudo inicializar AT+CREG?")
                    print(respuesta)
                    time.sleep(2)
                    #self.reiniciar_SIM()
                print("#####################################\n")

                ser.flushInput()
                ser.flushOutput()
                comando = "AT+CGREG?\r\n"
                ser.readline()
                ser.write(comando.encode())
                print(ser.readline())
                time.sleep(5)
                respuesta = ser.readline()
                if ',1' in respuesta.decode() or ',5' in respuesta.decode():
                    print(respuesta)
                    ser.flushInput()
                    ser.flushOutput()
                else:
                    print("No se pudo inicializar AT+CGREG?")
                    print(respuesta)
                    time.sleep(2)
                    #self.reiniciar_SIM()
                print("#####################################\n")

                ser.flushInput()
                ser.flushOutput()
                comando = "AT+QICSGP=1,1,\"internet.itelcel.com\",\"\",\"\",1\r\n"
                ser.readline()
                ser.write(comando.encode())
                print(ser.readline())
                time.sleep(5)
                respuesta = ser.readline()
                if 'OK' in respuesta.decode():
                    print(respuesta)
                    ser.flushInput()
                    ser.flushOutput()
                else:
                    print("No se pudo inicializar AT+QICSGP")
                    print(respuesta)
                    time.sleep(2)
                    #self.reiniciar_SIM()
                print("#####################################\n")

                ser.flushInput()
                ser.flushOutput()
                comando = "AT+QIACT=1\r\n"
                ser.readline()
                ser.write(comando.encode())
                print(ser.readline())
                time.sleep(8)
                ser.readline()
                respuesta = ser.readline()
                if 'OK' in respuesta.decode():
                    print(respuesta)
                    ser.flushInput()
                    ser.flushOutput()
                else:
                    print("No se pudo inicializar AT+QIACT=1")
                    print(respuesta)
                    time.sleep(2)
                    #self.reiniciar_SIM()
                print("#####################################")
            except Exception as e:
                print("FTP.py, linea 171, Error al inicializar SIM: "+str(e))
        
        global ConfigurarFTP      
        def ConfigurarFTP():
            try:
                cone=ConfConexionFTP+"\r\n"
                print("esto es cone "+cone)
                ser.write(cone.encode())
                print(ser.readline())
                Aux = ser.readline()
                print("salio "+Aux.decode())
                time.sleep(2)
                Tiempo="\"rsptimeout\""
                comando="AT+QFTPCFG="+Tiempo+",180\r\n"
                ser.write(comando.encode())
                print(ser.readline())
                Aux = ser.readline()
                print("salio "+Aux.decode())
                time.sleep(2)
                transmode="\"transmode\""
                comando="AT+QFTPCFG="+transmode+",1\r\n"
                ser.write(comando.encode())
                print(ser.readline())
                Aux = ser.readline()
                print("salio "+Aux.decode())
                time.sleep(2)
                filetype="\"filetype\""
                comando="AT+QFTPCFG="+filetype+",1\r\n"
                ser.write(comando.encode())
                print(ser.readline())
                Aux = ser.readline()
                print("salio "+Aux.decode())
                return True
            except Exception as e:
                print("FTP.py, linea 171, Error al ConfigurarFTP: "+str(e))
                return False
            
##########################################################################################################################################
        #Se establece la conexion con el servidor por medio del FTP
        global IniciarSesionFTP
        def IniciarSesionFTP():
            try:
                comando=ConexionFTP+"\r\n"
                ser.write(comando.encode())
                print("INTENTANDO..")
                print(ser.readline())
                Aux = ser.readline()
                print(Aux.decode())
                time.sleep(3)
                
                if Aux.decode() == "OK\r\n":
                    print("Conexion exitosa")
                    time.sleep(5)
                    UbicarPathFTP()
                else:
                    print("Reintentando...")
                    comando="AT+QFTPCLOSE\r\n"
                    ser.write(comando.encode())
                    time.sleep(5)
                    global contador
                    if contador >= 5:
                        print("No se pudo establecer la conexion con el servidor FTP")
                        return False
                    contador += 1
                    IniciarSesionFTP()
                return True
            except Exception as e:
                print("FTP.py, linea 171, Error al IniciarSesionFTP: "+str(e))
                return False
            
##########################################################################################################################################
        #Funcion para establecer la ruta de archivo que se quiere descargar por FTP
        global UbicarPathFTP
        def UbicarPathFTP():#se comienza hubicando la ruta
            try:
                comando='AT+QFTPCWD="/Pruebas/"' + "\r\n"
                ser.write(comando.encode())
                print(ser.readline())
                Aux = ser.readline()
                print("salio 1 "+Aux.decode())
                time.sleep(5)
                
                archivo="\"update.txt\""
                complemento="\"UFS:update.txt\""
                comando="AT+QFTPGET="+archivo+","+complemento+"\r\n"
                ser.write(comando.encode())
                time.sleep(5)
                print(ser.readline())
                Reintentar = "false"
                while True:
                    print("dentro del while")
                    Aux = ser.readline()
                    print(Aux.decode())
                    if Aux == "+QFTPGET: 0,0":
                        print("Ha ocurrido un error")
                        Reintentar = "True"
                        break
                    Cortada = Aux.decode()
                    Aux1 = Cortada.split(":")
                    if Aux1[0] == "+QFTPGET":
                        print("Revisando descargada...")
                        Cortada = Aux.decode()
                        Aux1 = Cortada.split(",")
                        if Aux1[0] == "+QFTPGET: 0":
                            print("Conexion del ftp correcta")
                            if Aux[1] > 0:
                                print("Verificando descarga")
                                break
                        else:
                            print("Ha ocurrido un error")
                            Reintentar = "True"
                            break
                    
                if Reintentar == "True":
                    IniciarSesionFTP()
                else:
                    leerArchivo()
                    return True
            except Exception as e:
                print("FTP.py, linea 171, Error al UbicarPathFTP: "+str(e))
                return False
            
##########################################################################################################################################
        #funcion para leer el txt descargado (base 64)
        global leerArchivo
        def leerArchivo():
            try:
                archivo="\"UFS:update.txt\""
                comando="AT+QFDWL="+archivo+"\r\n"
                ser.write(comando.encode())
                time.sleep(1)
                print("esto es el archivo: ")
                eux = ser.readlines()
            
                print(eux)
                todo = ""
                file = open("update.txt","w")
                
                i=0
                Base64 = ""
                
                while True:
                    i = i + 1
                    if eux[i] == b"CONNECT\r\n":
                        if eux[i+1] != b"\r\n":
                            Base64 = eux[i+1]
                            print("Encontrado")
                            file.write(Base64.decode('UTF-8') + os.linesep)
                            file.close()
                            
                            file = open('update.txt', 'rb') 
                            byte = file.read() 
                            file.close() 

                            decodeit = open('update.zip', 'wb') 
                            decodeit.write(base64.b64decode((byte))) 
                            decodeit.close() 
                            break
                        else:
                            print("Reiniciando descarga...")
                            #IniciarSesionFTP()
                            break
                return True
            except Exception as e:
                print("FTP.py, linea 171, Error al leer archivo: "+str(e))
                return False
            

    ###################################################################
    #Descompresion y movimiento de archivos
    ###################################################################
    
    #Funcion para descomprimir el archivo descargado
    #unar es una aplicacion que necesita ser installada para que unar -q funcione
    #Archivo descargado del servidor
    #Descomprime el archivo que debe ser un .rar con una carpeta (en .txt)
    #-f es para forzar la sobreescritura si existe ya un archivo igual

        global ActualizarArchivos
        def ActualizarArchivos(tamanio_esperado):
            time.sleep(1)
            filename = 'update.zip' 
            if os.path.exists(filename):
                try:
                    print("Descomprimiendo...")
                    subprocess.run('pwd', shell=True)
                    subprocess.run('sudo rm -rf update.txt', shell=True)
                    subprocess.run("sudo mv -f /home/pi/update.zip /home/pi/actualizacion/",shell=True)
                    subprocess.run("sudo unzip /home/pi/actualizacion/update.zip",shell=True)
                    print(".zip descomprimido")
                    if os.path.exists("/home/pi/update/"):
                        print("Carpeta descomprimida: update")
                        print("Verificamos el tamaño del archivo...")
                        tamanio_del_archivo = subprocess.run("du -s update", stdout=subprocess.PIPE, shell=True).stdout.decode()[:4]
                        print("El tamaño del archivo zip es: "+str(tamanio_del_archivo))
                        if int(tamanio_del_archivo) >= tamanio_esperado:
                            print(f"El tamaño del archivo zip {tamanio_del_archivo} es mayor a "+str(tamanio_esperado))
                            print("Procedemos a mover los archivos...")
                            subprocess.run('sudo rm -rf /home/pi/actualizacion/update.zip', shell=True)
                            #subprocess.run("sudo cp -r /home/pi/Urban_Urbano/ /home/pi/antigua/",shell=True)
                            subprocess.run('sudo rm -rf /home/pi/Urban_Urbano', shell=True)
                            subprocess.run("sudo mv -f /home/pi/update /home/pi/Urban_Urbano",shell=True)
                            if os.path.exists("/home/pi/Urban_Urbano/verificar_carpeta.py"):
                                subprocess.run("sudo mv -f /home/pi/Urban_Urbano/verificar_carpeta.py /home/pi/actualizacion/",shell=True)
                                print("Archivo verificar_carpeta.py movido")
                            print("#############################################")
                            print("Actualización completada")
                            print("#############################################")
                            return True
                        else:
                            print("El tamaño del archivo zip es menor al esperado")
                            print(f"El tamaño del archivo zip {tamanio_del_archivo} es menor a "+str(tamanio_esperado))
                    else:
                        print(f"No existe la carpeta descomprimida en /home/pi/update/")
                        return False
                    print("#############################################")
                    print("Algo fallo")
                    print("#############################################")
                    return False
                except Exception as e:
                    print(e)
                    return False
            else:
                print ("No se encontró el archivo")
                time.sleep(1)
                return False