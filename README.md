# Urban_Urbano
Software de validador para camiones de transporte urbano para la empresa Urban de Tampico.

**Autor: Ernesto Lomar**

Linea cronológica:
- v2.42:
  - Que todas las tramas tengan [ en el inicio de la trama y ] en el final de la trama.
  - Que las tramas 2, 4 y 5 respondan con el checksum calculado del contenido de la trama.
  - Que las tramas 2, 4 y 5 verifiquen el checksum recibido del socket con el que se calculo en la boletera.
  - Se quito la "D" de la función "realizar_accion".
  - La boletera ahora solo toma como respuestas correctas del servidor las que contienen un SKT en la respuesta.
  - La boletera ahora puede manejar estos errores ['ErIn', 'TrEm', 'ErTr', 'EmEr'] y vuelve a enviar la trama.
  - La boletera ahora también toma en cuenta la hora de la tarjeta para validar la vigencia.
  - Ahora la librería .so detecta cuando no se tiene conexión con el dispositivo NFC e intenta rehacer la conexión.
  - La boletera ahora tiene la posibilidad de enviar tramas informativas acerca de mal uso de tarjetas y cuando se hizo un intento fallido de impresión de ticket.
  - La boletera no se podrá actualizar por FTP en pleno viaje.
  - La boletera no puede iniciar un viaje si existe uno en curso.
  - Se acotaron los tiempos de la maquina de estado.
  - Se quitaron los saltos de linea (\n) de la trama 9 (IDSIM y MAC).
  - Se incluyo un candado en la función "mandar_datos" para que la basura que encuentra en el serial la pase de largo.
  - Cuando se detecta que un viaje se esta tratando de iniciar y ya existe uno actual, muestra una ventana emergente avisando sobre este suceso.
  - Aparece una ventana emergente de aviso cuando no se puede imprimir un ticket.
  - Cuando se trata de generar una venta cuando no existe un viaje iniciado, manda un aviso por pantalla y cierra toda la sesión hasta regresar a la pantalla de camiones.
  - La trama 4 incluye el monto total de las ventas realizadas en el viaje.
  - Cuando la boletera no puede conectarse a su socket asignado, intenta conectarse al socket siguiente (si tiene el socket 8201, se intenta conectar al 8202, si tiene el 8210 intenta al 8201, etc). Y cuando ya pasaron varios intentos y sigue sin consolidar los datos en el servidor regresa a su socket asignado desde un principio y repite lo mismo si es que sigue sin consolidar el envió de datos.
  - Se agregaron candados de seguridad para los datos de la trama 2, 4 y 5.
  - Se modifico el tiempo de arranque de la boletera de 20s a 18s.
  - La boletera ahora puede recibir una instrucción de CMD desde el servidor y ejecutarla.
  - Se implemento una nueva base de datos llamada horarios.
  - Ahora la boletera ya puede enviar tramas ACT cada media hora en el transcurso de todo el día.
  - Se implemento la eliminación automática de tramas 9 que tienes 15 días o mas almacenadas en la DB.
  - Se cambio el folio (contador) de los folio de viaje a 01.
  - Se modifico la comunicación del FTP a AWS.
- v1.31:
  - Agregando la opción de que cuando inicie el sistema o se actualice se le otorguen permisos de administrador a todos los archivos.
  - Se agregaron 3 intentos al momento de actualizar el sistema.
  - Se agregó un candado para los 3 bytes de archivos al momento de la actualización por FTP.
  - Se agrego una comparación de conexión con el servidor en la actualización FTP.
  - Se agrego la opción de que se pueda imprimir en el ticket el empleado que inicio el viaje y el que lo cerro.
  - Se reorganizo la estructura del ticket de corte en tres nuevas secciones, #General, #Inicio de viaje y #Fin de viaje.
  - El folio auto incrementable del folio de viaje se cambio a 40. 
  - En la ventana de corte se quito la opción de que se viera la vigencia de la tarjeta.
  - Se cambio la manera en la que se guarda la hora en la trama 2.
  - Se agregaron dos nuevas tramas 9, #ElegirServicio y #DentroServicio.
- v1.30:
  - Arreglando bug de que a todas las auto_asignaciones se les coloca el mismo folio de viaje.
  - Agregando la fecha como parámetro a la funcion *aniadir_folio_de_viaje_a_auto_asignacion*.
  - Arreglando bug de que no se puede cerrar el viaje, por problemas de impresión de ticket.
  - Modificando ventana de *FUERADEVIGENCIA* a *TARJETAINVALIDA* cuando la vigencia de la tarjeta no corresponde con los parámetros esperados.
  - Agregando mejoras de código en el archivo *impresora.py* y *corte.py*.
  - Arreglando bug de doble UID vació, cuando se apaga la boletera en la ventana de Chofer y cuando se inicia nuevamente la boletera el UID se pasa a vació. lo que ocasiona la doble coma en la trama 2.
  - En inicio.py se agrego la opción de que cuando se inicie el sistema en la ventana de chofer el valor del UID guardado en el .ini se guarde en variables globales.
