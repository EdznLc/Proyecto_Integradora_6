import mysql.connector

try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="bd_ventaropa" 
    )
    cursor = conexion.cursor(buffered=True)
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    conexion = None
    cursor = None