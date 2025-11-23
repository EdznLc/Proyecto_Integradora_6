import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import filedialog, messagebox
from datetime import datetime
import os

class GeneradorReportes:
    """
    Módulo encargado de transformar los datos crudos (listas de tuplas)
    en archivos físicos (.xlsx o .pdf) para el usuario.
    """

    # ==========================================
    # 1. EXPORTACIÓN A EXCEL
    # ==========================================
    @staticmethod
    def exportar_excel(datos, columnas, nombre_base_archivo):
        """
        Usa la librería 'pandas' porque es la forma más rápida y limpia
        de pasar datos a Excel sin complicarse con celdas individuales.
        """
        if not datos:
            messagebox.showwarning("Atención", "No hay datos para exportar.")
            return

        try:
            # 1. Convertir lista de datos a un DataFrame (Tabla virtual)
            df = pd.DataFrame(datos, columns=columnas)
            
            # 2. Generar nombre sugerido con fecha (ej: Clientes_20231122)
            fecha_hoy = datetime.now().strftime('%Y%m%d')
            nombre_sugerido = f"{nombre_base_archivo}_{fecha_hoy}"

            # 3. Abrir ventana para elegir dónde guardar
            ruta_archivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx", 
                filetypes=[("Archivos de Excel", "*.xlsx")],
                initialfile=nombre_sugerido
            )

            # Si el usuario cancela, ruta_archivo será vacío
            if not ruta_archivo: 
                return

            # 4. Guardar
            df.to_excel(ruta_archivo, index=False) # index=False quita la columna 0,1,2,3 automática
            messagebox.showinfo("Éxito", f"Reporte Excel guardado en:\n{ruta_archivo}")

        except PermissionError:
            messagebox.showerror("Error", "El archivo parece estar abierto en Excel.\nCierra el archivo e intenta de nuevo.")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"No se pudo exportar: {e}")

    # ==========================================
    # 2. EXPORTACIÓN A PDF
    # ==========================================
    @staticmethod
    def exportar_pdf(datos, columnas, titulo_reporte, nombre_base_archivo):
        """
        Genera un PDF 'dibujando' texto en coordenadas (x, y).
        Usa la librería reportlab.
        """
        if not datos:
            messagebox.showwarning("Atención", "No hay datos para exportar.")
            return

        try:
            # 1. Preparar archivo
            fecha_hoy = datetime.now().strftime('%Y%m%d')
            nombre_sugerido = f"{nombre_base_archivo}_{fecha_hoy}"
            
            ruta_archivo = filedialog.asksaveasfilename(
                defaultextension=".pdf", 
                filetypes=[("Archivos PDF", "*.pdf")],
                initialfile=nombre_sugerido
            )

            if not ruta_archivo: 
                return

            # 2. Configuración Inicial del "Lienzo" (Canvas)
            c = canvas.Canvas(ruta_archivo, pagesize=letter)
            ancho_pag, alto_pag = letter # Tamaño carta (612.0, 792.0 puntos)
            
            # Configuraciones de márgenes y posición
            y_actual = alto_pag - 50  # Empezamos 50 puntos abajo del borde superior
            margen_izq = 50
            altura_linea = 20
            
            # Cálculo dinámico del ancho de columnas
            # (Restamos 100 de margenes y dividimos entre cant. columnas)
            ancho_columna = (ancho_pag - 100) / len(columnas)

            # --- DIBUJAR TÍTULO ---
            c.setFont("Helvetica-Bold", 16)
            c.drawString(margen_izq, y_actual, titulo_reporte)
            c.setFont("Helvetica", 10)
            c.drawRightString(ancho_pag - 50, y_actual, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
            y_actual -= 40 # Bajamos el cursor

            # --- DIBUJAR ENCABEZADOS DE TABLA ---
            c.setFont("Helvetica-Bold", 9)
            x_temp = margen_izq
            
            for col in columnas:
                c.drawString(x_temp, y_actual, col.upper())
                x_temp += ancho_columna
            
            # Línea debajo de los encabezados
            y_actual -= 5
            c.line(margen_izq, y_actual, ancho_pag - 50, y_actual)
            y_actual -= 15 # Bajamos para los datos

            # --- DIBUJAR FILAS DE DATOS ---
            c.setFont("Helvetica", 8)
            
            for fila in datos:
                # Verificar si se acabó la hoja
                if y_actual < 50: 
                    c.showPage()          # Crea una página nueva
                    y_actual = alto_pag - 50 # Resetea la posición Y arriba
                    c.setFont("Helvetica", 8) # Hay que volver a poner la fuente en pág nueva

                x_temp = margen_izq
                for valor in fila:
                    texto = str(valor)
                    
                    # Truco: Si el texto es muy largo, lo cortamos para que no encime al vecino
                    # Aproximadamente 15-20 caracteres caben bien por columna promedio
                    limite_caracteres = int(ancho_columna / 5) 
                    if len(texto) > limite_caracteres:
                        texto = texto[:limite_caracteres-3] + "..."
                    
                    c.drawString(x_temp, y_actual, texto)
                    x_temp += ancho_columna
                
                y_actual -= altura_linea # Siguiente fila

            c.save() # Guardar y cerrar el PDF
            messagebox.showinfo("Éxito", "PDF generado correctamente.")
            
        except PermissionError:
            messagebox.showerror("Error", "El archivo PDF está abierto.\nCiérralo e intenta de nuevo.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar PDF: {e}")