from flask import Flask, jsonify
import pymysql.cursors
import os
from dotenv import load_dotenv
import json


load_dotenv()

app = Flask(__name__)

config = {
    'user': os.getenv('db_user'),
    'password': os.getenv('db_password'),
    'host': os.getenv('cloud_sql_host'),
    'database': os.getenv('db_name'),
    'port': os.getenv('db_port'),
}

db_connection_name=os.getenv('db_connection_name'),

# Ruta para la API en caso no se administre id
@app.route('/api/', methods=['GET'])
def main():
    return json.dumps({'error': 'ID NOT SUPPLIED'}),404


@app.route('/api/<id>', methods=['GET'])
def get_invitado(id):
    
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    
    if os.environ.get('GAE_ENV') == 'standard':
        # Configuración para conexión mediante IP interna de gcloud
        #Cambiar host por la IP interna de la instancia de Cloud SQL
        connection = pymysql.Connect(
                            #Cambiar el host por la ip privada de la instancia de Cloud SQL
                            host="10.9.16.3",
                            user=config['user'],
                            password=config['password'],
                            db=config['database'],
                            port=int(config['port']),
                        )
    else:
        connection = pymysql.Connect(
                            host=config['host'],
                            user=config['user'],
                            password=config['password'],
                            db=config['database'],
                            port=int(config['port']),
                        )
        
        
    try:
    
        with connection.cursor() as cursor:

            # Si el parámetro "id" no está presente, devolver un error
            if id is None:
                return json.dumps({'error': 'ID NOT SUPPLIED'}),404
            
            if id == "":
                return json.dumps({'error': 'ID NOT SUPPLIED'}),404

            # Crear un cursor para la base de datos
            with connection.cursor() as cursor:
                # Ejecutar la consulta SQL
                cursor.execute('SELECT * FROM Lista_de_invitados WHERE ID = %s', id)
                
                # Obtener los resultados de la consulta
                result= cursor.fetchone()
                

                # Si no se encontraron resultados, devolver un error
                if result is None:
                    return jsonify({'error': 'ID NOT FOUND'}),404

                # Devolver el resultado como JSON
                cursor.execute('SELECT * FROM Lista_de_invitados WHERE ID = %s', id)
                data=cursor.fetchall()
                result = {"ID": data[0][0], "SEX": data[0][1], "APELLIDOS": data[0][2], "NOMBRES": data[0][3], "NUMBER_GUEST": data[0][4], "MESA": data[0][5], "CELULAR": data[0][6], "CONFIRMADO": data[0][7]}
                j_result = json.dumps(result)
                return j_result,200
    finally:
        connection.close()


# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)