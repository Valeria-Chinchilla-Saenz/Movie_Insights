import pandas as pd
from eda.ClaseProcesadorEDA import CargadorDatos, LimpiadorColumnas, ProcesadorEDA

if __name__ == '__main__':
    #nombre del archivo
    nombre_archivo = "data/raw/tmdb_2020_to_2025.csv"

    #Instancia de la clase cargador de datos
    cargador = CargadorDatos(nombre_archivo)
    df = cargador.cargar_csv()

    if df is not None:
        #Exploracion de datos
        procesador_inicial = ProcesadorEDA(df)
        procesador_inicial.exploracion()

        #Instancia del limpiador de variables
        limpiador = LimpiadorColumnas(df)
        df_reducido = limpiador.eliminar_columnas()

        #Instancia del procesador eda
        ## Se usa el set de datos que posee las variables eliminadas
        procesador = ProcesadorEDA(df_reducido)
        df_limpio = procesador.limpieza_datos()

        print(procesador.resumen_estadistico()) #imprime el resumen estadistico
        print(procesador.matriz_correlacion()) #imprime la matriz de correlacion

        cargador.guardar_csv(df_limpio, nombre_archivo = "data/processed/tmdb_movies_clean.csv")