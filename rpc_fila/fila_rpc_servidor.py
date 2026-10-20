from xmlrpc.server import SimpleXMLRPCServer
import threading

turno = 0
lock = threading.Lock() #bloquear la variable 

#funcion para asignar los turnos y aumentar el contador de turno
def tomar_turno(apodo):
    global turno
    print("Apodo asignado: ", apodo)
    with lock:
        turno += 1
    return "Bienvenido, " + apodo + "!"

#funcion para devolver la cantidad de turnos actuales
def cuantos_van(): 
    print("Van: ", turno)
    return "Van: " + str(turno)


servidor = SimpleXMLRPCServer(("localhost", 5000))

#registrar las funciones
servidor.register_function(tomar_turno, "tomar_turno")
servidor.register_function(cuantos_van, "cuantos_van")
print("Servidor escuchando en el puerto 5000...")
servidor.serve_forever()
