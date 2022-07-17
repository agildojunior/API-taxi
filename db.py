import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

DATABASE = 'apptaxidb.db'

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#

def query_empresas_to_dict(conn , query):#funcao transformando tipo dos dados das empresas
    cursor = conn.cursor()
    cursor.execute(query)
    empresas_dict = [{'ID_empresa':row[0], 'nome':row[1], 'cnpj':row[2]}
                        for row in cursor.fetchall()]
    return empresas_dict


def query_taxis_to_dict(conn , query):#funcao transformando tipo dos dados das empresas
    cursor = conn.cursor()
    cursor.execute(query)
    taxis_dict = [{'ID_taxi':row[0], 'nome_motorista':row[1]}
                        for row in cursor.fetchall()]
    return taxis_dict


def query_corridas_to_dict(conn , query):#funcao transformando tipo dos dados das empresas
    cursor = conn.cursor()
    cursor.execute(query)
    corridas_dict = [{'ID_corrida':row[0], 'ID_empresa':row[1], 'ID_taxi':row[2], 'status':row[3], 'Cliente':row[4], 'destino':row[5], 'origem':row[6]}
                        for row in cursor.fetchall()]
    return corridas_dict

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

#inserir dados em empresas
def insert_empresas(args=()):
    sql = """
        INSERT INTO empresas (nome, cnpj)
        VALUES (?, ?)
        """
    cur = get_db().cursor()
    cur.execute(sql, args)
    get_db().commit()
    return cur.lastrowid

#inserir dados em taxis
def insert_taxis(args=()):
    sql = """
        INSERT INTO taxis (nome_motorista)
        VALUES (?)
        """
    cur = get_db().cursor()
    cur.execute(sql, args)
    get_db().commit()
    return cur.lastrowid

#inserir dados em corridas
def insert_corridas(args=()):
    sql = """
        INSERT INTO corridas (ID_corrida , ID_empresa, ID_taxi, status, Cliente, destino, origem)
        VALUES (? ,?, ?, ?, ?, ?, ?)
        """
    cur = get_db().cursor()
    cur.execute(sql, args)
    get_db().commit()
    return cur.lastrowid

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = [dict((cur.description[i][0], value) \
       for i, value in enumerate(row)) for row in cur.fetchall()]
    
    get_db().commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv
    

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')