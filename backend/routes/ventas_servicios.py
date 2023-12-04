from main import app, mysql
from flask import request, jsonify
from models.ventas_servicios import VentasServicios
from utils import requiere_token, recurso_usuario

@app.route('/usuario/<int:id_usuario>/factura/ventaservicio', methods=['POST'])
@requiere_token
@recurso_usuario
def crear_ventas_servicio(id_usuario):
    datos = request.get_json()

    try:
        nuevo_venta_servicio = VentasServicios.crear_ventas_servicio(datos)
        return jsonify(nuevo_venta_servicio),200
    except Exception as e:
        return jsonify({"message":e.args[0]}),400
    

@app.route('/usuario/<int:id_usuario>/factura/rankingventaservicio', methods=['GET'])
@requiere_token
@recurso_usuario
def ranking_ventas_servicios(id_usuario):
    try:
        lista_ranking = VentasServicios.ranking_ventas_servicios()
        return lista_ranking, 200
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400