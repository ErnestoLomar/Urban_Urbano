##########################################
# Autor:
# Fecha de creación: 26/04/2022
# Ultima modificación: 27/06/2022
#
# Script para administrar la base de datos local
##########################################
import sqlite3
URI = "/home/pi/Urban_Urbano/db/aforo.db"

# cambiar altitud a latitud
tabla_gps = '''CREATE TABLE IF NOT EXISTS gps ( 
    idMuestreo INTEGER PRIMARY KEY AUTOINCREMENT, 
    fechaGPS DATE, 
    horaGPS Time, 
    errorGPS VARCHAR(100) ,  
    longitudGPS REAL, 
    altitudGPS Real,  
    velocidadGPS REAL, 
    geocerca varchar, 
    folio INTEGER , 
    check_servidor varchar,
    folio_viaje VARCHAR(100)
)'''

tabla_aforo = ''' CREATE TABLE IF NOT EXISTS parametros (
    idTransportista int(4), 
    idUnidad int(5),
    puertoSocket int(10),
    intervaloGPS Real, 
    enableGPS boolean, 
    kmActual Real,
    inicio_folio int(10)
) '''

tabla_temp = ''' CREATE TABLE IF NOT EXISTS temp (
    idMuestreo int(4), 
    fechaElegida DATE, 
    horaElegida TIME, 
    origenFechaHora VARCHAR(100), 
    errorTempCPU VARCHAR(100), 
    errorTempGPU VARCHAR(100), 
    tempCPU Real, 
    tempGPU Real
) '''

tabla_estadistica_rpi = ''' CREATE TABLE IF NOT EXISTS boletera (
    idMuestreo INTEGER PRIMARY KEY AUTOINCREMENT,
    version_sw VARCHAR(30),
    version_hw VARCHAR(30),
    mac VARCHAR(60),
    sim VARCHAR(30),
    ns_tablilla VARCHAR(30),
    fecha DATE,
    hora TIME
) '''

tabla_estadistica_memoria = ''' CREATE TABLE IF NOT EXISTS memoria (
    idMuestreo INTEGER PRIMARY KEY AUTOINCREMENT,
    uso_memoria_ram VARCHAR(20),
    uso_memoria_rom VARCHAR(20)
) '''

def crear_tabla_gps():
    try:
        con = sqlite3.connect(URI,check_same_thread=False)
        cur = con.cursor()
        cur.execute(tabla_gps)
    except Exception as e:
        print("Problema al crear tabla del gps: ", e)


def crear_tabla_aforo():
    try:
        con = sqlite3.connect(URI,check_same_thread=False)
        cur = con.cursor()
        cur.execute(tabla_aforo)
    except Exception as e:
        print("Problema al crear tabla aforo: ", e)


def crear_tabla_temp():
    try:
        con = sqlite3.connect(URI,check_same_thread=False)
        cur = con.cursor()
        cur.execute(tabla_temp)
    except Exception as e:
        print("Problema al crear tabla de la temperatura: ", e)
        
def crear_tabla_boletera():
    try:
        con = sqlite3.connect(URI,check_same_thread=False)
        cur = con.cursor()
        cur.execute(tabla_estadistica_rpi)
    except Exception as e:
        print("Problema al crear tabla de la boletera: ", e)
        
def crear_tabla_memoria():
    try:
        con = sqlite3.connect(URI,check_same_thread=False)
        cur = con.cursor()
        cur.execute(tabla_estadistica_memoria)
    except Exception as e:
        print("Problema al crear tabla de la memoria: ", e)


def insertar_gps(fechaGPS, horaGPS, errorGPS, longitud, latitud, velocidadGPS, geocerca, folio, check_servidor, folio_viaje):
    # BD GPS
    try:
        con = sqlite3.connect(URI,check_same_thread=False)
        cur = con.cursor()
        cur.execute(
            f"INSERT INTO gps(fechaGPS, horaGPS, errorGPS,  longitudGPS, altitudGPS , velocidadGPS, geocerca, folio, check_servidor, folio_viaje ) VALUES ('{fechaGPS}', '{horaGPS}', '{errorGPS}' , '{longitud}','{latitud}','{velocidadGPS}','{geocerca}','{folio}','{check_servidor}', '{folio_viaje}' )")
        con.commit()
    except Exception as e:
        print(e)


def insertar_aforo(idTransportista, idUnidad, puertoSocket, intervaloGPS, enableGPS, kmActual, inicio_folio):
    # BD aforo
    con = sqlite3.connect(URI,check_same_thread=False)
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO parametros VALUES (' {idTransportista}','{idUnidad}','{puertoSocket}', '{intervaloGPS}', '{enableGPS}' , '{kmActual}', '{inicio_folio}')")
    con.commit()
    con.close()


def insertar_temp(idMuestreo, fechaElegida, horaElegida, origenFechaHora, errorTempCPU, errorTempGPU, tempCPU, tempGPU):
    # BD temp
    con = sqlite3.connect(URI,check_same_thread=False)
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO temp VALUES (' {idMuestreo}','{fechaElegida}', '{horaElegida}', '{origenFechaHora}' , '{errorTempCPU}','{errorTempGPU}','{tempCPU}','{tempGPU}' )")
    con.commit()
    con.close()
    
def insertar_estadistica_boletera(vs_sw, vs_hw, mac, sim, ns_tablilla, fecha, hora):
    # BD temp
    con = sqlite3.connect(URI,check_same_thread=False)
    cur = con.cursor()
    cur.execute(f"INSERT INTO boletera(version_sw, version_hw, mac, sim, ns_tablilla, fecha, hora) VALUES ('{vs_sw}','{vs_hw}', '{mac}', '{sim}' , '{ns_tablilla}','{fecha}','{hora}')")
    con.commit()
    con.close()

def insertar_estadistica_memoria(ram, rom):
    # BD temp
    con = sqlite3.connect(URI,check_same_thread=False)
    cur = con.cursor()
    cur.execute(f"INSERT INTO memoria(uso_memoria_ram, uso_memoria_rom) VALUES ('{ram}','{rom}')")
    con.commit()
    con.close()

def obtener_datos_no_enviados():
    con = sqlite3.connect(URI,check_same_thread=False)
    cur = con.cursor()
    select_rutas = f''' SELECT * FROM gps where check_servidor = 'error' ORDER BY idMuestreo ASC LIMIT 20'''
    cur.execute(select_rutas)
    resultado = cur.fetchall()
    return resultado


def actualizar_registro_gps(id):
    con = sqlite3.connect(URI,check_same_thread=False)
    cur = con.cursor()
    sql_update_query = f'''Update gps set check_servidor = 'OK' where idMuestreo = {id}'''
    cur.execute(sql_update_query)
    con.commit()
    con.close()

def obtener_datos_aforo():
    con = sqlite3.connect(URI,check_same_thread=False)
    cur = con.cursor()
    select_rutas = f''' SELECT * FROM parametros ORDER BY idTransportista DESC LIMIT 1'''
    cur.execute(select_rutas)
    resultado = cur.fetchone()
    return resultado

#Función para crear las tablas de las bases de datos
def crear_tablas():
    crear_tabla_aforo()
    crear_tabla_temp()
    crear_tabla_gps()
    crear_tabla_boletera()
    crear_tabla_memoria()
    
#insertar_aforo(1,21000,8150,0.0,0,0.0,51)