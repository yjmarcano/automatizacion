# ==========================================
# 1. IMPORTACIÓN DE LIBRERÍAS
# ==========================================

# import: Palabra reservada para cargar módulos (bibliotecas de funciones).
# as: Define un alias o "apodo" para no escribir el nombre largo cada vez.
import numpy as np  # Manejo de arreglos numéricos (vectores) y matemáticas.
import pandas as pd # Herramienta principal para manipular tablas de datos (DataFrames).
import os           # Módulo para interactuar con el sistema operativo (archivos y carpetas).
import urllib.request # Módulo para realizar peticiones de red (conectar a URLs).

# ==========================================
# 2. LECCIÓN 1: NUMPY (Creación de datos)
# ==========================================

# np.array(): Función que transforma una lista de Python en un arreglo de NumPy.
# Parámetro: [101...]: Una lista con los valores que queremos almacenar.
# ¿Por qué?: Los arreglos de NumPy consumen menos memoria y son mucho más rápidos que las listas.
ids = np.array([101, 102, 103, 104, 105, 106, 107, 108, 109, 110])

# np.nan: Es una constante que significa "Not a Number" (Dato nulo o vacío).
# Usamos 9999.0 como un "outlier" (valor extremo o erróneo) para practicar la limpieza.
montos = np.array([150.0, 200.0, 50.0, np.nan, 120.0, 450.0, 80.0, 210.0, 95.0, 9999.0])

# ==========================================
# 3. LECCIÓN 2 Y 3: CARGA DE DATOS LOCALES
# ==========================================

# Definición de variables de texto (Strings) con los nombres de tus archivos CSV.
file_contacto = 'clientes_contacto.xlsx - Sheet1.csv'
file_regiones = 'regiones.csv'

# os.path.exists(): Función que verifica si el archivo está físicamente en la carpeta.
# Parámetro: El nombre de la variable que contiene el nombre del archivo.
# and: Operador lógico que exige que ambas condiciones sean verdaderas para proceder.
if os.path.exists(file_contacto) and os.path.exists(file_regiones):
    
    # pd.read_csv(): Función que lee archivos de texto y los convierte en DataFrames (tablas).
    # Parámetro: La ruta del archivo CSV.
    df_contacto = pd.read_csv(file_contacto)
    df_regiones = pd.read_csv(file_regiones)
    
else:
    # pd.DataFrame(): Constructor que crea una tabla manual desde un diccionario.
    # Parámetro: Un diccionario {'NombreColumna': DatosColumna}.
    # ['user@mail.com']*10: Repite el texto 10 veces para llenar las filas.
    df_contacto = pd.DataFrame({'ID_Cliente': ids, 'Email': ['user@mail.com']*10})
    df_regiones = pd.DataFrame({'ID_Cliente': ids, 'Region': ['Norte']*10})

# Creamos una tabla uniendo los arreglos de IDs y montos que hicimos arriba.
df_ventas = pd.DataFrame({'ID_Cliente': ids, 'Monto': montos})

# ==========================================
# 4. CARGA DESDE WEB (Web Scraping)
# ==========================================

# Guardamos la dirección web de Wikipedia en una variable.
url = "https://es.wikipedia.org/wiki/ISO_3166-1"

# urllib.request.Request(): Prepara la petición antes de enviarla.
# Parámetro headers: Metadatos. 'User-Agent' simula que somos un navegador para evitar bloqueos (Error 403).
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

# with: Asegura que la conexión de red se cierre sola al terminar el bloque, evitando fugas de datos.
# urlopen(): Abre la conexión a la URL configurada.
with urllib.request.urlopen(req) as response:
    
    # pd.read_html(): Escanea el código HTML de la página en busca de etiquetas <table>.
    # Parámetro (response): El contenido de la página web.
    # Retorna: Una lista que contiene todas las tablas encontradas.
    tablas = pd.read_html(response)
    
    # if/else en una línea (Operador ternario): Evalúa cuántas filas tiene la tabla 0.
    # len(): Cuenta el número de filas. Si la primera tabla es muy pequeña, usa la segunda.
    df_temp = tablas[0] if len(tablas[0]) > 5 else tablas[1]
    
    # .iloc[:10, [0]]: Seleccionador por posición.
    # Parámetro 1 (:10): Indica que queremos las primeras 10 filas.
    # Parámetro 2 ([0]): Indica que queremos solo la columna en la posición 0 (la primera).
    # .copy(): Crea un objeto nuevo independiente en la memoria.
    # .reset_index(drop=True): Borra el índice de Wikipedia y pone uno limpio de 0 a 9.
    df_web = df_temp.iloc[:10, [0]].copy().reset_index(drop=True)
    
    # .columns: Atributo para asignar nombres nuevos a los encabezados de la tabla.
    df_web.columns = ['Pais']
    
    # Añadimos la columna ID para que la tabla sea compatible con el resto.
    df_web['ID_Cliente'] = ids

# ==========================================
# 5. LECCIÓN 3: UNIFICACIÓN (Merge)
# ==========================================

# pd.merge(): Función que une dos tablas basándose en una columna compartida (la "llave").
# Parámetro on='ID_Cliente': Especifica qué columna debe usar para emparejar las filas.
# Es como un rompecabezas: une los datos donde los IDs coincidan exactamente.
df_maestro = pd.merge(df_ventas, df_contacto, on='ID_Cliente')
df_maestro = pd.merge(df_maestro, df_regiones, on='ID_Cliente')
df_maestro = pd.merge(df_maestro, df_web, on='ID_Cliente')

# ==========================================
# 6. LECCIÓN 4: LIMPIEZA DE DATOS
# ==========================================

# .mean(): Método estadístico que suma todos los valores y los divide entre el total.
# Ignora automáticamente los valores nulos (NaN).
media = df_maestro['Monto'].mean()

# .fillna(): Método que busca los valores vacíos (nulos) y los rellena.
# Parámetro (media): El valor que calculamos arriba para reemplazar los huecos.
df_maestro['Monto'] = df_maestro['Monto'].fillna(media)

# Filtro Booleano: df[ condicion ]
# Solo conserva las filas donde el Monto es menor a 1000. Esto borra el 9999.0 erróneo.
df_limpio = df_maestro[df_maestro['Monto'] < 1000].copy()

# ==========================================
# 7. LECCIÓN 5: TRANSFORMACIÓN
# ==========================================

# .drop_duplicates(): Escanea la tabla y borra filas que sean 100% iguales a otra anterior.
df_limpio = df_limpio.drop_duplicates()

# .astype(str): Función de "Casting" (cambio de tipo de dato).
# Parámetro (str): Convierte los números (101) en texto ("101").
# ¿Por qué?: El ID es una etiqueta de nombre, no un valor para sumar matemáticamente.
df_limpio['ID_Cliente'] = df_limpio['ID_Cliente'].astype(str)

# Operación Vectorizada: Pandas multiplica cada celda de 'Monto' por 0.21 automáticamente.
# Crea una columna nueva llamada 'IVA' con el resultado.
df_limpio['IVA'] = df_limpio['Monto'] * 0.21

# ==========================================
# 8. LECCIÓN 6: EXPORTACIÓN
# ==========================================

# .to_csv / .to_excel: Métodos para escribir los datos en un archivo físico.
# Parámetro index=False: Indica que NO guarde la columna numérica extra que pone Pandas a la izquierda.
df_limpio.to_csv('resultado_final.csv', index=False)
df_limpio.to_excel('resultado_final.xlsx', index=False)

# print(): Imprime un mensaje final en la consola.
print("¡Proceso completado! Los archivos han sido generados correctamente.")