- v1.29:
  - Arreglando bug de que se imprimen los folios incorrectos.
- v1.28:
  - Quitando servicios 673 y 674 de la pension de Haciendas.
- v1.27:
  - Arreglando bug de la comparación de fechas en el primer día del mes.
- v1.26:
  - Correcciones de matriz tarifaría.
  - Actualización de base de datos *operadores*.
- v1.25:
  - Actualizando geocercas de *Monte Alto_1*, *La Morita_3*, *Independencia_1* y *Electricistas_1*.
- v1.24:
  - Añadiendo control de brillo en la pantalla desde el menu principal.
- v1.23:
  - Quitando el reinicio de los folios.
  - Añadiendo la opción de que el viaje se cierre de manera automática a las 2AM.
  - Cambiando el tiempo de envió de las tramas. De 30 segundos a 20 segundos para tramas 2,5 y 4. Y de 1 minuto a 30 segundos para la trama 3.
  - Se modifico la impresión de la fecha de inicio de viaje en el ticket y fin de viaje.
  - Actualizando librería .so para la opción de leer el nombre de operador de la tarjeta.
  - Agregando un candado de seguridad al momento de crear la trama 2 (inicio de viaje) para asegurar que el campo del CSN no se envié vació.
  - Se agrego un candado de seguridad en el folio auto incrementable del folio de viaje para asegurarse que se incremente.
  - Se agrego una nueva tabla llamada *boletera* y *memoria* donde próximamente se guardaran datos utilizados para futuras tramas.
  - Se quito "Vuelta" en la impresión del ticket.
  - Se quitaron renglones en el ticket.
  - Se agrego un candado de seguridad para cuando no se encuentre el numero de operador en la tarjeta se busque en la base de datos interna de operadores y ese dato sea el que se muestre en el ticket.
  - Se agrego un nuevo dato en el ticket llamado *"Ultimo folio"*
- v1.22:
  - Añadiendo lectura de número de operador de la tarjeta.
- v1.21:
  - Añadiendo la impresión de un nuevo ticket al cerrar el corte del viaje, para que ahora sean 3 impresiones de copias y cada una tendrá su respectivo nombre de a quien va dirigido (Jefe pensión, liquidación y operador).
  - Poniendo candado en el conteo de *total_de_folios* y *cantidad_a_liquidar* en la impresión de los tickets al cerrar el corte.
  - Añadiendo try-catch estratégicos en el inicio del sistema.
  - Hacemos la suma total del costo de las ventas realizadas en el viaje desde la base de datos.
  - Cambiamos la condición de si el UID esta vació de '== ""' a 'len() == 0'.
- v1.20:
  - Solucionando problema de la lectura de tickets de la base de datos.
- v1.19:
  - Agregando la eliminación de datos antiguos que sobrepasan los 15 días.
- v1.18:
  - Agregando inicio de sesión del GPS cuando no se obtienen coordenadas.
- v1.17:
  - Añadiendo la opción de poder hacer la actualización de software mediante 2 servidores con FTP.
  - Haciendo que cuando comience el software se enciende el GPS con *AT+QGPS=1*.
  - Corrigiendo bug de cuando no se hace ninguna venta.
- v1.16:
  - Agregando candado de seguridad en el CSN al crear la trama 2.
  - Quitando enters.
  - Quitando caracteres de tarjetas leídas.
  - Agregando candado de seguridad al crear trama 4.
  - Nueva comunicación con servidor de Azure.
- v1.15:
  - Modificando estructura de la función *handle_ok* cuando se inicia un viaje.
  - Añadiendo candado de seguridad del conteo de boletos registrados en la base de datos, los que se llevan en conteo y del folio de la ultima venta realizada.
  - Quitando botón de apagar raspberry de la ventana de chofer.
  - Quitando valor por defecto en la selección de pensión.
  - Añadiendo candado de verificación de si hay un fin de viaje por enviar al servidor antes de enviar un comienzo de viaje.
  - Agregando candados de seguridad al obtener el CSN.
  - Agregando candados de seguridad del CSN al crear trama 2.
  - Agregando candado de seguridad en la creación del folio de viaje.
  - Mejorando el envío de datos cronológicamente.
  - Cambiando nombres de variables para evitar la concatenación de datos.
  - Actualizando funciones del letrero de la ventana principal de *datos pendientes por enviar*
- v1.14:
  - Modificando la comparación de vigencias de tarjeta y actual a solo fechas.
- v1.13:
  - Agregando la detección de vigencia de las tarjetas al software.
  - Cambiando el inicio de folio a 60.
  - Poniendo el label del socket de la ventana principal en la cintilla.
  - Añadiendo nueva opción de *"Fuera de vigencia"* a las ventanas emergentes.
- v1.12:
  - Agregando opción en la base de datos para que se pueda iniciar el viaje desde un folio especifico.
  - Agregando nuevas bases de datos de matrices tarifarías y servicios.
  - Agregando nuevo letrero en la ventana principal de camiones que se mostrara por si llegara a faltar enviar un dato al servidor.
  - Quitando variable "en_viaje".
  - Modificando diseño de las ventanas inicio y enviar vuelta.
  - Quitando la opción de que no dejaba cerrar turno hasta que se enviaran todos los datos al servidor.
  - Añadiendo en la ventana principal el número de socket.
  - Corrigiendo error de *"por_aniadir"*.
