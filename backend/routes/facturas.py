import datetime
from models.facturas import Facturas
from main import app, mysql
from flask import request, jsonify

@app.route('/usuario/<int:id>/facturas',methods=['POST'])
def crear_factura(id,id_cliente=1):
    datos = request.get_json()
    datos["id_usuario"]=id
    datos["id_cliente"]=id_cliente
    try:
        nuevaFactura= Facturas.crear_factura(datos)
        return jsonify(nuevaFactura),201
    except Exception as e:
        return jsonify({"message":e.args[0]}),400