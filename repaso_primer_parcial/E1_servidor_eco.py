import socket

HOST = "0.0.0.0" 
PUERTO = 5000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

servidor.bind((HOST, PUERTO))


servidor.listen(1)
print(f"Servidor de eco escuchando en el puerto {PUERTO}...")

while True:
    conexion, direccion = servidor.accept()
    print(f"Cliente conectado desde {direccion}")

    buffer = ""   #bufer para acumular la informacion recibida por framing
    while True:
        datos = conexion.recv(1024)  
        if not datos:
            print(f"Cliente {direccion} se desconecto")
            break

        buffer += datos.decode("utf-8")

        #mientras haya algun un mensaje completo en el buffer, se trata
        while "\n" in buffer:
            mensaje, buffer = buffer.split("\n", 1)
            print(f"Recibido de {direccion}: {mensaje}")
            # sendall exige bytes -> encode
            conexion.sendall((mensaje + "\n").encode("utf-8"))

    conexion.close()   #cerramos el socket de ese cliente
