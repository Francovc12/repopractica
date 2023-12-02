from main import app,mysql
from models.clientes import Cliente
from flask import jsonify, request
import jwt
import datetime

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
    #si exite o no devuelvo un mensaje
    if not row:
        return jsonify({"message": "Usuario y/o Contraseña invalidos"}), 401    
    token = jwt.encode({
    "id": row[0],
    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes = 100)
    },app.config['SECRET_KEY'])
    return jsonify({"token": token, "id": row[0],"nombre_completo":row[3]}),200  