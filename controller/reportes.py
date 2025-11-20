import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import filedialog, messagebox
from datetime import datetime

class GeneradorReportes:
    
    @staticmethod
    def exportar_excel(datos, columnas, nombre_archivo):
        try:
            # Convertimos la lista de tuplas a un DataFrame de Pandas
            df = pd.DataFrame(datos, columns=columnas)
            
            path = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f"{nombre_archivo}_{datetime.now().strftime('%Y%m%d')}")
            if path:
                df.to_excel(path, index=False)
                messagebox.showinfo("Éxito", f"Archivo Excel guardado en:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

    @staticmethod
    def exportar_pdf(datos, columnas, titulo, nombre_archivo):
        try:
            path = filedialog.asksaveasfilename(defaultextension=".pdf", 
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"{nombre_archivo}_{datetime.now().strftime('%Y%m%d')}")
            if not path: return
            c = canvas.Canvas(path, pagesize=letter)
            width, height = letter
            y = height - 50
            # Título
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y, titulo)
            y -= 30
            
            # Encabezados
            c.setFont("Helvetica-Bold", 10)
            x_start = 50
            step = 500 / len(columnas) # Dividimos el ancho
            
            for i, col in enumerate(columnas):
                c.drawString(x_start + (i * step), y, col.upper())
            
            y -= 20
            c.line(50, y + 15, 550, y + 15) # Línea separadora

            # Datos
            c.setFont("Helvetica", 9)
            for fila in datos:
                if y < 50: # Nueva página si se acaba el espacio
                    c.showPage()
                    y = height - 50
                
                for i, valor in enumerate(fila):
                    c.drawString(x_start + (i * step), y, str(valor))
                y -= 15

            c.save()
            messagebox.showinfo("Éxito", f"PDF generado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar PDF: {e}")