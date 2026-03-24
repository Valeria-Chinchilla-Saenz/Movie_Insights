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
