import socket

PUERTO = 9000
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("localhost", PUERTO))
servidor.listen(1)

conexion, direccin = servidor.accept()
datos = conexion.recv(1024)
print("Datos recibidos: ", datos.decode())

conexion.close()
servidor.close()



