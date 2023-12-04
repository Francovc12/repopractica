import datetime
from models.facturas import Facturas
from main import app, mysql
from flask import request, jsonify
from utils import recurso_usuario, requiere_token

@app.route('/usuario/<int:id_usuario>/factura',methods=['POST'])
@requiere_token
@recurso_usuario
def crear_factura(id_usuario):
    datos = request.get_json()
    datos["id_usuario"]=id_usuario
    try:
        nuevaFactura= Facturas.crear_factura(datos)
        return jsonify(nuevaFactura),201
    except Exception as e:
        return jsonify({"message":e.args[0]}),400
    
@app.route('/usuario/<int:id_usuario>/factura', methods = ['GET'])
@requiere_token
@recurso_usuario
def obtener_facturas(id_usuario):
    try:
        lista_facturas = Facturas.ver_facturas(id_usuario)
        return lista_facturas , 200
    except Exception as e:
        return jsonify({"message":e.args[0]}), 400
        