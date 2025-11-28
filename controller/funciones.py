from tkinter import messagebox
from model import usuarioBD, clienteBD, ventaBD

class Funciones:
    """
    CONTROLADOR PRINCIPAL
    Gestiona la lógica de negocio y comunica la Vista con el Modelo.
    """

    # Diccionarios para traducir el método de pago (BD <-> Vista)
    MAPA_PAGO_BD = {"Efectivo": 1, "Tarjeta": 2, "Transferencia": 3}
    MAPA_PAGO_TXT = {1: "Efectivo", 2: "Tarjeta", 3: "Transferencia"}

    # ==========================================
    # 1. USUARIOS
    # ==========================================
    @staticmethod
    def ingresar(window, correo, password):
        if not correo or not password:
            messagebox.showwarning("Atención", "Por favor, llene todos los campos.")
            return

        usuario = usuarioBD.UsuarioBD.login(correo, password)
        
        if usuario:
            from view import interfaces 
            # Determinar rol basado en el número (1=Admin, 0=User)
            es_admin_num = usuario[4]
            rol_str = "admin" if es_admin_num == 1 else "user"
            
            # Mensaje de bienvenida
            messagebox.showinfo("Bienvenido", f"Hola {usuario[1]}")
            
            # Pasamos el usuario + el rol en texto a la siguiente ventana
            interfaces.Vista.menu_principal(window, usuario + (rol_str,)) 
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")

    @staticmethod
    def guardar_usuario_admin(window, username, correo, password, rol_texto, modal):
        if not username or not correo or not password:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return
            
        es_admin = 1 if rol_texto == "admin" else 0
        
        if usuarioBD.UsuarioBD.registrar(username, correo, password, es_admin):
            messagebox.showinfo("Éxito", "Usuario creado correctamente.")
            modal.destroy()
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario.\nVerifique que el correo no esté duplicado.")

    # ==========================================
    # 2. HERRAMIENTAS
    # ==========================================
    @staticmethod
    def ordenar_columna(tree, col, reverse):
        """Ordena las columnas de la tabla numéricamente o alfabéticamente"""
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        
        try:
            # Intenta ordenar como número (quitando signos de dinero)
            l.sort(key=lambda t: float(t[0].replace("$", "").replace(",", "")), reverse=reverse)
        except ValueError:
            # Si falla, ordena como texto normal
            l.sort(reverse=reverse)

        # Reordenar items
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        # Limpiar flechas anteriores de todas las columnas
        for column in tree["columns"]:
            titulo_limpio = tree.heading(column)["text"].replace(" ▲", "").replace(" ▼", "")
            tree.heading(column, text=titulo_limpio)

        # Agregar flecha a la columna actual
        flecha = " ▼" if reverse else " ▲"
        titulo_nuevo = tree.heading(col)["text"] + flecha
        tree.heading(col, text=titulo_nuevo, command=lambda: Funciones.ordenar_columna(tree, col, not reverse))

    # ==========================================
    # 3. CLIENTES
    # ==========================================
    @staticmethod
    def llenar_tabla_clientes(tree, usuario, filtro_texto=""):
        """Consulta los clientes y rellena el Treeview"""
        for item in tree.get_children(): 
            tree.delete(item)
        
        id_usuario = usuario[0]
        # El rol texto lo pusimos en la última posición en el login
        rol = usuario[-1] 
        
        datos = clienteBD.ClienteBD.consultar(id_usuario, rol)
        filtro = filtro_texto.lower() if filtro_texto else ""
        
        for row in datos:
            # row[2] es Nombre Completo (concatenado por SQL, lo usamos SOLO para filtrar)
            nombre_completo_busqueda = str(row[2]).lower()
            
            # Filtro de búsqueda
            if filtro and filtro not in nombre_completo_busqueda:
                continue 
            
            # DATOS REALES QUE VIENEN DEL MODELO (Indices ajustados al SQL de clienteBD):
            # 0:id, 3:tel, 4:dir, 5:cor, 6:edad, 7:NOM, 8:PAT, 9:MAT
            
            # Insertamos en orden visual: ID, Nombre, Paterno, Materno, Tel, Dir, Correo, Edad
            # OJO: row[7], row[8], row[9] son los campos separados que trae tu consulta SQL
            tree.insert("", "end", text=row[0], values=(
                row[0],   # ID
                row[7],   # Nombre
                row[8],   # Paterno
                row[9],   # Materno
                row[3],   # Teléfono
                row[4],   # Dirección
                row[5],   # Correo
                row[6]    # Edad
            ))

    @staticmethod
    def guardar_o_editar_cliente(parent, tree, id_cliente, usuario_actual, nombre, pat, mat, telefono: int, direccion, correo, edad: int, modal, callback=None):
        # Validaciones
        if not nombre:
            messagebox.showwarning("Atención", "El nombre es obligatorio.")
            return
        elif not pat:
            messagebox.showwarning("Atencion", "El apellido paterno es obligatorio.")
            return
        elif not telefono or len(telefono) < 10:
            messagebox.showwarning("Atencion", "El telefono es obligatorio y debe de componerse de 10 caracteres.")
            return
        elif not direccion:
            messagebox.showwarning("Atencion", "La direccion es obligatoria.")
            return
        elif not correo:
            messagebox.showwarning("Atencion", "El correo es obligatorio.")
            return
        elif not edad:
            messagebox.showwarning("Atencion", "La edad es obligatoria.")
            return
        elif edad not in range(0, 100):
            messagebox.showwarning("Atencion", "La Edad debe de estar en un rango entre 0 y 100 años.")
            return
        
        try: 
            edad_int = int(edad) if edad else 0
        except ValueError:
            messagebox.showwarning("Error", "La edad debe ser un número.") 
            return

        # Guardar o Actualizar
        if id_cliente is None:
            exito = clienteBD.ClienteBD.insertar(usuario_actual[0], nombre, pat, mat, telefono, direccion, correo, edad_int)
            msg = "Cliente registrado."
        else:
            exito = clienteBD.ClienteBD.actualizar(id_cliente, nombre, pat, mat, telefono, direccion, correo, edad_int)
            msg = "Cliente actualizado."
        
        if exito:
            messagebox.showinfo("Éxito", msg)
            modal.destroy()
            
            # Actualizar la tabla si existe (pantalla clientes)
            if tree: 
                Funciones.llenar_tabla_clientes(tree, usuario_actual)
            # Ejecutar callback si existe (pantalla ventas)
            if callback: 
                callback()
        else:
            messagebox.showerror("Error", "Ocurrió un error en la base de datos.")

    @staticmethod
    def borrar_cliente_tabla(window, usuario, id_cliente, tree):
        if not id_cliente: return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            if clienteBD.ClienteBD.eliminar(id_cliente):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                Funciones.llenar_tabla_clientes(tree, usuario)
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente.")

    # ==========================================
    # 4. VENTAS
    # ==========================================
    @staticmethod
    def llenar_tabla_ventas(tree, usuario, fecha_filtro=None):
        """Consulta las ventas y rellena el Treeview"""
        for item in tree.get_children(): 
            tree.delete(item)
        
        id_usuario = usuario[0]
        rol = usuario[5]
        
        datos = ventaBD.VentaBD.consultar_ventas(id_usuario, rol, fecha_filtro)
        
        for row in datos:
            # Traducir el número de pago a texto (1 -> Efectivo)
            texto_pago = Funciones.MAPA_PAGO_TXT.get(row[4], "Otro")
            
            # Formatear dinero
            monto_fmt = f"${row[2]}"
            
            # Insertar datos. IMPORTANTE: row[6] es el ID oculto del cliente
            tree.insert("", "end", text=row[0], values=(row[0], row[7], row[1], monto_fmt, row[3], texto_pago, row[5], row[6]))

    @staticmethod
    def guardar_o_editar_venta(window, tree, usuario, id_venta, cliente_str, monto, prendas, pago_txt, modal):
        if not cliente_str or not monto: 
            messagebox.showwarning("Atención", "Faltan datos para registrar la venta.")
            return
            
        try:
            # Obtener ID del cliente del string "ID - Nombre"
            id_cliente = cliente_str.split(" - ")[0]
            # Obtener ID del pago (Texto -> Número)
            id_pago = Funciones.MAPA_PAGO_BD.get(pago_txt, 1)
            
            if id_venta is None:
                exito = ventaBD.VentaBD.registrar_venta(usuario[0], id_cliente, float(monto), int(prendas), id_pago)
                msg = "Venta registrada exitosamente."
            else:
                exito = ventaBD.VentaBD.actualizar_venta(id_venta, id_cliente, float(monto), int(prendas), id_pago)
                msg = "Venta actualizada correctamente."
            
            if exito:
                messagebox.showinfo("Éxito", msg)
                modal.destroy()
                Funciones.llenar_tabla_ventas(tree, usuario)
            else:
                messagebox.showerror("Error", "Error al guardar en la base de datos.")
                
        except ValueError:
            messagebox.showerror("Error", "El monto y las prendas deben ser números válidos.")

    @staticmethod
    def borrar_venta_tabla(window, usuario, id_venta, tree):
        if not id_venta: return
        
        if messagebox.askyesno("Confirmar", "¿Desea anular esta venta?"):
            if ventaBD.VentaBD.eliminar_venta(id_venta):
                messagebox.showinfo("Éxito", "Venta anulada correctamente.")
                Funciones.llenar_tabla_ventas(tree, usuario)
            else:
                messagebox.showerror("Error", "No se pudo anular la venta.")