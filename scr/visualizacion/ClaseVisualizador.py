import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
class Visualizador:
    def __init__(self, df):
        self.df = df
        sns.set_theme(style="whitegrid")

#Histogramas,
    def histograma_Prom_votos(self):

        #filtro
        filtro_ceros= self.df[self.df['vote_average']>0].copy()

        fig, ax = plt.subplots(figsize=(10, 6))
        plt.hist(filtro_ceros['vote_average'], bins=30, color='skyblue', alpha=0.7) # bins es para ver mejor donde hay mas peliculas

        media = filtro_ceros['vote_average'].mean()
        ax.axvline(media, color='red', linestyle='dashed', linewidth=2, label=f'Media: {media:.2f}')

        plt.xlabel('Promedio de Votos ')
        plt.ylabel('Cantidad de Películas')
        plt.title('Catidad de peliculas y su distribucion de promedio de Votos')
        ax.text(0.1, 0.9,
                "Insight: La distribución es normal pero tiene un pico cerca del 6.2.\n"
                    "y esto lo que indica es que el catalogo tiene calidad balanceada,\n",
                transform=ax.transAxes, fontsize=8, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
        return fig

# scatter,
    def scatter_popularidad(self):

        filtro_ceros = self.df[(self.df['vote_average'] > 0) & (self.df['popularity'] > 0)].copy()

        tituloyInsight = (
            "<b>Relacion entre la Popularidad de las Peliculas y su Promedio de Votos</b><br>"
            
            "<i>¿Catidad de votos es igual a Popularidad?</i><br>"
            "<i>Notamos que las Calificaciones altas no garantizan la mayor popularidad </i>"
        )

        fig = px.scatter(filtro_ceros,x= 'vote_average',y='popularity',hover_name="title",color="vote_count",
                         title=tituloyInsight,labels={'vote_average': 'Calificación', 'popularity': 'Popularidad'})

        return fig

# heatmap
    def heatmap_correlacion(self, matriz_cal):
        fig, ax = plt.subplots(figsize=(12, 8))

        # 2. Dibujar la matriz
        i_m = ax.matshow(matriz_cal, cmap='YlGnBu', aspect='auto', origin='upper')
        ax.grid(False)

        plt.colorbar(i_m, label='Intensidad de Correlación')

        # Ciclo para los numeros
        for i in range(matriz_cal.shape[0]):
            for j in range(matriz_cal.shape[1]):
                valor = matriz_cal.iloc[i, j]

                ax.text(j, i, f'{valor:.2f}', ha='center', va='center', color='white', fontsize=10)

        # nombres reales de las columnas
        columnas = matriz_cal.columns.tolist()

        ax.set_xticks(range(len(columnas)))
        # se rota a  45 grados y alineacion a la izquierda para que no se superpongan
        ax.set_xticklabels(columnas, rotation=45, ha='left', fontsize=10)

        ax.set_yticks(range(len(columnas)))
        ax.set_yticklabels(columnas, fontsize=10)

        ax.set_title('Mapa de Correlaciones de Movie Insights', pad=30)
        ax.text(0.5, -0.25,
                "Insight: La correlacion mas relevante es entre 'vote_average' y 'vote_count' con un 0.37\n"
                "Esto sugiere que a mayor calidad(vote_average) percibida, mayor es el volumen de interaccion('vote_count').\n"
                "La popularidad muestra una independencia casi total de la calificación promedio de calidad(vote_average) con un 0.01",
                transform=ax.transAxes, fontsize=10, ha='center',
                bbox=dict(boxstyle='round', facecolor='azure', alpha=0.8))

        # no corta nada la mostrar
        plt.tight_layout()

        return fig


#barras verticales
    def barras_estadis(self, resumen_est, nom_columna):

        nombres= ['Minimo', 'Promedio', 'Maximo']
        valores = [resumen_est.loc['min',nom_columna], resumen_est.loc['mean',nom_columna], resumen_est.loc['max',nom_columna]]

        fig, ax = plt.subplots(figsize=(10, 6))

        barra= plt.bar(nombres,valores, color='skyblue')
        plt.bar_label(barra, padding=3, fmt='%.2f')

        plt.xlabel('Estadisticas')
        plt.ylabel(f'Valores de {nom_columna}')
        plt.title(f'Analisis de {nom_columna}: Minimo, Promedio y Maximo')

        diferencia = resumen_est.loc['max', nom_columna] / resumen_est.loc['mean', nom_columna]
        ax.text(0.5, 0.95,
                f"Insight: Existe una alta disparidad en {nom_columna}.\n"
                f"El valor máximo es aproximadamente {diferencia:.1f} veces mayor que el promedio,\n"
                "lo que confirma la presencia de 'Outliers' o exitos excepcionales en los datos.",
                transform=ax.transAxes, fontsize=9, ha='center', va='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        return fig

#barras
    def barras_idiomas(self):
        conteo_idiomas = self.df['original_language'].value_counts()
        idiomas = conteo_idiomas.index
        cantidades = conteo_idiomas.values

        fig, ax = plt.subplots(figsize=(12, 8))

        ax.bar(idiomas, cantidades, color='skyblue', edgecolor='black')

        ax.set_title('Distribucion del catalogo de las paliculas por Idioma Original')
        ax.set_xlabel('Idioma Original')
        ax.set_ylabel('Cantidad de Peliculas')

        plt.xticks(rotation=45)

        for i, v in enumerate(cantidades):
            ax.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=8)


        ax.text(0.95, 0.85,
                "Insight: El catalogo muestra que el inglés es el mas comun en los datos\n"
                "tiene mas de 5,500 títulos, lo que representa una centralizacion\n"
                "en la industria de Hollywood frente a otros mercados globales.",
                transform=ax.transAxes, fontsize=10, ha='right', va='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))



        plt.tight_layout()
        return fig


#barras horizontales
    def barrash_top10_votos(self):
        #Ordenar el DF por vote_count y tomar las top 10
        top_10 = self.df.nlargest(10, 'vote_count')

        tituloyInsight = (
            "<b>Top 10 Titulos con Mayor Cantidad de Votos</b><br>"

            "<i>Se puede ver que Spider-Man lidera con una diferencia masiva sobre el resto del catálogo.</i><br>"
        )
        fig = px.bar(top_10, x='vote_count', y='title', orientation='h', color='vote_count',
                     title=tituloyInsight,text="vote_count", color_continuous_scale='Blues' )


        fig.update_layout(yaxis={'categoryorder': 'total ascending'})  # Ordena de mayor a menor

        return fig


# Lineal
    def lineal_evolucion_anual(self):
        df_temp = self.df.copy()

        #Convertir a fecha y extraer el año
        df_temp['release_date'] = pd.to_datetime(df_temp['release_date'], errors='coerce')
        df_temp = df_temp.dropna(subset=['release_date'])
        df_temp['year'] = df_temp['release_date'].dt.year

        # Agrupar por año y calcular el promedio de popularidad
        promedio_anual = df_temp.groupby('year')['popularity'].mean().sort_index()

        fig, ax = plt.subplots(figsize=(12, 6))

        # Dibujar linea
        ax.plot(promedio_anual.index, promedio_anual.values,  color='skyblue',
                marker='.', linestyle='-', linewidth=2, label='Popularidad Promedio')


        ax.set_title('Tendencia Historica de Popularidad (Por Año)')
        ax.set_xlabel('Año de Estreno')
        ax.set_ylabel('Popularidad Promedio')

        # Cuadricula para facilitar la lectura
        ax.grid(True, linestyle='--', alpha=0.7)

        ax.text(0.02, 0.95,
                "Insight: Se observa un crecimiento a partir de 2024\n"
                "Esto sugiere que pudo haber ocurrido un aumento real \n"
                " en el consumo de cine post-pandemia o se digitalizaron mas obras en este periodo.",
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        plt.tight_layout()
        return fig

    def barras_pelicula_por_ano(self):
        df_temp = self.df.copy()

        #Limpiezar las fechas para tener el año
        df_temp['release_date'] = pd.to_datetime(df_temp['release_date'], errors='coerce')
        df_temp = df_temp.dropna(subset=['release_date', 'title'])
        df_temp['year'] = df_temp['release_date'].dt.year

        #Obtener la pelicula mas popular por año
        indices_max_pop = df_temp.groupby('year')['popularity'].idxmax()
        top_por_ano = df_temp.loc[indices_max_pop, ['year', 'title', 'popularity']]

        #Filtrar los últimos 15 años de lanzamientos
        ultimo_ano = top_por_ano['year'].max()
        top_por_ano = top_por_ano[top_por_ano['year'] > (ultimo_ano - 15)]
        top_por_ano = top_por_ano.sort_values('year')

        fig, ax = plt.subplots(figsize=(12, 9))

        #titulo como etiqueta del eje Y y el año como referencia
        y_labels = [f"{int(row['year'])}: {row['title']}" for _, row in top_por_ano.iterrows()]

        barras = ax.barh(y_labels, top_por_ano['popularity'], color='skyblue', edgecolor='black')

        ax.set_title('La Pelicula Mas Popular por Año', fontsize=16, pad=20)
        ax.set_xlabel('Nivel de Popularidad', fontsize=12)
        ax.set_ylabel('Año y Titulo', fontsize=12)

        # Añadir el valor de popularidad al final de la barra
        for i, barra in enumerate(barras):
            width = barra.get_width()
            ax.text(width + 5, i, f'{width:.1f}', va='center', fontweight='bold')

        ax.text(0.98, 0.2,
                "Insight: 'Frankenstein' (2025) rompe la tendencia historica\n"
                "con 951.3 puntos de popularidad, superando por mas de\n"
                "5 veces el exito del año anterior ('Abyss', 179.6).",
                transform=ax.transAxes, fontsize=10, ha='right',
                bbox=dict(boxstyle='round', facecolor='azure', alpha=0.8))

        plt.tight_layout()
        return fig


