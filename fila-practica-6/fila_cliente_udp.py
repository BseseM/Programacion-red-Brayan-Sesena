import socket

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        cliente.settimeout(3)
        cliente.sendto("CUANTOS\n".encode("utf-8"), ("127.0.0.1", 5001))
        datos, _ = cliente.recvfrom(1024)
        print(f"Servidor responde: {datos.decode('utf-8').strip()}")
main()
