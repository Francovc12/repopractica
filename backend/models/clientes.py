from main import mysql,DBError
from flask import jsonify

class Cliente():
    schema={
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
        self._activo = row[5]
        self._email = row[6]

    def to_json(self):
        return {
            "id_cliente": self._id_cliente,
            "id_usuario": self._id_usuario,
            "nombre": self._nombre,
            "apellido" : self._apellido,
            "dni" : self._dni,
            "activo": self._activo,
            "email": self._email
        }
    # Metodo para verificar los datos ingresados
    def verificacion_datos_ingresados(datos):
        if datos == None or type(datos) != dict:
            return False
        for key in Cliente.schema:
            if key not in datos:
                return False
            if type(datos[key]) != Cliente.schema[key]:
                return False
        return True
    
    # Esta funcion verifica si un cliente ya existe con su dni
    def cliente_existe(dni):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cliente WHERE dni = {0}'.format(dni))
        #cur.execute('SELECT * FROM cliente WHERE nombre = %s AND apellido = %s AND id_cliente = %s', (nombre, apellido, id_cliente))
        row = cur.fetchone()
        if cur.rowcount > 0:
            return True
        return False

    # Esta funcion crea un cliente
    def crear_cliente(datos):
        if Cliente.verificacion_datos_ingresados(datos):
            # check if client already exists
            #if Cliente.cliente_existe(datos["nombre"], datos["apellido"], datos["id_cliente"]):
            if Cliente.cliente_existe(datos['dni']):
                raise DBError("Error creando el cliente - el cliente ya existe")
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO cliente (id_usuario, nombre, apellido, dni, email, activo) VALUES (%s, %s, %s, %s, %s, %s)', 
                        (datos["id_usuario"], datos["nombre"], datos["apellido"], datos["dni"], datos["email"], datos["activo"]))
            mysql.connection.commit()
            if cur.rowcount > 0:
                # agarra el id de la ultima fila insertada
                cur.execute('SELECT LAST_INSERT_ID()')
                res = cur.fetchall()
                id = res[0][0]
                return Cliente((id, datos["id_usuario"], datos["nombre"], datos["apellido"], datos["dni"], datos["email"], datos["activo"])).to_json()
            raise DBError("Error creando el cliente - fila no insertada")
        raise TypeError("Error creando el cliente - esquema incorrecto")
    # Metodo para obtener los clientes de un usuario
    def clientes_por_usuario(id_usuario):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cliente WHERE id_usuario = {0} AND activo = 1'.format(id_usuario))
        datos = cur.fetchall()

        lista_clientes=[]

        for row in datos:
            objCliente = Cliente(row)
            lista_clientes.append(objCliente.to_json())

        return (lista_clientes)
    # Metodo para obtner un cliente por id
    def clientes_por_id(id_cliente):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cliente WHERE id_cliente = {0}'.format(id_cliente))
        data = cur.fetchall()
        if cur.rowcount > 0:
            return Cliente(data[0]).to_json()
        raise DBError("Error no se pudo encontrar el cliente por id - no row found")
    # Metodo para modificar un cliente 
    def modificar_cliente(id_usuario,id_cliente,datos):
        if Cliente.verificacion_datos_ingresados(datos):
            cur=mysql.connection.cursor()
            cur.execute('UPDATE cliente SET nombre = %s, apellido = %s, dni = %s, email = %s WHERE id_usuario= %s AND id_cliente= %s',
                        (datos["nombre"],datos["apellido"],datos["dni"],datos["email"],id_usuario, id_cliente))
            mysql.connection.commit()
            if cur.rowcount > 0 :
                return Cliente.clientes_por_id(id_cliente)
            raise DBError("Error al modificar cliente")
        raise TypeError("Error en los datos ingresados")
    # MEtodo para eliminar un cliente implementando un borrado logico
    def eliminar_cliente(id_usuario,id_cliente):
        cur=mysql.connection.cursor()
        cur.execute('UPDATE cliente SET activo = False WHERE id_usuario = %s AND id_cliente = %s;', (id_usuario, id_cliente))
        mysql.connection.commit()
        if cur.rowcount > 0 :
            return "Cliente eliminado"
        raise DBError("Error al eliminar cliente")