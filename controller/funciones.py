from tkinter import messagebox
from model import usuarioBD, clienteBD, ventaBD

class Funciones:
    # --- USUARIOS ---
    @staticmethod
    def ingresar(window, correo, password):
        if not correo or not password:
            messagebox.showwarning("Alerta", "Llene los campos")
            return
        usuario = usuarioBD.UsuarioBD.login(correo, password)
        if usuario:
            from view import interfaces
            # rol está en la columna 5 (id, nom, ape, corr, pass, rol)
            rol = usuario[5] if len(usuario) > 5 else "user"
            messagebox.showinfo("Bienvenido", f"Hola {usuario[1]} ({rol})")
            interfaces.Vista.menu_principal(window, usuario) 
        else:
            messagebox.showerror("Error", "Datos incorrectos")

    @staticmethod
    def guardar_usuario(window, nombre, apellidos, correo, password):
        if not nombre or not correo or not password:
            messagebox.showwarning("Alerta", "Campos vacíos")
            return
        exito = usuarioBD.UsuarioBD.registrar(nombre, apellidos, correo, password)
        if exito:
            from view import interfaces
            messagebox.showinfo("Éxito", "Usuario registrado")
            interfaces.Vista.login(window)
        else:
            messagebox.showerror("Error", "No se pudo registrar")

    # --- HELPER: ORDENAR TABLA CON FLECHAS ---
    @staticmethod
    def ordenar_columna(tree, col, reverse):
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0].replace("$", "")), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        for column in tree["columns"]:
            titulo_actual = tree.heading(column)["text"]
            titulo_limpio = titulo_actual.replace(" ▲", "").replace(" ▼", "")
            tree.heading(column, text=titulo_limpio)

        flecha = " ▼" if reverse else " ▲"
        titulo_nuevo = tree.heading(col)["text"] + flecha
        tree.heading(col, text=titulo_nuevo, command=lambda: Funciones.ordenar_columna(tree, col, not reverse))

    # --- CLIENTES ---
    @staticmethod
    def llenar_tabla_clientes(tree, usuario, filtro_texto=""):
        for item in tree.get_children(): tree.delete(item)
        
        id_usuario = usuario[0]
        rol = usuario[5] if len(usuario) > 5 else "user"
        
        datos = clienteBD.ClienteBD.consultar(id_usuario, rol)
        
        # --- Si llega None, lo convertimos a "" ---
        if filtro_texto is None: 
            filtro_texto = ""
        
        filtro_texto = filtro_texto.lower()
        
        for row in datos:
            # Filtro de texto (Nombre o Correo)
            if filtro_texto and (filtro_texto not in row[2].lower() and filtro_texto not in row[5].lower()):
                continue 
            
            # row: 0:id, 1:idu, 2:nom, 3:tel, 4:dir, 5:cor, 6:edad
            tree.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    @staticmethod
    def guardar_o_editar_cliente(parent, tree, id_cliente, usuario_actual, nombre, telefono, direccion, correo, edad, modal):
        if not nombre or not telefono:
            messagebox.showwarning("Alerta", "Nombre y Teléfono obligatorios")
            return
        if id_cliente is None:
            exito = clienteBD.ClienteBD.insertar(usuario_actual[0], nombre, telefono, direccion, correo, edad)
            msg = "Cliente creado"
        else:
            exito = clienteBD.ClienteBD.actualizar(id_cliente, nombre, telefono, direccion, correo, edad)
            msg = "Cliente actualizado"
        if exito:
            messagebox.showinfo("Éxito", msg)
            modal.destroy()
            Funciones.llenar_tabla_clientes(tree, usuario_actual)
        else:
            messagebox.showerror("Error", "Operación fallida")

    @staticmethod
    def borrar_cliente_tabla(window, usuario, id_cliente, tree):
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
            if clienteBD.ClienteBD.eliminar(id_cliente):
                messagebox.showinfo("Info", "Eliminado")
                Funciones.llenar_tabla_clientes(tree, usuario)
            else:
                messagebox.showerror("Error", "No se pudo eliminar")

    # --- VENTAS ---
    @staticmethod
    def llenar_tabla_ventas(tree, usuario, fecha_filtro=None):
        for item in tree.get_children(): tree.delete(item)
        
        id_usuario = usuario[0]
        rol = usuario[5] if len(usuario) > 5 else "user"
        
        datos = ventaBD.VentaBD.consultar_ventas(id_usuario, rol, fecha_filtro)
        
        for row in datos:
            nombre_vendedor = row[7]
            tree.insert("", "end", text=row[0], values=(row[0], nombre_vendedor, row[1], f"${row[2]}", row[3], row[4], row[5], row[6]))

    @staticmethod
    def guardar_o_editar_venta(window, tree, usuario_actual, id_venta, seleccion_cliente_str, monto, num_prendas, metodo_pago, modal):
        if not seleccion_cliente_str or not monto:
            messagebox.showwarning("Alerta", "Faltan datos")
            return
        try:
            id_cliente = seleccion_cliente_str.split(" - ")[0]
            if id_venta is None:
                exito = ventaBD.VentaBD.registrar_venta(usuario_actual[0], id_cliente, float(monto), int(num_prendas), metodo_pago)
                msg = "Venta registrada"
            else:
                exito = ventaBD.VentaBD.actualizar_venta(id_venta, id_cliente, float(monto), int(num_prendas), metodo_pago)
                msg = "Venta actualizada"

            if exito:
                messagebox.showinfo("Éxito", msg)
                modal.destroy()
                Funciones.llenar_tabla_ventas(tree, usuario_actual)
            else:
                messagebox.showerror("Error", "Error BD")
        except ValueError:
            messagebox.showerror("Error", "Monto y Prendas deben ser números")

    @staticmethod
    def borrar_venta_tabla(window, usuario, id_venta, tree):
        if messagebox.askyesno("Confirmar", "¿Anular esta venta?"):
            if ventaBD.VentaBD.eliminar_venta(id_venta):
                messagebox.showinfo("Info", "Venta anulada")
                Funciones.llenar_tabla_ventas(tree, usuario)
            else:
                messagebox.showerror("Error", "No se pudo eliminar")