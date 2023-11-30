from main import app, mysql
from flask import request, jsonify
import jwt
from functools import wraps

def requiere_token(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        token = None
        id_usuario = None
        
        if 'token-acceso' in request.headers:
            token = request.headers['token-acceso']    
        if not token:
            return jsonify({"message": "Falta token de acceso"}), 401
        
        if 'id-usuario' in request.headers:
            id_usuario = request.headers['id-usuario']
        if not id_usuario:
            return jsonify({"message": "Falta el id_usuario"}), 401
        
        try:
            datos = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print(datos)
            token_id = datos['id']
            
            if int(id_usuario) != int(token_id):
                return jsonify({"message": "Error de id_usuario"}), 401
        except Exception as e:
            return jsonify({"message": str(e)}), 401
        
        return func(*args, **kwargs)
    return decorated

def recurso_usuario(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        id_usuario_ruta = kwargs['id_usuario']
        id_usuario_header = request.headers['id-usuario']
        if int(id_usuario_ruta) != int(id_usuario_header):
            return jsonify({"message":"No tiene permisos para acceder a este recurso"})
        return func(*args, **kwargs)
    return decorated
        