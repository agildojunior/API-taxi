from urllib import response
import requests

api_url = "http://127.0.0.1:8090/add_empresas"
empresa = {"nome":"shopping","cnpj":"123456789000"}
response = requests.post(api_url, json=empresa)

print(response.json())


#empresas = [
#            {'ID_empresa':'1','nome':'Waterpark','cnpj':'123123123123' },
#            {'ID_empresa':'2','nome':'Shopping','cnpj':'123456789000' }
#
