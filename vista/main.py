"""
Módulo: vista.main
Proporciona una interfaz por consola para probar el controlador.
"""
from controlador import operaciones


def mostrar_menu() -> None:
    while True:
        print("\n--- GESTOR DE LIBROS (ORM) ---")
        print("1. Agregar libro")
        print("2. Listar todos")
        print("3. Buscar por autor")
        print("4. Actualizar precio por título")
        print("5. Eliminar por título")
        print("6. Salir")

        op = input("Seleccione una opción: ")

        if op == "1":
            t = input("Título: ")
            a = input("Autor: ")
            try:
                p = float(input("Precio: "))
                operaciones.agregar(t, a, p)
            except ValueError:
                print("Error: el precio debe ser un número. No se agregó el libro.")

        elif op == "2":
            libros = operaciones.listar()
            if libros:
                print("\nID | Título | Autor | Precio")
                print("-------------------------------")
                for x in libros:
                    print(f"{x.id:<2} {x.titulo:<15} {x.autor:<12} {x.precio:>6.2f}")
            else:
                print("No hay registros.")

        elif op == "3":
            a = input("Autor: ")
            libros = operaciones.buscar_por_autor(a)
            for x in libros:
                print(x)

        elif op == "4":
            t = input("Título: ")
            try:
                np = float(input("Nuevo precio: "))
                actualizado = operaciones.actualizar_precio(t, np)
                print("Actualizado." if actualizado else "No se encontró el título.")
            except ValueError:
                print("Error: el precio debe ser un número. No se actualizó.")

        elif op == "5":
            t = input("Título a eliminar: ")
            n = operaciones.eliminar_por_titulo(t)
            print(f"Registros eliminados: {n}")

        elif op == "6":
            print("Fin de la sesión.")
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    mostrar_menu()