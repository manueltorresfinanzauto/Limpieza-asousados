from sqlalchemy import create_engine, text
import pandas as pd
from CleaningData.config.sqlacces import connection_str_dw_fz as connection_str
from datetime import datetime
import re
 
class Demanda:
    """ 
    Class that gives the demanda of the car 
    """
    @staticmethod
    def _query_sql() -> str:
        """
        Generate the SQL query to retrieve the average grade
        Args:

        Returns:
            str: The SQL query
        """
        query  = """ select * FROM [Analitica].[pri].[demanda_vehiculos]

                """
        return query
    
    @staticmethod
    def clean_text(text):
        """Removes special characters, extra spaces, and bracketed content like '[2]'."""
        if isinstance(text, str):
            text = re.sub(r"\[.*?\]", "", text)  # Remove anything inside brackets, including the brackets
            text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Keep only letters, numbers, and spaces
            text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
            return text.upper()  # Ensure case consistency
        return text 
    
    @classmethod
    def search_demanda(cls, df_or) -> pd.DataFrame: 
        """
        Will search for the demand percentage value of the car in my input 

        Args:
            df (pd.DataFrame): Input DataFrame with N columns. 

        Return:
            df_merged (pd.DataFrame): Input DataFrame with N columns.
        """
        # Marca = Marca.upper(); Linea = Linea.upper()
        connect_str: str = connection_str
        engine = create_engine(connect_str, connect_args={"timeout": 30})
        query = cls._query_sql()
        df = pd.read_sql(query, engine)
        engine.dispose()
        df["Marca"] = df["Marca"].astype(str)
        df["Linea"] = df["Linea"].astype(str)
        df["Group_number"] = df["Group_number"].astype(int)

        today = datetime.today()

        # First day of the current month
        first_day_of_month = datetime(today.year, today.month, 1)
        
        df_or['Group_number'] = (((first_day_of_month.year - df_or['Fecha_venta'].dt.year) * 12 + 
                       (first_day_of_month.month - df_or['Fecha_venta'].dt.month)) / 12 + 1).astype(int)
        # df_or.to_csv('out.csv', index=False)

        df_or["Marca"] = df_or["Marca"].str.strip()
        df["Marca"] = df["Marca"].str.strip()
        df_or["Linea"] = df_or["Linea"].str.strip()
        df["Linea"] = df["Linea"].str.strip()
        df_or["Marca"] = df_or["Marca"].str.upper()
        df["Marca"] = df["Marca"].str.upper()
        df_or["Linea"] = df_or["Linea"].str.upper()
        df["Linea"] = df["Linea"].str.upper()
        df_or["Linea"] = df_or["Linea"].apply(cls.clean_text)
        df["Linea"] = df["Linea"].apply(cls.clean_text)

        try:
            # df_merged = df_or.merge(df[['Group_number', 'Marca', 'Linea', 'Percentage', 'Sales']], on=['Group_number', 'Marca', 'Linea'], how='left')
            df_single = df.groupby(['Group_number', 'Marca', 'Linea'], as_index=False).first()
            df_merged = df_or.merge(df_single[['Group_number', 'Marca', 'Linea', 'Percentage', 'Sales']], on=['Group_number', 'Marca', 'Linea'], how='left')
            return df_merged
        except KeyError as e:
            print(f'La entrada no coinciden, revisa los valores insertados - {e}')
        
             

if __name__ == '__main__': 

    df = pd.DataFrame({'Fecha_venta': pd.to_datetime(['2022-06-15', '2023-01-10', '2024-03-05', '2024-05-10'])})
    Demanda.search_demanda(df)