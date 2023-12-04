from main import mysql,DBError
from flask import jsonify

class Servicios():
    schema={
        "id_usuario": int,
        "nombre_servicio": str,
        "precio": float,
        "descripcion": str
    }

    def __init__(self,row):
        self._id_servicio = row[0]
        self._id_usuario = row[1]
        self._nombre_servicio = row[2]
        self._precio = row[3]
        self._descripcion = row[4]

    def to_json(self):
        return {  
            "id_servicio": self._id_servicio,
            "id_usuario": self._id_usuario,
            "nombre_servicio": self._nombre_servicio,
            "precio": self._precio,
            "descripcion": self._descripcion
        }
    
    # Metodo para verificar si un servicio ya existe
    def servicio_existe(nombre, id_usuario):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM servicios WHERE nombre_servicio = %s AND id_usuario = %s', (nombre, id_usuario))
        cur.fetchall()
        return cur.rowcount > 0
    
    # Metodo para identificar un servicio por su id
    def servicio_por_id(id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM servicios WHERE id_servicio = {0}'.format(id))
        data = cur.fetchone()
        if cur.rowcount > 0:
            return Servicios(data[0]).to_json()
        raise DBError("Error no se pudo obtener servicio por id - no row found")
    
    # Metodo para crear un servicio
    def crear_servicio(data):
        if Servicios.servicio_existe(data["nombre_servicio"], data["id_usuario"]):
            raise DBError("Error producto existe")
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO servicios (id_usuario, nombre_servicio, precio, descripcion) VALUES (%s,%s,%s,%s)',
                                      (data["id_usuario"],data["nombre_servicio"],data["precio"],data["descripcion"]))
        mysql.connection.commit()
        if cur.rowcount > 0:
            #obtengo el id servicio añadido
            cur.execute('SELECT LAST_INSERT_ID()')
            res = cur.fetchall()
            id = res[0][0]
            return Servicios((id,data["id_usuario"],data["nombre_servicio"],data["precio"],data["descripcion"])).to_json()
        raise DBError("error al crear el servicio")
    
    # Metodo para actualizar un servicio
    def actualizar_servicio(id_servicio,datos):
        cur=mysql.connection.cursor()
        cur.execute('UPDATE servicios SET nombre_servicio = %s,precio = %s, descripcion = %s WHERE id_servicio = %s',
                    (datos["nombre_servicio"],datos["precio"],datos["descripcion"],id_servicio))
        mysql.connection.commit()
        if cur.rowcount > 0 :
            return Servicios.servicio_por_id()(id_servicio)
        raise DBError("error al actualizar servicio")
    
    # Metodo para eliminar un servicio
    def eliminar_servicio(id_usuario,id_servicio):
        servicio = Servicios.servicio_por_id(id_servicio)
            
        if Servicios.servicio_existe(servicio["nombre_servicio"], id_usuario):
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM servicios WHERE id_servicio = {0}'.format(id_servicio))
            mysql.connection.commit()
            return {"message": "Se elimino un servicio"}
        raise DBError("error, no existe el servicio seleccionado")
    
    # Metodo para consultar todos los servicios de un usuario
    def obtener_servicios(id_usuario):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM servicios WHERE id_usuario = {0}'.format(id_usuario))
        data = cur.fetchall()
        lista_servicios =[]
        if cur.rowcount > 0:
            for row in data:
                objServicio = Servicios(row)
                lista_servicios.append(objServicio.to_json())
            return lista_servicios
        return jsonify("No hay Servicios cargados")