- v1.11:
  - Corrección de diseño de *enviar_vuelta*.
  - Arreglando glitch de cuando se cierra la ventana de chofer al no encontrar un servicio no se puede volver a meter a la misma.
- v1.10:
  - Agregando nuevas bases de datos, con nuevas matrices tarifarías, servicios, etc.
  - Nueva base de datos operadores.py.
  - Modificando diseño de ventana *enviar_vuelta*.
  - Añadiendo nombre y numero de empleado de operador en ticket de liquidación.
  - Solucionando espacio vació del UID.
  - Agregando parche para que no se dupliquen folios de ventas y no se sobrescriban en el servidor.
- v1.9:
  - Cambiando el numero de versión a variables globales.
  - Modificando query de la consulta de ventas de la petición "D".
  - Modificando las acciones de las peticiones del servidor.
  - Modificando estructura de la lectura de QR.
  - Modificando diseño de ventanas.
  - Añadiendo folio de viaje, folio de liquidación y versión del software a ticket de liquidación.
  - Modificando software para que no deje cerrar turno del operador hasta que se envíen todos los datos al servidor.
  - Arreglando bug de que el hilo de "enviar_vuelta" no se restablece al volver al restablecer la raspberry después de haber sido apagada.
  - Añadiendo nueva variable "en_viaje".
- v1.8:
  - Haciendo modificaciones en puertoSocket e idUnidad.
  - Modificando scrips de bases de datos.
  - Arreglando bug de que se truena el programa al darle doble click en el botón de terminar vuelta.
  - Agregando opción para que no se abran ventanas innecesarias.
- v1.7:
  - Mejorando la detección de la hora por SIM y GPS.
  - Modificando scripts de bases de datos.
  - Haciendo modificaciones en puertoSocket e idUnidad.
  - Agregando nuevas bases de datos
- v1.6:
  - Añadiendo verificación del tamaño del archivo que llega por FTP.
  - Añadiendo nuevo archivo "verificar_carpeta" para la detección de Urban_Urbano.
  - Mejorando la auto-actualización por FTP.
  - Modificando la lectura de transbordos.
  - Cambiando distancia minima de 0.004 a 0.003.
  - Creando nueva base de datos para los tickets usados.
  - Optimizando lectura en bases de datos.
  - Creando nuevo archivo "impresora.py" donde se concentra toda la impresión de tickets.
  - Modificando los archivos donde se imprimen tickets para que utilicen el archivo *impresora.py*
  - Añadiendo nueva base de datos.
  - Modificando el tamaño de las ventanas para que abarquen todo el espacio de la pantalla.
- v1.5:
  - Cambiando los tipo de hilos de la detección de geocercas y validación de datos de *threading* a *QThread*.
  - Corrigiendo la impresión de tickets de transbordo.
  - Haciendo más robusto el envío de datos por TCP/IP al servidor.
  - Añadiendo respuestas de las peticiones del servidor para el reenvió de datos.
  - Modificando trama 3 (envío de GNSS) para cuando no haya un viaje iniciado, se mande un 99 en el contador de folio de viaje, para así no perder coordenadas GNSS de una unidad a pesar de que no tenga folio de viaje asociado.
  - Añadiendo más información de retroalimentación al log.
  - Cambiando la reconexión al servidor cuando falla el envío de datos para que ahora solo al intento fallido 4 cierre y abra el socket y al intento 6 reinicie el módem Quectel.
  - Modificaciones del FrontEnd
- v1.4:
  - Haciendo que suene el zumbador al momento de que suceda cualquier error.
  - Priorizando el reinicio del Quectel al acumular muchos intentos fallidos de envíos de datos al servidor.
  - Cambiando diseño.
  - Mejorando condicional de conteo de datos enviados en la interfaz enviar_vuelta.
- v1.3:
  - Mejorando restablecimiento de la conexión del QR.
  - Añadiendo nuevo campo a la base de datos aforo.db donde se guardara el puerto del socket y así sera mas accesible para cambiarlo.
  - Mejorando el diseño de la ventana enviar_vuelta.
  - Optimizando el envió de datos a pesar de no contar con coordenadas GPS.
  - Optimizando la conexión de la impresora para la impresión de tickets.
- v1.2:
    - Mejorando la restauración de ventanas y datos por si llegara a ocurrir que el sistema se detenga de la nada cuando no debe.
- v1.1:
    - Mejorando la detección de geocercas.
    - Añadiendo lectura de códigos QR.
    - Optimizando código para una mayor eficiencia.
    - Añadiendo más opciones de ventanas emergentes.
    - Arreglando bugs y glitches generales que podrían afectar en lo proximo.
- v1.0:
    Sistema funcional para la venta de pasajes en transporte urbano, impresión de tickets con/sin QR, envió de datos mediante TCP/IP, auto actualizable mediante FTP y detección de geocercas.