import mysql.connector

try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="bd_ventaropa" # Cambiado a tu base de datos
    )
    cursor = conexion.cursor(buffered=True)
except:
    print("Error al conectar a la base de datos")
    conexion = None
    cursor = None