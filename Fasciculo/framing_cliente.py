import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("localhost", 5061))

cliente.send("Primer mensaje\nSegundo mensaje\nTercer mensaje\n".encode("utf-8"))
cliente.close()

