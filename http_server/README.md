# Practica 8 Servidor HTTP CRUD
Implementación de un servidor CRUD HTTP, el servidor es un servidor
de bitacora, que devuelve incidencias generadas y guardadas en un JSON.

A su vez el servidor crea los recursos /contadores y /logs.

+ Incidencias
Están diseñadas para sobrevivir a los reinicios porque se guardan 
de forma no volátil en un archivo físico (incidencias.json). Cada 
vez que se crea, modifica o elimina un registro (mediante POST, PATCH,
 PUT o DELETE), el servidor ejecuta la función guardar() para actualizar 
 el archivo en disco. Asimismo, al arrancar por primera vez, el servidor ejecuta
  cargar() para leer ese archivo y recuperar los datos, asegurando que el folio 
  (siguiente_id) continúe donde se quedo

+ Logs y Contadores

Por el contrario, la bitácora de peticiones (logs) y las estadísticas de uso 
(contadores) son estructuras que residen únicamente en la memoria RAM del programa 
(en variables globales de Python) durante la ejecución de la sesión. El código actual 
no incluye ninguna función que guarde estos datos en un archivo de texto o base de datos 
en disco. Por lo tanto, al detener el servidor (Ctrl + C), la memoria RAM se libera por 
completo y, al volver a iniciarlo, los contadores y registros se reinician a sus valores 
iniciales en cero

## Ejecución de los programas
Ejecutar primero el servidor
```bash
python3 servidor_bitacora_completo.py
```
Para el caso del cliente no se implementaron funciones como tal, el programa
ejecuta multiples secciones de código en la misma ejecución, sin embargo
se pueden comentar o descomentar secciones dependiendo de que se quiera probar
en el servidor.
```bash
pyhton3 cliente_bitacora.py
```
De igual forma se puede usar curl para consultar al servidor
```bash
# Crear (POST, datos en el cuerpo con -d)
curl -i -X POST http://localhost:8001/incidencias -H "Content-Type: application/json" -d
"{\"tipo\": \"vulnerabilidad\", \"descripcion\": \"SSH con contrasena debil\"}"

# Consultar todas, con filtro, o una por id (GET, datos en la URL)
curl http://localhost:8001/incidencias
curl "http://localhost:8001/incidencias?tipo=alerta"

# Modificar (PATCH: id en la ruta, cambios en el cuerpo)
10 curl -i -X PATCH http://localhost:8001/incidencias/1 -H "Content-Type: application/json" -d
"{\"estado\": \"resuelta\"}"

# Eliminar (DELETE: solo el id en la ruta)
curl -i -X DELETE http://localhost:8001/incidencias/1

# La auditoría del servidor
curl http://localhost:8001/contadores
curl http://localhost:8001/logs
```
