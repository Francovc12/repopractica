import datetime
from main import app, mysql, DBError
from models.ventas_productos import VentasProducto

class Facturas():
    schema:{
        "id_factura": int,
        "id_usuario": int,
        "id_cliente": int,
        "hora_fecha": datetime,
        "descuento" : int,
    }

    def __init__(self, row):
        self._id_factura = row[0]
        self._id_usuario = row[1]
        self._id_cliente = row[2]
        self._hora_fecha = row[3]
        self._cant_productos: row[4]
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
        id=Facturas.crear_id()
        datos["cant_productos"] = Facturas.cantidad_comprada(id)
        datos["TOTAL"]=Facturas.suma_total(id,datos["descuento"])
        datos["hora_fecha"]=datetime.datetime.utcnow()
        print (datos)
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
    

    def cantidad_comprada(id_factura):
        cant_productos = VentasProducto.consulta_cantidad(id_factura)
        return cant_productos