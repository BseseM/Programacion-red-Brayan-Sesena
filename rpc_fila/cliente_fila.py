import xmlrpc.client

#leer el apodo desde teclado o entrada estandar
apodo = input("Ingresa tu apodo: ")

servidor = xmlrpc.client.ServerProxy("http://localhost:5000")

#crear la variables que llaman a las funciones reales en el servidor
pedir_turno = servidor.tomar_turno(apodo)
turnos = servidor.cuantos_van()

#imprimir la respuesta generada por el servidor
print(pedir_turno)
print(turnos)

