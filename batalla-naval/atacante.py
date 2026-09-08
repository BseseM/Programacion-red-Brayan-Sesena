#Uso: python3 atacante.py 

import socket

# Crear socket cliente (socket)
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor (socket) con IP y puerto
cliente.connect(('10.208.128.116', 5050))

#Mientras haya conexion enviar coordenadas codificadas en utf-8
while True:
    # Enviar petición y codificar (send = encode)
    ataque = input("Ingresar coordenada de ataque (ej. B4): ")
    if not ataque:
        break
    cliente.send(ataque.encode('utf-8'))

    # Recibir respuesta y decodificar (receive = decode)
    respuesta = cliente.recv(1024).decode('utf-8')
    print(f"Respuesta del defensor: {respuesta}")

cliente.close()
