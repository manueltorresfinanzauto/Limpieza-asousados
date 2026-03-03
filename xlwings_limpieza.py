import xlwings as xw

def limpiar_rapido(file_path):
    app = xw.App(visible=False)
    wb = app.books.open(file_path)
    
    for sheet in wb.sheets:
        print(f"Limpiando {sheet.name}...")
        
        # Optimizamos desactivando el refresco de pantalla
        app.screen_updating = False
        
        # 16777215 = Blanco
        try:
            cell_api = sheet.used_range.api
            app.api.FindFormat.Font.Color = 16777215
            
            cell_api.Replace(What:="", Replacement:="", SearchFormat=True, ReplaceFormat=False)
        except Exception as e:
            print(f"No se encontraron celdas blancas en {sheet.name}")
            
        app.screen_updating = True

    wb.save()
    wb.close()
    app.quit()


ruta_e = r'Asousados_15_12_2025.xlsx'
limpiar_rapido(ruta_e)

