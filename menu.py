from simulador import ejecutar_simulaciones


def mostrar_menu():
    while True:
        print("\n===================================")
        print(" SOFTWARE FJ - MENU PRINCIPAL ")
        print("===================================")
        print("1. Ejecutar simulaciones")
        print("2. Información del sistema")
        print("3. Tipos de servicios")
        print("4. Salir")
        print("===================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\nEjecutando simulaciones del sistema...\n")
            ejecutar_simulaciones()

        elif opcion == "2":
            print("\nInformación del sistema")
            print("-----------------------------------")
            print("Sistema integral de gestión de clientes,")
            print("servicios y reservas para Software FJ.")
            print("Desarrollado con Programación Orientada a Objetos.")
            print("Incluye manejo avanzado de excepciones y logs.")

        elif opcion == "3":
            print("\nTipos de servicios disponibles")
            print("-----------------------------------")
            print("1. Reserva de salas")
            print("2. Alquiler de equipos")
            print("3. Asesorías especializadas")

        elif opcion == "4":
            print("\nSaliendo del sistema...")
            break

        else:
            print("\nError: opción inválida. Intente nuevamente.")
