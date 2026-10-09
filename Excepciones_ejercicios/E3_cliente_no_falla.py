import socket
import sys

def main():
    #pedir la IP del servidor al usuario
    host = input("Ingresa la IP del servidor: ").strip()
    if not host:
        print("Error: Debes ingresar una IP")
        sys.exit(1)  

    puerto = 5000

    try:
        conexion = socket.create_connection((host, puerto), timeout=5)
    except socket.gaierror:
        #Fallo al resolver la IP
        print(f"Error: La dirección IP no es valida")
        sys.exit(1)
    except ConnectionRefusedError:
        #no hay ningun servidor escuchando en ese puerto
        print(f"Error: No hay un servidor escuchando en {host}:{puerto}")
        sys.exit(1)
    except TimeoutError:
        #el servidor no responde a tiempo
        print(f"Error: El servidor {host}:{puerto} no respondio a tiempo")
        sys.exit(1)
    except KeyboardInterrupt:
        #el usuario cancela con Ctrl+C antes de conectar
        print("\nConexion cancelada por el usuario")
        sys.exit(1)

    
    with conexion:
        print(f"Conectado exitosamente a {host}:{puerto}")
        
        try:
            while True:
                mensaje = input("> ").strip()
                
                if not mensaje:
                    continue
                

                #envio y recepción de datos con framing
                conexion.sendall(f"{mensaje}\n".encode("utf-8"))
                
                datos = conexion.recv(1024)
                if datos:
                    respuesta = datos.decode("utf-8").strip()
                    print(f"Servidor responde: {respuesta}")
                else:
                    print("El servidor cerro la conexión sin enviar datos")
                    break

        except ConnectionResetError:
            #si el servidor se apaga repentinamente
            print("\nError: El servidor cerró la conexion inesperadamente")
            sys.exit(1)
        except TimeoutError:
            #si recv() sobrepasa el tiempo limite sin datos
            print("\nError: El servidor dejó de responder durante el envío del mensaje.")
            sys.exit(1)
        except KeyboardInterrupt:
            #captura Ctrl+C mientras el usuario escribe o espera respuesta
            print("\nCerrando socket...")
            sys.exit(0) 

main()
