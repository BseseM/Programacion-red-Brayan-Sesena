import socket
import threading

def atender_cliente(conexion, direccion):
    
    #variable local, cada cliente/hilo tiene su propio contador independiente
    contador_mensajes = 0
    
    try:
        with conexion:
            buffer = ""
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    break
                
                buffer += datos.decode("utf-8")
                
                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)
                    contador_mensajes += 1  #aumentar contador de esie hilo
                    
                    respuesta = f"{contador_mensajes}>{linea}\n"
                    conexion.sendall(respuesta.encode("utf-8"))

    except ConnectionResetError:
        print(f"El cliente {direccion} se desconecto abrutamente")
    except BrokenPipeError: #si el socket se cerro antes de tiempo
        print(f"No se pudo enviar respuesta al cliente {direccion}")
    finally:
        print(f"Conexion cerrada: {direccion}")

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        servidor.bind(("0.0.0.0", 5000))
    except OSError:
        #si el puerto 5000 está ocupado, el programa se detiene 
        print("El puerto 5000 esta")
        return

    servidor.listen()
    print("Servidor TCP escuchando en el puerto 5000...")

    while True:
        conexion, direccion = servidor.accept()
        #crear un hilo independiente para cada nueva conexión
        hilo = threading.Thread(target=atender_cliente, args=(conexion, direccion), daemon=True)
        hilo.start()

main()
