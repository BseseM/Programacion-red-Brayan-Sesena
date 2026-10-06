import socket
import threading

turno = 0
lock = threading.Lock()  #protege la sección crítica del contador

def aumentar_turno():
    global turno
    with lock:  #Uso de lock para evitar condiciones de carrera
        turno += 1


def atender_cliente_tcp(conexion, direccion):
    with conexion:
        buffer = ""
        while True:    
            datos = conexion.recv(1024)  #manejo del buffer/framing TCP
            if not datos:
                break
            buffer += datos.decode("utf-8")
            while "\n" in buffer:
                 apodo, buffer = buffer.split("\n", 1)
                 aumentar_turno() #aumentar el contador de turno tras obtener cada nuevo apodo  
                 respuesta = f"{turno}>{apodo}\n"  
                 conexion.sendall(respuesta.encode("utf-8"))

                 
#SERVIDOR UDP 
def servidor_udp():
    servidor_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_udp.bind(("0.0.0.0", 5001)) 
    print("Servidor UDP escuchando en el puerto 5001")
    
    while True:
        datos_udp, direccion_udp = servidor_udp.recvfrom(1024) 
        mensaje_udp = datos_udp.decode("utf-8").strip() #capturar los mensajes enviados por el cliente
        
        if mensaje_udp == "CUANTOS":
            respuesta_udp = f"van>{turno}\n" #mostrar el total de turnos 
        else:
            respuesta_udp = "consulta no reconocida\n"  
            
        servidor_udp.sendto(respuesta_udp.encode("utf-8"), direccion_udp) 

def main():
    #iniciar el servidor UDP en un hilo secudario como deamon a la par del servidor TCP
    hilo_udp = threading.Thread(target=servidor_udp, daemon=True)  #[cite: 4, 8]
    hilo_udp.start() 

    #iniciar el servidor TCP en el hilo principal
    servidor_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    servidor_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor_tcp.bind(("0.0.0.0", 5000))  
    servidor_tcp.listen() 
    print("Servidor TCP escuchando en el puerto 5000")
    
    while True:
        conexion_tcp, direccion_tcp = servidor_tcp.accept() 
        hilo_tcp = threading.Thread( #iniciar un hilo de ejecucion para cada cliente
            target=atender_cliente_tcp, 
            args=(conexion_tcp, direccion_tcp), 
            daemon=True
        ) 
        hilo_tcp.start()


main()
