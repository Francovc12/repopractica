from main import mysql,DBError
from flask import jsonify

class Producto():
    schema={
        "id_usuario": int,
        "nombre_producto": str,
        "marca": str,
        "precio": float,
        "categoria" : str,
        "descripcion": str,
        "stock": int
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

    def to_json(self):
        return {  
            "id_producto": self._id_producto,
            "id_usuario": self._id_usuario,
            "nombre_producto": self._nombre_producto,
            "marca": self._marca,
            "precio": self._precio,
            "categoria" : self._categoria,
            "descripcion": self._descripcion,
            "stock": self._stock
        }
    """Metodo para verificar la si un producto existe en la base de datos ingresando el nombre y el id_usuario"""
    def producto_existe(nombre, id_usuario):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos WHERE nombre_producto = %s AND id_usuario = %s', (nombre, id_usuario))
        cur.fetchall()
        return cur.rowcount > 0
    """Metodo para consultar en la base de datos un producto de acuierdo a su id_producto"""
    def producto_por_id(id_producto):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos WHERE id_producto = {0}'.format(id_producto))
        data = cur.fetchall()
        if cur.rowcount > 0:
            return Producto(data[0]).to_json()
        raise DBError("Error no se pudo obtener producto por id")
    """Metodo para consultar todos los productos de un usuario"""
    def obtener_productos(id_usuario):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos WHERE id_usuario = {0}'.format(id_usuario))
        data = cur.fetchall()
        lista_productos=[]
        if cur.rowcount > 0:            
            for row in data:
                objProducto = Producto(row)
                lista_productos.append(objProducto.to_json())
            return lista_productos
        return jsonify("No hay Productos cargados")
    """Metodo para realizar la creacion de un producto nuevo de acuerdo a los datos enviados desde el frontend"""
    def crear_producto(data):
        if Producto.producto_existe(data["nombre_producto"], data["id_usuario"]):
            raise DBError("Error producto existe")
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (id_usuario, nombre_producto, marca ,precio, categoria, descripcion, stock) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                            (data["id_usuario"],data["nombre_producto"],data["marca"],data["precio"],data["categoria"],data["descripcion"],data["stock"]))
        mysql.connection.commit()
        if cur.rowcount > 0:
            #obtengo el producto añadido
            cur.execute('SELECT LAST_INSERT_ID()')
            res = cur.fetchall()
            id = res[0][0]
            return Producto((id,data["id_usuario"],data["nombre_producto"],data["marca"],data["precio"],data["categoria"],data["descripcion"],data["stock"])).to_json()
        raise DBError("error al crear el producto")
    """Metodo para actualizar los datos de un Producto de acuerdo a su id"""
    def actualizar_producto(id_producto,datos):
        cur=mysql.connection.cursor()
        cur.execute('UPDATE productos SET nombre_producto = %s, marca = %s, precio = %s, categoria = %s, descripcion = %s, stock = %s, vendidos_producto = %s WHERE id_producto = %s',
                    (datos["nombre_producto"],datos["marca"],datos["precio"],datos["categoria"],datos["descripcion"],datos["stock"], datos['vendidos_producto'],id_producto))
        mysql.connection.commit()
        if cur.rowcount > 0 :
            return Producto.producto_por_id(id_producto)
        raise DBError("error al actualizar producto")
    """Metodo para eliminar un producto de acuerdo a su id_producto"""
    def eliminar_producto(id_usuario,id_producto):
        producto = Producto.producto_por_id(id_producto)
        #verifico si elk producto existe antes de eliminarlo
        if Producto.producto_existe(producto["nombre_producto"], id_usuario):
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM productos WHERE id_producto = {0}'.format(id_producto))
            mysql.connection.commit()
            return {"message": "Se elimino un producto"}
        raise DBError("Error no existe el producto seleccionado")