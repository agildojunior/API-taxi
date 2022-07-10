from urllib import response
import requests

def update(ID_empresa):
  rest = {"nome": "fanki du yudi que vai dar ps2", "cnpj":"40028922"}
  response = requests.put(f'http://127.0.0.1:8090/edit_empresas/{ID_empresa}', json=rest)
  print(response)

print(response)

update(1)
