import socket

PUERTO = 5050

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(("0.0.0.0", PUERTO))
print("Eco UDP escuchando en el puerto", PUERTO)

while True:
    datos, direccion = servidor.recvfrom(1024)
    mensaje = datos.decode("utf-8")
    print("Datagrama de", direccion, ":", mensaje)
    if mensaje.strip() == "":
        break
    eco = "ECO>" + mensaje

    servidor.sendto(eco.encode("utf-8"), direccion)

servidor.close()
print("Eco UDP terminado")
