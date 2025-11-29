import hashlib
from conexionBD import conexion, cursor

class UsuarioBD:
    """
    Clase encargada de la autenticación y gestión de usuarios en la base de datos.
    """

    @staticmethod
    def login(credencial, password):
        """Verifica las credenciales del usuario para iniciar sesión."""
        try:
            # 1. Encriptamos la contraseña recibida para compararla
            pass_encriptada = hashlib.sha256(password.encode()).hexdigest()
            
            # 2. Buscamos coincidencia en la BD
            sql = "SELECT * FROM usuarios WHERE (correo = %s OR username = %s) AND password = %s"
            cursor.execute(sql, (credencial, credencial, pass_encriptada))
            
            # Retorna la tupla con datos del usuario o None
            usuario = cursor.fetchone()
            return usuario
            
        except Exception as e:
            print(f"Error crítico en Login: {e}")
            return None

    @staticmethod
    def registrar(username, correo, password, es_admin_num=0):
        """Registra un nuevo usuario en la base de datos."""
        try:
            # 1. Encriptamos la contraseña antes de guardar
            pass_encriptada = hashlib.sha256(password.encode()).hexdigest()
            
            # 2. Insertamos el registro
            sql = """
                INSERT INTO usuarios (username, correo, password, es_admin) 
                VALUES (%s, %s, %s, %s)
            """
            val = (username, correo, pass_encriptada, es_admin_num)
            
            cursor.execute(sql, val)
            conexion.commit() # Guardamos cambios
            return True
            
        except Exception as e:
            conexion.rollback() # Deshacemos si hubo error
            print(f"Error al registrar usuario: {e}")
            return False