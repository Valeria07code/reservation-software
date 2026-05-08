# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

## Descripción del proyecto

Este proyecto fue desarrollado en Python utilizando Programación Orientada a Objetos (POO). El sistema permite gestionar clientes, servicios y reservas para la empresa ficticia Software FJ, sin utilizar bases de datos.

La aplicación implementa principios fundamentales de POO como:

- Abstracción
- Herencia
- Polimorfismo
- Encapsulación
- Manejo avanzado de excepciones

Además, el sistema incorpora registro de eventos y errores mediante archivos de logs para garantizar estabilidad y trazabilidad durante la ejecución.

---

## Funcionalidades principales

El sistema permite:

- Registrar clientes válidos e inválidos
- Crear diferentes tipos de servicios
- Gestionar reservas
- Confirmar y cancelar reservas
- Procesar pagos y cálculos de costos
- Validar datos ingresados
- Manejar errores sin detener la aplicación
- Registrar eventos y excepciones en archivos de logs

---

## Tipos de servicios implementados

### ServicioSala
Permite gestionar reservas de salas por horas, incluyendo opciones adicionales como catering.

### AlquilerEquipo
Gestiona el alquiler de equipos tecnológicos por días completos.

### AsesoriaEspecializada
Permite registrar asesorías especializadas por sesiones.

---

## Estructura del proyecto

```text
Proyecto/
│
├── main.py
├── simulador.py
├── entidades.py
├── excepciones.py
├── servicios_especializados.py
├── logger_config.py
├── logs/
│   └── eventos.log
└── README.md
```

---

## Clases principales

### Cliente
Gestiona la información de los clientes con validaciones estrictas de:
- nombre
- correo electrónico
- teléfono

### Servicio
Clase abstracta base para los diferentes tipos de servicios.

### Reserva
Gestiona el proceso de confirmación, cancelación y procesamiento de reservas.

### Excepciones personalizadas
El sistema implementa:
- ValidacionClienteError
- ServicioNoDisponibleError
- ReservaError

---

## Manejo de excepciones

El proyecto utiliza:
- try / except
- try / except / else
- try / except / finally
- excepciones personalizadas
- encadenamiento de excepciones con raise from

Esto permite que el sistema continúe funcionando incluso cuando ocurren errores.

---

## Registro de logs

Todos los eventos importantes y errores del sistema se almacenan en:

```text
logs/eventos.log
```

Esto permite realizar trazabilidad completa del funcionamiento del programa.

---

## Tecnologías utilizadas

- Python 3
- Programación Orientada a Objetos
- GitHub
- Logging de Python

---

## Cómo ejecutar el proyecto

1. Descargar o clonar el repositorio
2. Abrir el proyecto en Visual Studio Code
3. Ejecutar el archivo:

```text
main.py
```

---

## Integrantes del grupo

- Jhon Freddy Ramirez
- Valeria Cardozo Salazar
- Daniela Sánchez Morales

---

## Conclusión

Este proyecto permitió aplicar conceptos de programación orientada a objetos y manejo avanzado de excepciones en Python, desarrollando una solución modular, estable y robusta para la gestión de clientes, servicios y reservas sin utilizar bases de datos.
