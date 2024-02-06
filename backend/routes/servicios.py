from main import app,mysql
from models.servicios import Servicios
from flask import jsonify, request
from utils import requiere_token,recurso_usuario

#ruta para obtener todos los servicios de un usuario
@app.route('/usuario/<int:id_usuario>/servicios', methods = ['GET'])
@requiere_token
@recurso_usuario
def get_servicio(id_usuario):
    try:
        servicios = Servicios.obtener_servicios(id_usuario)
        return jsonify(servicios), 200
    except Exception as e:
        return jsonify({"message":e.args[0]}), 400 

#ruta para obtener un  servicio por id_servicio
#nota se puede ver servicios de otros usuarios
@app.route('/usuario/<int:id_usuario>/servicios/<int:id_servicio>', methods=['GET'])
@requiere_token
@recurso_usuario
def obtener_servicio_por_id(id_usuario, id_servicio):
    try:
        servicio_porID = Servicios.servicio_por_id(id_servicio)
        return jsonify(servicio_porID), 200
    except Exception as e:
        return  jsonify({"message": e.args[0]}), 400  

#misma ruta pero implementando el metodo post para agregar un nuevo servicio
@app.route('/usuario/<int:id_usuario>/servicios', methods = ['POST'])
@requiere_token
@recurso_usuario
def crear_servicio(id_usuario):
    datos = request.get_json()
    datos["id_usuario"] = id_usuario

    try:
        nuevo_servicio = Servicios.crear_servicio(datos)
        return jsonify(nuevo_servicio), 201
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400
    
#ruta para modificar los servicios con el metodo put
@app.route('/usuario/<int:id_usuario>/servicios/<int:id_serv>', methods = ['PUT'])
@requiere_token
@recurso_usuario
def modificar_servicio(id_usuario,id_serv):
    datos = request.get_json()
    datos["id_usuario"] = id_usuario
    try:
        modificar_servicio = Servicios.actualizar_servicio(id_serv,datos)
        return jsonify(modificar_servicio), 200
    except Exception as e:
        return jsonify({"message": e.args[0]}),400
    
#ruta para eliminar un servicio
@app.route('/usuario/<int:id_usuario>/servicios/<int:id_servicio>', methods = ['DELETE'])
@requiere_token
@recurso_usuario
def eliminar_usuario(id_usuario,id_servicio):
    try:
        eliminar = Servicios.eliminar_servicio(id_usuario,id_servicio)
        return jsonify(eliminar), 200
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400