import tkinter as tk
from tkinter import messagebox, ttk
import os

# Importaciones del proyecto (Controladores y Modelos)
from controller import funciones
from controller.reportes import GeneradorReportes
from model import clienteBD, ventaBD
# Nota: La importación de 'cursor' se maneja dentro de reportes para evitar ciclos, 
# pero idealmente debería estar en un archivo de consultas separado.

# ==========================================
# CONSTANTES DE DISEÑO (PALETA DE COLORES)
# ==========================================
BG_APP           = "#F3E5F5"  # Fondo general lila muy claro
BG_PANEL         = "#FFFFFF"  # Fondo blanco para tarjetas/paneles
COLOR_PRIMARY    = "#8E44AD"  # Morado principal
COLOR_SECONDARY  = "#9B59B6"  # Morado secundario
COLOR_TEXT_MAIN  = "#4A235A"  # Texto oscuro (morado casi negro)
COLOR_LILA_INPUT = "#E8DAEF"  # Fondo para inputs o headers de tabla
COLOR_BORDER     = "#D2B4DE"  # Bordes suaves

# Colores de Botones de Acción
BTN_EDIT_COLOR   = "#5B2C6F"  # Morado oscuro para editar
BTN_DELETE_COLOR = "#943126"  # Rojo ladrillo para borrar/anular
BTN_SUCCESS_COLOR= "#27AE60"  # Verde para excel
BTN_DANGER_COLOR = "#C0392B"  # Rojo brillante para PDF/Cerrar

# Fuentes
FONT_TITLE       = ("Segoe UI", 28, "bold")
FONT_SUBTITLE    = ("Segoe UI", 16)
FONT_BODY        = ("Segoe UI", 11)
FONT_BOLD        = ("Segoe UI", 11, "bold")
FONT_ICON        = ("Segoe UI", 40) # Para los emojis/iconos grandes

