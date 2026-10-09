import socket

def main():

    try:
        with socket.create_connection(("127.0.0.1", 5000), timeout=5) as conexion:
            while True:
                mensaje = input("> ").strip() 
                #envios de mensajes codificado con salto de linea
                if not mensaje: 
                    continue
                conexion.sendall(f"{mensaje}\n".encode("utf-8"))
                
                datos = conexion.recv(1024)
                if datos:
                    respuesta = datos.decode("utf-8").strip()
                    print(f"Servidor responde: {respuesta}")
                else:
                    print("El servidor cerró la conexion antes de tiempo")
                    break

    except ConnectionRefusedError:
        print(f"No hay un servidor escuchando en {ip_servidor}:{puerto}")
    except TimeoutError:
        print("El servidor no respondió a tiempo")
    except ConnectionResetError:
        print("Se perdio la conexión con el servidor repentinamente")

main()
