from main import mysql,DBError
from flask import jsonify
from models.facturas import Facturas
import datetime

class Usuario():
    schema={
        "nombre_usuario": str,
        "contrasenia": str,
        "nombre": str,
        "apellido": str,
        "telefono": int,
        "email": str
    }

    def __init__(self, row):
        self._id_usuario = row[0]
        self._nombre_usuario = row[1]
        self._contrasenia = row[2]
        self._nombre = row[3]
        self._apellido = row[4]
        self._telefono = row[5]
        self._email = row[6]

    def to_json(self):
        return {
            "id_usuario": self._id_usuario,
            "nombre_usuario": self._nombre_usuario,
            "contrasenia" : self._contrasenia,
            "nombre" : self._nombre,
            "apellido" : self._apellido,
            "telefono": self._telefono,
            "email": self._email
        }
    # Metodo para verificar los datos iungresados sean los correctos
    def verificacion_datos_ingresados(datos):
        if datos == None or type(datos) != dict:
            return False
        for key in Usuario.schema:
            if key not in datos:
                return False
            if type(datos[key]) != Usuario.schema[key]:
                return False
        return True
    # Metodo para verificar si el usuario existe en el caso de que el email ya estuviera registrado antes
    def usuario_existe(email):
        print(type(email))
        cur = mysql.connection.cursor()
        cur.execute("""SELECT email FROM usuario""")
        row = cur.fetchall()
        print(row)
        for i in row:
            if i[0] == email:
                return True
        return False    
        
    # Metodo para crear un usuario nuevo
    def crear_usuario(datos):
        if Usuario.verificacion_datos_ingresados(datos):
            if Usuario.usuario_existe(datos["email"]):
                raise DBError('El usuario existe email ya registrado')
            else:
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO usuario (nombre_usuario, contrasenia, nombre, apellido, telefono, email) VALUES (%s,%s,%s,%s,%s,%s)',
                            (datos['nombre_usuario'], datos['contrasenia'], datos['nombre'], datos['apellido'], datos['telefono'], datos['email']))
                mysql.connection.commit()

                if cur.rowcount > 0:
                    cur.execute('SELECT LAST_INSERT_ID()')
                    res = cur.fetchall()
                    id = res[0][0]
                    return Usuario((id,datos['nombre_usuario'], datos['contrasenia'], datos['nombre'], datos['apellido'], datos['telefono'], datos['email'])).to_json()
                raise DBError('no se pudo guardar nuevo usuario')
        raise TypeError('datos ingresados incorrectos')
    # Metodo para ver una factura registrada segun su id
    def verFactura(id_factura):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM facturas WHERE id_factura = {0};'.format(id_factura))
        datos = cur.fetchone()

        if cur.rowcount > 0:
            return Facturas(datos).to_json()
        raise DBError('No se encontro la factura')
    # Metodo para ver facturas relacionadas al cliente
    def verFacturasCliente(id_cliente):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM facturas WHERE id_cliente = {0};'.format(id_cliente))
        datos = cur.fetchall()

        facturas_cliente = []

        if cur.rowcount > 0:
            for row in datos:
                objFactura = Facturas(row)
                facturas_cliente.append(objFactura.to_json())
            return facturas_cliente
        raise DBError('No se encontraron facturas')
    #metodo para ver las facturas registradas por un usuario
    def historialVentas(id_usuario):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM facturas WHERE id_usuario = {0}'.format(id_usuario))
        datos = cur.fetchall()

        lista_ventas = []

        if cur.rowcount > 0:            
            for row in datos:
                objFactura = Facturas(row).to_json()
                lista_ventas.append(objFactura)
            return lista_ventas
        
        raise DBError("El usuario no registra ventas")
    
    # Metodo para ver el ranking de ventas segun el cliente
    def rankingVentasClientes(id_usuario):
        cur = mysql.connection.cursor()
        cur.execute('SELECT id_cliente, cant_productos FROM facturas GROUP BY id_cliente;')
        datos = cur.fetchall()

        ranking_clientes = []
        numero=0
        for row in datos:
            numero+=1
            cliente = row[0]
            cantidad = row[1]
            ranking = {"lugar":numero,"cliente": cliente, "cantidad": cantidad}
            ranking_clientes.append(ranking)

        return (ranking_clientes)

        