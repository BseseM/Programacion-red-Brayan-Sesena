import threading
import time

def saludar(nombre, saludos):
    try:
        for i in range(saludos):
            print(f"{nombre}: hola {i}")
            time.sleep(1)
    except TypeError:
        print(f"Los saludos deben ser un numero entero")
    

def main():
    personas = [("Ana", 3), ("Beto", 5), ("Cora", 2)]
    hilos = []
    
    for nombre, cantidad in personas:
        hilo = threading.Thread(target=saludar, args=(nombre,cantidad))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()
        
    print("Fin del programa")

main()


