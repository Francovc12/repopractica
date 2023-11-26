from main import app,mysql
from models.productos import Producto
from flask import jsonify, request

#ruta para obtener todos los productos de un usuario
@app.route('/usuario/<int:id>/productos', methods = ['GET'])
def get_productos(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto WHERE id_usuario = {0}'.format(id))
    data = cur.fetchall()
    lista_productos=[]
    
    for row in data:
        objProducto = Producto(row)
        lista_productos.append(objProducto.to_json())

    return jsonify(lista_productos)

#misma ruta pero implementando el metodo post para agregar un nuevo producto
@app.route('/usuario/<int:id>/productos', methods = ['POST'])
def crear_producto(id):
    datos = request.get_json()
    datos["id_usuario"] = id

    try:
        nuevo_producto = Producto.crear_producto(datos)
        return jsonify(nuevo_producto), 201
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400
    
#ruta para modificar los productos con el metodo put
@app.route('/usuario/<int:id>/productos/<int:id_prod>', methods = ['PUT'])
def modificar_producto(id,id_prod):
    datos = request.get_json()
    datos["id_usuario"] = id
    try:
        modificar_producto = Producto.actualizar_producto(id_prod,datos)
        return jsonify(modificar_producto), 200
    except Exception as e:
        return jsonify({"message": e.args[0]}),400