#COMENTAR o DESCOMENTAR SEGUN LO QUE SE QUIERA HACER

import urllib.request
import json

BASE = "http://localhost:8001"

print("--- 1. CREAR UNA INCIDENCIA (POST) ---")
url = f"{BASE}/incidencias"
data = json.dumps({"tipo": "alerta", "descripcion": "Escaneo de puertos no autorizado"}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")

try:
    with urllib.request.urlopen(req) as response:
        print("Codigo:", response.status)
        creada = json.loads(response.read().decode("utf-8"))
        print("Creada:", creada)
        inc_id = creada["id"]
except urllib.error.HTTPError as e:
    print("Error HTTP:", e.code, e.read().decode("utf-8"))


print("\n--- 2. CONSULTAR TODAS LAS INCIDENCIAS (GET) ---")
with urllib.request.urlopen(f"{BASE}/incidencias") as response:
    print("Total de incidencias:", len(json.loads(response.read().decode("utf-8"))))


print("\n--- 3. FILTROS COMBINADOS (GET /incidencias?tipo=alerta&estado=abierta) ---")
with urllib.request.urlopen(f"{BASE}/incidencias?tipo=alerta&estado=abierta") as response:
    print("Filtradas:", json.loads(response.read().decode("utf-8")))


print("\n--- 4. MODIFICAR CON PATCH ---")
url_patch = f"{BASE}/incidencias/{inc_id}"
data_patch = json.dumps({"estado": "resuelta"}).encode("utf-8")
req_patch = urllib.request.Request(url_patch, data=data_patch, headers={"Content-Type": "application/json"}, method="PATCH")

try:
    with urllib.request.urlopen(req_patch) as response:
        print("Codigo PATCH:", response.status)
        print("Actualizada:", json.loads(response.read().decode("utf-8")))
except urllib.error.HTTPError as e:
    print("Error HTTP:", e.code, e.read().decode("utf-8"))


print("\n--- 5. CONSULTAR CONTADORES Y LOGS ---")
with urllib.request.urlopen(f"{BASE}/contadores") as response:
    print("Contadores:", json.loads(response.read().decode("utf-8")))

with urllib.request.urlopen(f"{BASE}/logs") as response:
    print("Logs:", json.loads(response.read().decode("utf-8")))
    


print("\n--- 6. ELIMINAR CON DELETE ---")
req_del = urllib.request.Request(f"{BASE}/incidencias/{inc_id}", method="DELETE")
try:
    with urllib.request.urlopen(req_del) as response:
        print("Codigo DELETE (esperado 204 sin contenido):", response.status)
except urllib.error.HTTPError as e:
    print("Error HTTP:", e.code, e.read().decode("utf-8"))
