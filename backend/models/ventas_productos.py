import datetime
from main import app,mysql,DBError
from models.productos import Producto
from models.facturas import Facturas

class VentasProducto():
    schema:{
        "id_ventas_productos":int,
        "id_factura":int,
        "id_producto":int,
        "cantidad":int,
        "precio":int,
        "subtotal":int
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
    
    def cargar_detalleProducto(id):
        info_producto = Producto.producto_por_id(id)
        """aqui obtendre un diccionario
        {  
            "id_producto": self._id_producto,
            "id_usuario": self._id_usuario,
            "nombre_producto": self._nombre_producto,
            "marca": self._marca,
            "precio": self._precio,
            "categoria" : self._categoria,
            "descripcion": self._descripcion,
            "stock": self._stock,
            "vendidos": self._vendidos
        }"""
        
        return info_producto["precio"]
    
    def obtener_id():
        id = Facturas.crear_id()
        return id
    
    def crear_ventas_producto(datos):
        #realizo un llamdo a funciones para cargar datos anteriores
        datos["precio"]=VentasProducto.cargar_detalleProducto(datos["id_producto"])
        print(datos["precio"])
        datos["id_factura"]=VentasProducto.obtener_id()
        datos["subtotal"]=datos["cantidad"]*datos["precio"]
        print(datos["subtotal"])
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO ventas_productos (id_factura,id_producto,cantidad,precio,subtotal) VALUES (%s,%s,%s,%s,%s)',
                    (datos["id_factura"], datos["id_producto"],datos["cantidad"],datos["precio"],datos["subtotal"]))
        mysql.connection.commit()
        if cur.rowcount > 0:
            print(cur)
            cur.execute('SELECT LAST_INSERT_ID()')
            res = cur.fetchall()
            id = res[0][0]
            return VentasProducto((id,datos["id_factura"], datos["id_producto"],datos["cantidad"],datos["precio"],datos["subtotal"])).to_json()
        raise DBError("Error al crear venta de un producto")
    
    def consulta_cantidad(id_factura):
        cur = mysql.connection.cursor()
        cur.execute('SELECT sum(cantidad) FROM ventas_productos WHERE id_factura = %s;',(id_factura))
        cantidad = cur.fetchall()

        return cantidad