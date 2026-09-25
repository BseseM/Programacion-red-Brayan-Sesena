import socket

def armar_eco(mensaje, numero):
    eco = f"ECO#{numero}> " + mensaje
    conexion.send(eco.encode("utf-8"))
    
    
PUERTO = 5050

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind(("0.0.0.0", PUERTO))

servidor.listen(1)
print("Servidor escuchando en el puerto", PUERTO)

#a) en esta linea es donde el servidor se bloquea esperando al cliente
conexion, direccion = servidor.accept() 
print("Cliente conectado desde", direccion)

contador = 1
while True:
    #b) esta es la linea donde se bloque esperando datos
    datos = conexion.recv(1024)  
    if not datos:
        break
    mensaje = datos.decode("utf-8")
    armar_eco(mensaje, contador)
    contador += 1

conexion.close()
servidor.close()
print("Servidor eco terminado")

