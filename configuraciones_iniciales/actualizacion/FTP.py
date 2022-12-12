from glob import glob
import RPi.GPIO as GPIO
import serial
import time
import os
import subprocess
import time
import base64
import sys

sys.path.insert(1, '/home/pi/Urban_Urbano/db')

from queries import obtener_datos_aforo

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
    
#configuracion FTP Azure
cuenta_azure = "\"account\""
usuario_FTP_azure = "\"Abraham\""
contra_FTP_azure = "\"May0admin2022*\""
host_FTP_azure = "\"20.106.77.209\""
conf_conexion_FTP_azure = "AT+QFTPCFG="+cuenta_azure+","+usuario_FTP_azure+","+contra_FTP_azure
conexion_FTP_azure = "AT+QFTPOPEN="+host_FTP_azure+",21"

#configuracion FTP webhost
cuenta_webhost = "\"account\""
usuario_FTP_webhost = "\"recursosespirituales\""
contra_FTP_webhost = "\"1280x800\""
host_FTP_webhost = "\"files.000webhost.com\""
conf_conexion_FTP_webhost = "AT+QFTPCFG="+cuenta_webhost+","+usuario_FTP_webhost+","+contra_FTP_webhost
conexion_FTP_webhost = "AT+QFTPOPEN="+host_FTP_webhost+",21"

contador = 1
id_Unidad = str(obtener_datos_aforo()[1])
intentos_ftp = 0

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
        
        global verificar_memoria_UFS
        def verificar_memoria_UFS():
            global id_Unidad
            ser.flushInput()
            ser.flushOutput()
            print(ser.readline())
            Aux = ser.readline()
            print(Aux.decode())
            Aux = ser.readline()
            print(Aux.decode())
            verificar_archivos = "AT+QFLST=\"*\"\r\n"
            ser.write(verificar_archivos.encode())
            print(ser.readline())
            Aux = ser.readline()
            print(Aux.decode())
            if 'update.txt' in Aux.decode():
                print("Ya existe el archivo update.txt")
                eliminar_archivos = "AT+QFDEL=\"update.txt\"\r\n"
                ser.write(eliminar_archivos.encode())
                print(ser.readline())
                Aux = ser.readline()
                print(Aux.decode())
                Aux = ser.readline()
                print(Aux.decode())
            elif f'{id_Unidad}' in Aux.decode():
                print(f"Ya existe el archivo {id_Unidad}.txt")
                print(ser.readline())
                Aux = ser.readline()
                print(Aux.decode())
                eliminar_archivos = f"AT+QFDEL=\"{id_Unidad}.txt\"\r\n"
                ser.write(eliminar_archivos.encode())
                print(ser.readline())
                Aux = ser.readline()
                print(Aux.decode())
                Aux = ser.readline()
                print(Aux.decode())
            if os.path.exists('/home/pi/update.txt'):
                print("Ya existe el archivo update.txt")
                subprocess.run('rm -rf /home/pi/update.txt', shell=True)
            elif os.path.exists(f'/home/pi/{id_Unidad}'):
                print(f"Ya existe el archivo {id_Unidad}")
                subprocess.run(f'rm -rf /home/pi/{id_Unidad}', shell=True)
            ser.flushInput()
            ser.flushOutput()
            return True
        
        global ConfigurarFTP  
        def ConfigurarFTP(servidor, tamanio):
            try:
                if servidor == "web":
                    cone=conf_conexion_FTP_webhost+"\r\n"
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
                    IniciarSesionFTP("web", tamanio)
                elif servidor == "azure":
                    cone=conf_conexion_FTP_azure+"\r\n"
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
                    IniciarSesionFTP("azure", tamanio)
            except Exception as e:
                print("FTP.py, linea 171, Error al ConfigurarFTP: "+str(e))
                return False
            
##########################################################################################################################################
        #Se establece la conexion con el servidor por medio del FTP
        global IniciarSesionFTP
        def IniciarSesionFTP(servidor, tamanio):
            try:
                global intentos_ftp, contador
                if servidor == "web":
                    comando=conexion_FTP_webhost+"\r\n"
                    ser.write(comando.encode())
                    print("INTENTANDO..")
                    print(ser.readline())
                    Aux = ser.readline()
                    print(Aux.decode())
                    time.sleep(3)
                    
                    if Aux.decode() == "OK\r\n":
                        print("Conexion exitosa")
                        time.sleep(5)
                        contador = 0
                        intentos_ftp = 0
                        UbicarPathFTP("web", tamanio)
                    else:
                        print("Reintentando...")
                        comando="AT+QFTPCLOSE\r\n"
                        ser.write(comando.encode())
                        time.sleep(5)
                        if contador >= 6:
                            print("No se pudo establecer la conexion con el servidor FTP")
                            return False
                        contador += 1
                        intentos_ftp += 1
                        IniciarSesionFTP("web", tamanio)
                    contador = 0
                    intentos_ftp = 0
                    return True
                elif servidor == "azure":
                    comando=conexion_FTP_azure+"\r\n"
                    ser.write(comando.encode())
                    print("INTENTANDO..")
                    print(ser.readline())
                    Aux = ser.readline()
                    print(Aux.decode())
                    time.sleep(3)
                    
                    if Aux.decode() == "OK\r\n":
                        print("Conexion exitosa")
                        time.sleep(5)
                        contador = 0
                        intentos_ftp = 0
                        UbicarPathFTP("azure", tamanio)
                    else:
                        print("Reintentando...")
                        comando="AT+QFTPCLOSE\r\n"
                        ser.write(comando.encode())
                        time.sleep(5)
                        if contador >= 6:
                            print("No se pudo establecer la conexion con el servidor FTP")
                            return False
                        if intentos_ftp >= 3:
                            print("intentando con servidor webhost")
                            ConfigurarFTP("web", tamanio)
                        contador += 1
                        intentos_ftp += 1
                        IniciarSesionFTP("azure", tamanio)
                    contador = 0
                    intentos_ftp = 0
                    return True
            except Exception as e:
                print("FTP.py, linea 171, Error al IniciarSesionFTP: "+str(e))
                return False
            
