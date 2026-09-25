import socket

DESTINO = ("localhost", 5050)

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cliente.settimeout(3)
print("Eco UDP. Escribe tu mensaje o vacio (enter) para salir")

while True:
    mensaje = input("Mensaje ingresado: ")
    cliente.sendto(mensaje.encode("utf-8"), DESTINO)
    if mensaje == "":
        break
    try:
        datos, _ = cliente.recvfrom(1024)
        print("El servidor responde: ", datos.decode("utf-8")) 
    except socket.timeout:
        print("El datagrama se perdio sin aviso")
cliente.close()
print("Sesion terminada (dado a que no hay una conexion como tal)")   

