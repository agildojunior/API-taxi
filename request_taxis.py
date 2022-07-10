from urllib import response
import requests

api_url = "http://127.0.0.1:8090/add_taxis"
taxi = {"nome_motorista":"Leitinho"}
response = requests.post(api_url, json=taxi)

print(response.json())


#taxis = [
#            {'ID_taxi':'1','nome_motorista':'Everton'},
#            {'ID_taxi':'2','nome_motorista':'Raul'}
#]