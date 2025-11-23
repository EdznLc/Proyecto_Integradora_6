from tkinter import messagebox
# Importamos los modelos de base de datos
from model import usuarioBD, clienteBD, ventaBD

class Funciones:
    """
    CONTROLADOR:
    Esta clase actúa como intermediario. Recibe las acciones de la Vista (botones),
    valida los datos, llama al Modelo (BD) y decide qué respuesta mostrar al usuario.
    """

    # ==========================================
    # 1. GESTIÓN DE USUARIOS (Login y Registro)
    # ==========================================
    
    @staticmethod
    def ingresar(window, correo, password):
        """Valida credenciales e inicia la sesión"""
        if not correo or not password:
            messagebox.showwarning("Atención", "Por favor, llene todos los campos.")
            return

        usuario = usuarioBD.UsuarioBD.login(correo, password)
        
        if usuario:
            # Importación local para evitar 'Circular Import Error' 
            # (Porque vista importa funciones, y funciones importa vista)
            from view import interfaces 
            
            # Asumimos que el rol está en la posición 5 de la tupla usuario
            rol = usuario[5] if len(usuario) > 5 else "user"
            nombre = usuario[1]
            
            messagebox.showinfo("Bienvenido", f"Hola {nombre}, has iniciado como {rol.upper()}.")
            interfaces.Vista.menu_principal(window, usuario) 
        else:
            messagebox.showerror("Error de Acceso", "Correo o contraseña incorrectos.")

    @staticmethod
    def guardar_usuario_admin(window, nombre, apellidos, correo, password, rol, modal):
        """Registra un usuario desde el panel de Admin"""
        if not nombre or not correo or not password:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return
            
        # Llamamos al modelo pasándole el rol seleccionado
        exito = usuarioBD.UsuarioBD.registrar(nombre, apellidos, correo, password, rol)
        
        if exito:
            messagebox.showinfo("Éxito", f"Usuario {rol.upper()} creado correctamente.")
            modal.destroy() # Cerramos solo la ventanita, no el programa
        else:
            messagebox.showerror("Error", "No se pudo registrar (¿Correo duplicado?).")

    # ==========================================
    # 2. HERRAMIENTAS (HELPERS)
    # ==========================================
    
    @staticmethod
    def ordenar_columna(tree, col, reverse):
        """
        Función avanzada para ordenar las tablas al dar clic en la cabecera.
        Detecta si son números (dinero) o texto automáticamente.
        """
        # Obtenemos todos los datos de la columna seleccionada
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        
        try:
            # Intentamos ordenar como número (quitando signos de $)
            l.sort(key=lambda t: float(t[0].replace("$", "").replace(",", "")), reverse=reverse)
        except ValueError:
            # Si falla (es texto), ordenamos alfabéticamente
            l.sort(reverse=reverse)

        # Reordenamos los items en la vista
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        # Actualizamos los flechitas en los títulos (UX)
        for column in tree["columns"]:
            # Limpiamos flechas viejas de otras columnas
            titulo_actual = tree.heading(column)["text"]
            titulo_limpio = titulo_actual.replace(" ▲", "").replace(" ▼", "")
            tree.heading(column, text=titulo_limpio)

        # Ponemos la flecha nueva
        flecha = " ▼" if reverse else " ▲"
        titulo_nuevo = tree.heading(col)["text"] + flecha
        # Configuramos el comando para que el próximo clic invierta el orden (not reverse)
        tree.heading(col, text=titulo_nuevo, command=lambda: Funciones.ordenar_columna(tree, col, not reverse))

    # ==========================================
    # 3. LÓGICA DE CLIENTES
    # ==========================================
    
    @staticmethod
    def llenar_tabla_clientes(tree, usuario, filtro_texto=""):
        """Limpia y rellena el Treeview de clientes"""
        # 1. Limpiar tabla actual
        for item in tree.get_children(): 
            tree.delete(item)
        
        # 2. Obtener datos según rol
        id_usuario = usuario[0]
        rol = usuario[5] if len(usuario) > 5 else "user"
        
        datos = clienteBD.ClienteBD.consultar(id_usuario, rol)
        
        # 3. Normalizar filtro (minusculas para búsqueda insensible a mayúsculas)
        filtro = filtro_texto.lower() if filtro_texto else ""
        
        for row in datos:
            # row estructura: (id, id_usu, nom, tel, dir, cor, edad, vendedor_si_admin)
            nombre_cliente = str(row[2]).lower()
            correo_cliente = str(row[5]).lower()
            
            # Filtro simple en Python (Búsqueda por nombre o correo)
            if filtro and (filtro not in nombre_cliente and filtro not in correo_cliente):
                continue 
            
            # Insertar en tabla
            tree.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    @staticmethod
    def guardar_o_editar_cliente(parent, tree, id_cliente, usuario_actual, nombre, telefono, direccion, correo, edad, modal, callback=None):
        # 1. Validaciones de campos obligatorios
        if not nombre or not telefono:
            messagebox.showwarning("Datos Incompletos", "El nombre y teléfono son obligatorios.")
            return
            
        try:
            # Convertir edad a entero (si viene vacío poner 0)
            edad_int = int(edad) if edad else 0
        except ValueError:
            messagebox.showerror("Error de Formato", "La edad debe ser un número entero.")
            return

        # 2. Lógica de Guardado en BD
        if id_cliente is None:
            # NUEVO
            exito = clienteBD.ClienteBD.insertar(usuario_actual[0], nombre, telefono, direccion, correo, edad_int)
            mensaje = "Cliente registrado correctamente."
        else:
            # EDITAR
            exito = clienteBD.ClienteBD.actualizar(id_cliente, nombre, telefono, direccion, correo, edad_int)
            mensaje = "Cliente actualizado correctamente."

        # 3. Respuesta y Callbacks
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            modal.destroy() # Cerramos la ventana
            
            # --- ACTUALIZACIÓN INTELIGENTE ---
            # Si nos llamaron desde la pantalla de Clientes (tree existe), actualizamos la tabla
            if tree is not None:
                Funciones.llenar_tabla_clientes(tree, usuario_actual)
            
            # Si nos llamaron desde Ventas (callback existe), ejecutamos la recarga del combo
            if callback:
                callback() 
        else:
            messagebox.showerror("Error", "La operación falló en la base de datos.")

    @staticmethod
    def borrar_cliente_tabla(window, usuario, id_cliente, tree):
        """Elimina un cliente seleccionado"""
        if not id_cliente: return # Seguridad
        
        confirmar = messagebox.askyesno("Confirmar Eliminación", 
                                        "¿Está seguro de eliminar este cliente?\nEsta acción no se puede deshacer.")
        if confirmar:
            if clienteBD.ClienteBD.eliminar(id_cliente):
                messagebox.showinfo("Info", "Cliente eliminado.")
                Funciones.llenar_tabla_clientes(tree, usuario)
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente (posiblemente tiene ventas asociadas).")

    # ==========================================
    # 4. LÓGICA DE VENTAS
    # ==========================================
    
    @staticmethod
    def llenar_tabla_ventas(tree, usuario, fecha_filtro=None):
        """Rellena el historial de ventas"""
        for item in tree.get_children(): 
            tree.delete(item)
        
        id_usuario = usuario[0]
        rol = usuario[5] if len(usuario) > 5 else "user"
        
        datos = ventaBD.VentaBD.consultar_ventas(id_usuario, rol, fecha_filtro)
        
        for row in datos:
            # row estructura: (id_venta, nombre_cli, monto, prendas, pago, fecha, id_cli, nombre_vendedor)
            nombre_vendedor = row[7]
            
            # Formatear dinero con signo $
            monto_fmt = f"${row[2]}"
            
            tree.insert("", "end", text=row[0], values=(row[0], nombre_vendedor, row[1], monto_fmt, row[3], row[4], row[5], row[6]))

    @staticmethod
    def guardar_o_editar_venta(window, tree, usuario_actual, id_venta, seleccion_cliente_str, monto, num_prendas, metodo_pago, modal):
        """Procesa el formulario de venta"""
        # Validaciones
        if not seleccion_cliente_str:
            messagebox.showwarning("Atención", "Debe seleccionar un cliente.")
            return
        if not monto:
            messagebox.showwarning("Atención", "Debe ingresar el monto total.")
            return
            
        try:
            # Parsear datos
            # El string viene formato "ID - Nombre". Usamos split para sacar solo el ID.
            if " - " in seleccion_cliente_str:
                id_cliente = seleccion_cliente_str.split(" - ")[0]
            else:
                messagebox.showerror("Error", "Formato de cliente inválido.")
                return

            monto_float = float(monto)
            prendas_int = int(num_prendas)
            
            if id_venta is None:
                # NUEVA VENTA
                exito = ventaBD.VentaBD.registrar_venta(usuario_actual[0], id_cliente, monto_float, prendas_int, metodo_pago)
                mensaje = "Venta registrada con éxito."
            else:
                # EDITAR VENTA
                exito = ventaBD.VentaBD.actualizar_venta(id_venta, id_cliente, monto_float, prendas_int, metodo_pago)
                mensaje = "Venta modificada con éxito."

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                modal.destroy()
                Funciones.llenar_tabla_ventas(tree, usuario_actual)
            else:
                messagebox.showerror("Error BD", "Hubo un problema al guardar la venta.")
                
        except ValueError:
            messagebox.showerror("Error de Formato", "El 'Monto' y 'Prendas' deben ser valores numéricos válidos.")

    @staticmethod
    def borrar_venta_tabla(window, usuario, id_venta, tree):
        """Anula una venta existente"""
        if not id_venta: return

        if messagebox.askyesno("Confirmar Anulación", "¿Desea anular (borrar) esta venta del historial?"):
            if ventaBD.VentaBD.eliminar_venta(id_venta):
                messagebox.showinfo("Info", "Venta anulada correctamente.")
                Funciones.llenar_tabla_ventas(tree, usuario)
            else:
                messagebox.showerror("Error", "No se pudo anular la venta.")