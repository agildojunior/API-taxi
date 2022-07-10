from urllib import response
import requests

def update(ID_corrida):
  rest = {"ID_empresa":"1","ID_taxi":"1","status":"Concluido","Cliente":"GUGUGaiteiro","destino":"Pau dos ferros, Rua abobora, numero 800","origem":"Dr.Severiano, Rua tal, numero 100"}
  response = requests.put(f'http://127.0.0.1:8090/edit_corridas/{ID_corrida}', json=rest)
  print(response)

print(response)

update(1)
