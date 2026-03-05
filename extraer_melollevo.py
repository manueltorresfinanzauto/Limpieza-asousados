import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import numpy as np
from config.sqlacces import connection_str, connection_str_dw



def queries(n):
    if n == 1:
        query_s: str = """SELECT [placa]
      ,[valor_aprobado]
      ,[valor_comercial]
      ,[kpi]
      ,[valor_c]
      ,[origen]
      ,[inventario]
      ,[producto]
      ,[canal]
      ,[n_subasta]
      ,[fecha_fac]
      ,[mes_fac]
      ,[factura]
      ,[canal2]
      ,[fecha_insercion] FROM [DW_FZ].[drv].[land_mll_facturacion]"""
        return query_s
    if n == 2: 
        query_s: str = """SELECT * FROM  [Analitica].[pri].[pricing_brdp]"""
        return query_s
    if n == 3: 
        query_s: str = """SELECT * FROM [Analitica].[dbo].[peritajes_fasecolda]"""
        return query_s


def bases_melo():

    engine1 = create_engine(connection_str_dw)
    query1 = queries(1)
    df1 = pd.read_sql(query1, engine1)
    engine1.dispose()
    engine = create_engine(connection_str)
    query2 = queries(2)
    df2 = pd.read_sql(query2, engine)
    query3 = queries(3)
    df3 = pd.read_sql(query3, engine)
    engine.dispose()
    df1 = df1.rename(columns={'placa' : 'Placa'})
    df2 = df2.rename(columns={'Fecha_de_Inspeccion' : 'Fecha'})
    print(df1.shape)
    df_n1 = pd.merge(df1, df2, on='Placa', how='inner')
    df_n2 = pd.merge(df1, df3, on='Placa', how='inner')
    print(df_n1.shape)
    print(df_n2.shape)
    df_final = pd.concat([df_n1, df_n2], ignore_index=True)
    df_final = df_final.drop_duplicates(subset=['Placa', 'Fecha'], keep='first')
    print(df_final.shape)
    mask = df_final['Fecha'].isnull()
    df_final.loc[mask, 'Fecha'] = pd.to_datetime(
    "12/" + df_final.loc[mask, 'mes_fac'].astype(int).astype(str) + "/2025", 
    dayfirst=True)

    return df_final

if __name__ == '__main__':
    df = bases_melo()
    df_vacios = df[df['Fecha'].isnull()]

        # Imprimimos la dimensión (filas, columnas)
    print(f"Dimensiones de filas con 'A' vacío: {df_vacios.shape}")

        # Si solo quieres el número de filas:
    print(f"Total de registros con 'A' vacío: {df_vacios.shape[0]}")