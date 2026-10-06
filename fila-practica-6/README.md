# Sistema de turnos LA FILA
## Práctica 6
---
+ Caso: Se programará la fila de una ventanilla de atención: cada cliente que llega toma un turno y el servidor asigna números
consecutivos (1, 2, 3, …) sin repeticiones ni saltos. Varios clientes solicitan turno de forma simultánea, lo que justifica la
concurrencia con hilos; además, cualquier equipo puede consultar cuántos turnos se han asignado sin establecer
conexión, lo que justifica UDP.

- Canal TCP: El cliente se conecta y envía su apodo. El servidor
responde turno>N\n con su número asignado.

- Canal UDP: El cliente envía un datagrama con la palabra CUANTOS.
El servidor responde van>N\n con el total de turnos
asignados.
---
La implementación en Python se resuleve el tres programas:
- fila_servidor.py: el programa encargado de ejecutar ambos servidores (TCP y UDP) y de procesar los mensajes con framing para TCP y los datagramas para UDP. A su vez es quien
  envia los mensajes turno>apodo\n para los clientes TCP informado cual el su turno y su apodo, mientras que en el lado de UDP envia van>turno\n cuando el cliente UDP envia
  la cadena "CUANTOS".
- fila_cliente_udp.py: el programa envia un datagrama sin conexión con la cadena "CUANTOS" para saber la cantida total de turnos actuales tomados.
- fila_cliente_tco.py: el programa envia una cadena con el apodo del cliente. Dicho apodo es leido por entrada estandar.
---
- Antes de ejecutar: Verificar las IP a usar para probar más alla de localhost.
### Ejecución (ejecutar primero el servidor)
```bash
python3 fila_servidor.py
python3 fila_cliente_tcp.py
python3 fila_cliente_udp.py
```
 
