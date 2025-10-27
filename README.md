# Sistema de Gestión de Partidos de Fútbol

## Descripción

Sistema completo implementado en Python que permite gestionar información de partidos de fútbol mediante comandos y archivos de texto. El sistema incluye:

- **DSL Interno**: Patrón fluent interface para carga de equipos y jugadores
- **DSL Externo**: Parser con PLY para comandos de partidos desde archivos/consola
- **Sistema completo**: Menú interactivo, tablas de posiciones, goleadores y estadísticas

## Características Principales

### DSL Interno (Fluent Interface)
- Creación fluida de equipos y jugadores
- Validación automática de datos
- Control de números de camiseta únicos
- Sintaxis intuitiva y legible

### DSL Externo (PLY)
- Comandos específicos de fútbol
- Procesamiento desde archivos de texto
- Comandos interactivos por consola
- Validación de sintaxis y datos

### Funcionalidades del Sistema
- Carga de partidos (archivos y comandos)
- Tabla de posiciones por puntos
- Tabla de goleadores
- Listado de resultados de partidos
- Gestión completa de equipos

## Estructura del Proyecto

```
entregable 3/
├── main.py                 # Punto de entrada principal
├── models.py              # Modelos de datos (Equipo, Jugador, Partido, etc.)
├── requirements.txt       # Dependencias
├── README.md             # Documentación completa
├── src/
│   ├── menu.py          # Menú principal del sistema
│   ├── ui/
│   │   └── ui_renderer.py  # Renderizador de UI para terminal
│   ├── dsl_interno/
│   │   ├── __init__.py
│   │   └── dsl_interno.py  # DSL interno con fluent interface
│   └── dsl_externo/
│       ├── __init__.py
│       └── dsl_externo.py  # DSL externo con PLY
└── ejemplos/
    └── partidos_ejemplo.txt  # Archivo de ejemplo de partidos
```

## Instalación y Uso

### Requisitos
- Python 3.7+
- pip (gestor de paquetes de Python)

### Instalación
1. Clonar o descargar el repositorio
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Uso Básico

#### 1. Ejecutar el sistema
```bash
python main.py
```

#### 2. Crear equipos (obligatorio)
- Seleccionar opción 5: "Gestión de equipos"
- Crear al menos 2 equipos con códigos de 3 letras
- Agregar mínimo 11 jugadores por equipo

#### 3. Cargar partidos
- Seleccionar opción 1: "Carga de partidos"
- Elegir entre carga por comandos o archivo
- Seguir las instrucciones del sistema

#### 4. Ver estadísticas
- Opción 2: Tabla de posiciones
- Opción 3: Tabla de goleadores
- Opción 4: Resultados de partidos

## Uso del DSL Interno

### Crear Equipos
```python
from src.dsl_interno import nuevo_equipo

# Crear equipo usando fluent interface
barcelona = (nuevo_equipo()
            .con_nombre("Barcelona")
            .con_codigo("BAR")
            .agregar_jugador(1, "Ter Stegen")
            .agregar_jugador(2, "Sergi Roberto")
            .agregar_jugador(9, "Lewandowski"))
```

### Crear Jugadores
```python
from src.dsl_interno import nuevo_jugador

# Crear jugador usando fluent interface
jugador = (nuevo_jugador()
          .con_numero(10)
          .con_nombre("Messi"))
```

## Uso del DSL Externo

### Comandos Disponibles

#### Configuración del Partido
```
FECHA: DD/MM/YYYY
EQUIPO LOCAL: CODIGO
EQUIPO VISITANTE: CODIGO
FORMACION LOCAL: X-Y-Z
FORMACION VISITANTE: X-Y-Z
TITULARES LOCAL: 1,2,3,4,5,6,7,8,9,10,11
TITULARES VISITANTE: 1,2,3,4,5,6,7,8,9,10,11
BANCO LOCAL: 12,13,14,15,16,17
BANCO VISITANTE: 12,13,14,15,16,17
```

#### Eventos del Partido
```
GOL: EQUIPO, TIEMPO, AUTOR [, ASISTENTE]
TARJETA: EQUIPO, TIEMPO, JUGADOR, COLOR
CAMBIO: EQUIPO, TIEMPO, SALE, ENTRA
```

### Ejemplo de Archivo de Partidos
```
# Partido Barcelona vs Real Madrid
FECHA: 15/10/2023
EQUIPO LOCAL: BAR
EQUIPO VISITANTE: RMA
FORMACION LOCAL: 4-3-3
FORMACION VISITANTE: 4-4-2
TITULARES LOCAL: 1,2,3,4,5,6,7,8,9,10,11
TITULARES VISITANTE: 1,2,3,4,5,6,7,8,9,10,11
BANCO LOCAL: 12,13,14,15,16,17
BANCO VISITANTE: 12,13,14,15,16,17

GOL: BAR, 25, 9, 10
GOL: RMA, 45, 7
TARJETA: RMA, 30, 4, AMARILLA
CAMBIO: BAR, 70, 11, 12
```

## Características Técnicas

### Validaciones Implementadas
- Números de camiseta únicos por equipo
- Códigos de equipo de 3 letras
- Formaciones válidas
- 11 titulares por equipo
- Tiempos de eventos válidos
- Colores de tarjetas válidos

### Sistema de Puntos
- Ganador: 3 puntos
- Empate: 1 punto cada equipo
- Perdedor: 0 puntos

### Estadísticas Calculadas
- Partidos jugados
- Partidos ganados/empatados/perdidos
- Goles a favor/en contra
- Puntos totales
- Tabla de goleadores

## Menú del Sistema

1. **Carga de partidos**
   - a. Carga con comandos
   - b. Carga desde archivo

2. **Ver tabla de posiciones por puntos**

3. **Ver tabla de goleadores**

4. **Listar resultados de todos los partidos**

5. **Gestión de equipos**
   - a. Crear nuevo equipo
   - b. Mostrar todos los equipos
   - c. Mostrar jugadores de un equipo

## Ejemplos de Uso

### Crear un Equipo Completo
```python
from src.dsl_interno import SistemaFutbol

sistema = SistemaFutbol()

equipo = (sistema.crear_equipo()
          .con_nombre("Barcelona")
          .con_codigo("BAR")
          .agregar_jugador(1, "Ter Stegen")
          .agregar_jugador(9, "Lewandowski"))

sistema.registrar_equipo(equipo)
```

### Procesar Archivo de Partidos
```python
from src.dsl_externo import procesar_archivo_partidos

procesar_archivo_partidos("partidos.txt", sistema)
```

### Ver Estadísticas
```python
# Tabla de posiciones
tabla = sistema.obtener_tabla_posiciones()

# Tabla de goleadores
goleadores = sistema.obtener_tabla_goleadores()
```

## Archivos de Ejemplo

- `ejemplos/partidos_ejemplo.txt`: Archivo con partidos de ejemplo
- `demo.py`: Demostración completa del sistema con validaciones

## Tecnologías Utilizadas

- **Python 3.7+**: Lenguaje principal
- **PLY**: Parser para DSL externo
- **Dataclasses**: Modelos de datos
- **Type Hints**: Tipado estático
- **Fluent Interface**: Patrón de diseño para DSL interno


