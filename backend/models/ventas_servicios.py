import datetime
from main import app,mysql,DBError
from models.servicios import Servicios
from models.facturas import Facturas
from flask import jsonify

class VentasServicios():
    schema:{
        "id_ventas_servicios":int,
        "id_factura":int,
        "id_servicio":int,
        "precio":int,
        "subtotal":int
    }

    def __init__(self, row):
        self._id_ventas_servicios= row[0]
        self._id_factura = row[1]
        self._id_servicio = row[2]
        self._precio = row[3]
        self._subtotal = row[4]

    def to_json(self):
        return {
            "id_ventas_servicios":self._id_ventas_servicios,
            "id_factura":self._id_factura,
            "id_servicio":self._id_servicio,
            "precio":self._precio,
            "subtotal":self._subtotal
        }
    
    def cargar_detalleServicio(id):
        info_producto = Servicios.servicio_por_id(id)
        """aqui obtendre un diccionario
        {  
            "id_servicio": self._id_servicio,
            "id_usuario": self._id_usuario,
            "nombre_servicio": self._nombre_servicio,
            "precio": self._precio,
            "descripcion": self._descripcion,
        }"""
        
        return info_producto["precio"]
    
    def obtener_id():
        id = Facturas.crear_id()
        return id
    
    def crear_ventas_servicio(datos):
        #realizo un llamado a funciones para cargar datos anteriores
        datos["precio"]=VentasServicios.cargar_detalleServicio(datos["id_servicio"])
        print(datos["precio"])
        datos["id_factura"]=VentasServicios.obtener_id()
        datos["subtotal"]=datos["cantidad"]*datos["precio"]

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO ventas_servicios (id_factura,id_servicio,cantidad,precio,subtotal) VALUES (%s,%s,%s,%s)',
                    (datos["id_factura"],datos["id_servicio"],datos["cantidad"],datos["precio"],datos["subtotal"]))
        mysql.connection.commit()
        if cur.rowcount > 0:
            print(cur)
            cur.execute('SELECT LAST_INSERT_ID()')
            res = cur.fetchall()
            id = res[0][0]
            return VentasServicios((id,datos["id_factura"], datos["id_servicio"],datos["cantidad"],datos["precio"],datos["subtotal"])).to_json()
        raise DBError("Error al crear venta de un servicio")
    

    def ranking_ventas_servicios():
        cur = mysql.connection.cursor()
        cur.execute('SELECT id_servicio, SUM(cantidad) FROM ventas_servicios GROUP BY id_servicio;')
        datos = cur.fetchall()
        lista_servicios=[]
        if cur.rowcount > 0 : 
            for row in datos:
                datos = Servicios.servicio_por_id(row[0])
                ranking_productos={
                    "servicio": datos['nombre_servicio'],
                    "cantidad" : row[1],
                }
                lista_servicios.append(ranking_productos)
            return jsonify(lista_servicios)
        return jsonify({"message": "No hay ventas servicios cargados"})