##########################################################################################################################################
        #Funcion para establecer la ruta de archivo que se quiere descargar por FTP
        global UbicarPathFTP
        def UbicarPathFTP(servidor, tamanio):#se comienza ubicando la ruta
            try:
                if servidor == "azure":
                    global id_Unidad, intentos_ftp
                    comando = 'AT+QFTPCWD="/Actualizaciones/"' + "\r\n"
                    ser.write(comando.encode())
                    print(ser.readline())
                    Aux = ser.readline()
                    print("salio 1 "+Aux.decode())
                    time.sleep(5)
                    
                    archivo = f"\"{id_Unidad}.txt\""
                    complemento= f"\"UFS:{id_Unidad}.txt\""
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
                        IniciarSesionFTP("azure", tamanio)
                    else:
                        leerArchivo("azure", tamanio)
                        return True
                elif servidor == "web":
                    comando = 'AT+QFTPCWD="/Pruebas/"' + "\r\n"
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
                        IniciarSesionFTP("web", tamanio)
                    else:
                        leerArchivo("web", tamanio)
                        return True
            except Exception as e:
                print("FTP.py, linea 171, Error al UbicarPathFTP: "+str(e))
                return False
            
##########################################################################################################################################
        #funcion para leer el txt descargado (base 64)
        global leerArchivo
        def leerArchivo(servidor, tamanio):
            try:
                if servidor == "web":
                    archivo="\"update.txt\""
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
                    ActualizarArchivos(tamanio)
                    return True
                elif servidor == "azure":
                    global id_Unidad, intentos_ftp
                    archivo= f"\"{id_Unidad}.txt\""
                    comando="AT+QFDWL="+archivo+"\r\n"
                    ser.write(comando.encode())
                    time.sleep(1)
                    print("esto es el archivo: ")
                    eux = ser.readlines()
                
                    print(eux)
                    todo = ""
                    file = open(f"{id_Unidad}.txt","w")
                    
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
                                
                                file = open(f'{id_Unidad}.txt', 'rb') 
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
                    ActualizarArchivos(tamanio)
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
            global id_Unidad, intentos_ftp
            time.sleep(1)
            filename = 'update.zip' 
            if os.path.exists(filename):
                try:
                    print("Descomprimiendo...")
                    subprocess.run('pwd', shell=True)
                    subprocess.run('rm -rf update.txt', shell=True)
                    subprocess.run(f'rm -rf {id_Unidad}.txt', shell=True)
                    subprocess.run("mv -f /home/pi/update.zip /home/pi/actualizacion/",shell=True)
                    subprocess.run("unzip /home/pi/actualizacion/update.zip",shell=True)
                    print(".zip descomprimido")
                    if os.path.exists("/home/pi/update/"):
                        print("Carpeta descomprimida: update")
                        print("Verificamos el tamaño del archivo...")
                        tamanio_del_archivo = subprocess.run("du -s update", stdout=subprocess.PIPE, shell=True).stdout.decode()[:4]
                        print("El tamaño del archivo zip es: "+str(tamanio_del_archivo))
                        if int(tamanio_del_archivo) >= tamanio_esperado:
                            print(f"El tamaño del archivo zip {tamanio_del_archivo} es mayor a "+str(tamanio_esperado))
                            print("Procedemos a mover los archivos...")
                            subprocess.run('rm -rf /home/pi/actualizacion/update.zip', shell=True)
                            #subprocess.run("sudo cp -r /home/pi/Urban_Urbano/ /home/pi/antigua/",shell=True)
                            subprocess.run('rm -rf /home/pi/Urban_Urbano', shell=True)
                            subprocess.run("mv -f /home/pi/update /home/pi/Urban_Urbano",shell=True)
                            if os.path.exists("/home/pi/Urban_Urbano/verificar_carpeta.py"):
                                subprocess.run("mv -f /home/pi/Urban_Urbano/verificar_carpeta.py /home/pi/actualizacion/",shell=True)
                                print("Archivo verificar_carpeta.py movido")
                            
                            print(ser.readline())
                            Aux = ser.readline()
                            print(Aux.decode())
                            eliminar_archivos = "AT+QFDEL=\"update.txt\"\r\n"
                            ser.write(eliminar_archivos.encode())
                            print(ser.readline())
                            Aux = ser.readline()
                            print(Aux.decode())
                            ser.flushInput()
                            ser.flushOutput()
                            
                            print(ser.readline())
                            Aux = ser.readline()
                            print(Aux.decode())
                            eliminar_archivos = f"AT+QFDEL=\"{id_Unidad}.txt\"\r\n"
                            ser.write(eliminar_archivos.encode())
                            print(ser.readline())
                            Aux = ser.readline()
                            print(Aux.decode())
                            Aux = ser.readline()
                            print(Aux.decode())
                            ser.flushInput()
                            ser.flushOutput()
                            
                            print("#############################################")
                            print("Actualización completada")
                            print("#############################################")
                            time.sleep(8)
                            subprocess.run("sudo reboot", shell=True)
                            return True
                        else:
                            print("El tamaño del archivo zip es menor al esperado")
                            print(f"El tamaño del archivo zip {tamanio_del_archivo} es menor a "+str(tamanio_esperado))
                    else:
                        print(f"No existe la carpeta descomprimida como /home/pi/update/")
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