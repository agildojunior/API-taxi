from urllib import response
import requests

api_url = "http://127.0.0.1:8090/add_corridas"
corrida = {"ID_empresa":"2","ID_taxi":"2","status":"Concluido","Cliente":"Raul","destino":"Pau dos ferros, Rua abobora, numero 800","origem":"Pau dos ferros, Rua tal, numero 100"}
response = requests.post(api_url, json=corrida)

print(response.json())

#corridas = [
#            {'ID_corrida':'1','ID_empresa':'1','ID_taxi':'1','status':'Concluido','Cliente':'Junin' },
#            {'ID_corrida':'2','ID_empresa':'1','ID_taxi':'1','status':'Concluido','Cliente':'Leitinho' },
#            {'ID_corrida':'3','ID_empresa':'1','ID_taxi':'2','status':'Concluido','Cliente':'RaulDoCorote' },
#            {'ID_corrida':'4','ID_empresa':'2','ID_taxi':'2','status':'Concluido','Cliente':'GuguPimentinha' }
#]