from main import mysql,DBError
from flask import jsonify

class Cliente():
    schema={
        "id_cliente": int,
        "id_usuario": int,
        "nombre": str,
        "apellido": str,
        "dni": int,
        "email": str,
        "activo" : bool
    }

    def __init__(self, row):
        self._id_cliente = row[0]
        self._id_usuario = row[1]
        self._nombre = row[2]
        self._apellido = row[3]
        self._dni = row[4]
        self._email = row[5]
        self._activo = row[6]

    def to_json(self):
        return {
            "id_cliente": self._id_cliente,
            "id_usuario": self._id_usuario,
            "nombre": self._nombre,
            "apellido" : self._apellido,
            "dni" : self._dni,
            "email": self._email,
            "activo": self._activo,
        }
    
    # Esta funcion verifica si un cliente ya existe con su nombre, apellido e id
    def cliente_existe(nombre, apellido, id_cliente):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cliente WHERE nombre = %s AND apellido = %s AND id_cliente = %s', (nombre, apellido, id_cliente))
        cur.fetchall()
        return cur.rowcount > 0

    # Esta funcion crea un cliente
    def crear_cliente(datos):
        if Cliente.check_data_schema(datos):
            # check if client already exists
            if Cliente.cliente_existe(datos["nombre"], datos["apellido"], datos["id_cliente"]):
                raise DBError("Error creando el cliente - el cliente ya existe")
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO cliente (id_usuario, nombre, apellido, dni, email, activo) VALUES (%s, %s, %s, %s, %s, %s)', 
                        datos["id_usuario"], datos["nombre"], datos["apellido"], datos["dni"], datos["email"], datos["activo"])
            mysql.connection.commit()
            if cur.rowcount > 0:
                # agarra el id de la ultima fila insertada
                cur.execute('SELECT LAST_INSERT_ID()')
                res = cur.fetchall()
                id = res[0][0]
                return Cliente((id, datos["id_usuario"], datos["nombre"], datos["apellido"], datos["dni"], datos["email"], datos["activo"])).to_json()
            raise DBError("Error creando el cliente - fila no insertada")
        raise TypeError("Error creando el cliente - esquema incorrecto")

    def clientes_por_id(id_usuario):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cliente WHERE id_usuario = %s', (id_usuario))
        data = cur.fetchall()
        if cur.rowcount > 0:
            return Cliente(data[0]).to_json()
        raise DBError("Error no se pudo encontrar el cliente por id - no row found")
    
    def modificar_cliente(id_usuario,id_cliente,datos):
        cur=mysql.connection.cursor()
        cur.execute('UPDATE cliente SET nombre = %s, apellido = %s, dni = %s, email = %s, activo = %s WHERE id_usuario= %s AND id_cliente= %s',
                    (datos["nombre"],datos["apellido"],datos["dni"],datos["email"],datos["activo"],id_usuario, id_cliente))
        mysql.connection.commit()
        if cur.rowcount > 0 :
            return Cliente.clientes_por_id(id_usuario)
        raise DBError("Error al modificar cliente")
    
    def eliminar_cliente(id_usuario,id_cliente):
        cur=mysql.connection.cursor()
        cur.execute('UPDATE cliente SET activo = false, WHERE id_usuario= %s AND id_cliente= %s', (id_usuario, id_cliente))
        mysql.connection.commit()
        if cur.rowcount > 0 :
            return "Cliente eliminado"
        raise DBError("Error al eliminar cliente")