#Ejecucion: python3 atacante_udp.py
import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#establecer el socket de destino (IP, puerto )
servidor_destino = ('10.208.128.116', 5050)

#mientras se pueda hacer conexion intentar envir la coordenadas
while True:
    ataque = input("Coordenada de disparo: ")
    if not ataque:
        break
    #Se envia la coordenada codificada con utf-8
    cliente.sendto(ataque.encode('utf-8'), servidor_destino)
    respuesta, _ = cliente.recvfrom(1024)
    print(f"Respuesta recibida: {respuesta.decode('utf-8')}")

cliente.close()
