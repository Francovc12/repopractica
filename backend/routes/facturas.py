import datetime
from models.facturas import Facturas
from main import app, mysql
from flask import request, jsonify
from utils import recurso_usuario, requiere_token

@app.route('/usuario/<int:id_usuario>/factura',methods=['POST'])
@requiere_token
@recurso_usuario
def crear_factura(id_usuario,id_cliente=1):
    datos = request.get_json()
    datos["id_usuario"]=id_usuario
    datos["id_cliente"]=id_cliente
    try:
        nuevaFactura= Facturas.crear_factura(datos)
        return jsonify(nuevaFactura),201
    except Exception as e:
        return jsonify({"message":e.args[0]}),400