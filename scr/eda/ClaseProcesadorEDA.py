import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class CargadorDatos:
    def __init__(self, archivo):
        self.archivo = archivo
        self.df = None
        self.numfilas = 0
        self.nulos = 0.0 #cuenta si hay celdas vacias

    def cargar_csv(self):
        try:
            self.df = pd.read_csv(self.archivo, sep = ',')
            self.numfilas = len(self.df)

            total_celdas = self.df.size
            total_nulos = self.df.isnull().sum().sum()

            self.nulos = 0
            if total_celdas > 0:
                self.nulos = total_nulos / total_celdas * 100
            else:
                self.nulos = 0.0

            return self.df

        except FileNotFoundError:
            print("No se pudo cargar el archivo")
            return None

    def guardar_csv(self, dataframe, nombre_archivo = 'tmdb_movies_clean.csv'):

        try:
            dataframe.to_csv(nombre_archivo, index = False)
            print("Archivo guardado")
        except FileNotFoundError:
            print("No se pudo guardar el archivo")

class LimpiadorColumnas:
    def __init__(self, dataframe):
        self.df = dataframe.copy() #crea una copia del set de datos para alterar el original

    def eliminar_columnas(self):
        columnas_eliminadas = ['backdrop_path', 'poster_path']
        self.df.drop(columns = columnas_eliminadas, errors = 'ignore', inplace = True)
        return self.df

class ProcesadorEDA:
    def __init__(self, dataframe):
        self.df = dataframe.copy() #se trabaja desde una copia, asi un error no dañara el original

    def limpieza_datos(self):

        #Manejo de nulos
        self.df.dropna(subset = ['title', 'release_date'], inplace = True)
        self.df['vote_average'] = self.df['vote_average'].fillna(0.0) # Si no hay nota, asume 0
        self.df['vote_count'] = self.df['vote_count'].fillna(0)

        #Formato de datos correcto
        self.df['release_date'] = pd.to_datetime(self.df['release_date'], errors='coerce')
        self.df['popularity'] = pd.to_numeric(self.df['popularity'], errors='coerce')

        #Normalización de genero e idioma
        if 'original_language' in self.df.columns:
            self.df['original_language'] = self.df['original_language'].str.strip().str.upper() #elimina los espacios en blanco y lo pasa a mayuscula
            self.df['original_language'] = self.df['original_language'].astype('category')

        if 'genre_ids' in self.df.columns:
            #elimacion de los parentesis cuadrados
            self.df['genre_ids'] = self.df['genre_ids'].astype(str).str.replace(r'[\[\]]', '', regex=True)

        print("Limpieza completa")
        return self.df

    def resumen_estadistico(self):
        resumen = self.df.describe(include = 'number') #incluye solo las columnas numericas
        return resumen

    def matriz_correlacion(self):
        columnas_numericas = self.df. select_dtypes(include = 'number').corr(method = 'pearson')

        if 'id' in columnas_numericas.columns:
            columnas_numericas = columnas_numericas.drop(columns = ['id'])

        #Calculo de la correlacion
        matriz = columnas_numericas.corr(method = 'pearson')
        return matriz










