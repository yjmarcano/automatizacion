# Importación de librerías: Bloques de herramientas especializadas
import numpy as np  # Manejo de arreglos numéricos y valores matemáticos nulos
import pandas as pd # Manipulación de estructuras de datos en forma de tabla (DataFrames)
import os           # Gestión del sistema operativo (carpetas, rutas y archivos)
import urllib.request # Módulo para realizar peticiones a sitios web a través de la red

# --- LECCIÓN 1: NUMPY (Estructuras de datos básicas) ---
# np.array(): Convierte una lista de Python en un arreglo de NumPy (más rápido y eficiente)
ids = np.array([101, 102, 103, 104, 105, 106, 107, 108, 109, 110])

# np.nan: Es una constante que representa "Not a Number" (dato faltante o vacío)
# Los valores con decimales (.0) aseguran que el arreglo sea de tipo flotante (float)
montos = np.array([150.0, 200.0, 50.0, np.nan, 120.0, 450.0, 80.0, 210.0, 95.0, 9999.0])

# --- LECCIÓN 2 Y 3: CARGA Y CONTROL DE FLUJO ---
# Definimos variables de texto (strings) con los nombres de los archivos externos
file_contacto = 'clientes_contacto.xlsx - Sheet1.csv'
file_regiones = 'regiones.csv'

# os.path.exists(): Función booleana (True/False) que verifica la existencia de un archivo en el disco
if os.path.exists(file_contacto) and os.path.exists(file_regiones):
    # pd.read_csv(): Carga un archivo separado por comas y crea un objeto DataFrame
    df_contacto = pd.read_csv(file_contacto)
    df_regiones = pd.read_csv(file_regiones)
else:
    # pd.DataFrame(): Constructor que crea una tabla manual usando un diccionario {Columna: Datos}
    # ['texto']*10: Multiplica el texto para llenar 10 filas rápidamente con el mismo valor
    df_contacto = pd.DataFrame({'ID_Cliente': ids, 'Email': ['user@mail.com']*10})
    df_regiones = pd.DataFrame({'ID_Cliente': ids, 'Region': ['Norte']*10})

# Creamos el tercer DataFrame para las ventas usando los arreglos de la Lección 1
df_ventas = pd.DataFrame({'ID_Cliente': ids, 'Monto': montos})

# --- CARGA DESDE WEB (Web Scraping avanzado) ---
url = "https://es.wikipedia.org/wiki/ISO_3166-1"

# urllib.request.Request(): Crea un objeto de petición para configurar el acceso a la URL
# headers={'User-Agent': ...}: Engaña al servidor para que crea que somos un navegador Chrome/Firefox
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

# with ... as response: Abre la conexión y asegura que se cierre automáticamente al terminar
with urllib.request.urlopen(req) as response:
    # pd.read_html(): Escanea el código HTML en busca de tablas y devuelve una lista de DataFrames
    tablas = pd.read_html(response)
    
    # Operador ternario (if en una línea): Selecciona la tabla 0 si es grande, sino la 1
    # len(): Función que cuenta cuántas filas tiene el DataFrame
    df_temp = tablas[0] if len(tablas[0]) > 5 else tablas[1]
    
    # .iloc[:10, [0]]: Selector de Pandas por posición [filas, columnas]
    # :10 indica desde el inicio hasta la fila 10; [0] indica solo la primera columna
    # .copy(): Crea una copia física en memoria para evitar advertencias de edición (SettingWithCopy)
    # .reset_index(drop=True): Borra el índice viejo y crea uno nuevo de 0 a 9
    df_web = df_temp.iloc[:10, [0]].copy().reset_index(drop=True)
    
    # .columns: Atributo que permite asignar nombres nuevos a los encabezados de la tabla
    df_web.columns = ['Pais']
    
    # Asignación de columna: Crea la columna 'ID_Cliente' y le pega el arreglo 'ids'
    df_web['ID_Cliente'] = ids

# --- LECCIÓN 3: UNIFICACIÓN (MERGE) ---
# pd.merge(): Función para unir tablas basándose en una columna compartida (Join en SQL)
# on='ID_Cliente': Especifica que la unión se hace donde los IDs coincidan exactamente
df_maestro = pd.merge(df_ventas, df_contacto, on='ID_Cliente')
df_maestro = pd.merge(df_maestro, df_regiones, on='ID_Cliente')
df_maestro = pd.merge(df_maestro, df_web, on='ID_Cliente')

# --- LECCIÓN 4: LIMPIEZA DE DATOS ---
# .mean(): Método que suma los valores y divide por el total, ignorando los nulos (NaN)
media = df_maestro['Monto'].mean()

# .fillna(): Método para el tratamiento de datos faltantes; rellena los huecos con el valor dado
df_maestro['Monto'] = df_maestro['Monto'].fillna(media)

# Filtrado booleano: Evalúa cada fila y solo deja las que cumplen la condición (menor a 1000)
df_limpio = df_maestro[df_maestro['Monto'] < 1000].copy()

# --- LECCIÓN 5: TRANSFORMACIÓN ---
# .drop_duplicates(): Escanea la tabla y elimina filas que tengan datos idénticos
df_limpio = df_limpio.drop_duplicates()

# .astype(str): Cambia el formato del dato (de número entero a cadena de texto)
df_limpio['ID_Cliente'] = df_limpio['ID_Cliente'].astype(str)

# Operación vectorizada: Multiplica toda la columna 'Monto' por 0.21 de un solo golpe
df_limpio['IVA'] = df_limpio['Monto'] * 0.21

# --- LECCIÓN 6: EXPORTACIÓN ---
# .to_csv(): Escribe el DataFrame en un archivo de texto plano. index=False evita guardar el número de fila
df_limpio.to_csv('resultado_final.csv', index=False)

# .to_excel(): Genera un archivo binario de Excel (.xlsx)
df_limpio.to_excel('resultado_final.xlsx', index=False)

# Mensaje de confirmación final
print("¡Proceso completado! Los archivos han sido generados correctamente.")