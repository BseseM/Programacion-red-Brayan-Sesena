import socket
import time

def consultar(servidor, mensaje, reintentos):

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        cliente.settimeout(2)
        
        for intento in range(1, reintentos + 1):
            try:
                #Enviar datagrama 
                cliente.sendto(f"{mensaje}\n".encode("utf-8"), servidor)
                
                #esperar respuesta del servidor
                datos, _ = cliente.recvfrom(1024)
                return datos.decode("utf-8").strip()
                
            except TimeoutError:
                #calculo de la espera creciente exponencial: 1, 2 y 4 segundos
                espera = 2 ** (intento - 1)
                print(f"Intento {intento}/{reintentos}: Sin respuesta. Reintentando en {espera}seg...")
                time.sleep(espera)
                
    #si agoto los 3 intentos, devuelve None
    return None

def main():
    host = "127.0.0.1"
    puerto = 5001
    mensaje = "CUANTOS"
    reintentos = 3
    
    print(f"Consultando estado de LA FILA a {host}:{puerto}...")
    
    #llamada a la función con la palabra "CUANTOS"
    respuesta = consultar((host, puerto), mensaje, reintentos)
    
    
    if respuesta:
        print(f"Servidor responde: {respuesta}")
    else:
        print("El servidor no respondio tras los  3 intentos")

main()
