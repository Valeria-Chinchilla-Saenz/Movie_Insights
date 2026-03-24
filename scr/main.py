import pandas as pd
from eda.ClaseProcesadorEDA import CargadorDatos, LimpiadorColumnas, ProcesadorEDA
from visualizacion.ClaseVisualizador import Visualizador
import matplotlib.pyplot as plt
from helpers.ClaseUtilidades import Utilidades

if __name__ == '__main__':
    #nombre del archivo
    nombre_archivo = "data/raw/tmdb_2020_to_2025.csv"

    utilid = Utilidades()

    if utilid.validar_archivo(nombre_archivo):
        #para crear la carpeta
        utilid.crear_carpeta("data/processed")

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

            print("\nResumen estadistico")
            print(procesador.resumen_estadistico()) #imprime el resumen estadistico
            print("\nMatriz de correlacion")
            print(procesador.matriz_correlacion()) #imprime la matriz de correlacion

            cargador.guardar_csv(df_limpio, nombre_archivo = "data/processed/tmdb_movies_clean.csv")


            #Histograma
            viz = Visualizador(df_limpio)
            histo = viz.histograma_Prom_votos()
            plt.show()


            #Distibucion
            scatte = viz.scatter_popularidad()
            scatte.show()

            #Mapa correlacion
            proc = ProcesadorEDA(df_limpio)
            matriz_c = proc.matriz_correlacion()

            heat_map = viz.heatmap_correlacion(matriz_c)
            plt.show()

            #Grafico de las estadisticas

            resumen = proc.resumen_estadistico()

            print("\nColumnas disponibles para analizar:", resumen.columns.tolist())
            col_selecci = input("Escriba el nombre de la columna que desea graficar: ").strip()
            if col_selecci in resumen.columns:
                fig_est = viz.barras_estadis(resumen, col_selecci)
                plt.show()
            else:
                print(f"Error: La columna '{col_selecci}' no se encuentra en el dataset.")


            #barras idiomas

            bar_idiomas = viz.barras_idiomas()
            plt.show()


            #barras horizontales
            top_votos = viz.barrash_top10_votos()
            top_votos.show()

            # grafico lineal
            evo_fechas = viz.lineal_evolucion_anual()
            plt.show()

            # barras top anunal
            bar_top_anual = viz.barras_pelicula_por_ano()
            plt.show()
else:
        print("Error: El flujo se detuvo porque el archivo de origen no fue encontrado.")













