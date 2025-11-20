import tkinter as tk
from tkinter import messagebox, ttk
from controller import funciones
from controller.reportes import GeneradorReportes
from model import clienteBD, ventaBD, usuarioBD
import os

# --- PALETA DE COLORES ---
COLOR_FONDO      = "#F3E5F5"
COLOR_PANEL      = "#E1BEE7"
COLOR_BOTON      = "#8E44AD"
COLOR_TEXTO      = "#4A235A"
COLOR_BLANCO     = "#FFFFFF"

class Vista:
    # Variable de clase para guardar el logo y que todos los métodos estáticos lo vean
    logo_img = None 

    def __init__(self, window):
        self.window = window
        self.window.title("Bonitas Fashions - Sistema de Gestión")
        self.window.geometry("1150x750")
        self.window.config(bg=COLOR_FONDO)
        
        # Cargar Logo una sola vez al iniciar
        try:
            if os.path.exists("logo.png"):
                img_temp = tk.PhotoImage(file="logo.png")
                Vista.logo_img = img_temp.subsample(3, 3) 
        except Exception as e:
            print(f"Nota: No se encontró logo.png ({e})")

        # Estilos de Tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COLOR_BLANCO, foreground="black", rowheight=25, fieldbackground=COLOR_BLANCO, font=("Arial", 10))
        style.map('Treeview', background=[('selected', COLOR_BOTON)])
        style.configure("Treeview.Heading", background=COLOR_PANEL, foreground=COLOR_TEXTO, font=("Arial", 10, "bold"))
        
        # Arrancamos con Login
        Vista.login(window)
    
    @staticmethod
    def borrarPantalla(window):
        for widget in window.winfo_children():
            if isinstance(widget, tk.Menu): continue
            widget.destroy()
    
    # ==========================================
    # PANTALLA 1: LOGIN
    # ==========================================
    @staticmethod
    def login(window):
        Vista.borrarPantalla(window)
        window.config(menu=tk.Menu(window), bg=COLOR_FONDO)

        frame = tk.Frame(window, bg=COLOR_BLANCO, padx=40, pady=40, bd=1, relief="solid")
        frame.pack(expand=True)

        # Usamos Vista.logo_img (Variable de clase)
        if Vista.logo_img:
            lbl_img = tk.Label(frame, image=Vista.logo_img, bg=COLOR_BLANCO)
            lbl_img.pack(pady=(0, 10))

        tk.Label(frame, text="Bonitas Fashions", font=("Gabriola", 30, "bold"), bg=COLOR_BLANCO, fg=COLOR_BOTON).pack()
        tk.Label(frame, text="Acceso al Sistema", font=("Arial", 11), bg=COLOR_BLANCO, fg="gray").pack(pady=(0, 20))

        tk.Label(frame, text="Correo:", bg=COLOR_BLANCO, fg=COLOR_TEXTO, font=("Arial", 10, "bold")).pack(anchor="w")
        correo = tk.Entry(frame, width=30, font=("Arial", 11), bg="#F4F6F6", bd=1, relief="solid")
        correo.pack(pady=5, ipady=3)

        tk.Label(frame, text="Contraseña:", bg=COLOR_BLANCO, fg=COLOR_TEXTO, font=("Arial", 10, "bold")).pack(anchor="w")
        password = tk.Entry(frame, show="*", width=30, font=("Arial", 11), bg="#F4F6F6", bd=1, relief="solid")
        password.pack(pady=5, ipady=3)

        tk.Button(frame, text="INICIAR SESIÓN", bg=COLOR_BOTON, fg="white", width=25, height=2, font=("Arial", 10, "bold"), cursor="hand2",
            command=lambda: funciones.Funciones.ingresar(window, correo.get(), password.get())).pack(pady=20)
        
        tk.Button(frame, text="Crear cuenta nueva", fg=COLOR_BOTON, bg=COLOR_BLANCO, bd=0, cursor="hand2", font=("Arial", 9, "underline"),
            command=lambda: Vista.registro(window)).pack()

    # ==========================================
    # PANTALLA 2: REGISTRO
    # ==========================================
    @staticmethod
    def registro(window):
        Vista.borrarPantalla(window)
        frame = tk.Frame(window, bg=COLOR_BLANCO, padx=40, pady=40, bd=1, relief="solid"); frame.pack(expand=True)
        tk.Label(frame, text="Registro de Usuario", font=("Arial", 18, "bold"), bg=COLOR_BLANCO, fg=COLOR_BOTON).pack(pady=20)

        nom = tk.StringVar(); ape = tk.StringVar(); cor = tk.StringVar(); pas = tk.StringVar()

        def crear_input(lbl, var, show=None):
            tk.Label(frame, text=lbl, bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(anchor="w")
            tk.Entry(frame, textvariable=var, show=show, bg="#F4F6F6", width=30).pack(pady=5)

        crear_input("Nombre:", nom); crear_input("Apellidos:", ape); crear_input("Correo:", cor); crear_input("Contraseña:", pas, "*")

        tk.Button(frame, text="GUARDAR", bg=COLOR_BOTON, fg="white", width=20, cursor="hand2",
            command=lambda: funciones.Funciones.guardar_usuario(window, nom.get(), ape.get(), cor.get(), pas.get())).pack(pady=20)
        tk.Button(frame, text="Volver", bg=COLOR_BLANCO, fg="gray", bd=0, cursor="hand2", command=lambda: Vista.login(window)).pack()

    # ==========================================
    # PANTALLA 3: MENU PRINCIPAL
    # ==========================================
    @staticmethod
    def menu_principal(window, usuario=None):
        Vista.borrarPantalla(window)
        window.config(bg=COLOR_FONDO)
        
        nombre = usuario[1] if usuario else "Usuario"
        rol = usuario[5] if usuario and len(usuario)>5 else "user"
        
        menubar = tk.Menu(window); window.config(menu=menubar)
        menu_acc = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Mi Cuenta", menu=menu_acc)
        menu_acc.add_command(label="Cerrar Sesión", command=lambda: Vista.login(window))
        menu_acc.add_command(label="Salir", command=window.quit)

        frame_centro = tk.Frame(window, bg=COLOR_FONDO); frame_centro.pack(expand=True)

        if Vista.logo_img:
            tk.Label(frame_centro, image=Vista.logo_img, bg=COLOR_FONDO).pack(pady=10)

        tk.Label(frame_centro, text=f"Hola, {nombre}", font=("Gabriola", 36, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        tk.Label(frame_centro, text=f"Rol: {rol.upper()}", font=("Arial", 12), bg=COLOR_FONDO, fg="gray").pack(pady=(0, 30))
        
        frame_botones = tk.Frame(frame_centro, bg=COLOR_FONDO); frame_botones.pack()
        btn_style = {'width': 20, 'height': 2, 'font': ("Arial", 11, "bold"), 'cursor': "hand2", 'bd': 0, 'fg': "white"}

        tk.Button(frame_botones, text="👥 CLIENTES", bg="#9B59B6", command=lambda: Vista.interfaz_clientes(window, usuario), **btn_style).grid(row=0, column=0, padx=15)
        tk.Button(frame_botones, text="🛒 VENTAS", bg="#8E44AD", command=lambda: Vista.interfaz_ventas(window, usuario), **btn_style).grid(row=0, column=1, padx=15)
        tk.Button(frame_botones, text="📊 REPORTES", bg="#6C3483", command=lambda: Vista.interfaz_reportes(window, usuario), **btn_style).grid(row=0, column=2, padx=15)

    # ==========================================
    # PANTALLA 4: CLIENTES
    # ==========================================
    @staticmethod
    def interfaz_clientes(window, usuario):
        Vista.borrarPantalla(window)
        top = tk.Frame(window, pady=15, bg=COLOR_PANEL); top.pack(fill="x")
        tk.Label(top, text="GESTIÓN DE CLIENTES", font=("Arial", 16, "bold"), bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=20)

        search_frame = tk.Frame(top, bg=COLOR_PANEL); search_frame.pack(side="left", padx=40)
        tk.Label(search_frame, text="Buscar:", bg=COLOR_PANEL).pack(side="left")
        v_busqueda = tk.StringVar()
        tk.Entry(search_frame, textvariable=v_busqueda, width=25).pack(side="left", padx=5)
        tk.Button(search_frame, text="🔍", bg="white", bd=0, command=lambda: funciones.Funciones.llenar_tabla_clientes(tree, usuario, v_busqueda.get())).pack(side="left")

        tk.Button(top, text="+ NUEVO CLIENTE", bg=COLOR_BOTON, fg="white", font=("Arial", 9, "bold"),
            command=lambda: Vista.modal_cliente(window, usuario, None, tree)).pack(side="right", padx=20)

        center = tk.Frame(window, bg=COLOR_FONDO); center.pack(fill="both", expand=True, padx=20, pady=20)
        actions = tk.Frame(center, bg=COLOR_BLANCO, bd=1, relief="solid", padx=10, width=140)
        actions.pack(side="right", fill="y"); actions.pack_propagate(False)
        
        tk.Label(actions, text="Opciones", bg=COLOR_BLANCO, fg=COLOR_BOTON, font=("Arial", 11, "bold")).pack(pady=15)
        btn_edit = tk.Button(actions, text="Editar", bg="#F39C12", fg="white", width=12, cursor="hand2"); btn_edit.pack(pady=5)
        btn_del = tk.Button(actions, text="Eliminar", bg="#C0392B", fg="white", width=12, cursor="hand2"); btn_del.pack(pady=5)

        frame_t = tk.Frame(center); frame_t.pack(side="left", fill="both", expand=True)
        cols = ("id", "idu", "nom", "tel", "dir", "cor", "edad")
        tree = ttk.Treeview(frame_t, columns=cols, show="headings")
        headers = ["ID", "Reg.Por", "Nombre", "Teléfono", "Dirección", "Correo", "Edad"]
        for col, name in zip(cols, headers): tree.heading(col, text=name, command=lambda c=col: funciones.Funciones.ordenar_columna(tree, c, False))
        tree.column("id", width=30, anchor="center"); tree.column("idu", width=50, anchor="center"); tree.column("edad", width=40, anchor="center"); tree.column("nom", width=150)
        
        scrol = ttk.Scrollbar(frame_t, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrol.set); tree.pack(side="left", fill="both", expand=True); scrol.pack(side="right", fill="y")
        
        funciones.Funciones.llenar_tabla_clientes(tree, usuario)

        def get_sel(): sel = tree.selection(); return tree.item(sel) if sel else None
        btn_edit.config(command=lambda: Vista.modal_cliente(window, usuario, get_sel(), tree) if get_sel() else messagebox.showinfo("Ojo", "Selecciona"))
        btn_del.config(command=lambda: funciones.Funciones.borrar_cliente_tabla(window, usuario, get_sel()['text'], tree) if get_sel() else messagebox.showinfo("Ojo", "Selecciona"))
        
        tk.Button(window, text="⬅ Volver al Menú", bg="#5D6D7E", fg="white", command=lambda: Vista.menu_principal(window, usuario)).pack(pady=10)

    # ==========================================
    # PANTALLA 5: VENTAS
    # ==========================================
    @staticmethod
    def interfaz_ventas(window, usuario):
        Vista.borrarPantalla(window)
        top = tk.Frame(window, pady=15, bg=COLOR_PANEL); top.pack(fill="x")
        tk.Label(top, text="HISTORIAL DE VENTAS", font=("Arial", 16, "bold"), bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(side="left", padx=20)

        filter_frame = tk.Frame(top, bg=COLOR_PANEL); filter_frame.pack(side="left", padx=40)
        tk.Label(filter_frame, text="Fecha (YYYY-MM):", bg=COLOR_PANEL).pack(side="left")
        v_fecha = tk.StringVar()
        tk.Entry(filter_frame, textvariable=v_fecha, width=12).pack(side="left", padx=5)
        tk.Button(filter_frame, text="Filtrar", bg="white", bd=0, command=lambda: funciones.Funciones.llenar_tabla_ventas(tree, usuario, v_fecha.get())).pack(side="left")
        tk.Button(filter_frame, text="X", bg="#E74C3C", fg="white", bd=0, command=lambda: [v_fecha.set(""), funciones.Funciones.llenar_tabla_ventas(tree, usuario, None)]).pack(side="left", padx=2)

        tk.Button(top, text="+ NUEVA VENTA", bg=COLOR_BOTON, fg="white", font=("Arial", 9, "bold"),
            command=lambda: Vista.modal_venta(window, usuario, None, tree)).pack(side="right", padx=20)

        center = tk.Frame(window, bg=COLOR_FONDO); center.pack(fill="both", expand=True, padx=20, pady=20)
        actions = tk.Frame(center, bg=COLOR_BLANCO, bd=1, relief="solid", padx=10, width=140)
        actions.pack(side="right", fill="y"); actions.pack_propagate(False)
        tk.Label(actions, text="Opciones", bg=COLOR_BLANCO, fg=COLOR_BOTON, font=("Arial", 11, "bold")).pack(pady=15)
        btn_edit = tk.Button(actions, text="Editar", bg="#F39C12", fg="white", width=12, cursor="hand2"); btn_edit.pack(pady=5)
        btn_del = tk.Button(actions, text="Anular", bg="#C0392B", fg="white", width=12, cursor="hand2"); btn_del.pack(pady=5)

        frame_t = tk.Frame(center); frame_t.pack(side="left", fill="both", expand=True)
        cols = ("fol", "vend", "cli", "monto", "pren", "pago", "fecha", "idcli")
        tree = ttk.Treeview(frame_t, columns=cols, show="headings")
        headers = ["Folio", "Vendedor", "Cliente", "Total", "Prendas", "Pago", "Fecha"]
        for col, name in zip(cols[:-1], headers): tree.heading(col, text=name, command=lambda c=col: funciones.Funciones.ordenar_columna(tree, c, False))
        tree.column("fol", width=50, anchor="center"); tree.column("monto", width=80, anchor="e"); tree.column("pren", width=60, anchor="center"); tree.column("idcli", width=0, stretch=False)
        
        scrol = ttk.Scrollbar(frame_t, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrol.set); tree.pack(side="left", fill="both", expand=True); scrol.pack(side="right", fill="y")
        
        funciones.Funciones.llenar_tabla_ventas(tree, usuario)

        def get_sel(): sel = tree.selection(); return tree.item(sel) if sel else None
        btn_edit.config(command=lambda: Vista.modal_venta(window, usuario, get_sel(), tree) if get_sel() else messagebox.showinfo("Ojo", "Selecciona"))
        btn_del.config(command=lambda: funciones.Funciones.borrar_venta_tabla(window, usuario, get_sel()['text'], tree) if get_sel() else messagebox.showinfo("Ojo", "Selecciona"))
        tk.Button(window, text="⬅ Volver al Menú", bg="#5D6D7E", fg="white", command=lambda: Vista.menu_principal(window, usuario)).pack(pady=10)

    # ==========================================
    # PANTALLA 6: REPORTES
    # ==========================================
    @staticmethod
    def interfaz_reportes(window, usuario):
        Vista.borrarPantalla(window)
        rol = usuario[5] if usuario and len(usuario)>5 else "user"
        tk.Label(window, text="CENTRO DE REPORTES", font=("Gabriola", 30, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=20)
        main_frame = tk.Frame(window, bg=COLOR_FONDO); main_frame.pack(pady=10)

        def crear_bloque(titulo, col):
            f = tk.LabelFrame(main_frame, text=titulo, font=("Arial", 12, "bold"), padx=20, pady=20, bg="white", fg=COLOR_BOTON)
            f.grid(row=0, column=col, padx=20, sticky="n"); return f

        f_c = crear_bloque("📂 Clientes", 0); tk.Label(f_c, text="Exportar clientes", bg="white").pack(pady=5)
        bf_c = tk.Frame(f_c, bg="white"); bf_c.pack(pady=10)
        tk.Button(bf_c, text="Excel", bg="#27AE60", fg="white", width=8, command=lambda: Vista.generar_exportacion("clientes", "excel", usuario)).pack(side="left", padx=2)
        tk.Button(bf_c, text="PDF", bg="#C0392B", fg="white", width=8, command=lambda: Vista.generar_exportacion("clientes", "pdf", usuario)).pack(side="left", padx=2)

        f_v = crear_bloque("💰 Ventas", 1); tk.Label(f_v, text="Exportar historial", bg="white").pack(pady=5)
        bf_v = tk.Frame(f_v, bg="white"); bf_v.pack(pady=10)
        tk.Button(bf_v, text="Excel", bg="#27AE60", fg="white", width=8, command=lambda: Vista.generar_exportacion("ventas", "excel", usuario)).pack(side="left", padx=2)
        tk.Button(bf_v, text="PDF", bg="#C0392B", fg="white", width=8, command=lambda: Vista.generar_exportacion("ventas", "pdf", usuario)).pack(side="left", padx=2)

        if rol == 'admin':
            f_u = tk.LabelFrame(main_frame, text="🛡️ Admin", font=("Arial", 12, "bold"), padx=20, pady=20, bg="white", fg="red")
            f_u.grid(row=1, column=0, columnspan=2, pady=20, sticky="ew")
            tk.Button(f_u, text="Reporte Usuarios (Excel)", bg="#333", fg="white", command=lambda: Vista.generar_exportacion("usuarios", "excel", usuario)).pack()

        tk.Button(window, text="⬅ Volver al Menú", bg="#5D6D7E", fg="white", command=lambda: Vista.menu_principal(window, usuario)).pack(pady=30)

    @staticmethod
    def generar_exportacion(tipo, formato, usuario):
        rol = usuario[5]; id_usu = usuario[0]; datos = []; columnas = []; titulo = ""
        if tipo == "clientes":
            raw = clienteBD.ClienteBD.consultar(id_usu, rol)
            columnas = ["ID", "ID_Usu", "Nombre", "Teléfono", "Dirección", "Correo", "Edad"]
            if rol == 'admin': columnas.append("Vendedor")
            datos = raw; titulo = "Reporte Clientes"
        elif tipo == "ventas":
            raw = ventaBD.VentaBD.consultar_ventas(id_usu, rol)
            datos = [(r[0], r[1], r[2], r[3], r[4], r[5], r[7]) for r in raw]
            columnas = ["Folio", "Cliente", "Monto", "Prendas", "Pago", "Fecha", "Vendedor"]
            titulo = "Reporte Ventas"
        elif tipo == "usuarios":
            from model.conexionBD import cursor
            cursor.execute("SELECT id, nombre, apellidos, correo, rol FROM usuarios")
            datos = cursor.fetchall(); columnas = ["ID", "Nombre", "Apellidos", "Correo", "Rol"]; titulo = "Usuarios"
        
        if formato == "excel": GeneradorReportes.exportar_excel(datos, columnas, tipo)
        elif formato == "pdf": GeneradorReportes.exportar_pdf(datos, columnas, titulo, tipo)

    # --- MODALES ---
    @staticmethod
    def modal_cliente(parent, usuario, item_editar, tree):
        modal = tk.Toplevel(parent); modal.geometry("350x420"); modal.config(bg=COLOR_FONDO)
        v_nom = tk.StringVar(); v_tel = tk.StringVar(); v_dir = tk.StringVar(); v_cor = tk.StringVar(); v_edad = tk.IntVar()
        id_cli = None
        tit = "Editar Cliente" if item_editar else "Nuevo Cliente"
        modal.title(tit); tk.Label(modal, text=tit, font=("Arial", 14, "bold"), bg=COLOR_FONDO, fg=COLOR_BOTON).pack(pady=10)
        if item_editar:
            id_cli = item_editar['text']; vals = item_editar['values']
            v_nom.set(vals[2]); v_tel.set(vals[3]); v_dir.set(vals[4]); v_cor.set(vals[5]); v_edad.set(vals[6])

        def inp(l, v): tk.Label(modal, text=l, bg=COLOR_FONDO).pack(); tk.Entry(modal, textvariable=v).pack()
        inp("Nombre:", v_nom); inp("Teléfono:", v_tel); inp("Dirección:", v_dir); inp("Correo:", v_cor); inp("Edad:", v_edad)
        tk.Button(modal, text="GUARDAR", bg=COLOR_BOTON, fg="white", width=20,
            command=lambda: funciones.Funciones.guardar_o_editar_cliente(parent, tree, id_cli, usuario, v_nom.get(), v_tel.get(), v_dir.get(), v_cor.get(), v_edad.get(), modal)).pack(pady=20)

    @staticmethod
    def modal_venta(parent, usuario, item_editar, tree):
        modal = tk.Toplevel(parent); modal.geometry("350x450"); modal.config(bg=COLOR_FONDO)
        v_cli = tk.StringVar(); v_monto = tk.DoubleVar(); v_pren = tk.IntVar(value=1); v_met = tk.StringVar(); id_venta = None
        tit = "Editar Venta" if item_editar else "Nueva Venta"
        modal.title(tit); tk.Label(modal, text=tit, font=("Arial", 14, "bold"), bg=COLOR_FONDO, fg=COLOR_BOTON).pack(pady=10)
        rol = usuario[5] if len(usuario)>5 else "user"
        raw = clienteBD.ClienteBD.consultar(usuario[0], rol)
        lista_combo = [f"{c[0]} - {c[2]}" for c in raw]

        if item_editar:
            id_venta = item_editar['text']; vals = item_editar['values']
            v_cli.set(f"{vals[7]} - {vals[2]}"); v_monto.set(str(vals[3]).replace("$","")); v_pren.set(vals[4]); v_met.set(vals[5])

        tk.Label(modal, text="Cliente:", bg=COLOR_FONDO).pack()
        ttk.Combobox(modal, textvariable=v_cli, values=lista_combo, state="readonly", width=30).pack()
        tk.Label(modal, text="Total ($):", bg=COLOR_FONDO).pack(); tk.Entry(modal, textvariable=v_monto).pack()
        tk.Label(modal, text="Prendas:", bg=COLOR_FONDO).pack(); tk.Entry(modal, textvariable=v_pren).pack()
        tk.Label(modal, text="Pago:", bg=COLOR_FONDO).pack()
        cmb = ttk.Combobox(modal, textvariable=v_met, values=["Efectivo", "Tarjeta", "Transferencia"], state="readonly"); cmb.pack()
        if not item_editar: cmb.current(0)
        
        btn_txt = "ACTUALIZAR" if item_editar else "COBRAR"
        tk.Button(modal, text=btn_txt, bg=COLOR_BOTON, fg="white", width=20,
            command=lambda: funciones.Funciones.guardar_o_editar_venta(parent, tree, usuario, id_venta, v_cli.get(), v_monto.get(), v_pren.get(), v_met.get(), modal)).pack(pady=20)