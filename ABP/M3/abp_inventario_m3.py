class Producto:
    def __init__(self, nombre, precio, stock, categoria):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria

    def __str__(self):
        return f"[{self.categoria.upper()}] {self.nombre} -- Precio: ${self.precio} -- Stock: {self.stock} Unidades"

class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, nombre, precio, stock, categoria):
        nuevo = Producto(nombre, precio, stock, categoria)
        self.productos.append(nuevo)
        print(f" Producto: '{nombre}' registrado  ")    

    def buscar_producto(self, termino):
        encontrado = False
        for p in self.productos:
            if termino.lower() in p.nombre.lower() or termino.lower() in p.categoria.lower():
                print(p)
            encontrado = True
        if not encontrado:
            print(f"no hay resultados para {termino}")

    def eliminar_producto(self, nombre_prod):
        for p in self.productos:
            if p.nombre.lower() == nombre_prod.lower():
                self.productos.remove(p)
            print(f" '{nombre_prod}' eliminado   ")
            return
        print(" El producto no existe")

def ejecutar_catalogo():
    mi_inventario = Inventario()

    while True:
        print("-- Inventario --")
        print("1. Agregar  -- 2. Listar  -- 3. Buscar  -- 4. Eliminar  -- 5. Salir")
        opcion = input("Opcion: ")

        if opcion == "1":
            nom = input("Nombre:  ")
            pre = input("Precio: ")
            sto = input("Stock: ")
            cat = input("Categoria: ")
            mi_inventario.agregar_producto(nom, pre, sto, cat)

        elif opcion == "2":
            if not mi_inventario.productos:
                print("Inventario vacio")
            else:
                for prod in mi_inventario.productos:
                    print(prod)
        
        elif opcion == "3":
            bus = input("Buscar nombre o categoria: ")
            mi_inventario.buscar_producto(bus)

        elif opcion =="4":
            eli = input("Nombre a eliminar: ")
            mi_inventario.eliminar_producto(eli)

        elif opcion == "5":
            print("Saliendo....")
            break

        else:
            print("Opcion no valida")


# Línea: Verifica si este script se está ejecutando directamente en la computadora.
if __name__ == "__main__":
    # Línea: Llama a la función del menú para que todo comience.
    ejecutar_catalogo()
