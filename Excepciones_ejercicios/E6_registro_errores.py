import socket
import threading
import time

turno = 0  
lock = threading.Lock()  #

def registrar_log(direccion, descripcion):
    """Escribe un mensaje de error o evento en el archivo de bitacora"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    linea = f"{timestamp} {direccion} {descripcion}\n"
    
    with lock:  #protege la escritura en el archivo para evitar lineas entrelazadas o corruptas
        try:
            with open("servidor_errores.log", "a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except Exception as e:
            print(f"Error al escribir en la bitacora:")

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
                    # Captura bytes que no son UTF-8 ("basura")
                    texto_decodificado = datos.decode("utf-8")
                except UnicodeDecodeError:
                    mensaje_err = "se recibieron bytes no validos en UTF-8 (UnicodeDecodeError)"
                    print(f"[{direccion}] {mensaje_err}")
                    registrar_log(direccion, mensaje_err)
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
                        mensaje_err = "mensaje no reconocido"
                        print(f"[{direccion}] {mensaje_err}")
                        registrar_log(direccion, mensaje_err)
                        conexion.sendall("mensaje no reconocido\n".encode("utf-8"))

    except ConnectionResetError:
        mensaje_err = "conexion reiniciada por el cliente (ConnectionResetError)"
        print(f"[{direccion}] {mensaje_err}")
        registrar_log(direccion, mensaje_err)
    except BrokenPipeError:
        mensaje_err = "no se pudo enviar datos, la conexión se cerró (BrokenPipeError)"
        print(f"[{direccion}] {mensaje_err}")
        registrar_log(direccion, mensaje_err)
    finally:
        print(f"[{direccion}] Conexion cerrada")

def servidor_udp():
    servidor_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        servidor_udp.bind(("0.0.0.0", 5001))
        print("Servidor UDP escuchando en el puerto 5001")
    except OSError:
        mensaje_err = "el puerto UDP 5001 ya esta en uso"
        print(f"Error: {mensaje_err}")
        registrar_log("0.0.0.0:5001", mensaje_err)
        return

    while True:
        try:
            datos_udp, direccion_udp = servidor_udp.recvfrom(1024)
            
            try:
                mensaje_udp = datos_udp.decode("utf-8").strip()
            except UnicodeDecodeError:
                mensaje_err = "codificación inválida UTF-8 en datagrama UDP"
                print(f"[UDP {direccion_udp}] {mensaje_err}")
                registrar_log(direccion_udp, mensaje_err)
                servidor_udp.sendto("consulta no reconocida\n".encode("utf-8"), direccion_udp)
                continue

            if mensaje_udp == "CUANTOS":
                with lock:
                    respuesta_udp = f"van>{turno}\n"
            else:
                respuesta_udp = "consulta no reconocida\n"
                registrar_log(direccion_udp, f"consulta UDP no reconocida: '{mensaje_udp}'")
                
            servidor_udp.sendto(respuesta_udp.encode("utf-8"), direccion_udp)
        except Exception as e:
            print("Error en el socket UDP")
            registrar_log("UDP", f"error en socket UDP: {e}")

def main():
    hilo_udp = threading.Thread(target=servidor_udp, daemon=True)
    hilo_udp.start()

    servidor_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        servidor_tcp.bind(("0.0.0.0", 5000))
    except OSError:
        mensaje_err = "el puerto TCP 5000 esta ocupado por otro proceso"
        print(f"Error: {mensaje_err}")
        registrar_log("0.0.0.0:5000", mensaje_err)
        return

    servidor_tcp.listen()
    print("Servidor TCP escuchando en el puerto 5000")
    
    while True:
        try:
            conexion_tcp, direccion_tcp = servidor_tcp.accept()
            hilo_tcp = threading.Thread(
                target=atender_cliente_tcp, 
                args=(conexion_tcp, direccion_tcp), 
                daemon=True)
            hilo_tcp.start()
        except KeyboardInterrupt:
            print("\nServidor detenido manualmente (Ctrl+C).")
            break
        except Exception as e:
            print(f"Error al aceptar conexion TCP: {e}")
            registrar_log("TCP", f"error al aceptar conexion: {e}")


main()
