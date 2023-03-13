from flask import Flask, request, jsonify
import pymysql.cursors
import os


app = Flask(__name__)


# Conexión a la base de datos
connection = pymysql.Connect(
    host=os.environ.get('MYSQL_HOST'),
    user=os.environ.get('MYSQL_USER'),
    password=os.environ.get('MYSQL_PASSWORD'),
    db=os.environ.get('MYSQL_DATABASE'),
    port=os.environ.get('MYSQL_PORT'),
)

# Ruta para la API
@app.route('/api/query')
def query():
    # Obtener el valor del parámetro "id" de la consulta
    id = request.args.get('id')

    # Si el parámetro "id" no está presente, devolver un error
    if id is None:
        return jsonify({'error': 'No se proporcionó un valor para el parámetro "id".'})

    # Crear un cursor para la base de datos
    with connection.cursor() as cursor:
        # Ejecutar la consulta SQL
        cursor.execute('SELECT * FROM Lista_de_invitados WHERE ID = %s', id)
        
        # Obtener los resultados de la consulta
        result = cursor.fetchone()

        # Si no se encontraron resultados, devolver un error
        if result is None:
            return jsonify({'error': 'No se encontró un registro con el ID proporcionado.'})

        # Devolver el resultado como JSON
        return jsonify(result)

# Iniciar la aplicación
if __name__ == '__main__':
    app.run()