from conexionBD import conexion, cursor 

class ClienteBD:
    """
    Clase para gestionar los Clientes (CRUD).
    Maneja apellidos separados en BD pero unidos para la vista.
    """

    @staticmethod
    def insertar(id_usuario, nombre, pat, mat, telefono, direccion, correo, edad):
        try:
            sql = """
                INSERT INTO clientes 
                (id_usuario_registro, nombre, apellido_paterno, apellido_materno, telefono, direccion, correo, edad) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (id_usuario, nombre, pat, mat, telefono, direccion, correo, edad)
            
            cursor.execute(sql, val)
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error Inseting Client: {e}")
            return False

    @staticmethod
    def consultar(id_usuario, rol):
        try:
            # CONCAT_WS une el nombre y apellidos con espacios para mostrarlos juntos en la tabla
            sql = """
                SELECT 
                    c.id_cliente, 
                    c.id_usuario_registro, 
                    CONCAT_WS(' ', c.nombre, c.apellido_paterno, c.apellido_materno), 
                    c.telefono, 
                    c.direccion, 
                    c.correo, 
                    c.edad, 
                    c.nombre, 
                    c.apellido_paterno, 
                    c.apellido_materno, 
                    u.username
                FROM clientes c 
                INNER JOIN usuarios u ON c.id_usuario_registro = u.id_usuario
            """
            
            # Si no es admin, filtramos para ver solo sus propios clientes
            if rol != 'admin' and rol != 1:
                sql += " WHERE c.id_usuario_registro = %s"
                cursor.execute(sql, (id_usuario,))
            else:
                sql+="ORDER BY c.id_cliente ASC"
                cursor.execute(sql)
                
            return cursor.fetchall()
        except Exception as e:
            print(f"Error Consulting Clients: {e}")
            return []

    @staticmethod
    def actualizar(id_cliente, nombre, pat, mat, telefono, direccion, correo, edad):
        try:
            sql = """
                UPDATE clientes 
                SET nombre=%s, apellido_paterno=%s, apellido_materno=%s, 
                    telefono=%s, direccion=%s, correo=%s, edad=%s 
                WHERE id_cliente=%s
            """
            val = (nombre, pat, mat, telefono, direccion, correo, edad, id_cliente)
            
            cursor.execute(sql, val)
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error Updating Client: {e}")
            return False

    @staticmethod
    def eliminar(id_cliente):
        try:
            sql = "DELETE FROM clientes WHERE id_cliente = %s"
            cursor.execute(sql, (id_cliente,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error Deketing Client: {e}")
            return False