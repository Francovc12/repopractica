from main import app, mysql
from flask import request, jsonify
from models.detalle_factura import Detalle

@app.route('/usuario/factura/detalle', methods=['POST'])
def crear_dtproducto():
    datos = request.get_json()
    #datos["id_factura"]= id
    try:
        nuevo_dtProducto = Detalle.crear_detalleFactura(datos)
        return jsonify(nuevo_dtProducto),200
    except Exception as e:
        return jsonify({"message":e.args[0]}),400
    