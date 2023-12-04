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

    def verFacturasCliente(id_cliente):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM facturas WHERE id_cliente = %s;', (id_cliente))
        datos = cur.fetchall()

        facturas_cliente = []

        if cur.rowcount > 0:
            for row in datos:
                objFactura = Facturas(row)
                facturas_cliente.append(objFactura.to_json())
            return facturas_cliente
        raise DBError('No se encontraron facturas')

    def historialVentas(id_usuario):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM facturas WHERE id_usuario = %s', (id_usuario))
        datos = cur.fetchall()

        lista_ventas = []

        if cur.rowcount > 0:            
            for row in datos:
                objFactura = Facturas(row)
                lista_ventas.append(objFactura.to_json())
            return lista_ventas
        
        raise DBError("El usuario no registra ventas")
    

    def rankingVentasClientes(id_usuario):
        cur = mysql.connection.cursor()
        cur.execute('SELECT id_cliente, cant_productos FROM facturas GROUP BY id_cliente;')
        datos = cur.fetchall()

        ranking_clientes = []

        for row in datos:
            cliente = row[0]
            cantidad = row[1]
            ranking = {"cliente": cliente, "cantidad": cantidad}
            ranking_clientes.append(ranking)

        return jsonify(ranking_clientes)

        