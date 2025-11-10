"""
Módulo: vista.main
Proporciona una interfaz por consola para probar el controlador.
"""

from controlador import operaciones


def mostrar_menu() -> None:
    while True:
        print("\n--- GESTOR DE LIBROS (ORM) ---")
        print("1. Agregar categoría")
        print("2. Listar categorías")
        print("3. Agregar libro")
        print("4. Listar libros")
        print("5. Buscar por categoría")
        print("6. Actualizar precio por título")
        print("7. Eliminar por título")
        print("8. Salir")

        op = input("Seleccione una opción: ").strip()

        if op == "1":
            nombre = input("Nombre de la categoría: ").strip()
            if operaciones.crear_categoria(nombre):
                print("Categoría creada.")
            else:
                print("Error al crear categoría. ¿Ya existe?")

        elif op == "2":
            categorias = operaciones.listar_categorias()
            if categorias:
                for c in categorias:
                    print(c)
            else:
                print("No hay categorías.")

        elif op == "3":
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            try:
                precio = float(input("Precio: ").strip())
            except ValueError:
                print("El precio debe ser un número.")
                continue
            cat_nombre = input("Nombre de la categoría existente: ").strip()
            categorias = operaciones.listar_categorias()
            cat_obj = next((x for x in categorias if x.nombre == cat_nombre), None)
            if not cat_obj:
                print("Categoría no encontrada. Crea la categoría primero.")
                continue
            ok = operaciones.agregar_libro(titulo, autor, precio, cat_obj.id)
            print("Libro agregado." if ok else "Error al agregar libro.")

        elif op == "4":
            libros = operaciones.listar_libros()
            if libros:
                for l in libros:
                    print(l)
            else:
                print("No hay libros.")

        elif op == "5":
            cat = input("Nombre de la categoría: ").strip()
            resultados = operaciones.buscar_por_categoria(cat)
            if resultados:
                for l in resultados:
                    print(l)
            else:
                print("No se encontraron libros para esa categoría.")

        elif op == "6":
            titulo = input("Título a actualizar: ").strip()
            try:
                nuevo_precio = float(input("Nuevo precio: ").strip())
            except ValueError:
                print("El nuevo precio debe ser numérico.")
                continue
            actualizado = operaciones.actualizar_precio(titulo, nuevo_precio)
            print("Actualizado." if actualizado else "No se encontró el título.")

        elif op == "7":
            titulo = input("Título a eliminar: ").strip()
            n = operaciones.eliminar_por_titulo(titulo)
            print(f"Registros eliminados: {n}")

        elif op == "8":
            print("Saliendo.")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    mostrar_menu()
