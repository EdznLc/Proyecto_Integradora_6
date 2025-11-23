import hashlib
# Importamos explícitamente la conexión y el cursor
from model.conexionBD import conexion, cursor

class UsuarioBD:
    """
    Clase encargada de la autenticación y gestión de usuarios.
    Utiliza SHA-256 para el hash de contraseñas (Nivel básico de seguridad).
    """

    @staticmethod
    def login(correo, password):
        try:
            # 1. Encriptamos la contraseña recibida para compararla con la BD
            pass_encriptada = hashlib.sha256(password.encode()).hexdigest()
            
            # 2. Buscamos usuario que coincida en correo Y contraseña
            sql = "SELECT * FROM usuarios WHERE correo = %s AND password = %s"
            cursor.execute(sql, (correo, pass_encriptada))
            
            usuario = cursor.fetchone()
            
            # usuario será una tupla con los datos (id, nombre, ..., rol) o None si no existe
            return usuario
            
        except Exception as e:
            print(f"Error crítico en Login: {e}")
            return None

    @staticmethod
    def registrar(nombre, apellidos, correo, password, rol="ususario"):
        try:
            # 1. Encriptamos la contraseña antes de guardarla
            pass_encriptada = hashlib.sha256(password.encode()).hexdigest()
            
            # 2. Definimos la consulta. Asignamos 'usuario' como rol predeterminado.
            sql = """
                INSERT INTO usuarios (nombre, apellidos, correo, password, rol) 
                VALUES (%s, %s, %s, %s, %s)
            """
            val = (nombre, apellidos, correo, pass_encriptada, rol)
            
            cursor.execute(sql, val)
            conexion.commit() # Confirmar cambios
            return True
            
        except Exception as e:
            # Si ocurre un error (ej. correo duplicado), deshacemos cualquier cambio pendiente
            conexion.rollback()
            print(f"Error al registrar usuario: {e}")
            return False