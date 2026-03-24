import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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
        return fig

# scatter,
    def scatter_popularidad(self):

        filtro_ceros = self.df[self.df['vote_average'] > 0][['vote_average', 'popularity']].copy()

        fig, ax = plt.subplots(figsize=(10, 6))
        plt.scatter(filtro_ceros['vote_average'],filtro_ceros['popularity'],  color='skyblue')
        plt.xlabel("promedio de votos")
        plt.ylabel("nivel de popularidad")
        plt.title("Relacion entre la Popularidad de las Peliculas y su Promedio de Votos")
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

        # no corta nada la mostrar
        plt.tight_layout()

        return fig


#barras verticales
    def barras_estadis(self, resumen_est, nom_columna):

        nombres= ['Mínimo', 'Promedio', 'Máximo']
        valores = [resumen_est.loc['min',nom_columna], resumen_est.loc['mean',nom_columna], resumen_est.loc['max',nom_columna]]

        fig, ax = plt.subplots(figsize=(10, 6))

        barra= plt.bar(nombres,valores, color='skyblue')
        plt.bar_label(barra, padding=3, fmt='%.2f')

        plt.xlabel('Estadísticas')
        plt.ylabel(f'Valores de {nom_columna}')
        plt.title(f'Análisis de {nom_columna}: Mínimo, Promedio y Máximo')

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
        ax.set_ylabel('Cantidad de Películas')

        plt.xticks(rotation=45)

        for i, v in enumerate(cantidades):
            ax.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        return fig


#barras horizontales
    def barrash_top10_votos(self):
        #Ordenar el DF por vote_count y tomar las top 10
        top_10 = self.df.nlargest(10, 'vote_count')

        fig, ax = plt.subplots(figsize=(12, 8))

        barras = ax.barh(top_10['title'], top_10['vote_count'],
                         color='skyblue', edgecolor='black')

        # La barra numero 1 sale arriba con esto
        ax.invert_yaxis()

        ax.set_title('Top 10 Títulos con Mayor Cantidad de Votos')
        ax.set_xlabel('Cantidad de Votos')
        ax.set_ylabel('Título de la Película')

        # Añadir el número exacto al final de cada barra
        for i, barra in enumerate(barras):
            votos = top_10['vote_count'].iloc[i]
            ax.text(votos + (votos * 0.01), i, f'{int(votos)}',
                    va='center', fontsize=10, fontweight='bold')

        plt.tight_layout()
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

        ax.set_title('La Pelicula Mas Popular por Año de Estreno', fontsize=16, pad=20)
        ax.set_xlabel('Nivel de Popularidad', fontsize=12)
        ax.set_ylabel('Año y Titulo', fontsize=12)

        # Añadir el valor de popularidad al final de la barra
        for i, barra in enumerate(barras):
            width = barra.get_width()
            ax.text(width + 5, i, f'{width:.1f}', va='center', fontweight='bold')

        plt.tight_layout()
        return fig


