from urllib import response
import requests

api_url = "http://127.0.0.1:8090/empresas/delete/5"

response = requests.delete(api_url)

print(response)


#empresas = [
#            {'ID_empresa':'1','nome':'Waterpark','cnpj':'123123123123' },
#            {'ID_empresa':'2','nome':'Shopping','cnpj':'123456789000' }
#]