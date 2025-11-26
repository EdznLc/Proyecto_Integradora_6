import tkinter as tk
from tkinter import messagebox, ttk
import os

# Importaciones del proyecto
from controller import funciones
from controller.reportes import GeneradorReportes
from model import clienteBD

# ==========================================
# CONSTANTES DE DISEÑO (PALETA DE COLORES)
# ==========================================
BG_APP           = "#F3E5F5"
BG_PANEL         = "#FFFFFF"
COLOR_PRIMARY    = "#8E44AD"
COLOR_SECONDARY  = "#9B59B6"
COLOR_TEXT_MAIN  = "#4A235A"
COLOR_LILA_INPUT = "#E8DAEF"
COLOR_BORDER     = "#D2B4DE"

BTN_EDIT_COLOR   = "#5B2C6F"
BTN_DELETE_COLOR = "#943126"
BTN_SUCCESS_COLOR= "#27AE60"
BTN_DANGER_COLOR = "#C0392B"

FONT_TITLE       = ("Segoe UI", 28, "bold")
FONT_SUBTITLE    = ("Segoe UI", 16)
FONT_BODY        = ("Segoe UI", 11)
FONT_BOLD        = ("Segoe UI", 11, "bold")
FONT_ICON        = ("Segoe UI", 40)

class Vista:
    """
    Clase principal de la Interfaz Gráfica.
    """
    logo_img = None 

    def __init__(self, window):
        self.window = window
        self._configurar_ventana()
        self._cargar_recursos()
        self._configurar_estilos()
        Vista.login(window)

    def _configurar_ventana(self):
        self.window.title("Bonitas Fashions - Manager System")
        self.window.geometry("1200x800")
        self.window.config(bg=BG_APP)

    def _cargar_recursos(self):
        try:
            if os.path.exists("logo.png"):
                img_temp = tk.PhotoImage(file="logo.png")
                Vista.logo_img = img_temp.subsample(3, 3) 
        except Exception as e:
            print(f"Nota: No se encontró logo.png ({e})")

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Estilo Tabla
        style.configure("Treeview", background="white", foreground="#333", rowheight=35, fieldbackground="white", borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#E8DAEF", foreground=COLOR_TEXT_MAIN, borderwidth=0, font=("Segoe UI", 11, "bold"))
        style.map('Treeview', background=[('selected', COLOR_PRIMARY)])
        
        # Estilo Combobox
        style.configure("TCombobox", fieldbackground="white", background="white", arrowcolor=COLOR_PRIMARY, borderwidth=1, relief="solid")
        style.map('TCombobox', fieldbackground=[('readonly', 'white')], selectbackground=[('readonly', 'white')], selectforeground=[('readonly', COLOR_TEXT_MAIN)])

    # ==========================================
    # HERRAMIENTAS (HELPERS)
    # ==========================================
    @staticmethod
    def borrar_pantalla(window):
        for widget in window.winfo_children():
            if isinstance(widget, tk.Menu): continue
            widget.destroy()

    @staticmethod
    def crear_boton(parent, text, command, color=COLOR_PRIMARY, width=15):
        return tk.Button(parent, text=text, command=command, bg=color, fg="white", font=("Segoe UI", 10, "bold"),
            bd=0, highlightthickness=0, padx=15, pady=10, cursor="hand2", width=width, activebackground="#4A235A", activeforeground="white")

    # --- VALIDADORES ---
    @staticmethod
    def validar_solo_numeros(texto):
        if texto == "": return True
        if texto.isdigit(): return True
        return False

    @staticmethod
    def validar_decimales(texto):
        if texto == "": return True
        try: float(texto); return True
        except ValueError: return False

    @staticmethod
    def validar_telefono(texto):
        if texto == "": return True
        if texto.isdigit() and len(texto) <= 10: return True
        return False

    @staticmethod
    def crear_input(parent, variable, show=None, justify="left", validacion=None):
        vcmd = None
        if validacion == "int":
            func = parent.register(Vista.validar_solo_numeros)
            vcmd = (func, '%P')
        elif validacion == "float":
            func = parent.register(Vista.validar_decimales)
            vcmd = (func, '%P')
        elif validacion == "tel":
            func = parent.register(Vista.validar_telefono)
            vcmd = (func, '%P')

        entry = tk.Entry(parent, textvariable=variable, show=show, justify=justify, font=("Segoe UI", 11), 
            bg="white", bd=1, relief="solid", fg=COLOR_TEXT_MAIN, validate="key" if validacion else "none", validatecommand=vcmd)
        entry.config(highlightthickness=1, highlightbackground=COLOR_BORDER, highlightcolor=COLOR_PRIMARY)
        entry.pack(fill="x", ipady=6)
        return entry

    # ==========================================
    # 1. LOGIN & REGISTRO ADMIN
    # ==========================================
    @staticmethod
    def login(window):
        Vista.borrar_pantalla(window)
        window.config(menu=tk.Menu(window), bg=BG_APP)
        
        main_container = tk.Frame(window, bg=BG_APP); main_container.pack(expand=True)
        card = tk.Frame(main_container, bg="white", padx=60, pady=60); card.pack(padx=10, pady=10)
        
        if Vista.logo_img: tk.Label(card, image=Vista.logo_img, bg="white").pack(pady=(0, 15))
        tk.Label(card, text="Bonitas Fashions", font=("Gabriola", 32, "bold"), bg="white", fg=COLOR_PRIMARY).pack()
        
        v_cor = tk.StringVar(); v_pas = tk.StringVar()
        tk.Label(card, text="Correo Electrónico", bg="white", font=FONT_BOLD, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        Vista.crear_input(card, v_cor)
        tk.Label(card, text="Contraseña", bg="white", font=FONT_BOLD, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(10,0))
        Vista.crear_input(card, v_pas, show="*")
        
        tk.Frame(card, bg="white", height=20).pack()
        Vista.crear_boton(card, "INICIAR SESIÓN", lambda: funciones.Funciones.ingresar(window, v_cor.get(), v_pas.get()), width=25).pack(fill="x")

    @staticmethod
    def modal_usuario(parent):
        """Registrar Usuario (ADMIN ONLY)"""
        modal = tk.Toplevel(parent)
        modal.geometry("400x500")
        modal.config(bg="white")
        modal.title("Registrar Nuevo Usuario")
        
        tk.Label(modal, text="Nuevo Usuario", font=("Segoe UI", 16, "bold"), bg="white", fg=COLOR_PRIMARY).pack(pady=20)
        f = tk.Frame(modal, bg="white", padx=40); f.pack(fill="both")
        
        v_user = tk.StringVar(); v_cor = tk.StringVar(); v_pas = tk.StringVar(); v_rol = tk.StringVar(value="usuario")

        def crear_fila(texto, variable, show=None):
            tk.Label(f, text=texto, bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0))
            Vista.crear_input(f, variable, show=show)

        crear_fila("Nombre de Usuario (Username)", v_user)
        crear_fila("Correo Electrónico", v_cor)
        crear_fila("Contraseña", v_pas, "*")
        
        tk.Label(f, text="Rol del Sistema", bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0))
        ttk.Combobox(f, textvariable=v_rol, values=["usuario", "admin"], state="readonly").pack(fill="x", ipady=5)
        
        tk.Frame(modal, bg="white", height=20).pack()
        Vista.crear_boton(modal, "CREAR USUARIO", 
            lambda: funciones.Funciones.guardar_usuario_admin(parent, v_user.get(), v_cor.get(), v_pas.get(), v_rol.get(), modal)).pack(fill="x", padx=40, pady=20)

    # ==========================================
    # 2. DASHBOARD
    # ==========================================
    @staticmethod
    def menu_principal(window, usuario=None):
        Vista.borrar_pantalla(window); window.config(bg=BG_APP)
        nombre_usu = usuario[1] if usuario else "Usuario"
        rol_usu = usuario[5] if usuario and len(usuario)>5 else "user"

        # Header
        nav = tk.Frame(window, bg="white", height=60, padx=30); nav.pack(fill="x")
        if Vista.logo_img: tk.Label(nav, text=" Bonitas Fashions", font=("Gabriola", 22, "bold"), bg="white", fg=COLOR_PRIMARY).pack(side="left")
        tk.Button(nav, text="Cerrar Sesión", bg="white", fg=COLOR_TEXT_MAIN, bd=0, font=FONT_BOLD, cursor="hand2", command=lambda: Vista.login(window)).pack(side="right")
        
        # Contenido
        content = tk.Frame(window, bg=BG_APP); content.pack(expand=True)
        if Vista.logo_img: tk.Label(content, image=Vista.logo_img, bg=BG_APP).pack(pady=10)
        
        tk.Label(content, text=f"Hola, {nombre_usu}", font=("Gabriola", 48), bg=BG_APP, fg=COLOR_TEXT_MAIN).pack()
        tk.Label(content, text=f"Panel de Control ({rol_usu.upper()})", font=("Segoe UI", 14), bg=BG_APP, fg="gray").pack(pady=(0, 40))
        
        grid = tk.Frame(content, bg=BG_APP); grid.pack()
        
        def crear_tile(col, texto, icono, comando):
            f = tk.Frame(grid, bg="white", width=220, height=180, cursor="hand2"); f.grid(row=0, column=col, padx=20); f.pack_propagate(False)
            tk.Label(f, text=icono, font=FONT_ICON, bg="white", fg=COLOR_PRIMARY).pack(expand=True)
            tk.Label(f, text=texto, font=("Segoe UI", 14, "bold"), bg="white", fg=COLOR_TEXT_MAIN).pack(pady=(0, 20))
            for w in [f] + f.winfo_children(): w.bind("<Button-1>", lambda e: comando())

        crear_tile(0, "CLIENTES", "👥", lambda: Vista.interfaz_clientes(window, usuario))
        crear_tile(1, "VENTAS", "🛍️", lambda: Vista.interfaz_ventas(window, usuario))
        crear_tile(2, "REPORTES", "📊", lambda: Vista.interfaz_reportes(window, usuario))
        if rol_usu == 'admin': crear_tile(3, "USUARIOS", "🔐", lambda: Vista.modal_usuario(window))

    # ==========================================
    # 3. CLIENTES
    # ==========================================
    @staticmethod
    def interfaz_clientes(window, usuario):
        Vista.borrar_pantalla(window)
        # Header
        header = tk.Frame(window, bg="white", pady=15, padx=30); header.pack(fill="x")
        tk.Button(header, text="⬅ INICIO", bg="white", fg="gray", bd=0, font=FONT_BOLD, command=lambda: Vista.menu_principal(window, usuario)).pack(side="left")
        tk.Label(header, text=" |   CLIENTES", bg="white", fg=COLOR_TEXT_MAIN, font=("Segoe UI", 18, "bold")).pack(side="left")
        Vista.crear_boton(header, "+ NUEVO CLIENTE", lambda: Vista.modal_cliente(window, usuario, None, tree)).pack(side="right")
        
        # Body
        body = tk.Frame(window, bg=BG_APP, padx=30, pady=30); body.pack(fill="both", expand=True)
        toolbar = tk.Frame(body, bg=BG_APP); toolbar.pack(fill="x", pady=(0, 10))
        
        v_bus = tk.StringVar(); e_bus = tk.Entry(toolbar, textvariable=v_bus, width=30); e_bus.pack(side="left")
        tk.Button(toolbar, text="🔍", command=lambda: funciones.Funciones.llenar_tabla_clientes(tree, usuario, v_bus.get())).pack(side="left", padx=5)
        tk.Button(toolbar, text="✖", bg=BTN_DANGER_COLOR, fg="white", command=lambda: [v_bus.set(""), funciones.Funciones.llenar_tabla_clientes(tree, usuario)]).pack(side="left")

        # Tabla
        cols = ("id", "idu", "nom", "tel", "dir", "cor", "edad")
        tree = ttk.Treeview(body, columns=cols, show="headings")
        headers = ["ID", "Reg.Por", "Nombre Completo", "Teléfono", "Dirección", "Correo", "Edad"]
        for c, h in zip(cols, headers): tree.heading(c, text=h, command=lambda _c=c: funciones.Funciones.ordenar_columna(tree, _c, False))
        
        tree.column("id", width=40, anchor="center")
        tree.column("idu", width=0, stretch=False)
        tree.column("nom", anchor="w")      # Nombre a la izquierda
        tree.column("tel", anchor="center") # Telefono al centro
        tree.column("dir", anchor="w")      # Dirección a la izquierda
        tree.column("cor", anchor="center") # Correo al centro
        tree.column("edad", width=50, anchor="center")
        tree.pack(side="left", fill="both", expand=True)
        
        # Acciones
        actions = tk.Frame(body, bg=BG_APP, width=150); actions.pack(side="right", fill="y", padx=(15, 0)); actions.pack_propagate(False)
        def get_sel(): return tree.item(tree.selection()) if tree.selection() else None
        Vista.crear_boton(actions, "Editar", lambda: Vista.modal_cliente(window, usuario, get_sel(), tree) if get_sel() else messagebox.showwarning("Atención", "Seleccione un registro"), BTN_EDIT_COLOR).pack(fill="x", pady=5)
        Vista.crear_boton(actions, "Eliminar", lambda: funciones.Funciones.borrar_cliente_tabla(window, usuario, get_sel()['text'], tree) if get_sel() else messagebox.showwarning("Atención", "Seleccione un registro"), BTN_DELETE_COLOR).pack(fill="x", pady=5)
        
        funciones.Funciones.llenar_tabla_clientes(tree, usuario)

    @staticmethod
    def modal_cliente(parent, usuario, item_editar, tree, callback=None):
        modal = tk.Toplevel(parent); modal.geometry("400x650"); modal.config(bg="white")
        v_nom = tk.StringVar(); v_pat = tk.StringVar(); v_mat = tk.StringVar()
        v_tel = tk.StringVar(); v_dir = tk.StringVar(); v_cor = tk.StringVar(); v_edad = tk.StringVar()
        id_cli = None; tit = "Nuevo Cliente"

        if item_editar:
            tit = "Editar Cliente"; id_cli = item_editar['text']; vals = item_editar['values']
            partes = vals[2].split(" ")
            v_nom.set(partes[0] if len(partes)>0 else "")
            v_pat.set(partes[1] if len(partes)>1 else "")
            v_tel.set(vals[3]); v_dir.set(vals[4]); v_cor.set(vals[5]); v_edad.set(vals[6])

        tk.Label(modal, text=tit, font=("Segoe UI", 16, "bold"), bg="white", fg=COLOR_PRIMARY).pack(pady=10)
        f = tk.Frame(modal, bg="white", padx=40); f.pack(fill="both")
        
        def crear_fila(texto, variable, validacion=None): 
            tk.Label(f, text=texto, bg="white", fg="gray", anchor="w").pack(fill="x", pady=(5,0))
            Vista.crear_input(f, variable, validacion=validacion)
        
        crear_fila("Nombre(s)", v_nom)
        crear_fila("Apellido Paterno", v_pat)
        crear_fila("Apellido Materno (Opcional)", v_mat)
        crear_fila("Teléfono", v_tel, "tel")
        crear_fila("Dirección", v_dir)
        crear_fila("Correo Electrónico", v_cor)
        crear_fila("Edad", v_edad, "int")
        
        tk.Frame(modal, bg="white", height=10).pack()
        Vista.crear_boton(modal, "GUARDAR", lambda: funciones.Funciones.guardar_o_editar_cliente(
            parent, tree, id_cli, usuario, v_nom.get(), v_pat.get(), v_mat.get(), v_tel.get(), v_dir.get(), v_cor.get(), v_edad.get(), modal, callback)).pack(fill="x", padx=40, pady=20)

    # ==========================================
    # 4. VENTAS
    # ==========================================
    @staticmethod
    def interfaz_ventas(window, usuario):
        Vista.borrar_pantalla(window)
        # Header
        header = tk.Frame(window, bg="white", pady=15, padx=30); header.pack(fill="x")
        tk.Button(header, text="⬅ INICIO", bg="white", fg="gray", bd=0, font=FONT_BOLD, command=lambda: Vista.menu_principal(window, usuario)).pack(side="left")
        tk.Label(header, text=" |   HISTORIAL VENTAS", bg="white", fg=COLOR_TEXT_MAIN, font=("Segoe UI", 18, "bold")).pack(side="left")
        Vista.crear_boton(header, "+ NUEVA VENTA", lambda: Vista.modal_venta(window, usuario, None, tree)).pack(side="right")
        
        # Body
        body = tk.Frame(window, bg=BG_APP, padx=30, pady=30); body.pack(fill="both", expand=True)
        
        # Buscador Simple con Etiqueta
        toolbar = tk.Frame(body, bg=BG_APP); toolbar.pack(fill="x", pady=(0, 10))
        tk.Label(toolbar, text="Filtrar por Fecha (YYYY-MM):", bg=BG_APP, fg=COLOR_TEXT_MAIN, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 5))
        
        v_fec = tk.StringVar()
        e_fec = tk.Entry(toolbar, textvariable=v_fec, width=20)
        e_fec.pack(side="left")
        
        tk.Button(toolbar, text="🔍", command=lambda: funciones.Funciones.llenar_tabla_ventas(tree, usuario, v_fec.get())).pack(side="left", padx=5)
        tk.Button(toolbar, text="✖", bg=BTN_DANGER_COLOR, fg="white", command=lambda: [v_fec.set(""), funciones.Funciones.llenar_tabla_ventas(tree, usuario, None)]).pack(side="left")

        # Tabla
        cols = ("fol", "vend", "cli", "monto", "pren", "pago", "fecha", "idcli")
        tree = ttk.Treeview(body, columns=cols, show="headings")
        headers = ["Folio", "Vendedor", "Cliente", "Total", "Prendas", "Pago", "Fecha"]
        for c, h in zip(cols[:-1], headers): tree.heading(c, text=h, command=lambda _c=c: funciones.Funciones.ordenar_columna(tree, _c, False))
        
        tree.column("fol", width=50, anchor="center")
        tree.column("vend", anchor="w")        # Vendedor Izquierda
        tree.column("cli", anchor="w")         # Cliente Izquierda
        tree.column("monto", width=80, anchor="center") # Centrado
        tree.column("pren", width=60, anchor="center")  # Centrado
        tree.column("pago", anchor="center")   # Centrado
        tree.column("fecha", anchor="center")  # Centrado
        tree.column("idcli", width=0, stretch=False) # Oculto

        tree.pack(side="left", fill="both", expand=True)
        
        # Acciones
        actions = tk.Frame(body, bg=BG_APP, width=150); actions.pack(side="right", fill="y", padx=(15, 0)); actions.pack_propagate(False)
        def get_sel(): return tree.item(tree.selection()) if tree.selection() else None
        Vista.crear_boton(actions, "Editar", lambda: Vista.modal_venta(window, usuario, get_sel(), tree) if get_sel() else messagebox.showwarning("Atención", "Seleccione un registro"), BTN_EDIT_COLOR).pack(fill="x", pady=5)
        Vista.crear_boton(actions, "Anular", lambda: funciones.Funciones.borrar_venta_tabla(window, usuario, get_sel()['text'], tree) if get_sel() else messagebox.showwarning("Atención", "Seleccione un registro"), BTN_DELETE_COLOR).pack(fill="x", pady=5)
        
        e_fec.bind("<Return>", lambda e: funciones.Funciones.llenar_tabla_ventas(tree, usuario, v_fec.get()))
        funciones.Funciones.llenar_tabla_ventas(tree, usuario)

    @staticmethod
    def modal_venta(parent, usuario, item_editar, tree):
        modal = tk.Toplevel(parent); modal.geometry("400x600"); modal.config(bg="white"); tit="Nueva Venta"; id_venta=None
        v_cli = tk.StringVar(); v_monto = tk.StringVar(); v_pren = tk.StringVar(value="1"); v_met = tk.StringVar()

        rol = usuario[5] if len(usuario)>5 else "user"
        data_cli = clienteBD.ClienteBD.consultar(usuario[0], rol)
        lista_combo = [f"{c[0]} - {c[2]}" for c in data_cli]

        if item_editar:
            tit = "Editar Venta"; id_venta = item_editar['text']; vals = item_editar['values']
            try: 
                v_cli.set(f"{vals[7]} - {vals[2]}")
                v_monto.set(str(vals[3]).replace("$",""))
                v_pren.set(vals[4])
                v_met.set(vals[5])
            except IndexError:
                messagebox.showerror("Error", "Faltan datos ocultos.")
                modal.destroy(); return

        def recargar_combo():
            d_new = clienteBD.ClienteBD.consultar(usuario[0], rol)
            l_new = [f"{c[0]} - {c[2]}" for c in d_new]
            combo['values'] = l_new; 
            if l_new: combo.current(len(l_new)-1)

        tk.Label(modal, text=tit, font=("Segoe UI", 16, "bold"), bg="white", fg=COLOR_PRIMARY).pack(pady=20)
        f = tk.Frame(modal, bg="white", padx=40); f.pack(fill="both")
        
        tk.Label(f, text="Cliente", bg="white", fg="gray", anchor="w").pack(fill="x")
        fc = tk.Frame(f, bg="white"); fc.pack(fill="x")
        combo = ttk.Combobox(fc, textvariable=v_cli, values=lista_combo, state="readonly"); combo.pack(side="left", fill="x", expand=True)
        if not item_editar: tk.Button(fc, text="➕", bg="#27AE60", fg="white", bd=0, command=lambda: Vista.modal_cliente(parent, usuario, None, None, callback=recargar_combo)).pack(side="left", padx=5)

        tk.Label(f, text="Monto ($)", bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0))
        Vista.crear_input(f, v_monto, validacion="float")
        tk.Label(f, text="Prendas", bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0))
        Vista.crear_input(f, v_pren, validacion="int")
        
        tk.Label(f, text="Método Pago", bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0))
        c_pay = ttk.Combobox(f, textvariable=v_met, values=["Efectivo", "Tarjeta", "Transferencia"], state="readonly"); c_pay.pack(fill="x", ipady=5)
        if not item_editar: c_pay.current(0)
        
        tk.Frame(modal, bg="white", height=20).pack()
        Vista.crear_boton(modal, "GUARDAR", lambda: funciones.Funciones.guardar_o_editar_venta(parent, tree, usuario, id_venta, v_cli.get(), v_monto.get(), v_pren.get(), v_met.get(), modal)).pack(fill="x", padx=40, pady=20)

    # ==========================================
    # 5. REPORTES
    # ==========================================
    @staticmethod
    def interfaz_reportes(window, usuario):
        Vista.borrar_pantalla(window)
        header = tk.Frame(window, bg="white", pady=15, padx=30); header.pack(fill="x")
        tk.Button(header, text="⬅ INICIO", bg="white", fg="gray", bd=0, font=FONT_BOLD, command=lambda: Vista.menu_principal(window, usuario)).pack(side="left")
        
        grid = tk.Frame(window, bg=BG_APP); grid.pack(expand=True)
        def crear_tarjeta(col, tit, tipo, color):
            f = tk.Frame(grid, bg="white", width=250, height=180, padx=20, pady=20); f.grid(row=0, column=col, padx=20); f.pack_propagate(False)
            tk.Label(f, text=tit, font=("Segoe UI", 16, "bold"), bg="white", fg=color).pack(pady=(0,20))
            Vista.crear_boton(f, "Excel", lambda: Vista.generar_exportacion(tipo, "excel", usuario), BTN_SUCCESS_COLOR).pack(fill="x", pady=2)
            Vista.crear_boton(f, "PDF", lambda: Vista.generar_exportacion(tipo, "pdf", usuario), BTN_DANGER_COLOR).pack(fill="x", pady=2)

        crear_tarjeta(0, "Clientes", "clientes", COLOR_PRIMARY)
        crear_tarjeta(1, "Ventas", "ventas", COLOR_PRIMARY)
        if usuario[5] == 'admin': crear_tarjeta(2, "Usuarios", "usuarios", "red")

    @staticmethod
    def generar_exportacion(tipo, fmt, usuario):
        from controller.reportes import GeneradorReportes
        GeneradorReportes.generar(tipo, fmt, usuario)