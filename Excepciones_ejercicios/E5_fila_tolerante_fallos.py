import socket
import threading

turno = 0  
lock = threading.Lock()  #protege la seccion critica del contador

def aumentar_turno():
    global turno
    with lock: 
        turno += 1
    

def atender_cliente_tcp(conexion, direccion):
    try:
        with conexion:
            buffer = ""
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    break
                
                try:
                    #captura bytes que no son UTF-8 ("basura")
                    texto_decodificado = datos.decode("utf-8")
                except UnicodeDecodeError:
                    print(f"Se recibieron bytes no validos en UTF-8")
                    buffer = ""
                    continue

                buffer += texto_decodificado
                
                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)
                    apodo = linea.strip()
                    
                    if apodo:
                        aumentar_turno()
                        respuesta = f"turno>{turno}\n"
                        conexion.sendall(respuesta.encode("utf-8"))
                        print(f"[{direccion}] Turno {turno} asignado a: '{apodo}'")
                    else:
                        #mensajes que no siguen el protocolo
                        print(f"[{direccion}] mensaje no reconocido")
                        conexion.sendall("mensaje no reconocido\n".encode("utf-8"))

    except ConnectionResetError:
        print(f"[{direccion}] El cliente se desconecto")
    except BrokenPipeError:
        print(f"[{direccion}] No se pudo enviar datos, la conexion se cerro")
    finally:
        print(f"[{direccion}] Conexion cerrada")

def servidor_udp():
    servidor_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        servidor_udp.bind(("0.0.0.0", 5001))
        print("Servidor UDP escuchando en el puerto 5001")
    except OSError:
        print("Error: El puerto UDP 5001 ya está en uso.")
        return

    while True:
        try:
            datos_udp, direccion_udp = servidor_udp.recvfrom(1024)
            
            try:
                mensaje_udp = datos_udp.decode("utf-8").strip()
            except UnicodeDecodeError:
                print(f"[UDP {direccion_udp}] codificación invalida")
                servidor_udp.sendto("consulta no reconocida\n".encode("utf-8"), direccion_udp)
                continue

            #CUANTOS -> van>N\n
            if mensaje_udp == "CUANTOS":
                with lock:
                    respuesta_udp = f"van>{turno}\n"
            else:
                respuesta_udp = "consulta no reconocida\n"
                
            servidor_udp.sendto(respuesta_udp.encode("utf-8"), direccion_udp)
        except Exception as e:
            print("Error en el socket UDP")

def main():
    #onicia el hilo secundario daemon para el servidor UDP
    hilo_udp = threading.Thread(target=servidor_udp, daemon=True)
    hilo_udp.start()

    #inicia el servidor TCP
    servidor_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        servidor_tcp.bind(("0.0.0.0", 5000))
    except OSError:
        print("Error: el puerto TCP 5000 esta ocupado por otro proceso")
        return

    servidor_tcp.listen()
    print("Servidor TCP escuchando en el puerto 5000")
    
    while True:
        try:
            conexion_tcp, direccion_tcp = servidor_tcp.accept()
            # Hilo de atención por cliente
            hilo_tcp = threading.Thread(
                target=atender_cliente_tcp, 
                args=(conexion_tcp, direccion_tcp), 
                daemon=True
            )
            hilo_tcp.start()
        except KeyboardInterrupt:
            print("\nServidor detenido manualmente (Ctrl+C).")
            break
        except Exception as e:
            print(f"Error al aceptar conexión TCP: {e}")

main()
