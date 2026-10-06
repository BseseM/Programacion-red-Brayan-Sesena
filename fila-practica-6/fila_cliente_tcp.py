import socket

def main():
    
    apodo = input("Ingresa tu apodo: ").strip()
    
    with socket.create_connection(("127.0.0.1", 5000)) as conexion:
        #envia el apodo con el delimitador \n
        conexion.sendall(f"{apodo}\n".encode("utf-8"))
        
        respuesta = conexion.recv(1024).decode("utf-8").strip()
        print(f"Servidor responde: {respuesta}")

main()
