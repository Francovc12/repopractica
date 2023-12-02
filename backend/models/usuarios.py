from main import mysql,DBError
from flask import jsonify
from facturas import *

class Usuario():
    schema={
        "id_usuario": int,
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
    
    def verFactura(id_factura):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM facturas WHERE id_factura = %s;', (id_factura))
        datos = cur.fetchone()

        if cur.rowcount > 0:
            return Facturas((id,datos["id_cliente"], datos["hora_fecha"], datos["descuento"], datos["TOTAL"])).to_json()
        raise DBError('No se encontro la factura')


    def historialVentas(self):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM facturas WHERE id_usuario = %s', (self._id_usuario))
        datos = cur.fetchall()

        lista_ventas=[]

        if cur.rowcount > 0:            
            for row in datos:
                objFactura = Facturas(row)
                lista_ventas.append(objFactura.to_json())
            return lista_ventas
        
        return jsonify("El usuario no registra ventas")
    

    # def rankingVentasClientes(self):
