import tkinter as tk
from tkinter import messagebox, ttk
from controller import funciones
from controller.reportes import GeneradorReportes
from model import clienteBD, ventaBD, usuarioBD
import os

# --- PALETA DE COLORES BOUTIQUE ---
BG_APP           = "#F3E5F5"
BG_PANEL         = "#FFFFFF"
COLOR_PRIMARY    = "#8E44AD"
COLOR_SECONDARY  = "#9B59B6"
COLOR_TEXT_MAIN  = "#4A235A"
COLOR_LILA_INPUT = "#E8DAEF"
COLOR_BORDER     = "#D2B4DE"

BTN_EDIT_COLOR   = "#5B2C6F"
BTN_DELETE_COLOR = "#943126"
BTN_X_COLOR      = "#C0392B"

FONT_TITLE       = ("Segoe UI", 28, "bold") 
FONT_SUBTITLE    = ("Segoe UI", 16)
FONT_BODY        = ("Segoe UI", 11) 
FONT_BOLD        = ("Segoe UI", 11, "bold")

class Vista:
    logo_img = None 

    def __init__(self, window):
        self.window = window
        self.window.title("Bonitas Fashions - Manager")
        self.window.geometry("1200x800")
        self.window.config(bg=BG_APP)
        
        try:
            if os.path.exists("logo.png"):
                img_temp = tk.PhotoImage(file="logo.png")
                Vista.logo_img = img_temp.subsample(3, 3) 
        except Exception as e:
            print(f"Nota: No se encontró logo.png")

        # --- ESTILOS MODERNOS (CORREGIDOS PARA COMBOBOX) ---
        style = ttk.Style()
        style.theme_use("clam")
        
        # Tabla
        style.configure("Treeview", background="white", foreground="#333", rowheight=35, fieldbackground="white", borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#E8DAEF", foreground=COLOR_TEXT_MAIN, borderwidth=0, font=("Segoe UI", 11, "bold"))
        style.map('Treeview', background=[('selected', COLOR_PRIMARY)])
        
        # --- ARREGLO DEL COMBOBOX GRIS ---
        # Configuramos para que el campo (field) sea blanco siempre
        style.configure("TCombobox", 
                        fieldbackground="white", 
                        background="white", 
                        arrowcolor=COLOR_PRIMARY, # Flechita morada
                        borderwidth=1,
                        relief="solid")
        
        # Mapeo para cuando está activo/readonly (evitar gris)
        style.map('TCombobox', fieldbackground=[('readonly', 'white')],
            selectbackground=[('readonly', 'white')],
            selectforeground=[('readonly', COLOR_TEXT_MAIN)])

        Vista.login(window)
    
    @staticmethod
    def borrarPantalla(window):
        for widget in window.winfo_children():
            if isinstance(widget, tk.Menu): continue
            widget.destroy()

    @staticmethod
    def btn_moderno(parent, text, command, color=COLOR_PRIMARY, width=15, height=1):
        return tk.Button(parent, text=text, command=command,
            bg=color, fg="white", font=("Segoe UI", 10, "bold"),
            bd=0, highlightthickness=0, padx=15, pady=10, cursor="hand2",
            activebackground="#4A235A", activeforeground="white")

    # --- HELPER: INPUT VISIBLE ---
    @staticmethod
    def entry_visible(parent, variable, show=None, justify="left"):
        e = tk.Entry(parent, textvariable=variable, show=show, justify=justify,
            font=("Segoe UI", 11), bg="white", bd=1, relief="solid", fg=COLOR_TEXT_MAIN)
        e.config(highlightthickness=1, highlightbackground=COLOR_BORDER, highlightcolor=COLOR_PRIMARY)
        e.pack(fill="x", ipady=6)

    # ==========================================
    # 1. LOGIN
    # ==========================================
    @staticmethod
    def login(window):
        Vista.borrarPantalla(window)
        window.config(menu=tk.Menu(window), bg=BG_APP)
        main_container = tk.Frame(window, bg=BG_APP); main_container.pack(expand=True)
        card = tk.Frame(main_container, bg="white", padx=60, pady=60); card.pack(padx=10, pady=10)
        if Vista.logo_img: tk.Label(card, image=Vista.logo_img, bg="white").pack(pady=(0, 15))
        tk.Label(card, text="Bonitas Fashions", font=("Gabriola", 32, "bold"), bg="white", fg=COLOR_PRIMARY).pack()
        tk.Label(card, text="Bienvenido de nuevo", font=FONT_BODY, bg="white", fg="gray").pack(pady=(0, 30))
        v_cor = tk.StringVar(); v_pas = tk.StringVar()
        tk.Label(card, text="Correo Electrónico", bg="white", font=FONT_BOLD, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        Vista.entry_visible(card, v_cor); tk.Label(card, text="", bg="white").pack()
        tk.Label(card, text="Contraseña", bg="white", font=FONT_BOLD, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        Vista.entry_visible(card, v_pas, "*"); tk.Label(card, text="", bg="white").pack()
        Vista.btn_moderno(card, "INICIAR SESIÓN", lambda: funciones.Funciones.ingresar(window, v_cor.get(), v_pas.get()), width=25).pack(fill="x", pady=10)
        tk.Button(card, text="Crear una cuenta", fg=COLOR_SECONDARY, bg="white", bd=0, cursor="hand2", font=("Segoe UI", 10, "underline"),
            command=lambda: Vista.registro(window)).pack()

    # ==========================================
    # 2. REGISTRO
    # ==========================================
    @staticmethod
    def registro(window):
        Vista.borrarPantalla(window)
        container = tk.Frame(window, bg=BG_APP); container.pack(expand=True, fill="both", padx=20, pady=20)
        card = tk.Frame(container, bg="white", padx=80, pady=60); card.pack()
        tk.Label(card, text="Crear Cuenta", font=("Segoe UI", 26, "bold"), bg="white", fg=COLOR_PRIMARY).pack(pady=(0, 10))
        form_frame = tk.Frame(card, bg="white", width=400); form_frame.pack(fill="x")
        nom = tk.StringVar(); ape = tk.StringVar(); cor = tk.StringVar(); pas = tk.StringVar()
        def row(lbl, var, show=None): tk.Label(form_frame, text=lbl, bg="white", fg=COLOR_TEXT_MAIN, font=FONT_BOLD).pack(anchor="w", pady=(15, 5)); Vista.entry_visible(form_frame, var, show)
        row("Nombre(s)", nom); row("Apellidos", ape); row("Correo Electrónico", cor); row("Contraseña", pas, "*")
        tk.Frame(card, bg="white", height=30).pack() 
        Vista.btn_moderno(card, "GUARDAR REGISTRO", lambda: funciones.Funciones.guardar_usuario(window, nom.get(), ape.get(), cor.get(), pas.get()), width=30).pack(fill="x")
        tk.Button(card, text="Cancelar y Volver", bg="white", fg="gray", bd=0, cursor="hand2", font=("Segoe UI", 10), command=lambda: Vista.login(window)).pack(pady=15)

    # ==========================================
    # 3. MENU PRINCIPAL
    # ==========================================
    @staticmethod
    def menu_principal(window, usuario=None):
        Vista.borrarPantalla(window); window.config(bg=BG_APP)
        nombre = usuario[1] if usuario else "Usuario"; rol = usuario[5] if usuario and len(usuario)>5 else "user"
        nav = tk.Frame(window, bg="white", height=60, padx=30); nav.pack(fill="x")
        if Vista.logo_img: tk.Label(nav, text=" Bonitas Fashions", font=("Gabriola", 22, "bold"), bg="white", fg=COLOR_PRIMARY).pack(side="left")
        tk.Button(nav, text="Cerrar Sesión", bg="white", fg=COLOR_TEXT_MAIN, bd=0, font=FONT_BOLD, cursor="hand2", command=lambda: Vista.login(window)).pack(side="right")
        content = tk.Frame(window, bg=BG_APP); content.pack(expand=True)
        if Vista.logo_img: tk.Label(content, image=Vista.logo_img, bg=BG_APP).pack(pady=10)
        tk.Label(content, text=f"Hola, {nombre}", font=("Gabriola", 48), bg=BG_APP, fg=COLOR_TEXT_MAIN).pack()
        tk.Label(content, text=f"Panel de Control ({rol.upper()})", font=("Segoe UI", 14), bg=BG_APP, fg="gray").pack(pady=(0, 40))
        grid = tk.Frame(content, bg=BG_APP); grid.pack()
        def tile(col, txt, icon_char, cmd):
            f = tk.Frame(grid, bg="white", width=220, height=180, cursor="hand2"); f.grid(row=0, column=col, padx=20); f.pack_propagate(False)
            lbl_icon = tk.Label(f, text=icon_char, font=("Segoe UI", 40), bg="white", fg=COLOR_PRIMARY, cursor="hand2"); lbl_icon.pack(expand=True)
            lbl_txt = tk.Label(f, text=txt, font=("Segoe UI", 14, "bold"), bg="white", fg=COLOR_TEXT_MAIN, cursor="hand2"); lbl_txt.pack(pady=(0, 20))
            for w in [f, lbl_icon, lbl_txt]: w.bind("<Button-1>", lambda e: cmd())
        tile(0, "CLIENTES", "👥", lambda: Vista.interfaz_clientes(window, usuario))
        tile(1, "VENTAS", "🛍️", lambda: Vista.interfaz_ventas(window, usuario))
        tile(2, "REPORTES", "📊", lambda: Vista.interfaz_reportes(window, usuario))

    # ==========================================
    # 4. CLIENTES
    # ==========================================
    @staticmethod
    def interfaz_clientes(window, usuario):
        Vista.borrarPantalla(window)
        header = tk.Frame(window, bg="white", pady=15, padx=30); header.pack(fill="x")
        tk.Button(header, text="⬅ INICIO", bg="white", fg="gray", bd=0, font=FONT_BOLD, command=lambda: Vista.menu_principal(window, usuario)).pack(side="left")
        tk.Label(header, text=" |   CLIENTES", bg="white", fg=COLOR_TEXT_MAIN, font=("Segoe UI", 18, "bold")).pack(side="left")
        Vista.btn_moderno(header, "+ NUEVO CLIENTE", lambda: Vista.modal_cliente(window, usuario, None, tree)).pack(side="right")
        body = tk.Frame(window, bg=BG_APP, padx=30, pady=30); body.pack(fill="both", expand=True)
        toolbar = tk.Frame(body, bg=BG_APP); toolbar.pack(fill="x", pady=(0, 10))
        f_search = tk.Frame(toolbar, bg=COLOR_LILA_INPUT, padx=5, pady=5); f_search.pack(side="left")
        v_bus = tk.StringVar(); e_bus = tk.Entry(f_search, textvariable=v_bus, bg=COLOR_LILA_INPUT, bd=0, font=("Segoe UI", 11), width=30); e_bus.pack(side="left", padx=10)
        tk.Button(f_search, text="✖", bg=BTN_X_COLOR, fg="white", bd=0, font=("Arial", 8, "bold"), width=3, cursor="hand2", command=lambda: [v_bus.set(""), funciones.Funciones.llenar_tabla_clientes(tree, usuario, None)]).pack(side="right")
        tk.Button(f_search, text="🔍", bg=COLOR_LILA_INPUT, bd=0, cursor="hand2", command=lambda: funciones.Funciones.llenar_tabla_clientes(tree, usuario, v_bus.get())).pack(side="right", padx=5)
        border_frame = tk.Frame(body, bg=COLOR_TEXT_MAIN, padx=2, pady=2); border_frame.pack(side="left", fill="both", expand=True)
        cols = ("id", "idu", "nom", "tel", "dir", "cor", "edad")
        tree = ttk.Treeview(border_frame, columns=cols, show="headings")
        headers = ["ID", "Reg.Por", "Nombre", "Teléfono", "Dirección", "Correo", "Edad"]
        for c, h in zip(cols, headers): tree.heading(c, text=h, command=lambda _c=c: funciones.Funciones.ordenar_columna(tree, _c, False))
        tree.column("id", width=40, anchor="center"); tree.column("idu", width=0, stretch=False); tree.column("edad", width=50, anchor="center")
        scrol = ttk.Scrollbar(border_frame, orient="vertical", command=tree.yview); tree.configure(yscroll=scrol.set); tree.pack(side="left", fill="both", expand=True); scrol.pack(side="right", fill="y")
        actions = tk.Frame(body, bg=BG_APP, width=150); actions.pack(side="right", fill="y", padx=(15, 0)); actions.pack_propagate(False)
        tk.Label(actions, text="Opciones", bg=BG_APP, fg=COLOR_TEXT_MAIN, font=FONT_BOLD).pack(pady=(0, 10))
        def get_sel(): sel = tree.selection(); return tree.item(sel) if sel else None
        Vista.btn_moderno(actions, "Editar", lambda: Vista.modal_cliente(window, usuario, get_sel(), tree) if get_sel() else messagebox.showinfo("!", "Selecciona"), BTN_EDIT_COLOR).pack(fill="x", pady=5)
        Vista.btn_moderno(actions, "Eliminar", lambda: funciones.Funciones.borrar_cliente_tabla(window, usuario, get_sel()['text'], tree) if get_sel() else messagebox.showinfo("!", "Selecciona"), BTN_DELETE_COLOR).pack(fill="x", pady=5)
        e_bus.bind("<Return>", lambda e: funciones.Funciones.llenar_tabla_clientes(tree, usuario, v_bus.get()))
        funciones.Funciones.llenar_tabla_clientes(tree, usuario)

    # ==========================================
    # 5. VENTAS
    # ==========================================
    @staticmethod
    def interfaz_ventas(window, usuario):
        Vista.borrarPantalla(window)
        header = tk.Frame(window, bg="white", pady=15, padx=30); header.pack(fill="x")
        tk.Button(header, text="⬅ INICIO", bg="white", fg="gray", bd=0, font=FONT_BOLD, command=lambda: Vista.menu_principal(window, usuario)).pack(side="left")
        tk.Label(header, text=" |   HISTORIAL VENTAS", bg="white", fg=COLOR_TEXT_MAIN, font=("Segoe UI", 18, "bold")).pack(side="left")
        Vista.btn_moderno(header, "+ NUEVA VENTA", lambda: Vista.modal_venta(window, usuario, None, tree)).pack(side="right")
        body = tk.Frame(window, bg=BG_APP, padx=30, pady=30); body.pack(fill="both", expand=True)
        toolbar = tk.Frame(body, bg=BG_APP); toolbar.pack(fill="x", pady=(0, 10))
        f_search = tk.Frame(toolbar, bg=COLOR_LILA_INPUT, padx=5, pady=5); f_search.pack(side="left")
        tk.Label(f_search, text="Fecha (YYYY-MM):", bg=COLOR_LILA_INPUT, fg="gray", font=("Arial", 9)).pack(side="left", padx=5)
        v_fec = tk.StringVar(); e_fec = tk.Entry(f_search, textvariable=v_fec, bg=COLOR_LILA_INPUT, bd=0, font=("Segoe UI", 11), width=15); e_fec.pack(side="left", padx=5)
        tk.Button(f_search, text="✖", bg=BTN_X_COLOR, fg="white", bd=0, font=("Arial", 8, "bold"), width=3, cursor="hand2", command=lambda: [v_fec.set(""), funciones.Funciones.llenar_tabla_ventas(tree, usuario, None)]).pack(side="right")
        tk.Button(f_search, text="🔍", bg=COLOR_LILA_INPUT, bd=0, cursor="hand2", command=lambda: funciones.Funciones.llenar_tabla_ventas(tree, usuario, v_fec.get())).pack(side="right", padx=5)
        border_frame = tk.Frame(body, bg=COLOR_TEXT_MAIN, padx=2, pady=2); border_frame.pack(side="left", fill="both", expand=True)
        cols = ("fol", "vend", "cli", "monto", "pren", "pago", "fecha", "idcli")
        tree = ttk.Treeview(border_frame, columns=cols, show="headings")
        headers = ["Folio", "Vendedor", "Cliente", "Total", "Prendas", "Pago", "Fecha"]
        for c, h in zip(cols[:-1], headers): tree.heading(c, text=h, command=lambda _c=c: funciones.Funciones.ordenar_columna(tree, _c, False))
        tree.column("fol", width=50, anchor="center"); tree.column("monto", width=80, anchor="e"); tree.column("pren", width=60, anchor="center"); tree.column("idcli", width=0, stretch=False)
        scrol = ttk.Scrollbar(border_frame, orient="vertical", command=tree.yview); tree.configure(yscroll=scrol.set); tree.pack(side="left", fill="both", expand=True); scrol.pack(side="right", fill="y")
        actions = tk.Frame(body, bg=BG_APP, width=150); actions.pack(side="right", fill="y", padx=(15, 0)); actions.pack_propagate(False)
        tk.Label(actions, text="Opciones", bg=BG_APP, fg=COLOR_TEXT_MAIN, font=FONT_BOLD).pack(pady=(0, 10))
        def get_sel(): sel = tree.selection(); return tree.item(sel) if sel else None
        Vista.btn_moderno(actions, "Editar", lambda: Vista.modal_venta(window, usuario, get_sel(), tree) if get_sel() else messagebox.showinfo("!", "Selecciona"), BTN_EDIT_COLOR).pack(fill="x", pady=5)
        Vista.btn_moderno(actions, "Anular", lambda: funciones.Funciones.borrar_venta_tabla(window, usuario, get_sel()['text'], tree) if get_sel() else messagebox.showinfo("!", "Selecciona"), BTN_DELETE_COLOR).pack(fill="x", pady=5)
        funciones.Funciones.llenar_tabla_ventas(tree, usuario)

    # ==========================================
    # 6. REPORTES
    # ==========================================
    @staticmethod
    def interfaz_reportes(window, usuario):
        Vista.borrarPantalla(window); rol = usuario[5] if usuario and len(usuario)>5 else "user"
        header = tk.Frame(window, bg="white", pady=15, padx=30); header.pack(fill="x")
        tk.Button(header, text="⬅ INICIO", bg="white", fg="gray", bd=0, font=FONT_BOLD, command=lambda: Vista.menu_principal(window, usuario)).pack(side="left")
        tk.Label(header, text=" |   REPORTES", bg="white", fg=COLOR_TEXT_MAIN, font=("Segoe UI", 18, "bold")).pack(side="left")
        main = tk.Frame(window, bg=BG_APP); main.pack(fill="both", expand=True, padx=40, pady=40); grid = tk.Frame(main, bg=BG_APP); grid.pack()
        def card_rep(col, title, tipo, color):
            f = tk.Frame(grid, bg="white", width=250, height=180, padx=20, pady=20); f.grid(row=0, column=col, padx=20); f.pack_propagate(False)
            tk.Label(f, text=title, font=("Segoe UI", 16, "bold"), bg="white", fg=color).pack(pady=(0, 20))
            Vista.btn_moderno(f, "Exportar Excel", lambda: Vista.generar_exportacion(tipo, "excel", usuario), "#27AE60").pack(fill="x", pady=2)
            Vista.btn_moderno(f, "Exportar PDF", lambda: Vista.generar_exportacion(tipo, "pdf", usuario), "#C0392B").pack(fill="x", pady=2)
        card_rep(0, "Clientes", "clientes", COLOR_PRIMARY); card_rep(1, "Ventas", "ventas", COLOR_PRIMARY)
        if rol == 'admin':
            f = tk.Frame(grid, bg="white", width=250, height=180, padx=20, pady=20); f.grid(row=0, column=2, padx=20); f.pack_propagate(False)
            tk.Label(f, text="Admin", font=("Segoe UI", 16, "bold"), bg="white", fg="red").pack(pady=(0, 20))
            Vista.btn_moderno(f, "Usuarios (Excel)", lambda: Vista.generar_exportacion("usuarios", "excel", usuario), "#333").pack(fill="x", pady=2)
        tk.Button(window, text="⬅ Volver al Menú", bg="#5D6D7E", fg="white", command=lambda: Vista.menu_principal(window, usuario)).pack(pady=30)

    @staticmethod
    def generar_exportacion(tipo, formato, usuario):
        rol = usuario[5]; id_usu = usuario[0]; datos = []; columnas = []; titulo = ""
        if tipo == "clientes":
            raw = clienteBD.ClienteBD.consultar(id_usu, rol); columnas = ["ID", "ID_Usu", "Nombre", "Teléfono", "Dirección", "Correo", "Edad"]
            if rol == 'admin': columnas.append("Vendedor")
            datos = raw; titulo = "Reporte Clientes"
        elif tipo == "ventas":
            raw = ventaBD.VentaBD.consultar_ventas(id_usu, rol)
            datos = [(r[0], r[1], r[2], r[3], r[4], r[5], r[7]) for r in raw]
            columnas = ["Folio", "Cliente", "Monto", "Prendas", "Pago", "Fecha", "Vendedor"]; titulo = "Reporte Ventas"
        elif tipo == "usuarios":
            from model.conexionBD import cursor
            cursor.execute("SELECT id, nombre, apellidos, correo, rol FROM usuarios")
            datos = cursor.fetchall(); columnas = ["ID", "Nombre", "Apellidos", "Correo", "Rol"]; titulo = "Usuarios"
        if formato == "excel": GeneradorReportes.exportar_excel(datos, columnas, tipo)
        elif formato == "pdf": GeneradorReportes.exportar_pdf(datos, columnas, titulo, tipo)

    # --- MODALES (CORREGIDOS CON ESTILO BLANCO) ---
    @staticmethod
    def modal_cliente(parent, usuario, item_editar, tree):
        modal = tk.Toplevel(parent); modal.geometry("400x550"); modal.config(bg="white")
        v_nom = tk.StringVar(); v_tel = tk.StringVar(); v_dir = tk.StringVar(); v_cor = tk.StringVar(); v_edad = tk.IntVar()
        id_cli = None
        tit = "Editar Cliente" if item_editar else "Nuevo Cliente"
        modal.title(tit); tk.Label(modal, text=tit, font=("Segoe UI", 16, "bold"), bg="white", fg=COLOR_PRIMARY).pack(pady=20)
        if item_editar:
            id_cli = item_editar['text']; vals = item_editar['values']
            v_nom.set(vals[2]); v_tel.set(vals[3]); v_dir.set(vals[4]); v_cor.set(vals[5]); v_edad.set(vals[6])
        f = tk.Frame(modal, bg="white", padx=40); f.pack(fill="both")
        def row(t, v): tk.Label(f, text=t, bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0)); Vista.entry_visible(f, v)
        row("Nombre", v_nom); row("Teléfono", v_tel); row("Dirección", v_dir); row("Correo", v_cor); row("Edad", v_edad)
        tk.Frame(modal, bg="white", height=20).pack()
        Vista.btn_moderno(modal, "GUARDAR", lambda: funciones.Funciones.guardar_o_editar_cliente(parent, tree, id_cli, usuario, v_nom.get(), v_tel.get(), v_dir.get(), v_cor.get(), v_edad.get(), modal)).pack(fill="x", padx=40, pady=20)

    @staticmethod
    def modal_venta(parent, usuario, item_editar, tree):
        modal = tk.Toplevel(parent); modal.geometry("400x550"); modal.config(bg="white")
        v_cli = tk.StringVar(); v_monto = tk.DoubleVar(); v_pren = tk.IntVar(value=1); v_met = tk.StringVar(); id_venta = None
        tit = "Editar Venta" if item_editar else "Nueva Venta"
        modal.title(tit); tk.Label(modal, text=tit, font=("Segoe UI", 16, "bold"), bg="white", fg=COLOR_PRIMARY).pack(pady=20)
        rol = usuario[5] if len(usuario)>5 else "user"
        raw = clienteBD.ClienteBD.consultar(usuario[0], rol)
        lista_combo = [f"{c[0]} - {c[2]}" for c in raw]
        if item_editar:
            id_venta = item_editar['text']; vals = item_editar['values']
            v_cli.set(f"{vals[7]} - {vals[2]}"); v_monto.set(str(vals[3]).replace("$","")); v_pren.set(vals[4]); v_met.set(vals[5])
        f = tk.Frame(modal, bg="white", padx=40); f.pack(fill="both")
        
        tk.Label(f, text="Cliente", bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0))
        # Combobox blanco y limpio
        ttk.Combobox(f, textvariable=v_cli, values=lista_combo, state="readonly").pack(fill="x", ipady=5)
        
        def row(t, v): tk.Label(f, text=t, bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0)); Vista.entry_visible(f, v)
        row("Total $", v_monto); row("Prendas", v_pren)
        
        tk.Label(f, text="Pago", bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0))
        c = ttk.Combobox(f, textvariable=v_met, values=["Efectivo", "Tarjeta", "Transferencia"], state="readonly"); c.pack(fill="x", ipady=5)
        if not item_editar: c.current(0)

        btn = "ACTUALIZAR" if item_editar else "COBRAR"
        Vista.btn_moderno(modal, btn, lambda: funciones.Funciones.guardar_o_editar_venta(parent, tree, usuario, id_venta, v_cli.get(), v_monto.get(), v_pren.get(), v_met.get(), modal)).pack(fill="x", padx=40, pady=20)