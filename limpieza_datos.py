from CleaningData.clean_main import clean_total 
from reorganizar_aso import asousados_organizar
from main_base_v2 import limpieza_v2
from extraer_melollevo import bases_melo
import pandas as pd

# path = r'../brdp_25_02_2026.xlsx'
# name_out = 'brdp_25_02_2026_clean.csv'
# clean_total(path, name_out)


dict_limpieza = {1 : asousados_organizar ,
                 2 : limpieza_v2,
                 3 : bases_melo}

# asousados_organizar()

def ejecutar_limpieza(n):

    funcion = dict_limpieza.get(n)

    if funcion:
        print(f"Ejecutando la opción {n}...")
        df = funcion()
        df_f = clean_total(df)
        df_f.to_excel('prueba1.xlsx', index=False)
        return df_f
    else:
        print("Opción no válida. Por favor elige 1, 2 o 3.")


ejecutar_limpieza(1)