import hashlib
from model.conexionBD import *

class UsuarioBD:
    @staticmethod
    def login(correo, password):
        try:
            pass_encriptada = hashlib.sha256(password.encode()).hexdigest()
            # Traemos todo (*) para obtener también el rol
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND password = %s", (correo, pass_encriptada))
            usuario = cursor.fetchone()
            return usuario
        except:
            return None

    @staticmethod
    def registrar(nombre, apellidos, correo, password):
        try:
            pass_encriptada = hashlib.sha256(password.encode()).hexdigest()
            # Por defecto el rol será 'usuario' (definido en la BD)
            sql = "INSERT INTO usuarios (nombre, apellidos, correo, password, rol) VALUES (%s, %s, %s, %s, 'usuario')"
            val = (nombre, apellidos, correo, pass_encriptada)
            cursor.execute(sql, val)
            conexion.commit()
            return True
        except:
            return False