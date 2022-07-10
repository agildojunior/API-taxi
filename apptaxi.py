import sqlite3
from ssl import HAS_TLSv1_1
from flask import Flask, request, Response, g, jsonify
import db

app = Flask(__name__)
app.config['DEBUG']=True #atualizar sempre que mudar algo.

DB_URL = 'apptaxidb.db'


#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#pegar dados do banco
@app.before_request
def before_request():
    print("conectando ao banco...")
    conn = sqlite3.connect(DB_URL)
    g.conn = conn
#saindo do banco de dados
@app.teardown_request
def after_request(exception):
    if g.conn is not None:
        g.conn.close()
        print("Saindo do banco de dados...")
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

#teste
@app.route("/", methods=['GET'])
def teste():
    return '<h1>teste home page</h1>'

#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#inserir dados em empresas 
@app.route("/add_empresas",methods=['POST'])
def add_empresas():
    if request.is_json:
        empresas = request.get_json()
        id = db.insert_empresas(
            (
                empresas['nome'],
                empresas['cnpj'], 
            )
        )
        return {"id":id}, 201
    return {"error": "Request must be JSON"}, 415

#inserir dados em taxis
@app.route("/add_taxis",methods=['POST'])
def add_taxis():
    if request.is_json:
        taxis = request.get_json()
        id = db.insert_taxis(
            (
                taxis['nome_motorista'],
            )
        )
        return {"id":id}, 201
    return {"error": "Request must be JSON"}, 415

#inserir dados em corridas
@app.route("/add_corridas",methods=['POST'])
def add_corridas():
    if request.is_json:
        corridas = request.get_json()
        id = db.insert_corridas(
            (
                corridas['ID_empresa'],
                corridas['ID_taxi'],
                corridas['status'],
                corridas['Cliente'],
                corridas['destino'],
                corridas['origem'],
            )
        )
        return {"id":id}, 201
    return {"error": "Request must be JSON"}, 415
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#todos os dados das empresas
def query_empresas_to_dict(conn , query):#funcao transformando tipo dos dados das empresas
    cursor = conn.cursor()
    cursor.execute(query)
    empresas_dict = [{'ID_empresa':row[0], 'nome':row[1], 'cnpj':row[2]}
                        for row in cursor.fetchall()]
    return empresas_dict
@app.route("/empresas", methods=['GET'])
def get_empresas():
    #receber dados do banco
    query = """
        SELECT ID_empresa, nome, cnpj
        FROM empresas;
    """
    empresas_dict = query_empresas_to_dict(g.conn , query) #funcao transformando tipo dos dados

    return {'empresas': empresas_dict}


#todos os dados dos taxis
def query_taxis_to_dict(conn , query):#funcao transformando tipo dos dados das empresas
    cursor = conn.cursor()
    cursor.execute(query)
    taxis_dict = [{'ID_taxi':row[0], 'nome_motorista':row[1]}
                        for row in cursor.fetchall()]
    return taxis_dict
@app.route("/taxis", methods=['GET'])
def get_taxis():
    #receber dados do banco
    query = """
        SELECT ID_taxi, nome_motorista
        FROM taxis;
    """
    taxis_dict = query_taxis_to_dict(g.conn , query) #funcao transformando tipo dos dados

    return {'taxis': taxis_dict}


#todos os dados das corridas
def query_corridas_to_dict(conn , query):#funcao transformando tipo dos dados das empresas
    cursor = conn.cursor()
    cursor.execute(query)
    corridas_dict = [{'ID_corrida':row[0], 'ID_empresa':row[1], 'ID_taxi':row[2], 'status':row[3], 'Cliente':row[4], 'destino':row[5], 'origem':row[6]}
                        for row in cursor.fetchall()]
    return corridas_dict
@app.route("/corridas", methods=['GET'])
def get_corridas():
    #receber dados do banco
    query = """
        SELECT ID_corrida, ID_empresa, ID_taxi, status, Cliente, destino, origem
        FROM corridas;
    """
    corridas_dict = query_corridas_to_dict(g.conn , query) #funcao transformando tipo dos dados

    return {'corridas': corridas_dict}

#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

#editar dados de uma empresa
@app.route("/edit_empresas/<int:ID_empresa>", methods=["PUT"])
def update_empresa(ID_empresa):
    empresas = request.get_json()
    db.query_db(f'UPDATE empresas SET nome = "{empresas["nome"]}", cnpj = "{empresas["cnpj"]}" where ID_empresa = {ID_empresa}')
    return 'ok', 200

#editar dados de um taxi
@app.route("/edit_taxis/<int:ID_taxi>", methods=["PUT"])
def update_taxis(ID_taxi):
    taxis = request.get_json()
    db.query_db(f'UPDATE taxis SET nome_motorista = "{taxis["nome_motorista"]}" where ID_taxi = {ID_taxi}')
    return 'ok', 200

#editar dados de uma corrida
@app.route("/edit_corridas/<int:ID_corrida>", methods=["PUT"])
def update_corridas(ID_corrida):
    corridas = request.get_json()
    db.query_db(f'UPDATE corridas SET ID_empresa = "{corridas["ID_empresa"]}", ID_taxi = "{corridas["ID_taxi"]}", status = "{corridas["status"]}", Cliente = "{corridas["Cliente"]}", destino = "{corridas["destino"]}", origem = "{corridas["origem"]}" where ID_corrida = {ID_corrida}')
    return 'ok', 200

#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

#Deletar empresa especifica pelo ID_empresa
@app.route("/empresas/delete/<int:id>", methods=["DELETE"])
def delete_address(id):
    db.query_db(f'DELETE from empresas WHERE ID_empresa= {id}')
    return 'ok', 200

#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

#filtrar corridas de uma empresa especifica
#@app.route("/corridas/empresa/<ID_empresa>" , methods=['GET'])
#def get_corridas_empresa(ID_empresa):
#    out_corridas = []
#    for corrida in corridas:
#        if ID_empresa == corrida['ID_empresa']: #verificando se o ID da empresa é igual a ID da empresa que eu solicitei
#            out_corridas.append(corrida)
#    return {'corridas': out_corridas}

#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#iniciar o banco de dados----------------------------------------------------------

if __name__ == '__main__':
    init_db = False
    
    db.init_app(app)
    
    if init_db:
        with app.app_context():
            db.init_db()
    
    app.run(debug=True,host="0.0.0.0", port=8090)