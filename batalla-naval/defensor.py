#Uso: python3 defensor.py

import socket

# Coordenadas definidas de la flota
BARCOS = {"A1", "A2", "B3", "C4"}

# Crear socket (socket) cliente
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asociar a IP y puerto 5050 (bind) del servidor
servidor.bind(('10.208.128.237', 5050))

# Esperar conexiones (listen)
servidor.listen(1)
print("Defensor esperando en puerto 5050...")

# Aceptar conexión bloqueante (accept)
conexion, direccion = servidor.accept()
print(f"Atacante conectado desde {direccion}")

while True:
    datos = conexion.recv(1024)
    if not datos:
        break
        
    #Decodificar las coordenadas recibidas  
    coordenada = datos.decode('utf-8').strip().upper()

    if coordenada in BARCOS:
        respuesta = "TOCADO"
        BARCOS.remove(coordenada)
    else:
        respuesta = "AGUA"

    print(f"Ataque: {coordenada} | Evaluación: {respuesta} | Barcos restantes: {len(BARCOS)}")
    conexion.send(respuesta.encode('utf-8'))

conexion.close()
servidor.close()
    
