from flask import Flask , request ,jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import jwt
import datetime

#inicio una instancia de flask
app = Flask(__name__)

CORS(app)
#configuro MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = None
app.config['MYSQL_DB'] = 'db_api_proyecto'

app.config['SECRET_KEY'] = 'app_123'#importante para usar jwt
mysql = MySQL(app)
 


@app.route('/login', methods =['POST'])
def login():
    auth = request.authorization
    print (auth)
    """control: existen valores para la autenticacion"""
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Complete los campos"}), 401

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario WHERE username = %s AND password = %s;',(auth.username,auth.password))
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

    
if __name__ == '__main__':
    app.run(debug=True, port = 5000)