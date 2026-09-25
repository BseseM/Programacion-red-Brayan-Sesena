import socket
import time

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("localhost", 5199))
servidor.listen(1)
print("servidor, esperando conexion...")

conexion, direccion = servidor.accept()
print("servidor, cliente conectado:", direccion)

conexion.settimeout(5)

inicio = time.time()
datos = conexion.recv(1024)

espera = time.time() - inicio
print("servidor> recv() regreso despues de {:.1f} segundos de espera".format(espera))
print("servidor> llego:", datos.decode())
conexion.close()
servidor.close()
