from urllib import response
import requests

def update(ID_taxi):
  rest = {"nome_motorista": "RaulDoCorote"}
  response = requests.put(f'http://127.0.0.1:8090/edit_taxis/{ID_taxi}', json=rest)
  print(response)

print(response)

update(1)
