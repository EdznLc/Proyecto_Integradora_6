import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# ==========================================================================
# 1. AJUSTE DE RUTAS
# ==========================================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ==========================================================================
# 2. IMPORTACIONES
# ==========================================================================
try:
    from controller.funciones import Funciones
except ImportError as e:
    print("Error de importación crítico. Asegúrate de ejecutar esto desde la carpeta raíz o src.")
    raise e

class TestFunciones(unittest.TestCase):

    # ==========================================
    # TEST: Validaciones de Registro de Usuario
    # ==========================================
    
    @patch('tkinter.messagebox.showwarning')
    def test_guardar_usuario_admin_sin_password(self, mock_warning):
        """Prueba que falle si no hay contraseña"""
        window = MagicMock()
        modal = MagicMock()
        
        Funciones.guardar_usuario_admin(
            window, 
            "usuario_test", 
            "test@mail.com", 
            "", # Password vacío
            "admin", 
            modal
        )
        mock_warning.assert_called_with("Atención", "Necesita ingresar una contraseña.")

    @patch('tkinter.messagebox.showwarning')
    def test_guardar_usuario_admin_password_corta(self, mock_warning):
        """Prueba que falle si la contraseña es muy corta"""
        window = MagicMock()
        modal = MagicMock()
        
        Funciones.guardar_usuario_admin(
            window, 
            "usuario_test", 
            "test@mail.com", 
            "123", # Password corto
            "admin", 
            modal
        )
        mock_warning.assert_called_with("Atención", "La contraseña es muy corta, debe tener más de 8 caracteres.")


    @patch('model.usuarioBD.UsuarioBD.registrar')
    @patch('tkinter.messagebox.showinfo')
    def test_guardar_usuario_admin_exito(self, mock_info, mock_registrar):
        """Prueba un registro exitoso simulando la BD"""
        # Simulamos que la BD devuelve True
        mock_registrar.return_value = True 
        
        window = MagicMock()
        modal = MagicMock()

        Funciones.guardar_usuario_admin(
            window, "UserOK", "ok@mail.com", "password123", "admin", modal
        )

        # Verificamos que se llamó a la BD con los datos correctos (es_admin=1)
        mock_registrar.assert_called_with("UserOK", "ok@mail.com", "password123", 1)
        # Verificamos que se cerró la ventana modal
        modal.destroy.assert_called()

    # ==========================================
    # TEST: Validaciones de Clientes
    # ==========================================

    @patch('tkinter.messagebox.showwarning')
    def test_guardar_cliente_edad_invalida(self, mock_warning):
        """Prueba validación de edad > 100"""
        Funciones.guardar_o_editar_cliente(
            parent=None, tree=None, id_cliente=None, usuario_actual=[1],
            nombre="Juan", pat="Perez", mat="Lopez", telefono="1234567890",
            direccion="Calle 1", correo="juan@mail.com", 
            edad=150, # Edad inválida
            modal=MagicMock()
        )
        mock_warning.assert_called_with("Atencion", "La Edad debe de estar en un rango entre 0 y 100 años.")

    @patch('model.clienteBD.ClienteBD.insertar')
    @patch('tkinter.messagebox.showinfo')
    def test_guardar_cliente_nuevo_exito(self, mock_info, mock_insertar):
        """Prueba insertar cliente exitosamente"""
        mock_insertar.return_value = True
        modal = MagicMock()
        tree = MagicMock()
        usuario_actual = [99] # ID usuario ficticio

        Funciones.guardar_o_editar_cliente(
            parent=None, tree=tree, id_cliente=None, usuario_actual=usuario_actual,
            nombre="Ana", pat="Gomez", mat="Ruiz", telefono="5555555555",
            direccion="Av. Siempre Viva", correo="ana@test.com", edad=25,
            modal=modal
        )

        mock_insertar.assert_called_with(99, "Ana", "Gomez", "Ruiz", "5555555555", "Av. Siempre Viva", "ana@test.com", 25)
        mock_info.assert_called_with("Éxito", "Cliente registrado.")

    # ==========================================
    # TEST: Validaciones de Ventas
    # ==========================================

    @patch('tkinter.messagebox.showwarning')
    def test_guardar_venta_monto_excesivo(self, mock_warning):
        """Prueba validación de monto máximo"""
        Funciones.guardar_o_editar_venta(
            window=None, tree=None, usuario=[], id_venta=None,
            cliente_str="1 - Juan", 
            monto=15000, # Monto excesivo
            prendas=2, pago_txt="Efectivo", modal=MagicMock()
        )
        mock_warning.assert_called_with("Atención", "Monto fuera de rango (Max: 10,000)")

    @patch('model.ventaBD.VentaBD.consultar_ventas') 
    @patch('model.ventaBD.VentaBD.registrar_venta')
    @patch('tkinter.messagebox.showinfo')
    def test_guardar_venta_conversion_datos(self, mock_info, mock_registrar, mock_consultar):
        """Prueba que el string del cliente 'ID - Nombre' se separa correctamente"""
        
        # 1. Configuramos los simuladores
        mock_registrar.return_value = True
        mock_consultar.return_value = [] # La tabla se recargará vacía (sin error)
        
        modal = MagicMock()
        usuario = [5, "Juan", "Perez", "X", 1, "admin"] 
        
        # Simulamos los inputs de la vista
        cliente_str = "10 - Pedro Paramo" 
        pago_txt = "Tarjeta" 
        
        Funciones.guardar_o_editar_venta(
            window=None, tree=MagicMock(), usuario=usuario, id_venta=None,
            cliente_str=cliente_str, monto=500, prendas=3, pago_txt=pago_txt, modal=modal
        )

        # Verificamos que a la BD llegó el ID 10 y el pago 2
        mock_registrar.assert_called_with(5, "10", 500.0, 3, 2)

if __name__ == '__main__':
    unittest.main()