class Vista:
    """
    Clase principal que maneja toda la interfaz gráfica (GUI).
    Todos los métodos son estáticos para ser llamados desde el controlador 
    sin necesidad de instanciar la clase múltiples veces.
    """
    logo_img = None 

    def __init__(self, window):
        self.window = window
        self._configurar_ventana()
        self._cargar_recursos()
        self._configurar_estilos()
        
        # Iniciar en la pantalla de Login
        Vista.login(window)

    def _configurar_ventana(self):
        """Configuración básica de la ventana principal"""
        self.window.title("Bonitas Fashions - Manager System")
        self.window.geometry("1200x800")
        self.window.config(bg=BG_APP)

    def _cargar_recursos(self):
        """Carga de imágenes y recursos externos"""
        try:
            if os.path.exists("logo.png"):
                img_temp = tk.PhotoImage(file="logo.png")
                # Subsample reduce la imagen (3 veces más pequeña)
                Vista.logo_img = img_temp.subsample(3, 3) 
        except Exception as e:
            print(f"Advertencia: No se pudo cargar 'logo.png'. Error: {e}")

    def _configurar_estilos(self):
        """Definición de estilos personalizados para Treeview y Combobox"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # --- Estilo de Tabla (Treeview) ---
        style.configure("Treeview", 
                        background="white", 
                        foreground="#333", 
                        rowheight=35, 
                        fieldbackground="white", 
                        borderwidth=0, 
                        font=("Segoe UI", 10))
        
        style.configure("Treeview.Heading", 
                        background="#E8DAEF", 
                        foreground=COLOR_TEXT_MAIN, 
                        borderwidth=0, 
                        font=("Segoe UI", 11, "bold"))
        
        # Color al seleccionar una fila
        style.map('Treeview', background=[('selected', COLOR_PRIMARY)])
        
        # --- Estilo de Combobox (Lista desplegable) ---
        style.configure("TCombobox", 
                        fieldbackground="white", 
                        background="white", 
                        arrowcolor=COLOR_PRIMARY, 
                        borderwidth=1,
                        relief="solid")
        
        # Evitar que se ponga gris cuando es 'readonly'
        style.map('TCombobox', 
                        fieldbackground=[('readonly', 'white')],
                        selectbackground=[('readonly', 'white')],
                        selectforeground=[('readonly', COLOR_TEXT_MAIN)])

    # ==========================================
    # HELPER METHODS (COMPONENTES REUTILIZABLES)
    # ==========================================
    
    @staticmethod
    def borrar_pantalla(window):
        """Limpia todos los widgets de la ventana actual"""
        for widget in window.winfo_children():
            if isinstance(widget, tk.Menu): 
                continue # No borrar el menú superior si existe
            widget.destroy()

    @staticmethod
    def crear_boton(parent, text, command, color=COLOR_PRIMARY, width=15):
        """Crea un botón con el estilo moderno de la app"""
        return tk.Button(parent, 
            text=text, 
            command=command,
            bg=color, 
            fg="white", 
            font=("Segoe UI", 10, "bold"),
            bd=0, 
            highlightthickness=0, 
            padx=15, 
            pady=10, 
            cursor="hand2",
            width=width,
            activebackground="#4A235A", # Color al presionar
            activeforeground="white")

    @staticmethod
    def crear_input(parent, variable, show=None, justify="left", validacion=None):
        # Configuramos la validación (si se pide)
        vcmd = None
        if validacion == "int":
            func_val = parent.register(Vista.validar_solo_numeros)
            vcmd = (func_val, '%P')
        elif validacion == "float":
            func_val = parent.register(Vista.validar_decimales)
            vcmd = (func_val, '%P')

        # Creamos el input con la configuración de validación
        entry = tk.Entry(parent, 
            textvariable=variable, 
            show=show, 
            justify=justify,
            font=("Segoe UI", 11), 
            bg="white", 
            bd=1, 
            relief="solid", 
            fg=COLOR_TEXT_MAIN,
            validate="key" if validacion else "none", # Activar validación al teclear
            validatecommand=vcmd)
        
        entry.config(highlightthickness=1, 
            highlightbackground=COLOR_BORDER, 
            highlightcolor=COLOR_PRIMARY)
        entry.pack(fill="x", ipady=6) 
        return entry

    # --- VALIDADORES DE TEXTO ---
    @staticmethod
    def validar_solo_numeros(texto_nuevo):
        """
        Permite solo números enteros Y un máximo de 10 caracteres.
        Ideal para teléfonos móviles.
        """
        # 1. Si está vacío (borrando), permitir.
        if texto_nuevo == "":
            return True
            
        # 2. Revisar que sean dígitos Y que no se pase de 10 caracteres
        if texto_nuevo.isdigit() and len(texto_nuevo) <= 10:
            return True
            
        # Si llega aquí (es letra o son 11+ caracteres), bloquear.
        return False

    @staticmethod
    def validar_decimales(texto_nuevo):
        """Permite números y un punto decimal (Ej: Precio)"""
        if texto_nuevo == "": return True
        try:
            float(texto_nuevo)
            return True
        except ValueError:
            return False

    # ==========================================
    # 1. AUTENTICACIÓN (LOGIN Y REGISTRO)
    # ==========================================
    
    @staticmethod
    def login(window):
        Vista.borrar_pantalla(window)
        window.config(menu=tk.Menu(window), bg=BG_APP) # Resetear menú y fondo
        
        # Contenedor central
        main_container = tk.Frame(window, bg=BG_APP)
        main_container.pack(expand=True)
        
        # Tarjeta blanca
        card = tk.Frame(main_container, bg="white", padx=60, pady=60)
        card.pack(padx=10, pady=10)
        
        # Logo y Título
        if Vista.logo_img: 
            tk.Label(card, image=Vista.logo_img, bg="white").pack(pady=(0, 15))
            
        tk.Label(card, text="Bonitas Fashions", font=("Gabriola", 32, "bold"), bg="white", fg=COLOR_PRIMARY).pack()
        tk.Label(card, text="Bienvenido de nuevo", font=FONT_BODY, bg="white", fg="gray").pack(pady=(0, 30))
        
        # Variables
        var_correo = tk.StringVar()
        var_pass = tk.StringVar()
        
        # Formulario
        tk.Label(card, text="Correo Electrónico", bg="white", font=FONT_BOLD, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        Vista.crear_input(card, var_correo)
        tk.Label(card, text="", bg="white").pack() # Espaciador
        
        tk.Label(card, text="Contraseña", bg="white", font=FONT_BOLD, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        Vista.crear_input(card, var_pass, show="*")
        tk.Label(card, text="", bg="white").pack() # Espaciador
        
        # Botones
        Vista.crear_boton(card, "INICIAR SESIÓN", 
            lambda: funciones.Funciones.ingresar(window, var_correo.get(), var_pass.get()), 
            width=25).pack(fill="x", pady=10)
    
    @staticmethod
    def registro(window):
        Vista.borrar_pantalla(window)
        
        container = tk.Frame(window, bg=BG_APP)
        container.pack(expand=True, fill="both", padx=20, pady=20)
        
        card = tk.Frame(container, bg="white", padx=80, pady=60)
        card.pack()
        
        tk.Label(card, text="Crear Cuenta", font=("Segoe UI", 26, "bold"), bg="white", fg=COLOR_PRIMARY).pack(pady=(0, 10))
        
        form_frame = tk.Frame(card, bg="white", width=400)
        form_frame.pack(fill="x")
        
        # Variables
        var_nom = tk.StringVar()
        var_ape = tk.StringVar()
        var_cor = tk.StringVar()
        var_pas = tk.StringVar()
        
        # Helper interno para filas del formulario
        def crear_fila(label_text, variable, show_char=None):
            tk.Label(form_frame, text=label_text, bg="white", fg=COLOR_TEXT_MAIN, font=FONT_BOLD).pack(anchor="w", pady=(15, 5))
            Vista.crear_input(form_frame, variable, show_char)

        crear_fila("Nombre(s)", var_nom)
        crear_fila("Apellidos", var_ape)
        crear_fila("Correo Electrónico", var_cor)
        crear_fila("Contraseña", var_pas, "*")
        
        tk.Frame(card, bg="white", height=30).pack() # Espaciador
        
        Vista.crear_boton(card, "GUARDAR REGISTRO", 
            lambda: funciones.Funciones.guardar_usuario(window, var_nom.get(), var_ape.get(), var_cor.get(), var_pas.get()), 
            width=30).pack(fill="x")
        
        tk.Button(card, text="Cancelar y Volver", bg="white", fg="gray", bd=0, cursor="hand2", 
            font=("Segoe UI", 10), 
            command=lambda: Vista.login(window)).pack(pady=15)

    # ==========================================
    # 2. DASHBOARD / MENÚ PRINCIPAL
    # ==========================================
    
    @staticmethod
    def menu_principal(window, usuario=None):
        Vista.borrar_pantalla(window)
        window.config(bg=BG_APP)
        
        # Extracción de datos de usuario de forma segura
        nombre_usu = usuario[1] if usuario else "Usuario"
        # Asumiendo que el rol está en la posición 5
        rol_usu = usuario[5] if usuario and len(usuario) > 5 else "user"

        # --- Barra de Navegación Superior ---
        nav = tk.Frame(window, bg="white", height=60, padx=30)
        nav.pack(fill="x")
        
        if Vista.logo_img: 
            tk.Label(nav, text=" Bonitas Fashions", font=("Gabriola", 22, "bold"), bg="white", fg=COLOR_PRIMARY).pack(side="left")
            
        tk.Button(nav, text="Cerrar Sesión", bg="white", fg=COLOR_TEXT_MAIN, bd=0, font=FONT_BOLD, cursor="hand2", 
            command=lambda: Vista.login(window)).pack(side="right")
        
        # --- Contenido Principal ---
        content = tk.Frame(window, bg=BG_APP)
        content.pack(expand=True)
        
        if Vista.logo_img: 
            tk.Label(content, image=Vista.logo_img, bg=BG_APP).pack(pady=10)
            
        tk.Label(content, text=f"Hola, {nombre_usu}", font=("Gabriola", 48), bg=BG_APP, fg=COLOR_TEXT_MAIN).pack()
        tk.Label(content, text=f"Panel de Control ({rol_usu.upper()})", font=("Segoe UI", 14), bg=BG_APP, fg="gray").pack(pady=(0, 40))
        
        # Grid de Opciones (Tarjetas)
        grid_opciones = tk.Frame(content, bg=BG_APP)
        grid_opciones.pack()
        
        def crear_tile(columna, texto, icono, comando):
            frame_tile = tk.Frame(grid_opciones, bg="white", width=220, height=180, cursor="hand2")
            frame_tile.grid(row=0, column=columna, padx=20)
            frame_tile.pack_propagate(False) # Respetar tamaño fijo
            
            lbl_icon = tk.Label(frame_tile, text=icono, font=FONT_ICON, bg="white", fg=COLOR_PRIMARY, cursor="hand2")
            lbl_icon.pack(expand=True)
            
            lbl_txt = tk.Label(frame_tile, text=texto, font=("Segoe UI", 14, "bold"), bg="white", fg=COLOR_TEXT_MAIN, cursor="hand2")
            lbl_txt.pack(pady=(0, 20))
            
            # Hacer que todo el cuadro sea clickeable
            for widget in [frame_tile, lbl_icon, lbl_txt]:
                widget.bind("<Button-1>", lambda e: comando())

        crear_tile(0, "CLIENTES", "👥", lambda: Vista.interfaz_clientes(window, usuario))
        crear_tile(1, "VENTAS", "🛍️", lambda: Vista.interfaz_ventas(window, usuario))
        crear_tile(2, "REPORTES", "📊", lambda: Vista.interfaz_reportes(window, usuario))

        if rol_usu == 'admin':
            crear_tile(3, "USUARIOS", "🔐", lambda: Vista.modal_usuario(window))

    # ==========================================
    # 3. GESTIÓN DE CLIENTES
    # ==========================================
    
    @staticmethod
    def interfaz_clientes(window, usuario):
        Vista.borrar_pantalla(window)
        
        # --- Header ---
        header = tk.Frame(window, bg="white", pady=15, padx=30)
        header.pack(fill="x")
        
        tk.Button(header, text="⬅ INICIO", bg="white", fg="gray", bd=0, font=FONT_BOLD, 
            command=lambda: Vista.menu_principal(window, usuario)).pack(side="left")
        
        tk.Label(header, text=" |   CLIENTES", bg="white", fg=COLOR_TEXT_MAIN, font=("Segoe UI", 18, "bold")).pack(side="left")
        
        # Botón Nuevo Cliente
        Vista.crear_boton(header, "+ NUEVO CLIENTE", 
            lambda: Vista.modal_cliente(window, usuario, None, tree)).pack(side="right")
        
        # --- Cuerpo ---
        body = tk.Frame(window, bg=BG_APP, padx=30, pady=30)
        body.pack(fill="both", expand=True)
        
        # --- Barra de Búsqueda ---
        toolbar = tk.Frame(body, bg=BG_APP)
        toolbar.pack(fill="x", pady=(0, 10))
        
        f_search = tk.Frame(toolbar, bg=COLOR_LILA_INPUT, padx=5, pady=5)
        f_search.pack(side="left")
        
        var_busqueda = tk.StringVar()
        entry_busqueda = tk.Entry(f_search, textvariable=var_busqueda, bg=COLOR_LILA_INPUT, bd=0, font=("Segoe UI", 11), width=30)
        entry_busqueda.pack(side="left", padx=10)
        
        # Botón limpiar (X)
        tk.Button(f_search, text="✖", bg=BTN_DANGER_COLOR, fg="white", bd=0, font=("Arial", 8, "bold"), width=3, cursor="hand2", 
            command=lambda: [var_busqueda.set(""), funciones.Funciones.llenar_tabla_clientes(tree, usuario, None)]).pack(side="right")
        
        # Botón buscar (Lupa)
        tk.Button(f_search, text="🔍", bg=COLOR_LILA_INPUT, bd=0, cursor="hand2", 
            command=lambda: funciones.Funciones.llenar_tabla_clientes(tree, usuario, var_busqueda.get())).pack(side="right", padx=5)
        
        # --- Tabla (Treeview) ---
        border_frame = tk.Frame(body, bg=COLOR_TEXT_MAIN, padx=2, pady=2)
        border_frame.pack(side="left", fill="both", expand=True)
        
        columnas = ("id", "idu", "nom", "tel", "dir", "cor", "edad")
        tree = ttk.Treeview(border_frame, columns=columnas, show="headings")
        
        # Configurar cabeceras
        headers_texto = ["ID", "Reg.Por", "Nombre", "Teléfono", "Dirección", "Correo", "Edad"]
        for col_id, texto in zip(columnas, headers_texto):
            tree.heading(col_id, text=texto, 
                command=lambda _c=col_id: funciones.Funciones.ordenar_columna(tree, _c, False))
        
        # Configurar anchos específicos
        tree.column("id", width=40, anchor="center")
        tree.column("idu", width=0, stretch=False) # Oculto visualmente si se desea
        tree.column("edad", width=50, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(border_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- Acciones Laterales ---
        actions_panel = tk.Frame(body, bg=BG_APP, width=150)
        actions_panel.pack(side="right", fill="y", padx=(15, 0))
        actions_panel.pack_propagate(False)
        
        tk.Label(actions_panel, text="Opciones", bg=BG_APP, fg=COLOR_TEXT_MAIN, font=FONT_BOLD).pack(pady=(0, 10))
        
        def obtener_seleccion():
            seleccion = tree.selection()
            if seleccion:
                return tree.item(seleccion)
            return None
        
        # Botones de Editar y Eliminar
        Vista.crear_boton(actions_panel, "Editar", 
            lambda: Vista.modal_cliente(window, usuario, obtener_seleccion(), tree) if obtener_seleccion() 
            else messagebox.showwarning("Atención", "Seleccione un cliente para editar."), 
            BTN_EDIT_COLOR).pack(fill="x", pady=5)
            
        Vista.crear_boton(actions_panel, "Eliminar", 
            lambda: funciones.Funciones.borrar_cliente_tabla(window, usuario, obtener_seleccion()['text'], tree) if obtener_seleccion() 
            else messagebox.showwarning("Atención", "Seleccione un cliente para eliminar."), 
            BTN_DELETE_COLOR).pack(fill="x", pady=5)

        # Buscar al presionar Enter
        entry_busqueda.bind("<Return>", lambda e: funciones.Funciones.llenar_tabla_clientes(tree, usuario, var_busqueda.get()))
        
        # Carga inicial de datos
        funciones.Funciones.llenar_tabla_clientes(tree, usuario)

    # ==========================================
    # 4. GESTIÓN DE VENTAS
    # ==========================================
    
    @staticmethod
    def interfaz_ventas(window, usuario):
        Vista.borrar_pantalla(window)
        
        # --- Header ---
        header = tk.Frame(window, bg="white", pady=15, padx=30)
        header.pack(fill="x")
        
        tk.Button(header, text="⬅ INICIO", bg="white", fg="gray", bd=0, font=FONT_BOLD, 
            command=lambda: Vista.menu_principal(window, usuario)).pack(side="left")
        
        tk.Label(header, text=" |   HISTORIAL VENTAS", bg="white", fg=COLOR_TEXT_MAIN, font=("Segoe UI", 18, "bold")).pack(side="left")
        
        Vista.crear_boton(header, "+ NUEVA VENTA", 
            lambda: Vista.modal_venta(window, usuario, None, tree)).pack(side="right")
        
        # --- Cuerpo ---
        body = tk.Frame(window, bg=BG_APP, padx=30, pady=30)
        body.pack(fill="both", expand=True)
        
        # --- Filtros ---
        toolbar = tk.Frame(body, bg=BG_APP)
        toolbar.pack(fill="x", pady=(0, 10))
        
        f_search = tk.Frame(toolbar, bg=COLOR_LILA_INPUT, padx=5, pady=5)
        f_search.pack(side="left")
        
        tk.Label(f_search, text="Fecha (YYYY-MM):", bg=COLOR_LILA_INPUT, fg="gray", font=("Arial", 9)).pack(side="left", padx=5)
        
        var_fecha = tk.StringVar()
        entry_fecha = tk.Entry(f_search, textvariable=var_fecha, bg=COLOR_LILA_INPUT, bd=0, font=("Segoe UI", 11), width=15)
        entry_fecha.pack(side="left", padx=5)
        
        tk.Button(f_search, text="✖", bg=BTN_DANGER_COLOR, fg="white", bd=0, font=("Arial", 8, "bold"), width=3, cursor="hand2", 
            command=lambda: [var_fecha.set(""), funciones.Funciones.llenar_tabla_ventas(tree, usuario, None)]).pack(side="right")
        
        tk.Button(f_search, text="🔍", bg=COLOR_LILA_INPUT, bd=0, cursor="hand2", 
            command=lambda: funciones.Funciones.llenar_tabla_ventas(tree, usuario, var_fecha.get())).pack(side="right", padx=5)
        
        # --- Tabla Ventas ---
        border_frame = tk.Frame(body, bg=COLOR_TEXT_MAIN, padx=2, pady=2)
        border_frame.pack(side="left", fill="both", expand=True)
        
        cols = ("fol", "vend", "cli", "monto", "pren", "pago", "fecha", "idcli")
        tree = ttk.Treeview(border_frame, columns=cols, show="headings")
        
        headers = ["Folio", "Vendedor", "Cliente", "Total", "Prendas", "Pago", "Fecha"]
        # idcli es una columna oculta, no iteramos sobre ella para los headers visibles
        for c, h in zip(cols[:-1], headers): 
            tree.heading(c, text=h, command=lambda _c=c: funciones.Funciones.ordenar_columna(tree, _c, False))
            
        tree.column("fol", width=50, anchor="center")
        tree.column("monto", width=80, anchor="e")
        tree.column("pren", width=60, anchor="center")
        tree.column("idcli", width=0, stretch=False) # Oculto
        
        scrol = ttk.Scrollbar(border_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrol.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrol.pack(side="right", fill="y")
        
        # --- Panel Acciones ---
        actions = tk.Frame(body, bg=BG_APP, width=150)
        actions.pack(side="right", fill="y", padx=(15, 0))
        actions.pack_propagate(False)
        
        tk.Label(actions, text="Opciones", bg=BG_APP, fg=COLOR_TEXT_MAIN, font=FONT_BOLD).pack(pady=(0, 10))
        
        def obtener_seleccion_venta():
            seleccion = tree.selection()
            return tree.item(seleccion) if seleccion else None

        Vista.crear_boton(actions, "Editar", 
            lambda: Vista.modal_venta(window, usuario, obtener_seleccion_venta(), tree) if obtener_seleccion_venta() 
            else messagebox.showwarning("Atención", "Seleccione una venta para editar."), 
            BTN_EDIT_COLOR).pack(fill="x", pady=5)
            
        Vista.crear_boton(actions, "Anular", 
            lambda: funciones.Funciones.borrar_venta_tabla(window, usuario, obtener_seleccion_venta()['text'], tree) if obtener_seleccion_venta() 
            else messagebox.showwarning("Atención", "Seleccione una venta para anular."), 
            BTN_DELETE_COLOR).pack(fill="x", pady=5)
        
        funciones.Funciones.llenar_tabla_ventas(tree, usuario)

    # ==========================================
    # 5. REPORTES
    # ==========================================
    
    @staticmethod
    def interfaz_reportes(window, usuario):
        Vista.borrar_pantalla(window)
        rol_usu = usuario[5] if usuario and len(usuario)>5 else "user"
        
        # --- Header ---
        header = tk.Frame(window, bg="white", pady=15, padx=30)
        header.pack(fill="x")
        
        tk.Button(header, text="⬅ INICIO", bg="white", fg="gray", bd=0, font=FONT_BOLD, 
            command=lambda: Vista.menu_principal(window, usuario)).pack(side="left")
        
        tk.Label(header, text=" |   REPORTES", bg="white", fg=COLOR_TEXT_MAIN, font=("Segoe UI", 18, "bold")).pack(side="left")
        
        # --- Grid de Reportes ---
        main_frame = tk.Frame(window, bg=BG_APP)
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        grid = tk.Frame(main_frame, bg=BG_APP)
        grid.pack()
        
        def crear_tarjeta_reporte(columna, titulo, tipo_reporte, color_texto):
            frame_card = tk.Frame(grid, bg="white", width=250, height=180, padx=20, pady=20)
            frame_card.grid(row=0, column=columna, padx=20)
            frame_card.pack_propagate(False)
            
            tk.Label(frame_card, text=titulo, font=("Segoe UI", 16, "bold"), bg="white", fg=color_texto).pack(pady=(0, 20))
            
            Vista.crear_boton(frame_card, "Exportar Excel", 
                lambda: Vista.generar_exportacion(tipo_reporte, "excel", usuario), 
            BTN_SUCCESS_COLOR).pack(fill="x", pady=2)

            Vista.crear_boton(frame_card, "Exportar PDF", 
                lambda: Vista.generar_exportacion(tipo_reporte, "pdf", usuario), 
                BTN_DANGER_COLOR).pack(fill="x", pady=2)

        # Tarjetas estándar
        crear_tarjeta_reporte(0, "Clientes", "clientes", COLOR_PRIMARY)
        crear_tarjeta_reporte(1, "Ventas", "ventas", COLOR_PRIMARY)
        
        # Tarjeta Admin
        if rol_usu == 'admin':
            frame_admin = tk.Frame(grid, bg="white", width=250, height=180, padx=20, pady=20)
            frame_admin.grid(row=0, column=2, padx=20)
            frame_admin.pack_propagate(False)
            
            tk.Label(frame_admin, text="Admin", font=("Segoe UI", 16, "bold"), bg="white", fg="red").pack(pady=(0, 20))
            
            Vista.crear_boton(frame_admin, "Usuarios (Excel)", 
                lambda: Vista.generar_exportacion("usuarios", "excel", usuario), 
                "#333").pack(fill="x", pady=2)
        
        # Botón volver inferior
        tk.Button(window, text="⬅ Volver al Menú", bg="#5D6D7E", fg="white", 
            command=lambda: Vista.menu_principal(window, usuario)).pack(pady=30)

    @staticmethod
    def generar_exportacion(tipo, formato, usuario):
        """Prepara los datos y llama al generador de reportes"""
        rol = usuario[5]
        id_usu = usuario[0]
        datos = []
        columnas = []
        titulo = ""
        
        try:
            if tipo == "clientes":
                raw_data = clienteBD.ClienteBD.consultar(id_usu, rol)
                columnas = ["ID", "ID_Usu", "Nombre", "Teléfono", "Dirección", "Correo", "Edad"]
                if rol == 'admin': 
                    columnas.append("Vendedor")
                datos = raw_data
                titulo = "Reporte Clientes"
                
            elif tipo == "ventas":
                raw_data = ventaBD.VentaBD.consultar_ventas(id_usu, rol)
                # Reordenamos los datos para el reporte para que sean más legibles
                datos = [(r[0], r[1], r[2], r[3], r[4], r[5], r[7]) for r in raw_data]
                columnas = ["Folio", "Cliente", "Monto", "Prendas", "Pago", "Fecha", "Vendedor"]
                titulo = "Reporte Ventas"
                
            elif tipo == "usuarios":
                # Importación local para evitar error circular
                from model.conexionBD import cursor
                cursor.execute("SELECT id, nombre, apellidos, correo, rol FROM usuarios")
                datos = cursor.fetchall()
                columnas = ["ID", "Nombre", "Apellidos", "Correo", "Rol"]
                titulo = "Reporte de Usuarios del Sistema"

            # Ejecutar exportación según formato
            if formato == "excel":
                GeneradorReportes.exportar_excel(datos, columnas, tipo)
            elif formato == "pdf":
                GeneradorReportes.exportar_pdf(datos, columnas, titulo, tipo)
                
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"Ocurrió un error al generar el reporte: {str(e)}")

    # ==========================================
    # 6. VENTANAS EMERGENTES (MODALES)
    # ==========================================

    @staticmethod
    def modal_cliente(parent, usuario, item_editar, tree, callback=None):
        modal = tk.Toplevel(parent)
        modal.geometry("400x550")
        modal.config(bg="white")
        
        # Variables
        v_nom = tk.StringVar(); v_tel = tk.StringVar()
        v_dir = tk.StringVar(); v_cor = tk.StringVar(); v_edad = tk.StringVar()
        id_cli = None
        titulo = "Nuevo Cliente"

        # Cargar datos si es edición
        if item_editar:
            titulo = "Editar Cliente"
            id_cli = item_editar['text']
            vals = item_editar['values']
            v_nom.set(vals[2]); v_tel.set(vals[3])
            v_dir.set(vals[4]); v_cor.set(vals[5]); v_edad.set(vals[6])

        modal.title(titulo)
        tk.Label(modal, text=titulo, font=("Segoe UI", 16, "bold"), bg="white", fg=COLOR_PRIMARY).pack(pady=20)
        
        f_form = tk.Frame(modal, bg="white", padx=40)
        f_form.pack(fill="both")
        
        # Helper para crear filas (validación opcional)
        def agregar_fila(texto_label, variable, tipo_validacion=None):
            tk.Label(f_form, text=texto_label, bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0))
            Vista.crear_input(f_form, variable, validacion=tipo_validacion)

        # Campos
        agregar_fila("Nombre Completo", v_nom)
        agregar_fila("Teléfono", v_tel, "int")     # <--- Solo Números 
        agregar_fila("Dirección", v_dir)
        agregar_fila("Correo Electrónico", v_cor)
        agregar_fila("Edad", v_edad, "int")        # <--- Solo Números
        
        tk.Frame(modal, bg="white", height=20).pack()

        # Botón Guardar (Pasando el callback)
        Vista.crear_boton(modal, "GUARDAR DATOS", 
            lambda: funciones.Funciones.guardar_o_editar_cliente(
            parent, tree, id_cli, usuario, 
            v_nom.get(), v_tel.get(), v_dir.get(), v_cor.get(), v_edad.get(), 
            modal, callback
            )).pack(fill="x", padx=40, pady=20)

    @staticmethod
    def modal_venta(parent, usuario, item_editar, tree):
        modal = tk.Toplevel(parent)
        modal.geometry("400x600")
        modal.config(bg="white")
        
        v_cli = tk.StringVar(); v_monto = tk.StringVar(); v_pren = tk.StringVar(value="1"); v_met = tk.StringVar()
        id_venta = None; titulo = "Nueva Venta"
        
        # 1. Obtener lista inicial de clientes
        rol = usuario[5] if len(usuario) > 5 else "user"
        data_clientes = clienteBD.ClienteBD.consultar(usuario[0], rol)
        lista_combo = [f"{c[0]} - {c[2]}" for c in data_clientes]
        
        if item_editar:
            titulo = "Editar Venta"
            id_venta = item_editar['text']; vals = item_editar['values']
            v_cli.set(f"{vals[7]} - {vals[2]}") 
            v_monto.set(str(vals[3]).replace("$", ""))
            v_pren.set(vals[4]); v_met.set(vals[5])

        # --- FUNCIÓN CALLBACK: Se ejecutará al cerrar el modal de cliente ---
        def recargar_combo_clientes():
            # Volver a pedir los datos a la BD
            datos_nuevos = clienteBD.ClienteBD.consultar(usuario[0], rol)
            lista_nueva = [f"{c[0]} - {c[2]}" for c in datos_nuevos]
            # Actualizar el combobox
            combo_cli['values'] = lista_nueva
            # Auto-seleccionar el último (el nuevo)
            if lista_nueva:
                combo_cli.current(len(lista_nueva) - 1)

        modal.title(titulo)
        tk.Label(modal, text=titulo, font=("Segoe UI", 16, "bold"), bg="white", fg=COLOR_PRIMARY).pack(pady=20)
        
        f_form = tk.Frame(modal, bg="white", padx=40)
        f_form.pack(fill="both")
        
        # --- SECCIÓN CLIENTE (COMBO + BOTÓN) ---
        tk.Label(f_form, text="Seleccionar Cliente", bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0))
        
        # Creamos un frame horizontal para poner el Combo y el Botón juntos
        f_combo_container = tk.Frame(f_form, bg="white")
        f_combo_container.pack(fill="x")
        
        combo_cli = ttk.Combobox(f_combo_container, textvariable=v_cli, values=lista_combo, state="readonly")
        combo_cli.pack(side="left", fill="x", expand=True, ipady=5)
        
        # Solo mostrar el botón de agregar si NO estamos editando
        if not item_editar:
            tk.Button(f_combo_container, text="➕", bg="#27AE60", fg="white", bd=0, font=("Segoe UI", 10, "bold"), cursor="hand2",
                # Al dar click: Abre modal cliente -> tree=None -> callback=recargar
                command=lambda: Vista.modal_cliente(parent, usuario, None, None, callback=recargar_combo_clientes))\
                .pack(side="left", padx=(5, 0), fill="y")
        
        # --- SECCIÓN DATOS NUMÉRICOS ---
        def agregar_fila(texto_label, variable, tipo_validacion=None):
            tk.Label(f_form, text=texto_label, bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0))
            Vista.crear_input(f_form, variable, validacion=tipo_validacion)
            
        agregar_fila("Monto Total ($)", v_monto, "float") # <--- Valida decimales
        agregar_fila("Cantidad de Prendas", v_pren, "int") # <--- Valida enteros
        
        # --- SECCIÓN PAGO ---
        tk.Label(f_form, text="Método de Pago", bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0))
        combo_pago = ttk.Combobox(f_form, textvariable=v_met, values=["Efectivo", "Tarjeta", "Transferencia"], state="readonly")
        combo_pago.pack(fill="x", ipady=5)
        
        if not item_editar:
            combo_pago.current(0)

        btn_txt = "ACTUALIZAR" if item_editar else "COBRAR"
        Vista.crear_boton(modal, btn_txt, 
            lambda: funciones.Funciones.guardar_o_editar_venta(
            parent, tree, usuario, id_venta, 
            v_cli.get(), v_monto.get(), v_pren.get(), v_met.get(), modal
            )).pack(fill="x", padx=40, pady=20)
    
    @staticmethod
    def modal_usuario(parent):
        """Ventana emergente para que el Admin cree nuevos usuarios"""
        modal = tk.Toplevel(parent)
        modal.geometry("400x550")
        modal.config(bg="white")
        modal.title("Registrar Nuevo Usuario")
        
        tk.Label(modal, text="Nuevo Usuario", font=("Segoe UI", 16, "bold"), bg="white", fg=COLOR_PRIMARY).pack(pady=20)
        
        f_form = tk.Frame(modal, bg="white", padx=40)
        f_form.pack(fill="both")
        
        # Variables
        v_nom = tk.StringVar()
        v_ape = tk.StringVar()
        v_cor = tk.StringVar()
        v_pas = tk.StringVar()
        v_rol = tk.StringVar(value="usuario") # Valor por defecto

        def fila(txt, var, show=None):
            tk.Label(f_form, text=txt, bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0))
            Vista.crear_input(f_form, var, show=show)

        fila("Nombre", v_nom)
        fila("Apellidos", v_ape)
        fila("Correo Electrónico", v_cor)
        fila("Contraseña", v_pas, "*")
        
        # Selector de Rol (Combobox)
        tk.Label(f_form, text="Rol del Sistema", bg="white", fg="gray", anchor="w").pack(fill="x", pady=(10,0))
        combo_rol = ttk.Combobox(f_form, textvariable=v_rol, values=["usuario", "admin"], state="readonly")
        combo_rol.pack(fill="x", ipady=5)
        
        tk.Frame(modal, bg="white", height=20).pack()

        Vista.crear_boton(modal, "CREAR USUARIO", 
            lambda: funciones.Funciones.guardar_usuario_admin(
            parent, v_nom.get(), v_ape.get(), v_cor.get(), v_pas.get(), v_rol.get(), modal
            )).pack(fill="x", padx=40, pady=20)