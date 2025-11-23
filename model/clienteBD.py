# Importamos explícitamente lo que necesitamos, no todo (*)
from model.conexionBD import conexion, cursor 
import traceback # Útil para ver detalles profundos del error si es necesario

class ClienteBD:
    """
    Clase encargada de todas las operaciones CRUD (Crear, Leer, Actualizar, Borrar)
    para la tabla 'clientes'.
    """

    @staticmethod
    def insertar(id_usuario, nombre, telefono, direccion, correo, edad):
        try:
            sql = """
                INSERT INTO clientes (id_usuario, nombre, telefono, direccion, correo, edad) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            val = (id_usuario, nombre, telefono, direccion, correo, edad)
            
            cursor.execute(sql, val)
            conexion.commit()
            return True
            
        except Exception as e:
            #Imprimimos el error para saber qué pasó
            print(f"Error al insertar cliente: {e}")
            return False

    @staticmethod
    def consultar(id_usuario, rol):
        try:
            # Limpiamos resultados pendientes del cursor si los hubiera
            try: cursor.fetchall() 
            except: pass 

            if rol == 'admin':
                # Admin: Ve clientes + nombre del vendedor (JOIN)
                sql = """
                    SELECT c.id, c.id_usuario, c.nombre, c.telefono, c.direccion, c.correo, c.edad, u.nombre 
                    FROM clientes c 
                    INNER JOIN usuarios u ON c.id_usuario = u.id
                """
                cursor.execute(sql)
            else:
                # Usuario Normal: Solo ve sus propios registros
                sql = "SELECT * FROM clientes WHERE id_usuario = %s"
                cursor.execute(sql, (id_usuario,))
            
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Error al consultar clientes: {e}")
            return []

    @staticmethod
    def actualizar(id_cliente, nombre, telefono, direccion, correo, edad):
        try:
            sql = """
                UPDATE clientes 
                SET nombre=%s, telefono=%s, direccion=%s, correo=%s, edad=%s 
                WHERE id=%s
            """
            val = (nombre, telefono, direccion, correo, edad, id_cliente)
            
            cursor.execute(sql, val)
            conexion.commit()
            
            # Verificamos si realmente se actualizó alguna fila
            if cursor.rowcount > 0:
                return True
            else:
                print("No se encontró el cliente o los datos eran idénticos.")
                return False
                
        except Exception as e:
            print(f"Error al actualizar cliente: {e}")
            return False

    @staticmethod
    def eliminar(id_cliente):
        try:
            sql = "DELETE FROM clientes WHERE id = %s"
            cursor.execute(sql, (id_cliente,))
            conexion.commit()
            return True
            
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")
            return False