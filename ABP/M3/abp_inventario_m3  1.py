# =================================================================
# PROYECTO: SISTEMA DE CATÁLOGO DE PRODUCTOS
# =================================================================

# Línea: Define el inicio de la clase 'Producto'. Es el molde general.
class Producto:
    # Línea: Define el constructor. Se ejecuta al crear cada producto.
    # Recibe 'self' (el objeto mismo) y 4 parámetros con los datos del producto.
    def __init__(self, nombre, precio, stock, categoria):
        # Línea: Toma el parámetro 'nombre' y lo guarda en el atributo 'self.nombre'.
        # Esto hace que el dato sea permanente dentro del objeto.
        self.nombre = nombre
        # Línea: Guarda el precio recibido en la propiedad del objeto.
        self.precio = precio
        # Línea: Guarda la cantidad disponible en la propiedad del objeto.
        self.stock = stock
        # Línea: Guarda la categoría (ej: "Lácteos") en la propiedad del objeto.
        self.categoria = categoria

    # Línea: Método para convertir el objeto en una cadena de texto (String).
    # Recibe 'self' para poder leer los datos que guardamos en el __init__.
    def __str__(self):
        # Línea: Retorna un texto formateado. 'upper()' pone la categoría en mayúsculas.
        return f"📦 [{self.categoria.upper()}] {self.nombre} | Precio: ${self.precio} | Stock: {self.stock}"


# Línea: Define la clase 'Inventario' que controlará la lista de productos.
class Inventario:
    # Línea: Constructor de la clase gestora. No recibe parámetros externos.
    def __init__(self):
        # Línea: Crea una lista vacía llamada 'productos'.
        # Al usar 'self.', la lista pertenece a toda la clase y no se borra.
        self.productos = []

    # Línea: Define la función para agregar. Recibe los datos para el nuevo producto.
    def agregar_producto(self, nombre, precio, stock, categoria):
        # Línea: Crea una instancia real llamada 'nuevo' usando el molde 'Producto'.
        # Aquí pasamos los parámetros que recibió esta función hacia el constructor de Producto.
        nuevo = Producto(nombre, precio, stock, categoria)
        # Línea: Usa el método '.append()' para meter el objeto 'nuevo' en la lista.
        self.productos.append(nuevo)
        # Línea: Muestra un mensaje confirmando que se usó el nombre del producto.
        print(f"✅ Producto '{nombre}' añadido.")

    # Línea: Define la función de búsqueda. Recibe el parámetro 'termino'.
    def buscar_producto(self, termino):
        # Línea: Variable 'booleana' para rastrear si encontramos algo (empieza en Falso).
        encontrado = False
        # Línea: Inicia un bucle 'for' que revisa cada producto 'p' dentro de la lista.
        for p in self.productos:
            # Línea: Condicional que compara el término buscado con el nombre o categoría.
            # '.lower()' iguala todo a minúsculas para que la búsqueda sea exacta.
            if termino.lower() in p.nombre.lower() or termino.lower() in p.categoria.lower():
                # Línea: Si hay coincidencia, imprime el producto 'p'.
                print(p)
                # Línea: Cambia la variable a True porque ya encontramos al menos uno.
                encontrado = True
        
        # Línea: Si al terminar el bucle 'encontrado' sigue en False, ejecuta esto:
        if not encontrado:
            # Línea: Informa que no hubo resultados para ese parámetro.
            print(f"❌ No hay resultados para: {termino}")

    # Línea: Función para borrar. Recibe el parámetro 'nombre_prod'.
    def eliminar_producto(self, nombre_prod):
        # Línea: Bucle para recorrer la lista y buscar el nombre.
        for p in self.productos:
            # Línea: Compara el nombre del producto actual con el parámetro recibido.
            if p.nombre.lower() == nombre_prod.lower():
                # Línea: Si coincide, usa '.remove()' para borrar el objeto 'p' de la lista.
                self.productos.remove(p)
                # Línea: Avisa que el borrado fue exitoso.
                print(f"🗑️ '{nombre_prod}' eliminado.")
                # Línea: 'return' finaliza la función inmediatamente (ya no hace falta seguir buscando).
                return 
        # Línea: Esta línea solo se ejecuta si el 'return' de arriba nunca se activó.
        print("❌ El producto no existe.")


# Línea: Define la función que maneja el menú visual.
def ejecutar_catalogo():
    # Línea: Crea el objeto 'mi_inventario' que tiene la lista y las funciones.
    mi_inventario = Inventario()
    
    # Línea: Bucle 'while' que será verdadero siempre. Mantiene el programa abierto.
    while True:
        # Líneas: Imprimen el menú de opciones en la consola.
        print("\n--- SISTEMA DE CATÁLOGO ---")
        print("1. Agregar | 2. Ver | 3. Buscar | 4. Eliminar | 5. Salir")

        # Línea: Captura la opción del usuario como texto.
        opcion = input("Opción: ")

        # Línea: Si la opción es "1", entra a registrar.
        if opcion == "1":
            # Líneas: 'input' pide datos y los guarda en variables locales temporales.
            nom = input("Nombre: ")
            pre = input("Precio: ")
            sto = input("Stock: ")
            cat = input("Categoría: ")
            # Línea: Llama a la función 'agregar_producto' y le pasa las variables como parámetros.
            mi_inventario.agregar_producto(nom, pre, sto, cat)

        # Línea: Si la opción es "2", entra a mostrar todo.
        elif opcion == "2":
            # Línea: Verifica si la lista está vacía usando 'if not'.
            if not mi_inventario.productos:
                # Línea: Si está vacía, avisa al usuario.
                print("Catálogo vacío.")
            # Línea: Si tiene contenido (else)...
            else:
                # Línea: Recorre la lista 'productos' y muestra cada uno.
                for prod in mi_inventario.productos:
                    print(prod)

        # Línea: Si la opción es "3", entra a buscar.
        elif opcion == "3":
            # Línea: Pide el dato que servirá como parámetro de búsqueda.
            bus = input("Buscar nombre o categoría: ")
            # Línea: Llama a la función enviando 'bus' como argumento.
            mi_inventario.buscar_producto(bus)

        # Línea: Si la opción es "4", entra a eliminar.
        elif opcion == "4":
            # Línea: Pide el nombre para el parámetro de eliminación.
            eli = input("Nombre a eliminar: ")
            # Línea: Ejecuta la función de borrado.
            mi_inventario.eliminar_producto(eli)

        # Línea: Si la opción es "5", termina el programa.
        elif opcion == "5":
            # Línea: Despedida.
            print("Saliendo...")
            # Línea: 'break' detiene el bucle 'while True' de forma definitiva.
            break 

        # Línea: Si el usuario escribe cualquier otra cosa que no sea 1-5.
        else:
            # Línea: Avisa del error de entrada.
            print("⚠️ Opción no válida.")

# Línea: Verifica si este script se está ejecutando directamente en la computadora.
if __name__ == "__main__":
    # Línea: Llama a la función del menú para que todo comience.
    ejecutar_catalogo()