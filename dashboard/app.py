import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scr.eda.ClaseProcesadorEDA import CargadorDatos, LimpiadorColumnas, ProcesadorEDA
from scr.visualizacion.ClaseVisualizador import Visualizador
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuracion de la pagina
st.set_page_config(page_title="Movie Insights Dashboard", layout="wide")

#Cargar los datos limpios
ruta_limpia = "data/processed/tmdb_movies_clean.csv"

@st.cache_data
def datos_procesados():
    cargador = CargadorDatos(ruta_limpia)
    df = cargador.cargar_csv()
    return df

df = datos_procesados()

if df is not None:
    st.title("Movie Insights: Análisis 2020-2025")
    st.markdown("---")# linea que hace unan divicion visual

    # Metricas principales
    col1, col2, col3 = st.columns(3) # son tres columnas para mostrar las metricas
    # aqui se le dice que mosotrar en cada columna
    with col1:
        st.metric("Total Películas", len(df))
    with col2:
        st.metric("Promedio Votos", round(df['vote_average'].mean(), 2))
    with col3:
        st.metric("Máxima Popularidad", df['popularity'].max())

    st.markdown("---")

    # Grficos interactivos
    col_iz1, col_de2 = st.columns(2)

    with col_iz1:
        st.subheader("Histograma para apreciar cual es la cantidad peliculas con mayor promedio de voto")


        fig_hist = px.histogram(df, x="vote_average", nbins=20,
                                title="Catidad de peliculas y su distribucion de promedio de Votos", color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig_hist, use_container_width=True)


    with col_de2:
        viz = Visualizador(df)

        st.subheader("Scatter que muestra la relacion que existe entre la popularidad y el promedio de votos que tienen las peliculas")
        fig_scatter = viz.scatter_popularidad()
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    col_iz3, col_de4 = st.columns(2)

    with col_iz3:
        proc = ProcesadorEDA(df)

        st.subheader("Heatmap que muestra las correlaciones que existen entre cada columna del set de datos")

        matriz_c = proc.matriz_correlacion()
        fig_heat = px.imshow(matriz_c, text_auto=True, aspect="auto",
                          title="Mapa de Correlaciones de Movie Insights",
                          color_continuous_scale='RdBu_r')
        st.plotly_chart(fig_heat, use_container_width=True)

    with col_de4:
        resumen = proc.resumen_estadistico()
        st.subheader("Grafico de barras verticales que muestran el analisis comparatorio resumen estadistico realizado en la ClaseProcesadorEDA")
        resumen = proc.resumen_estadistico()

        filas_uso = ['mean', 'min', 'max']
        resumen_filtrado = resumen.loc[filas_uso]

        opciones_menu = resumen_filtrado.columns.tolist()
        col_selecci = st.selectbox("Selecciona la metrica a analizar:",opciones_menu,key = "selector")

        fig_est = px.bar(resumen_filtrado, x=resumen_filtrado.index, y=col_selecci, title=f"Analisis de el  Minimo, Promedio y Maximo de: {col_selecci}", labels={'index': 'Estadisticas', col_selecci: 'Valores'}, color=resumen_filtrado.index,
            text_auto='.2f',color_discrete_map={'mean': '#636EFA', 'min': '#EF553B', 'max': '#00CC96'} )
        st.plotly_chart(fig_est, use_container_width=True)

    st.markdown("---")

    col_iz5, col_de6 = st.columns(2)

    with col_iz5:
        st.subheader("Grafico de barras horizontales que muestra las 10 peliculas mas votadas dentro del set de datos")
        fig_top = viz.barrash_top10_votos()
        st.plotly_chart(fig_top, use_container_width=True)

    with col_de6:
        st.subheader("Grafico de barras verticales que muestra la tendencia en los idiomas presentes en el dataset")
        idiomas = df['original_language'].value_counts().head(10)
        fig_pie = px.pie(values=idiomas.values, names=idiomas.index,
                         title="Distribucion del catalogo de las paliculas por Idioma Original, el Top 10")
        st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("---")

    col_iz7, col_de8 = st.columns(2)
    with col_iz7:
        df['release_date'] = pd.to_datetime(df['release_date'])
        df['release_year'] = df['release_date'].dt.year

        st.subheader("Grafico lineal que muestra la tendencia historica de la popularidad")
        # Agrupa por año y calcula el promedio de la popularidad
        df_evolucion = df.groupby('release_year')['popularity'].mean().reset_index()

        fig_lineal = px.line(df_evolucion, x='release_year', y='popularity',title="Tendencia Historica de Popularidad (Por Año)",
                             markers=True, labels={'release_year': 'Año de Estreno', 'popularity': 'Popularidad Promedio'}) # el markers es para que se vean los puntos exactos

        fig_lineal.update_traces(line_color='#FF4B4B', line_width=3)
        st.plotly_chart(fig_lineal, use_container_width=True)

    with col_de8:
        st.subheader("Grafico de barras verticales que muestra la pelicula mas popular y su año ")
        df['release_date'] = pd.to_datetime(df['release_date'])
        df['release_year'] = df['release_date'].dt.year

        #Con esto se tiene la pelicula top por año
        idx_max = df.groupby('release_year')['popularity'].idxmax()
        df_top_anual = df.loc[idx_max].sort_values('release_year')

        fig_anual = px.bar(df_top_anual, x='release_year', y='popularity',hover_data=['title'],text='title',title="La Pelicula Mas Popular por Año",
                           color='popularity',color_continuous_scale='Viridis')

        fig_anual.update_traces(textposition='outside')
        st.plotly_chart(fig_anual, use_container_width=True)
else:
    st.error(f"No se encontró el archivo en {ruta_limpia}.")

#Usar esto en la terminal para cargar el streamlit si no funciona instalandolo
#En caso de que instalando no funcione hay que usar esta linea en la terminal cada vez que se quiera ejecutar el codigo
# streamlit se ejecuta en la terminal
#& "C:\Users\estef\AppData\Local\Programs\Python\Python314\python.exe" -m streamlit run dashboard/app.py
