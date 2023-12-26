import datetime
from main import mysql, DBError

class Facturas():
    schema={
        "id_cliente": int,
        "descuento" : int,
    }

    def __init__(self, row):
        self._id_factura = row[0]
        self._id_cliente = row[1]
        self._id_usuario = row[2]
        self._hora_fecha = row[3]
        self._cant_productos = row[4]
        self._descuento = row[5]
        self._TOTAL = row[6]

    def to_json(self):
        return {
            "id_factura": self._id_factura,
            "id_usuario": self._id_usuario,
            "id_cliente": self._id_cliente,
            "hora_fecha": self._hora_fecha,
            "cant_productos": self._cant_productos,
            "descuento" : self._descuento,
            "TOTAL" : self._TOTAL
        }
    # Metodo para verificar los datos ingresados
    def verificacion_datos_ingresados(datos):
        if datos == None or type(datos) != dict:
            return False
        for key in Facturas.schema:
            if key not in datos:
                return False
            if type(datos[key]) != Facturas.schema[key]:
                return False
        return True
    #falta sumar los servicios
    def suma_total(id,descuento):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM ventas_productos WHERE id_factura = {0}'.format(id))
        info_dtfacturas=cur.fetchall()
        subtotal=0
        for row in info_dtfacturas:
            subtotal+= row[-1]
        if (subtotal!=0):
            return subtotal-descuento
        raise DBError("no se cargo ninguna venta de producto")
            
    #en esta funcion falta agregar para que  sume los servicios adquiridos    
    def cantidad_comprada(id_factura):
        cur = mysql.connection.cursor()
        cur.execute('SELECT sum(cantidad) FROM ventas_productos WHERE id_factura = {0};'.format(id_factura))
        cantidad = cur.fetchall()
        return cantidad  

    def crear_id():
        #consulto las cuantas facturas existentes hay 
        cur = mysql.connection.cursor()
        cur.execute('SELECT id_factura, COUNT(*) FROM facturas')
        existen_ids=cur.fetchall()
        if cur.rowcount > 0:
            id_factura = existen_ids[0][1] + 1
            return id_factura
        raise DBError('no se obtuvo las id')


    def crear_factura(datos):
        if Facturas.verificacion_datos_ingresados(datos):
            id=Facturas.crear_id()
            datos["cant_productos"] = Facturas.cantidad_comprada(id)
            print("paso1")
            datos["TOTAL"]=Facturas.suma_total(id,datos["descuento"])
            print("paso1")
            datos["hora_fecha"]=datetime.datetime.utcnow()
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO facturas (id_usuario,id_cliente,hora_fecha,cant_productos,descuento,TOTAL) VALUES (%s,%s,%s,%s,%s,%s)',
                        (datos["id_usuario"],datos["id_cliente"],datos["hora_fecha"],datos["cant_productos"],datos["descuento"],datos["TOTAL"]))
            mysql.connection.commit()
            if cur.rowcount > 0:
                #obtengo la ultima factura
                cur.execute('SELECT LAST_INSERT_ID()')
                res = cur.fetchall()
                id = res[0][0]
                return Facturas((id,datos["id_usuario"],datos["id_cliente"], datos["hora_fecha"],datos["cant_productos"], datos["descuento"], datos["TOTAL"])).to_json()
            raise DBError("Error al crear la factura")
        raise TypeError("Error al crear nueva factura - verifique los datos")

    def ver_facturas(id_usuario):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM facturas WHERE id_usuario= {0}'.format(id_usuario))
        datos = cur.fetchall()
        lista_facturas=[]
        for row in datos:
            factura=Facturas(row).to_json()
            lista_facturas.append(factura)
        return lista_facturas
        