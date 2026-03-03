import pandas as pd
import re
import unidecode
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_distances
from rapidfuzz import fuzz
from config.sqlacces import connection_str
from sqlalchemy import create_engine, text
from fuzzywuzzy import fuzz

class tf_idf_assign:
    """ 
    Class to assign the cod fasecolda with the brand and reference as inputs.
    """
    @staticmethod
    def cleaning_text(text):
        text = re.sub(r",", " ", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\[.*?\]", "", text)
        text = str(text).lower().strip()
        return unidecode.unidecode(text)

    @staticmethod
    def remove_duplicate_words(text):
        words = text.split()
        return " ".join(dict.fromkeys(words))
    
    @staticmethod
    def _query_sql(ch : int) -> str: 
        """
        Generate the SQL query to retrieve the average grade.

        Args:

        Returns:
            str: The SQL query.
        """

        if ch == 1:
            query = '''
                    SELECT
                        [Marca]
                        ,[Clase]
                        ,[Codigo]
                        ,[Homologocodigo]
                        ,[Referencia1]
                        ,[Referencia2]
                        ,[Referencia3]
                    FROM [Analitica].[dbo].[COD_Fasecolda]

                '''
        if ch == 2:
            query = '''
                    SELECT
                        [Marca]
                        ,[Clase]
                        ,[Codigo]
                        ,[Homologocodigo]
                        ,[Referencia1]
                        ,[Referencia2]
                        ,[Referencia3]
                        ,[Combustible]
                    FROM [Analitica].[dbo].[COD_Fasecolda]

                '''
        
        return query

    @staticmethod
    def clean_text(text):
        """Removes special characters, extra spaces, and bracketed content like '[2]'."""
        if isinstance(text, str):
            text = re.sub(r"\[.*?\]", "", text)  # Remove anything inside brackets, including the brackets
            text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Keep only letters, numbers, and spaces
            text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
            return text.lower()  # Ensure case consistency
        return text 
    
    @staticmethod
    def jaccard_similarity(set1, set2):
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0

    @classmethod
    def marca_cofc(cls, df):
        connect_str: str = connection_str
        engine = create_engine(connect_str)
        query = cls._query_sql(ch=1)
        df_cf = pd.read_sql(query, engine)
        engine.dispose()
        df_cf['Referencia1'] = df_cf['Referencia1'].apply(cls.clean_text)
        df_cf['Referencia2'] = df_cf['Referencia2'].apply(cls.clean_text)
        df_cf['Referencia3'] = df_cf['Referencia3'].apply(cls.clean_text)
        df_cf['Reference'] = df_cf['Referencia1'] + ' ' + df_cf['Referencia2'] + ' ' + df_cf['Referencia3'] 
        try:
            df['Reference'] = df['Referencia'].apply(cls.clean_text)
        except:
            try:
                df['Reference'] = df['Linea'] + ' ' + df['Referencia']
                df['Reference'] = df['Reference'].apply(cls.clean_text)
                print('Linea+referencia')
            except:
                df['Reference'] = df['Linea'].apply(cls.clean_text)
                print('Linea')

        df['Marca'].str.lower()
        df_cf['Marca'].str.lower()

        df["match"] = None
        df["cod_fasecolda"] = None
        
        # Iterar por cada marca en común
        for marca in df["Marca"].unique():
            df_marca = df[df["Marca"] == marca].copy()
            df_cf_marca = df_cf[df_cf["Marca"] == marca].copy()
            
            if df_cf_marca.empty:
                continue  # Si no hay referencias en df_cf para la marca, pasar
            
            # Vectorizar solo las referencias dentro de la misma marca
            vectorizer = TfidfVectorizer()
            vectorizer.fit(pd.concat([df_marca["Reference"], df_cf_marca["Reference"]]))

            tfidf_df1 = vectorizer.transform(df_marca["Reference"])
            tfidf_df2 = vectorizer.transform(df_cf_marca["Reference"])
            
            # Calcular distancias Manhattan
            manhattan_distances = pairwise_distances(tfidf_df1, tfidf_df2, metric="manhattan")
            most_similar_indices = manhattan_distances.argmin(axis=1)

            # Asignar valores basados en la similitud
            df.loc[df["Marca"] == marca, "cod_fasecolda"] = df_cf_marca.iloc[most_similar_indices]["Codigo"].values
            df.loc[df["Marca"] == marca, "match"] = df_cf_marca.iloc[most_similar_indices]["Reference"].values
            df.loc[df["Marca"] == marca, "manhattan"] = manhattan_distances.min(axis=1)
            df.loc[df["Marca"] == marca, "%_similitud"] = (1 / (1 + df.loc[df["Marca"] == marca, "manhattan"])) * 100
            df.loc[df["Marca"] == marca, "REFERENCIA1_FASECOLDA"] = df_cf_marca.iloc[most_similar_indices]["Referencia1"].values
            df.loc[df["Marca"] == marca, "REFERENCIA2_FASECOLDA"] = df_cf_marca.iloc[most_similar_indices]["Referencia2"].values
            df.loc[df["Marca"] == marca, "REFERENCIA3_FASECOLDA"] = df_cf_marca.iloc[most_similar_indices]["Referencia3"].values
            df.loc[df["Marca"] == marca, "MARCA_FASECOLDA"] = df_cf_marca.iloc[most_similar_indices]["Marca"].values

            # Comparación fuzzy
            df.loc[df["Marca"] == marca, "comparacion fuzzy"] = df[df["Marca"] == marca].apply(
                lambda row: fuzz.token_sort_ratio(row["Reference"], row["match"]) > 40, axis=1
            )
            df.loc[df["Marca"] == marca, "%"] = df[df["Marca"] == marca].apply(
                lambda row: fuzz.partial_ratio(row["Reference"], row["match"]), axis=1
            )

            # 1. Siempre quitar si % < 40
            df.loc[(df["Marca"] == marca) & (df["%"] < 40), "cod_fasecolda"] = pd.NA

            # 2. Si comparacion fuzzy es False y % <= 70, quitar
            df.loc[(df["Marca"] == marca) & (df["comparacion fuzzy"] == False) & (df["%"] <= 78), "cod_fasecolda"] = pd.NA


        return df


    
