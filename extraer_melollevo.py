import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import numpy as np
from config.sqlacces import connection_str



def queries(n):
    if n == 1:
        query_s: str = "SELECT * FROM [DW_FZ].[drv].[land_mll_facturacion]"
        return query_s
    if n == 2: 
        query_s: str = """SELECT * FROM  [Analitica].[pri].[pricing_brdp]
        """
    if n == 3: 
        query_s: str = """SELECT * FROM [Analitica].[dbo].[peritajes_fasecolda]"""


def bases_melo():
    connect_str: str = connection_str
    engine = create_engine(connect_str)
    query = queries(1)
    df1 = pd.read_sql(query, engine)
    query = queries(2)
    df2 = pd.read_sql(query, engine)
    query = queries(3)
    df3 = pd.read_sql(query, engine)
    engine.dispose()

    df_n1 = pd.merge(df1, df2, on='Placa', how='inner')
    df_n2 = pd.merge(df1, df3, on='Placa', how='inner')
    df_final = pd.concat([df_n1, df_n2], ignore_index=True)
    df_final = df_final.drop_duplicates(subset=['Placa', 'Fecha'], keep='first')

    return df_final

