from conexionBD import conexion, cursor

class VentaBD:
    """
    Clase para gestionar las Ventas.
    """

    @staticmethod
    def registrar_venta(id_usuario, id_cliente, monto, num_prendas, metodo_pago_num):
        try:
            sql = """
                INSERT INTO ventas (id_usuario, id_cliente, metodo_pago, monto, num_prendas, fecha) 
                VALUES (%s, %s, %s, %s, %s, NOW())
            """
            val = (id_usuario, id_cliente, metodo_pago_num, monto, num_prendas)
            
            cursor.execute(sql, val)
            conexion.commit()
            return True
        except Exception as e:
            conexion.rollback()
            print(f"Error Registering Sale: {e}")
            return False

    @staticmethod
    def consultar_ventas(id_usuario, rol, fecha_filtro=None):
        try:
            # Obtenemos datos uniendo tablas para mostrar nombres en lugar de IDs
            base_sql = """
                SELECT 
                    v.id_venta, 
                    CONCAT_WS(' ', c.nombre, c.apellido_paterno, c.apellido_materno), 
                    v.monto, 
                    v.num_prendas, 
                    v.metodo_pago, 
                    v.fecha, 
                    c.id_cliente, 
                    u.username
                FROM ventas v
                INNER JOIN clientes c ON v.id_cliente = c.id_cliente
                INNER JOIN usuarios u ON v.id_usuario = u.id_usuario
            """
            
            filtros = []
            params = []

            # Filtro por Rol (Seguridad)
            if rol != 1 and rol != 'admin':
                filtros.append("v.id_usuario = %s")
                params.append(id_usuario)

            # Filtro por Fecha (Buscador)
            if fecha_filtro:
                filtros.append("v.fecha LIKE %s")
                params.append(f"{fecha_filtro}%")

            if filtros:
                base_sql += " WHERE " + " AND ".join(filtros)
            
            base_sql += " ORDER BY v.id_venta DESC"

            cursor.execute(base_sql, tuple(params))
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Error consulting sale: {e}")
            return []

    @staticmethod
    def actualizar_venta(id_venta, id_cliente, monto, num_prendas, metodo_pago_num):
        try:
            sql = """
                UPDATE ventas 
                SET id_cliente=%s, monto=%s, num_prendas=%s, metodo_pago=%s 
                WHERE id_venta=%s
            """
            val = (id_cliente, monto, num_prendas, metodo_pago_num, id_venta)
            
            cursor.execute(sql, val)
            conexion.commit()
            return True
        except Exception as e:
            conexion.rollback()
            print(f"Error Updating sale: {e}")
            return False

    @staticmethod
    def eliminar_venta(id_venta):
        try:
            cursor.execute("DELETE FROM ventas WHERE id_venta = %s", (id_venta,))
            conexion.commit()
            return True
        except:
            conexion.rollback()
            return False