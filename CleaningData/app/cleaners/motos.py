from sqlalchemy import create_engine, text
import pandas as pd
from CleaningData.config.sqlacces import connection_str_dw_fz


class Motos:

    @staticmethod
    def _query_sql() -> str: 
        """
        Generate the SQL query to retrieve the average grade.

        Args:

        Returns:
            str: The SQL query.
        """
        query = """ 
                SELECT
                    [Marca]
                    ,[Clase]
                    ,[Codigo]
                    ,[Homologocodigo]
                    ,[Referencia1]
                    ,[Referencia2]
                    ,[Referencia3]
                    ,[IdServicio]
                    ,[Servicio]
                    ,[Combustible]
                    ,[Transmision]
                FROM [Analitica].[dbo].[COD_Fasecolda]
                where Clase IN ('MOTOCICLETA', 'CHASIS', 'REMOLCADOR', 'ISOCARRO', 'CUATRIMOTO', 'CAMION', 'CARROTANQUE','MOTOCARRO','FURGONETA','FURGON','REMOLQUE','VOLQUETA','BUS / BUSETA / MICROBUS')
        """
        return query
    
    @classmethod
    def find_motos(cls, df):

        connect_str: str = connection_str_dw_fz
        engine = create_engine(connect_str)
        query = cls._query_sql()
        df_fase = pd.read_sql(query, engine)
        engine.dispose()
        df_fase = df_fase.rename(columns={'Codigo' : 'Cod_fasecolda'})
        # print(df_fase.columns.tolist())
        df_filter = df[~df['Cod_fasecolda'].isin(df_fase['Cod_fasecolda'])]
        
        return df_filter    
