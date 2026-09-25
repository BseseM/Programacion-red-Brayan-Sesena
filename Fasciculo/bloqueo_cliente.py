import socket
import time
ESPERA = 7

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("localhost", 5199))
print("cliente conectado;", ESPERA, "segundos antes de enviar...")
time.sleep(ESPERA)
cliente.send("ya llegue!".encode())
cliente.close()
