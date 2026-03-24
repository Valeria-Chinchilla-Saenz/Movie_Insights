# Movie_Insights
Un sistema en Python con Programacion Orientada a Objetos que analiza datos de películas.

### Librerias utilizadas
Se utiliza las librerias pandas y maptplotlib para realizar el análisis.
#### Codigo para cargar las librerias
import pandas as pd

import matplotlib.pyplot as plt

### Estructura del sistema

scr/eda: centraliza la lógica de la limpieza y el análisis estdistico.

scr/visualizacion: gestiona la generación de gráficos y mapas de calor.

scr/helpers: optimiza la ejecución mediante las funciones de soporte y utilidades reutilizables.

data/raw: almacena el set de datos original sin procesar (solo lectura).

data/processed: almacena el set de datos limpio tras la ejecución.

notebooks: presentación interactiva con el análisis visual y explicativo paso a paso.

### Explicación de ClaseProcesadorEDA.py

### Clase CargadorDatos 
La clase CargadorDatos automatiza la lectura de los archivos CSV y genera un diagnostico inicial de la calidad de los datos (conteo de nulos y registros).

### Clase LimpiadorColumnas 
La clase LimpiadorColumnas crea una copia del set de datos original y elimina las variables 'backdrop_path', 'poster_path', estas variables se eliminaron debido a que no aportan al ánalisis.

### Clase ProcesadorEDA
La clase ProcesadorEDA contiene los siguientes métodos:

- El método exploración permite explorar y conocer el set de datos antes de la limpieza.

- El método limpieza de datos permite limpiar el set de datos. Este permite realizar por medio del manejo de nulos la imputación de la variable 'overview', además le da formato de datos correctos a las variables 'popularity' y 'release_date'. Luego en la variable 'original_language' se realiza la limpieza de los espacios invisibles y lo convierte a mayuscula y también en la variable 'genre_ids' se eliminan los parentisis cuadrados. Y finalmente retorna el set de datos limpio. 

- El método resumen estadistico muestra las medidas de las variables númericas.

- El método matriz de correlación genera un mapa que mide que tan fuerte es la relación entre las variables númericas (sin tomar encuenta la varible 'id').


### Explicación de ClaseVisualizador.py

La clase Visualizador es la encargada de transformar el set de datos procesado en representaciones gráficas.

El histograma prom votos muestra cual es la cantidad de peliculas con mayor promedio de voto lo hace primero filtrando los ceros existentes en la columna 'vote_average', utilizando la variable que guarda el resultado de la acción anterior, crea el histograma que muestra los resultados. También se utiliza una línea que marca la media de la variable 'vote_average' así como un insight que resume el analisis de los resultados. 

El diagrama de dispersión popularidad muestra la relación que existe entre la popularidad y el promedio de votos que tienen las peliculas. Lo primero que hace es un filtrado de ceros existentes en la columna 'vote_average' y 'popularity', utilizando la variable que guarda el resultado de la acción anterior, crea el diagrama de dispersión que mestra los resultados. 

El mapa de calor muestra las correlaciones que existen entre cada columna del set de datos. Hace un ciclo de los numeros y añade los nombres reales de las columnas y dibuja la matriz.

El gráfico de barras verticales estadistic muestra el analisis comparativo del promedio, minimo, maximo del resumen estadistico realizado en la clase ProcesadorEDA. 

El gráfico de barras idiomas muestra la tendencia de los idiomas presentes en el set de datos.  

El gráfico de lineal de la evolución anual muestra la tendencia historica de la popularidad. Lo primero que hace es utilizar una copia del set de datos, convierte a fecha y extrae el año agrupandolo por año y calcula el promedio de la propularidad, crea el gráfico líneal.

El gráfico de barras horizontales de las peliculas por año muestra la película más popular y su año de lanzamiento. Lo primero que hace es realizar una copia del set de datos, limpia las fechas para obtener el año y obtener así la pelicula más popular y hace un filtro de los últimos 15 años de lanzamientos, y crea del gráfico.