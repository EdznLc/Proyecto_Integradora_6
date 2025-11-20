import tkinter as tk
from tkinter import messagebox, ttk
from controller import funciones
from controller.reportes import GeneradorReportes # <--- NUEVO IMPORT
from model import clienteBD, ventaBD, usuarioBD # <--- NUEVO IMPORT

class Vista:
    def __init__(self, window):
        window.title("Sistema Venta Ropa")
        window.geometry("1150x750")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        Vista.login(window)
    
    @staticmethod
    def borrarPantalla(window):
        for widget in window.winfo_children():
            if isinstance(widget, tk.Menu): continue
            widget.destroy()
    
    # --- LOGIN ---
    @staticmethod
    def login(window):
        Vista.borrarPantalla(window); window.config(menu=tk.Menu(window))
        tk.Label(window, text="INICIAR SESIÓN", font=("Arial", 24, "bold")).pack(pady=50)
        frame = tk.Frame(window, bg="#eee", padx=20, pady=20); frame.pack()
        tk.Label(frame, text="Correo:").grid(row=0, column=0, pady=10)
        correo = tk.Entry(frame, width=30); correo.grid(row=0, column=1, pady=10)
        tk.Label(frame, text="Password:").grid(row=1, column=0, pady=10)
        password = tk.Entry(frame, show="*", width=30); password.grid(row=1, column=1, pady=10)
        tk.Button(window, text="ENTRAR", bg="#333", fg="white", width=20,
            command=lambda: funciones.Funciones.ingresar(window, correo.get(), password.get())).pack(pady=20)
        tk.Button(window, text="Registrarse", fg="blue", bd=0, command=lambda: Vista.registro(window)).pack()

    # --- REGISTRO ---
    @staticmethod
    def registro(window):
        Vista.borrarPantalla(window)
        tk.Label(window, text="NUEVO USUARIO", font=("Arial", 20)).pack(pady=30)
        frame = tk.Frame(window); frame.pack()
        nom = tk.StringVar(); ape = tk.StringVar(); cor = tk.StringVar(); pas = tk.StringVar()
        tk.Label(frame, text="Nombre:").grid(row=0, column=0); tk.Entry(frame, textvariable=nom).grid(row=0, column=1)
        tk.Label(frame, text="Apellidos:").grid(row=1, column=0); tk.Entry(frame, textvariable=ape).grid(row=1, column=1)
        tk.Label(frame, text="Correo:").grid(row=2, column=0); tk.Entry(frame, textvariable=cor).grid(row=2, column=1)
        tk.Label(frame, text="Password:").grid(row=3, column=0); tk.Entry(frame, textvariable=pas, show="*").grid(row=3, column=1)
        tk.Button(window, text="GUARDAR", bg="green", fg="white",
            command=lambda: funciones.Funciones.guardar_usuario(window, nom.get(), ape.get(), cor.get(), pas.get())).pack(pady=20)
        tk.Button(window, text="Volver", command=lambda: Vista.login(window)).pack()

    # --- MENU PRINCIPAL ---
    @staticmethod
    def menu_principal(window, usuario=None):
        Vista.borrarPantalla(window)
        nombre = usuario[1] if usuario else "Usuario"
        rol = usuario[5] if usuario and len(usuario)>5 else "user"
        
        menubar = tk.Menu(window); window.config(menu=menubar)
        menu_acc = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sistema", menu=menu_acc)
        menu_acc.add_command(label="Cerrar Sesión", command=lambda: Vista.login(window))
        menu_acc.add_command(label="Salir", command=window.quit)

        tk.Label(window, text=f"BIENVENIDO: {nombre}", font=("Arial", 20)).pack(pady=10)
        tk.Label(window, text=f"Rol: {rol.upper()}", font=("Arial", 12), fg="gray").pack(pady=5)
        
        frame = tk.Frame(window); frame.pack(pady=20)
        tk.Button(frame, text="👥 CLIENTES", width=20, height=3, bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
            command=lambda: Vista.interfaz_clientes(window, usuario)).grid(row=0, column=0, padx=15)
        tk.Button(frame, text="🛒 VENTAS", width=20, height=3, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
            command=lambda: Vista.interfaz_ventas(window, usuario)).grid(row=0, column=1, padx=15)
        
        tk.Button(frame, text="📊 REPORTES", width=20, height=3, bg="#9C27B0", fg="white", font=("Arial", 10, "bold"),
            command=lambda: Vista.interfaz_reportes(window, usuario)).grid(row=0, column=2, padx=15)


    # =======================
    # REPORTES Y EXPORTACIÓN
    # =======================
    @staticmethod
    def interfaz_reportes(window, usuario):
        Vista.borrarPantalla(window)
        rol = usuario[5] if usuario and len(usuario)>5 else "user"
        
        tk.Label(window, text="CENTRO DE REPORTES", font=("Arial", 22, "bold"), fg="#333").pack(pady=20)
        tk.Label(window, text="Selecciona qué datos deseas exportar", font=("Arial", 12)).pack(pady=5)

        # Contenedor Principal
        main_frame = tk.Frame(window); main_frame.pack(pady=20)

        # --- SECCIÓN CLIENTES ---
        frame_cli = tk.LabelFrame(main_frame, text="📂 Base de Datos de Clientes", font=("Arial", 12, "bold"), padx=20, pady=20)
        frame_cli.grid(row=0, column=0, padx=20)
        
        tk.Label(frame_cli, text="Exportar lista completa de clientes").pack(pady=5)
        
        btn_frame_c = tk.Frame(frame_cli); btn_frame_c.pack(pady=10)
        tk.Button(btn_frame_c, text="Excel", bg="#1D6F42", fg="white", width=10, 
            command=lambda: Vista.generar_exportacion("clientes", "excel", usuario)).pack(side="left", padx=5)
        tk.Button(btn_frame_c, text="PDF", bg="#B30B00", fg="white", width=10,
            command=lambda: Vista.generar_exportacion("clientes", "pdf", usuario)).pack(side="left", padx=5)
        tk.Button(btn_frame_c, text="JSON", bg="#F7DF1E", width=10,
            command=lambda: Vista.generar_exportacion("clientes", "json", usuario)).pack(side="left", padx=5)

        # --- SECCIÓN VENTAS ---
        frame_ven = tk.LabelFrame(main_frame, text="💰 Historial de Ventas", font=("Arial", 12, "bold"), padx=20, pady=20)
        frame_ven.grid(row=0, column=1, padx=20)
        
        tk.Label(frame_ven, text="Exportar registro histórico de ventas").pack(pady=5)
        
        btn_frame_v = tk.Frame(frame_ven); btn_frame_v.pack(pady=10)
        tk.Button(btn_frame_v, text="Excel", bg="#1D6F42", fg="white", width=10,
            command=lambda: Vista.generar_exportacion("ventas", "excel", usuario)).pack(side="left", padx=5)
        tk.Button(btn_frame_v, text="PDF", bg="#B30B00", fg="white", width=10,
            command=lambda: Vista.generar_exportacion("ventas", "pdf", usuario)).pack(side="left", padx=5)
        tk.Button(btn_frame_v, text="JSON", bg="#F7DF1E", width=10,
            command=lambda: Vista.generar_exportacion("ventas", "json", usuario)).pack(side="left", padx=5)

        # --- SECCIÓN USUARIOS (SOLO ADMIN) ---
        if rol == 'admin':
            frame_usu = tk.LabelFrame(main_frame, text="🛡️ Usuarios del Sistema (Admin)", font=("Arial", 12, "bold"), padx=20, pady=20, fg="red")
            frame_usu.grid(row=1, column=0, columnspan=2, pady=20, sticky="ew")
            
            tk.Button(frame_usu, text="Exportar Usuarios (Excel)", bg="#333", fg="white", width=25,
                command=lambda: Vista.generar_exportacion("usuarios", "excel", usuario)).pack()

        tk.Button(window, text="⬅ Volver al Menú", command=lambda: Vista.menu_principal(window, usuario)).pack(pady=30)

    # --- LÓGICA INTERMEDIA PARA PREPARAR DATOS ---
    @staticmethod
    def generar_exportacion(tipo, formato, usuario):
        rol = usuario[5]
        id_usu = usuario[0]
        
        datos = []
        columnas = []
        titulo = ""

        if tipo == "clientes":
            # Reutilizamos el modelo existente
            raw_data = clienteBD.ClienteBD.consultar(id_usu, rol)
            # raw_data trae tuplas. Definimos nombres de columnas
            columnas = ["ID", "ID_Usu", "Nombre", "Teléfono", "Dirección", "Correo", "Edad"]
            if rol == 'admin': columnas.append("Vendedor") # Si es admin trae una col extra
            
            datos = raw_data
            titulo = "Reporte de Clientes"

        elif tipo == "ventas":
            raw_data = ventaBD.VentaBD.consultar_ventas(id_usu, rol)
            # indices: 0:id, 1:cli, 2:monto, 3:pren, 4:pago, 5:fecha, 6:idcli, 7:vendedor
            # Vamos a limpiar los datos para el reporte (quitando id oculto)
            datos_limpios = []
            for r in raw_data:
                # (Folio, Cliente, Monto, Prendas, Pago, Fecha, Vendedor)
                datos_limpios.append((r[0], r[1], r[2], r[3], r[4], r[5], r[7]))
            
            columnas = ["Folio", "Cliente", "Monto", "Prendas", "Pago", "Fecha", "Vendedor"]
            datos = datos_limpios
            titulo = "Reporte de Ventas"

        elif tipo == "usuarios":
            # Consulta rápida directa (usualmente iría en el modelo, pero para no complicar más)
            from model.conexionBD import cursor, conexion
            cursor.execute("SELECT id, nombre, apellidos, correo, rol FROM usuarios")
            datos = cursor.fetchall()
            columnas = ["ID", "Nombre", "Apellidos", "Correo", "Rol"]
            titulo = "Listado de Usuarios"

        # LLAMAMOS AL GENERADOR
        if formato == "excel":
            GeneradorReportes.exportar_excel(datos, columnas, tipo)
        elif formato == "json":
            GeneradorReportes.exportar_json(datos, columnas, tipo)
        elif formato == "pdf":
            GeneradorReportes.exportar_pdf(datos, columnas, titulo, tipo)


    
    # --- CLIENTES ---
    @staticmethod
    def interfaz_clientes(window, usuario):
        Vista.borrarPantalla(window)
        top = tk.Frame(window, pady=10, bg="#eee"); top.pack(fill="x")
        tk.Label(top, text="CLIENTES", font=("Arial", 16, "bold"), bg="#eee").pack(side="left", padx=20)

        search_frame = tk.Frame(top, bg="#eee"); search_frame.pack(side="left", padx=40)
        tk.Label(search_frame, text="Buscar:", bg="#eee").pack(side="left")
        v_busqueda = tk.StringVar()
        ent_search = tk.Entry(search_frame, textvariable=v_busqueda, width=25)
        ent_search.pack(side="left", padx=5)
        tk.Button(search_frame, text="🔍", command=lambda: funciones.Funciones.llenar_tabla_clientes(tree, usuario, v_busqueda.get())).pack(side="left")

        btn_new = tk.Button(top, text="+ NUEVO", bg="#4CAF50", fg="white", width=15)
        btn_new.pack(side="right", padx=20)

        center = tk.Frame(window); center.pack(fill="both", expand=True, padx=20, pady=10)
        actions = tk.Frame(center, bg="white", bd=1, relief="solid", padx=10, width=140)
        actions.pack(side="right", fill="y"); actions.pack_propagate(False)
        tk.Label(actions, text="Opciones", bg="white", font=("Arial", 11, "bold")).pack(pady=15)
        btn_edit = tk.Button(actions, text="Editar", bg="orange", width=12); btn_edit.pack(pady=5)
        btn_del = tk.Button(actions, text="Eliminar", bg="red", fg="white", width=12); btn_del.pack(pady=5)

        frame_t = tk.Frame(center); frame_t.pack(side="left", fill="both", expand=True)
        cols = ("id", "idu", "nom", "tel", "dir", "cor", "edad")
        tree = ttk.Treeview(frame_t, columns=cols, show="headings")
        headers = ["ID", "Reg.Por", "Nombre", "Teléfono", "Dirección", "Correo", "Edad"]
        for col, name in zip(cols, headers):
            tree.heading(col, text=name, command=lambda c=col: funciones.Funciones.ordenar_columna(tree, c, False))
        tree.column("id", width=30, anchor="center"); tree.column("idu", width=50, anchor="center")
        tree.column("edad", width=40, anchor="center"); tree.column("nom", width=150)
        
        scrol = ttk.Scrollbar(frame_t, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrol.set); tree.pack(side="left", fill="both", expand=True); scrol.pack(side="right", fill="y")
        
        ent_search.bind("<Return>", lambda e: funciones.Funciones.llenar_tabla_clientes(tree, usuario, v_busqueda.get()))
        funciones.Funciones.llenar_tabla_clientes(tree, usuario)

        def get_sel(): sel = tree.selection(); return tree.item(sel) if sel else None
        btn_new.config(command=lambda: Vista.modal_cliente(window, usuario, None, tree))
        btn_edit.config(command=lambda: Vista.modal_cliente(window, usuario, get_sel(), tree) if get_sel() else messagebox.showinfo("Ojo", "Selecciona"))
        btn_del.config(command=lambda: funciones.Funciones.borrar_cliente_tabla(window, usuario, get_sel()['text'], tree) if get_sel() else messagebox.showinfo("Ojo", "Selecciona"))
        tk.Button(window, text="⬅ Volver", command=lambda: Vista.menu_principal(window, usuario)).pack(pady=10)

    # --- MODAL CLIENTE ---
    @staticmethod
    def modal_cliente(parent, usuario, item_editar, tree):
        modal = tk.Toplevel(parent); modal.geometry("350x400")
        v_nom = tk.StringVar(); v_tel = tk.StringVar(); v_dir = tk.StringVar(); v_cor = tk.StringVar(); v_edad = tk.IntVar()
        id_cli = None
        if item_editar:
            modal.title("Editar"); id_cli = item_editar['text']; vals = item_editar['values']
            v_nom.set(vals[2]); v_tel.set(vals[3]); v_dir.set(vals[4]); v_cor.set(vals[5]); v_edad.set(vals[6])
        else: modal.title("Nuevo")
        tk.Label(modal, text="Nombre:").pack(); tk.Entry(modal, textvariable=v_nom).pack()
        tk.Label(modal, text="Teléfono:").pack(); tk.Entry(modal, textvariable=v_tel).pack()
        tk.Label(modal, text="Dirección:").pack(); tk.Entry(modal, textvariable=v_dir).pack()
        tk.Label(modal, text="Correo:").pack(); tk.Entry(modal, textvariable=v_cor).pack()
        tk.Label(modal, text="Edad:").pack(); tk.Entry(modal, textvariable=v_edad).pack()
        tk.Button(modal, text="GUARDAR", bg="green", fg="white",
            command=lambda: funciones.Funciones.guardar_o_editar_cliente(parent, tree, id_cli, usuario, v_nom.get(), v_tel.get(), v_dir.get(), v_cor.get(), v_edad.get(), modal)).pack(pady=20)

    # --- VENTAS ---
    @staticmethod
    def interfaz_ventas(window, usuario):
        Vista.borrarPantalla(window)
        top = tk.Frame(window, pady=10, bg="#e0f7fa"); top.pack(fill="x")
        tk.Label(top, text="HISTORIAL VENTAS", font=("Arial", 16, "bold"), bg="#e0f7fa").pack(side="left", padx=20)

        # Filtro Fecha
        filter_frame = tk.Frame(top, bg="#e0f7fa"); filter_frame.pack(side="left", padx=40)
        tk.Label(filter_frame, text="Fecha (YYYY-MM):", bg="#e0f7fa").pack(side="left")
        v_fecha = tk.StringVar()
        tk.Entry(filter_frame, textvariable=v_fecha, width=12).pack(side="left", padx=5)
        tk.Button(filter_frame, text="Filtrar", command=lambda: funciones.Funciones.llenar_tabla_ventas(tree, usuario, v_fecha.get())).pack(side="left")
        tk.Button(filter_frame, text="X", command=lambda: [v_fecha.set(""), funciones.Funciones.llenar_tabla_ventas(tree, usuario, None)]).pack(side="left", padx=2)

        btn_new = tk.Button(top, text="+ VENTA", bg="#4CAF50", fg="white", width=15); btn_new.pack(side="right", padx=20)

        center = tk.Frame(window); center.pack(fill="both", expand=True, padx=20, pady=10)
        actions = tk.Frame(center, bg="white", bd=1, relief="solid", padx=10, width=140)
        actions.pack(side="right", fill="y"); actions.pack_propagate(False)
        tk.Label(actions, text="Opciones", bg="white").pack(pady=15)
        btn_edit = tk.Button(actions, text="Editar", bg="orange", width=12); btn_edit.pack(pady=5)
        btn_del = tk.Button(actions, text="Anular", bg="red", fg="white", width=12); btn_del.pack(pady=5)

        frame_t = tk.Frame(center); frame_t.pack(side="left", fill="both", expand=True)
        cols = ("fol", "vend", "cli", "monto", "pren", "pago", "fecha", "idcli")
        tree = ttk.Treeview(frame_t, columns=cols, show="headings")
        headers = ["Folio", "Vendedor", "Cliente", "Total", "Prendas", "Pago", "Fecha"]
        for col, name in zip(cols[:-1], headers):
            tree.heading(col, text=name, command=lambda c=col: funciones.Funciones.ordenar_columna(tree, c, False))
        tree.column("fol", width=50, anchor="center"); tree.column("monto", width=80, anchor="e")
        tree.column("pren", width=60, anchor="center"); tree.column("idcli", width=0, stretch=False)
        
        scrol = ttk.Scrollbar(frame_t, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrol.set); tree.pack(side="left", fill="both", expand=True); scrol.pack(side="right", fill="y")
        
        funciones.Funciones.llenar_tabla_ventas(tree, usuario)

        def get_sel(): sel = tree.selection(); return tree.item(sel) if sel else None
        btn_new.config(command=lambda: Vista.modal_venta(window, usuario, None, tree))
        btn_edit.config(command=lambda: Vista.modal_venta(window, usuario, get_sel(), tree) if get_sel() else messagebox.showinfo("Ojo", "Selecciona"))
        btn_del.config(command=lambda: funciones.Funciones.borrar_venta_tabla(window, usuario, get_sel()['text'], tree) if get_sel() else messagebox.showinfo("Ojo", "Selecciona"))
        tk.Button(window, text="⬅ Volver", command=lambda: Vista.menu_principal(window, usuario)).pack(pady=10)

    # --- MODAL VENTA ---
    @staticmethod
    def modal_venta(parent, usuario, item_editar, tree):
        modal = tk.Toplevel(parent); modal.geometry("350x450")
        v_cli = tk.StringVar(); v_monto = tk.DoubleVar(); v_pren = tk.IntVar(value=1); v_met = tk.StringVar(); id_venta = None
        tit = "Editar Venta" if item_editar else "Nueva Venta"; modal.title(tit)
        rol = usuario[5] if len(usuario)>5 else "user"
        raw = clienteBD.ClienteBD.consultar(usuario[0], rol)
        lista_combo = [f"{c[0]} - {c[2]}" for c in raw]

        if item_editar:
            id_venta = item_editar['text']; vals = item_editar['values']
            v_cli.set(f"{vals[7]} - {vals[2]}")
            v_monto.set(str(vals[3]).replace("$",""))
            v_pren.set(vals[4]); v_met.set(vals[5])

        tk.Label(modal, text="Cliente:").pack()
        ttk.Combobox(modal, textvariable=v_cli, values=lista_combo, state="readonly", width=30).pack()
        tk.Label(modal, text="Total ($):").pack(); tk.Entry(modal, textvariable=v_monto).pack()
        tk.Label(modal, text="Prendas:").pack(); tk.Entry(modal, textvariable=v_pren).pack()
        tk.Label(modal, text="Pago:").pack()
        cmb = ttk.Combobox(modal, textvariable=v_met, values=["Efectivo", "Tarjeta", "Transferencia"], state="readonly"); cmb.pack()
        if not item_editar: cmb.current(0)
        
        btn_txt = "ACTUALIZAR" if item_editar else "COBRAR"
        tk.Button(modal, text=btn_txt, bg="#009688", fg="white", width=20,
            command=lambda: funciones.Funciones.guardar_o_editar_venta(parent, tree, usuario, id_venta, v_cli.get(), v_monto.get(), v_pren.get(), v_met.get(), modal)).pack(pady=30)