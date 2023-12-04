from main import app, mysql
from flask import request, jsonify
from models.ventas_productos import VentasProducto
from utils import requiere_token, recurso_usuario

@app.route('/usuario/<int:id_usuario>/factura/ventaproducto', methods=['POST'])
@requiere_token
@recurso_usuario
def crear_venta_producto(id_usuario):
    datos = request.get_json()
    try:
        nuevo_dtProducto = VentasProducto.crear_ventas_producto(datos)
        return jsonify(nuevo_dtProducto),200
    except Exception as e:
        return jsonify({"message":e.args[0]}),400
    
@app.route('/usuario/<int:id_usuario>/factura/Rankingventaproducto', methods=['GET'])
@requiere_token
@recurso_usuario
def Ranking_ventasProductos(id_usuario):
    try:
        lista_ranking = VentasProducto.Ranking_ventas_productos()
        return lista_ranking, 200
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400
    