from main import app,mysql
from models.clientes import Cliente
from flask import jsonify, request


# Ruta para obtener todos los clientes de un usuario

@app.route('/usuario/<int:id_usuario>/clientes', methods = ['GET'])
def clientes_por_id(id_usuario):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente WHERE id_usuario = {0}'.format(id_usuario))
    data = cur.fetchall()
    print(data)

    lista_clientes=[]

    for row in data:
        objCliente = Cliente(row)
        lista_clientes.append(objCliente.to_json())

    return jsonify(lista_clientes)


# Ruta para modificar un cliente

@app.route('/usuario/<int:id_usuario>/clientes/<int:id_cliente>', methods = ['PUT'])
def modificar_cliente(id_usuario,id_cliente,datos):
    datos = request.get_json()

    try:
        modificar_cliente = Cliente.modificar_cliente(id_usuario,id_cliente,datos)
        return jsonify(modificar_cliente), 200
    except Exception as e:
        return jsonify({"message": e.args[0]}),400


# Ruta para eliminar un cliente

@app.route('/usuario/<int:id_usuario>/clientes/<int:id_cliente>', methods = ['PUT'])
def eliminar_cliente(id_usuario,id_cliente):
    try:
        Cliente.eliminar_cliente(id_usuario,id_cliente)
    except Exception as e:
        return jsonify({"message": e.args[0]}),400