from main import mysql,DBError
from flask import jsonify

class Producto():
    schema={
        #"id_producto": int,
        "id_usuario": int,
        "nombre_producto": str,
        "marca": str,
        "precio": float,
        "categoria" : str,
        "descripcion": str,
        "stock": int,
        #"vendidos":int
    }

    def __init__(self,row):
        self._id_producto = row[0]
        self._id_usuario = row[1]
        self._nombre_producto = row[2]
        self._marca = row[3]
        self._precio = row[4]
        self._categoria = row[5]
        self._descripcion = row[6]
        self._stock = row[7]
        self._vendidos = 0

    def to_json(self):
        return {  
            "id_producto": self._id_producto,
            "id_usuario": self._id_usuario,
            "nombre_producto": self._nombre_producto,
            "marca": self._marca,
            "precio": self._precio,
            "categoria" : self._categoria,
            "descripcion": self._descripcion,
            "stock": self._stock,
            "vendidos": self._vendidos
        }
    
    def producto_existe(nombre, id_usuario):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM producto WHERE nombre_producto = %s AND id_usuario = %s', (nombre, id_usuario))
        cur.fetchall()
        return cur.rowcount > 0
    
    def producto_por_id(id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM producto WHERE id_producto = {0}'.format(id))
        data = cur.fetchall()
        if cur.rowcount > 0:
            return Producto(data[0]).to_json()
        raise DBError("Error no se pudo obtener producto por id - no row found")
    
    def crear_producto(data):
        if Producto.producto_existe(data["nombre_producto"], data["id_usuario"]):
            raise DBError("Error producto existe")
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO producto (id_usuario, nombre_producto, marca ,precio, categoria, descripcion, stock) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                                      (data["id_usuario"],data["nombre_producto"],data["marca"],data["precio"],data["categoria"],data["descripcion"],data["stock"]))
        mysql.connection.commit()
        if cur.rowcount > 0:
            #obtengo el producto añadido
            cur.execute('SELECT LAST_INSERT_ID()')
            res = cur.fetchall()
            id = res[0][0]
            return Producto((id,data["id_usuario"],data["nombre_producto"],data["marca"],data["precio"],data["categoria"],data["descripcion"],data["stock"])).to_json()
        raise DBError("error al crear el producto")
    
    def actualizar_producto(id_producto,datos):
        cur=mysql.connection.cursor()
        cur.execute('UPDATE producto SET nombre_producto = %s, marca = %s, precio = %s, categoria = %s, descripcion = %s, stock = %s, vendidos_producto = %s WHERE id_producto = %s',
                    (datos["nombre_producto"],datos["marca"],datos["precio"],datos["categoria"],datos["descripcion"],datos["stock"], datos['vendidos_producto'],id_producto))
        mysql.connection.commit()
        if cur.rowcount > 0 :
            return Producto.producto_por_id(id_producto)
        raise DBError("error al actualizar producto")
    