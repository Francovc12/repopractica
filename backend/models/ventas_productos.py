import datetime
from main import app,mysql,DBError
from flask import jsonify
from models.productos import Producto
from models.facturas import Facturas

class VentasProducto():
    schema:{
        "id_producto":int,
        "cantidad":int,
    }

    def __init__(self, row):
        self._id_ventas_productos= row[0]
        self._id_factura = row[1]
        self._id_producto = row[2]
        self._cantidad = row[3]
        self._precio = row[4]
        self._subtotal = row[5]

    def to_json(self):
        return {
            "id_ventas_productos":self._id_ventas_productos,
            "id_factura":self._id_factura,
            "id_producto":self._id_producto,
            "cantidad":self._cantidad,
            "precio":self._precio,
            "subtotal":self._subtotal
        }
    def verificacion_datos_ingresados(datos):
        if datos == None or type(datos) != dict:
            return False
        for key in VentasProducto.schema:
            if key not in datos:
                return False
            if type(datos[key]) != VentasProducto.schema[key]:
                return False
        return True
    
    def cargar_detalleProducto(id):
        info_producto = Producto.producto_por_id(id)
        return info_producto["precio"]
    #metodo para obtener un id nuevo con el cual se generara una nueva factura
    def obtener_id():
        id = Facturas.crear_id()
        return id
    #metodo para restar la cantidad pedida del stock
    def guardar_stock(id_producto, cantidad):
        info_producto = Producto.producto_por_id(id_producto)
        restar_al_stock = info_producto['stock'] - cantidad
        return restar_al_stock
    
    def consulta_cantidad(id_factura):
        cur = mysql.connection.cursor()
        cur.execute('SELECT sum(cantidad) FROM ventas_productos WHERE id_factura = %s;',(id_factura))
        cantidad = cur.fetchall()

        return cantidad   
        
    def crear_ventas_producto(datos):
        if VentasProducto.verificacion_datos_ingresados(datos):
            #realizo un llamdo a funciones para cargar datos anteriores
            datos["precio"]=VentasProducto.cargar_detalleProducto(datos["id_producto"])
            datos["id_factura"]=VentasProducto.obtener_id()
            datos["subtotal"]=datos["cantidad"]*datos["precio"]
            stock_restante = VentasProducto.guardar_stock(datos['id_producto'],datos['cantidad'])
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO ventas_productos (id_factura,id_producto,cantidad,precio,subtotal) VALUES (%s,%s,%s,%s,%s)',
                        (datos["id_factura"], datos["id_producto"],datos["cantidad"],datos["precio"],datos["subtotal"]))
            mysql.connection.commit()
            if cur.rowcount > 0:
                print(cur)
                cur.execute('SELECT LAST_INSERT_ID()')
                res = cur.fetchall()
                id = res[0][0]
                Producto.actualizar_stock(datos['id_producto'], stock_restante)
                return VentasProducto((id,datos["id_factura"], datos["id_producto"],datos["cantidad"],datos["precio"],datos["subtotal"])).to_json()
            raise DBError("Error al crear venta de un producto")
        raise TypeError("Error al crear Ventas_Producto - verifique los datos")
    
    def Ranking_ventas_productos():
        cur = mysql.connection.cursor()
        cur.execute('SELECT id_producto, SUM(cantidad) FROM ventas_productos GROUP BY id_producto;')
        datos = cur.fetchall()
        lista_productos=[]
        if cur.rowcount > 0 : 
            for row in datos:
                datos = Producto.producto_por_id(row[0])
                ranking_productos={
                    "producto": datos['nombre_producto'],
                    "cantidad" : row[1],
                }
                lista_productos.append(ranking_productos)
            return jsonify(lista_productos)
        return jsonify({"message": "No hay ventas productos cargados"})
