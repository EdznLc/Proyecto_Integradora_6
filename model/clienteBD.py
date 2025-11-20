from model.conexionBD import *

class ClienteBD:
    @staticmethod
    def insertar(id_usuario, nombre, telefono, direccion, correo, edad):
        try:
            sql = "INSERT INTO clientes (id_usuario, nombre, telefono, direccion, correo, edad) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (id_usuario, nombre, telefono, direccion, correo, edad)
            cursor.execute(sql, val)
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    def consultar(id_usuario, rol):
        try:
            if rol == 'admin':
                # Admin ve los clientes de TODOS (y el nombre del vendedor)
                sql = "SELECT c.*, u.nombre as vendedor FROM clientes c INNER JOIN usuarios u ON c.id_usuario = u.id"
                cursor.execute(sql)
            else:
                # Usuario normal solo ve LOS SUYOS
                sql = "SELECT * FROM clientes WHERE id_usuario = %s"
                cursor.execute(sql, (id_usuario,))
            
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def actualizar(id_cliente, nombre, telefono, direccion, correo, edad):
        try:
            sql = "UPDATE clientes SET nombre=%s, telefono=%s, direccion=%s, correo=%s, edad=%s WHERE id=%s"
            val = (nombre, telefono, direccion, correo, edad, id_cliente)
            cursor.execute(sql, val)
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    def eliminar(id_cliente):
        try:
            cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente,))
            conexion.commit()
            return True
        except:
            return False