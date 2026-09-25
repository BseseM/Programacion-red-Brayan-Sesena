import socket 

PUERTO = 5061

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("localhost", PUERTO))
servidor.listen(1)
print("Servidor framing escuchando en ", PUERTO)

conexion, direccion = servidor.accept()
print("Servidor framing cliente: ", direccion)

buffer = ""
while True:
    datos = conexion.recv(1024)
    if not datos:
        break
    buffer += datos.decode("utf-8")
    while "\n" in buffer:
        mensaje, buffer = buffer.split("\n", 1)
        print("Servidor framing, mensaje completo recibido:", mensaje)

conexion.close()
servidor.close()

