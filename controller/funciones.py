from tkinter import messagebox
import re
from model import usuarioBD, clienteBD, ventaBD

class Funciones:
    """
    CONTROLADOR PRINCIPAL
    Maneja la lógica de negocio, validaciones y comunicación con la BD.
    """

    # --- CAMBIO 1: MAPAS EN INGLÉS PARA COINCIDIR CON LA INTERFAZ ---
    MAPA_PAGO_BD = {"Cash": 1, "Credit Card": 2, "Transfer": 3}
    MAPA_PAGO_TXT = {1: "Cash", 2: "Credit Card", 3: "Transfer"}

    # ==========================================
    # HERRAMIENTAS DE VALIDACIÓN
    # ==========================================
    @staticmethod
    def es_nombre_valido(texto):
        """Revisa que solo tenga letras y espacios"""
        patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
        return re.match(patron, texto) is not None

    @staticmethod
    def es_correo_valido(texto):
        """Revisa formato básico de correo"""
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(patron, texto) is not None

    # ==========================================
    # 1. USUARIOS
    # ==========================================
    @staticmethod
    def ingresar(window, correo, password):
        if not correo or not password:
            # CAMBIO: Mensaje en inglés
            messagebox.showwarning("Attention", "Please, fill in all the fields.")
            return

        usuario = usuarioBD.UsuarioBD.login(correo, password)
        
        if usuario:
            from view import interfaces 
            es_admin_num = usuario[4] 
            rol_str = "admin" if es_admin_num == 1 else "user"
            
            usuario_con_rol = usuario + (rol_str,)
            
            # CAMBIO: Mensaje en inglés
            messagebox.showinfo("Welcome", f"Access Granted.\n\nUser: {usuario[1]}\nRole: {rol_str.upper()}")
            interfaces.Vista.menu_principal(window, usuario_con_rol) 
        else:
            # CAMBIO: Mensaje en inglés
            messagebox.showerror("Access Error", "Incorrect Email or Password.")

    @staticmethod
    def guardar_usuario_admin(window, username, correo, password, rol_texto, modal):
        if not username or not correo or not password:
            messagebox.showwarning("Attention", "All fields are required.")
            return

        if not Funciones.es_correo_valido(correo):
            messagebox.showwarning("Invalid Email", "The email format is invalid (example@mail.com).")
            return

        elif len(password) not in range(8, 21):
            if len(password) < 8:
                messagebox.showwarning("Attention", "Password is too short. It must be at least 8 characters.")
                return
            else:
                messagebox.showwarning("Attention", "Password is too long. It must be at most 20 characters.")
                return

        if usuarioBD.UsuarioBD.existe_correo(correo):
            messagebox.showerror("Duplicate Email", f"The email '{correo}' is already registered.")
            return
            
        es_admin_num = 1 if rol_texto == "Admin" else 0
        
        if usuarioBD.UsuarioBD.registrar(username, correo, password, es_admin_num):
            messagebox.showinfo("Success", "User created successfully.")
            modal.destroy()
        else:
            messagebox.showerror("Error", "Could not register user.")

    # ==========================================
    # 2. HERRAMIENTAS TABLAS
    # ==========================================
    @staticmethod
    def ordenar_columna(tree, col, reverse):
        """Ordena y limpia flechas"""
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0].replace("$", "").replace(",", "")), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        for column in tree["columns"]:
            titulo_limpio = tree.heading(column)["text"].replace(" ▲", "").replace(" ▼", "")
            tree.heading(column, text=titulo_limpio)

        flecha = " ▼" if reverse else " ▲"
        tree.heading(col, text=tree.heading(col)["text"] + flecha, command=lambda: Funciones.ordenar_columna(tree, col, not reverse))

    # ==========================================
    # 3. CLIENTES
    # ==========================================
    @staticmethod
    def llenar_tabla_clientes(tree, usuario, filtro_texto=""):
        for item in tree.get_children(): tree.delete(item)
        id_usuario = usuario[0]; rol = usuario[5] 
        rol_bd = 'admin' if rol == 'admin' else 'user'
        
        datos = clienteBD.ClienteBD.consultar(id_usuario, rol_bd)
        filtro = filtro_texto.lower() if filtro_texto else ""
        
        for row in datos:
            if filtro and filtro not in str(row[2]).lower(): continue 
            tree.insert("", "end", text=row[0], values=(row[0], row[7], row[8], row[9], row[3], row[4], row[5], row[6]))

    @staticmethod
    def guardar_o_editar_cliente(parent, tree, id_cliente, usuario_actual, nombre, pat, mat, telefono, direccion, correo, edad, modal, callback=None):
        if not nombre:
            messagebox.showwarning("Attention", "Name is obligatory.")
            return
        elif not pat:
            messagebox.showwarning("Attention", "The first last name is obligatory.")
            return
        if not Funciones.es_nombre_valido(nombre) or not Funciones.es_nombre_valido(pat):
            messagebox.showwarning("Invalid Text", "Names cannot contain numbers.")
            return
        elif not telefono or len(telefono) < 10:
            messagebox.showwarning("Attention", "The phone is obligatory and must consist of 10 digits.")
            return
        elif not direccion:
            messagebox.showwarning("Attention", "The address is obligatory.")
            return
        elif not correo:
            messagebox.showwarning("Attention", "The email is obligatory")
            return
        elif not edad:
            messagebox.showwarning("Attention", "The age is obligatory")
            return
        elif edad not in range(0, 100):
            messagebox.showwarning("Attention", "The age must be in the range of 1-100.")
            return
        
        try: 
            edad_int = int(edad) if edad else 0
        except ValueError: 
            messagebox.showwarning("Error", "Age must be a valid number.")
            return

        if id_cliente is None:
            exito = clienteBD.ClienteBD.insertar(usuario_actual[0], nombre, pat, mat, telefono, direccion, correo, edad_int)
            msg = "Client registered successfully."
        else:
            exito = clienteBD.ClienteBD.actualizar(id_cliente, nombre, pat, mat, telefono, direccion, correo, edad_int)
            msg = "Client updated successfully."

        if exito:
            messagebox.showinfo("Success", msg)
            modal.destroy()
            if tree: Funciones.llenar_tabla_clientes(tree, usuario_actual)
            if callback: callback()
        else:
            messagebox.showerror("Error", "Maybe the email is already registered, try again.")

    @staticmethod
    def borrar_cliente_tabla(window, usuario, id_cliente, tree):
        if not id_cliente: return
        # CAMBIO: Mensaje en inglés
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this client?\nThis action cannot be undone."):
            if clienteBD.ClienteBD.eliminar(id_cliente):
                messagebox.showinfo("Success", "Client deleted.")
                Funciones.llenar_tabla_clientes(tree, usuario)
            else:
                messagebox.showerror("Error", "Could not delete client (Check for existing sales).")

    # ==========================================
    # 4. VENTAS
    # ==========================================
    @staticmethod
    def llenar_tabla_ventas(tree, usuario, fecha_filtro=None):
        for item in tree.get_children(): tree.delete(item)
        id_usu = usuario[0]
        rol = usuario[5]
        rol_bd = 'admin' if rol == 'admin' else 'user'
        
        datos = ventaBD.VentaBD.consultar_ventas(id_usu, rol_bd, fecha_filtro)
        
        for row in datos:
            # Traducir pago (1 -> Cash)
            txt_pago = Funciones.MAPA_PAGO_TXT.get(row[4], "Unknown")
            tree.insert("", "end", text=row[0], values=(row[0], row[7], row[1], f"${row[2]}", row[3], txt_pago, row[5], row[6]))

    @staticmethod
    def guardar_o_editar_venta(window, tree, usuario, id_venta, cli_str, monto, prendas, pago_txt, modal):
        if not cli_str:
            messagebox.showwarning("Attention", "The client name is obligatory.")
            return
        elif monto <= 0 or monto >= 10000: 
            messagebox.showwarning("Atención", "Total out of range (Max: 10,000)")
            return
        elif prendas not in range(1, 100):
            messagebox.showwarning("Atención", "Amount out of range (1-100).")
            return
    
        try:
            id_cli = cli_str.split(" - ")[0]
            # Convertir Texto a ID (Cash -> 1)
            id_pago = Funciones.MAPA_PAGO_BD.get(pago_txt, 1)
            
            if id_venta is None:
                exito = ventaBD.VentaBD.registrar_venta(usuario[0], id_cli, float(monto), int(prendas), id_pago)
                msg = "Sale registered successfully."
            else:
                exito = ventaBD.VentaBD.actualizar_venta(id_venta, id_cli, float(monto), int(prendas), id_pago)
                msg = "Sale updated successfully."
            
            if exito:
                messagebox.showinfo("Success", msg)
                modal.destroy()
                Funciones.llenar_tabla_ventas(tree, usuario)
            else:
                messagebox.showerror("Error", "Database Error.")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid numbers.")
        
    @staticmethod
    def borrar_venta_tabla(window, usuario, id_venta, tree):
        if not id_venta: return
        if messagebox.askyesno("Confirm Void", "Do you want to void this sale?"):
            if ventaBD.VentaBD.eliminar_venta(id_venta):
                messagebox.showinfo("Success", "Sale voided.")
                Funciones.llenar_tabla_ventas(tree, usuario)
            else:
                messagebox.showerror("Error", "Could not void sale.")