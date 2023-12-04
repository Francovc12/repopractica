from main import app,mysql
from models.clientes import Cliente
from flask import jsonify, request
import jwt
import datetime
from models.usuarios import *
from utils import requiere_token, recurso_usuario


# Ruta para logear

@app.route('/login', methods =['POST'])
def login():
    auth = request.authorization
    print (auth)
    """control: existen valores para la autenticacion"""
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Complete los campos"}), 401

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario WHERE nombre_usuario = %s AND contrasenia = %s;',(auth.username,auth.password))
    row = cur.fetchone()
    print(row)
    #si existe o no devuelvo un mensaje
    if not row:
        return jsonify({"message": "Usuario y/o Contraseña invalidos"}), 401    
    token = jwt.encode({
    "id": row[0],
    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes = 100)
    },app.config['SECRET_KEY'])
    return jsonify({"token": token, "id": row[0],"nombre_completo":row[3]}),200  


# Ruta para ver una factura en especifico

@app.route('/usuarios/<int:id_usuario>/facturas/<int:id_factura>', methods = ['GET'])
@requiere_token
@recurso_usuario
def verFactura(id_usuario, id_factura):
    try:
        factura = Usuario.verFactura(id_factura)
        return jsonify(factura), 200
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400
    

# Ruta para ver todas las facturas de un cliente

@app.route('/usuarios/<int:id_usuario>/facturas/clientes/<int:id_cliente>', methods = ['GET'])
@requiere_token
@recurso_usuario
def verFacturasCliente(id_usuario, id_cliente):
    try:
        lista_facturas = Usuario.verFacturasCliente(id_cliente)
        return jsonify(lista_facturas), 200
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400


# Ruta para ver el historial de ventas de un usuario

@app.route('/usuarios/<int:id_usuario>/historialventas', methods =['GET'])
@requiere_token
@recurso_usuario
def historialVentas(id_usuario):
    try:
        historial_ventas = Usuario.historialVentas(id_usuario)
        return jsonify(historial_ventas), 200
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400
    

# Ruta para ver el ranking de ventas de sus clientes

@app.route('/usuarios/<int:id_usuario>/rankingventasclientes', methods =['GET'])
@requiere_token
@recurso_usuario
def rankingVentasClientes(id_usuario):
    try:
        ranking_clientes = Usuario.rankingVentasClientes(id_usuario)
        return jsonify(ranking_clientes), 200
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400