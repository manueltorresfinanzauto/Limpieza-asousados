import numpy as np
import pandas as pd
import xlwings as xw


ruta_e = r'Asousados_15_12_2025.xlsx'



def limpiar_celdas_blancas(file_path):
    # Abrir el libro
    wb = xw.Book(file_path)
    
    for sheet in wb.sheets:
        print(f"Procesando hoja: {sheet.name}")
        
        # Obtenemos el rango usado en la hoja
        rango = sheet.used_range
        
        for cell in rango:
            # En VBA: RGB(255, 255, 255) es color blanco
            # En xlwings, el color de la fuente se accede así:
            if cell.api.Font.Color == 16777215: # 16777215 es el equivalente decimal de blanco
                cell.clear_contents()
                
    wb.save()
    wb.close()

limpiar_celdas_blancas(ruta_e)