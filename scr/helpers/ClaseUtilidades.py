import os

class Utilidades:
    def __init__(self, df = None):
        self.df = df

    def validar_archivo(self, ruta_archivo):
        #Verifica si existe el archivo antes de realizar la carga
        if os.path.exists(ruta_archivo):
            print(f"Archivo {ruta_archivo} existe")
            return True
        else:
            print(f"Archivo {ruta_archivo} no existe")
            return False

    def crear_carpeta(self, ruta_carpeta):
        #Crea la carpeta solamente si no existe
        try:
            if not os.path.exists(ruta_carpeta):
                os.makedirs(ruta_carpeta)
                print(f"Carpeta creada con exito: {ruta_carpeta}")
                return True
            else:
                print("Carpeta ya existe, revisa si no estas omitiendo un paso")
                return False

        except Exception as e:
            print("Error al crear carpeta")
            return False

