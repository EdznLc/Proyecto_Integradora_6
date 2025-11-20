from model.conexionBD import *

class VentaBD:
    @staticmethod
    def registrar_venta(id_usuario, id_cliente, monto, num_prendas, metodo_pago):
        try:
            sql = "INSERT INTO ventas (id_usuario, id_cliente, monto, num_prendas, metodo_pago, fecha) VALUES (%s, %s, %s, %s, %s, NOW())"
            val = (id_usuario, id_cliente, monto, num_prendas, metodo_pago)
            cursor.execute(sql, val)
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    def consultar_ventas(id_usuario, rol, fecha_filtro=None):
        try:
            # Consulta base uniendo tablas para ver nombres
            base_sql = """
                SELECT v.id, c.nombre, v.monto, v.num_prendas, v.metodo_pago, v.fecha, c.id, u.nombre 
                FROM ventas v
                INNER JOIN clientes c ON v.id_cliente = c.id
                INNER JOIN usuarios u ON v.id_usuario = u.id
            """
            
            filtros = []
            params = []

            # 1. Filtro de Rol
            if rol != 'admin':
                filtros.append("v.id_usuario = %s")
                params.append(id_usuario)

            # 2. Filtro de Fecha (Opcional)
            if fecha_filtro:
                filtros.append("v.fecha LIKE %s")
                params.append(f"{fecha_filtro}%")

            # Aplicar filtros si existen
            if filtros:
                base_sql += " WHERE " + " AND ".join(filtros)
            
            base_sql += " ORDER BY v.id DESC"

            cursor.execute(base_sql, tuple(params))
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def actualizar_venta(id_venta, id_cliente, monto, num_prendas, metodo_pago):
        try:
            sql = "UPDATE ventas SET id_cliente=%s, monto=%s, num_prendas=%s, metodo_pago=%s WHERE id=%s"
            val = (id_cliente, monto, num_prendas, metodo_pago, id_venta)
            cursor.execute(sql, val)
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    def eliminar_venta(id_venta):
        try:
            cursor.execute("DELETE FROM ventas WHERE id = %s", (id_venta,))
            conexion.commit()
            return True
        except:
            return False