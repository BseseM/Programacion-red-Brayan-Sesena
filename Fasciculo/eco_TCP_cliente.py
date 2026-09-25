import socket

IP_SERVIDOR = "localhost"
PUERTO = 5050

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#c) en esta linea es donde se dispoara el handshake
cliente.connect((IP_SERVIDOR, PUERTO))
print("Conectado al servidor eco. Escribe el mensaje o vacio (Enter) para salir")

while True:
    mensaje = input("Mensaje escrito:")
    if mensaje == "":
        break
    cliente.send(mensaje.encode("utf-8"))
    eco = cliente.recv(1024).decode("utf-8")
    print("Respuesta del servidor:", eco)

cliente.close()
print("Conexion cerrada")
