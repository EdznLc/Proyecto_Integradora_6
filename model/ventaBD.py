from model.conexionBD import conexion, cursor

class VentaBD:
    """
    Clase para gestionar el historial de ventas.
    Incluye lógica para filtrar reportes por fecha y rol de usuario.
    """

    # ==========================================
    # 1. REGISTRAR (CREATE)
    # ==========================================
    @staticmethod
    def registrar_venta(id_usuario, id_cliente, monto, num_prendas, metodo_pago):
        try:
            # Usamos NOW() de SQL para que la fecha sea exacta del servidor
            sql = """
                INSERT INTO ventas (id_usuario, id_cliente, monto, num_prendas, metodo_pago, fecha) 
                VALUES (%s, %s, %s, %s, %s, NOW())
            """
            val = (id_usuario, id_cliente, monto, num_prendas, metodo_pago)
            
            cursor.execute(sql, val)
            conexion.commit()
            return True
            
        except Exception as e:
            conexion.rollback() # Importante: Deshacer cambios si falla
            print(f"Error al registrar venta: {e}")
            return False

    # ==========================================
    # 2. CONSULTAR (READ - Con Filtros Dinámicos)
    # ==========================================
    @staticmethod
    def consultar_ventas(id_usuario, rol, fecha_filtro=None):
        try:
            # Consulta Base: Traemos datos de la venta + Nombre Cliente + Nombre Vendedor
            # Usamos alias (v, c, u) para escribir menos y ser más claros
            base_sql = """
                SELECT 
                    v.id,           -- 0
                    c.nombre,       -- 1 (Nombre Cliente)
                    v.monto,        -- 2
                    v.num_prendas,  -- 3
                    v.metodo_pago,  -- 4
                    v.fecha,        -- 5
                    c.id,           -- 6 (ID Cliente oculto)
                    u.nombre        -- 7 (Nombre Vendedor)
                FROM ventas v
                INNER JOIN clientes c ON v.id_cliente = c.id
                INNER JOIN usuarios u ON v.id_usuario = u.id
            """
            
            filtros = []
            params = []

            # --- Lógica de Filtros ---
            
            # 1. Si NO es admin, solo ve sus propias ventas
            if rol != 'admin':
                filtros.append("v.id_usuario = %s")
                params.append(id_usuario)

            # 2. Si hay texto en el buscador de fecha (YYYY-MM)
            if fecha_filtro:
                # Usamos LIKE para buscar coincidencias de texto en la fecha
                filtros.append("v.fecha LIKE %s")
                params.append(f"{fecha_filtro}%")

            # --- Armado final de la consulta ---
            if filtros:
                # Unimos los filtros con " AND "
                # Ejemplo: "WHERE v.id_usuario = 1 AND v.fecha LIKE '2023%'"
                base_sql += " WHERE " + " AND ".join(filtros)
            
            # Ordenamos por ID descendente (las más nuevas primero)
            base_sql += " ORDER BY v.id DESC"

            cursor.execute(base_sql, tuple(params))
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Error al consultar historial de ventas: {e}")
            return []

    # ==========================================
    # 3. ACTUALIZAR (UPDATE)
    # ==========================================
    @staticmethod
    def actualizar_venta(id_venta, id_cliente, monto, num_prendas, metodo_pago):
        try:
            sql = """
                UPDATE ventas 
                SET id_cliente=%s, monto=%s, num_prendas=%s, metodo_pago=%s 
                WHERE id=%s
            """
            val = (id_cliente, monto, num_prendas, metodo_pago, id_venta)
            
            cursor.execute(sql, val)
            conexion.commit()
            return True
            
        except Exception as e:
            conexion.rollback()
            print(f"Error al actualizar venta: {e}")
            return False

    # ==========================================
    # 4. ELIMINAR / ANULAR (DELETE)
    # ==========================================
    @staticmethod
    def eliminar_venta(id_venta):
        try:
            sql = "DELETE FROM ventas WHERE id = %s"
            cursor.execute(sql, (id_venta,))
            
            conexion.commit()
            return True
            
        except Exception as e:
            conexion.rollback()
            print(f"Error al eliminar venta: {e}")
            return False