from main import app, mysql
from flask import request, jsonify
from models.ventas_productos import VentasProducto
from utils import requiere_token, recurso_usuario

@app.route('/usuario/<int:id_usuario>/factura/venta-producto', methods=['POST'])
@requiere_token
@recurso_usuario
def crear_dtproducto(id_usuario):
    datos = request.get_json()
    #datos["id_factura"]= id
    try:
        nuevo_dtProducto = VentasProducto.crear_ventas_producto(datos)
        return jsonify(nuevo_dtProducto),200
    except Exception as e:
        return jsonify({"message":e.args[0]}),400
    