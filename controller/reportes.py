import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import filedialog, messagebox
from datetime import datetime
from model import clienteBD, ventaBD
from conexionBD import cursor

class GeneradorReportes:
    """
    Controlador para exportar datos a Excel y PDF.
    """

    MAPA_PAGO_TXT = {1: "Efectivo", 2: "Tarjeta", 3: "Transferencia"}

    @staticmethod
    def generar(tipo, formato, usuario):
        rol = usuario[5]
        id_usu = usuario[0]
        datos = []
        columnas = []
        titulo = ""

        try:
            if tipo == "clientes":
                raw = clienteBD.ClienteBD.consultar(id_usu, rol)
                datos_limpios = []
                for r in raw:
                    fila = [r[0], r[2], r[3], r[4], r[5], r[6]]
                    if rol == 'admin' or rol == 1: fila.append(r[10])
                    datos_limpios.append(fila)
                
                columnas = ["ID", "Nombre Completo", "Teléfono", "Dirección", "Correo", "Edad"]
                if rol == 'admin' or rol == 1: columnas.append("Vendedor")
                datos = datos_limpios
                titulo = "Reporte de Clientes"

            elif tipo == "ventas":
                raw = ventaBD.VentaBD.consultar_ventas(id_usu, rol)
                datos_limpios = []
                for r in raw:
                    txt_pago = GeneradorReportes.MAPA_PAGO_TXT.get(r[4], "Otro")
                    fila = [r[0], r[1], r[2], r[3], txt_pago, r[5], r[7]]
                    datos_limpios.append(fila)

                columnas = ["Folio", "Cliente", "Monto ($)", "Prendas", "Pago", "Fecha", "Vendedor"]
                datos = datos_limpios
                titulo = "Reporte de Ventas"

            elif tipo == "usuarios":
                sql = "SELECT id_usuario, username, correo, es_admin FROM usuarios"
                cursor.execute(sql)
                raw = cursor.fetchall()
                datos_limpios = []
                for r in raw:
                    rol_str = "ADMINISTRADOR" if r[3] == 1 else "Vendedor"
                    datos_limpios.append([r[0], r[1], r[2], rol_str])
                
                columnas = ["ID", "Username", "Correo", "Rol"]
                datos = datos_limpios
                titulo = "Lista de Usuarios"

            if formato == "excel":
                GeneradorReportes._exportar_excel_pandas(datos, columnas, tipo)
            elif formato == "pdf":
                GeneradorReportes._exportar_pdf_canvas(datos, columnas, titulo, tipo)

        except Exception as e:
            messagebox.showerror("Error Reporte", f"Fallo al generar datos: {e}")

    @staticmethod
    def _exportar_excel_pandas(datos, columnas, nombre_base):
        if not datos: messagebox.showwarning("Atención", "Sin datos para exportar."); return
        try:
            df = pd.DataFrame(datos, columns=columnas)
            archivo = f"{nombre_base}_{datetime.now().strftime('%Y%m%d')}"
            path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")], initialfile=archivo)
            if path:
                df.to_excel(path, index=False)
                messagebox.showinfo("Éxito", f"Excel guardado:\n{path}")
        except PermissionError: messagebox.showerror("Error", "Cierre el archivo Excel e intente de nuevo")
        except Exception as e: messagebox.showerror("Error", str(e))

    @staticmethod
    def _exportar_pdf_canvas(datos, columnas, titulo, nombre_base):
        if not datos: messagebox.showwarning("Atención", "Sin datos para exportar."); return
        try:
            archivo = f"{nombre_base}_{datetime.now().strftime('%Y%m%d')}"
            path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")], initialfile=archivo)
            if not path: return

            c = canvas.Canvas(path, pagesize=letter)
            w, h = letter
            y = h - 50; x = 50
            
            c.setFont("Helvetica-Bold", 16); c.drawString(x, y, titulo)
            c.setFont("Helvetica", 10); c.drawRightString(w-50, y, datetime.now().strftime("%d/%m/%Y"))
            y -= 40

            ancho_col = (w - 100) / len(columnas)
            c.setFont("Helvetica-Bold", 9)
            for i, col in enumerate(columnas): c.drawString(x + (i*ancho_col), y, col.upper())
            y -= 5; c.line(x, y, w-50, y); y -= 15

            c.setFont("Helvetica", 8)
            for fila in datos:
                if y < 50: c.showPage(); y = h - 50; c.setFont("Helvetica", 8)
                for i, val in enumerate(fila):
                    txt = str(val)
                    if len(txt) > int(ancho_col/5): txt = txt[:int(ancho_col/5)-3] + "..."
                    c.drawString(x + (i*ancho_col), y, txt)
                y -= 20
            
            c.save()
            messagebox.showinfo("Éxito", "PDF Generado correctamente.")
        except PermissionError: messagebox.showerror("Error", "El PDF está abierto, ciérrelo.")
        except Exception as e: messagebox.showerror("Error", str(e))