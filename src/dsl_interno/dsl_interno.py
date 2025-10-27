"""
DSL Interno con Patrón Fluent Interface
Para la carga de equipos y jugadores de fútbol
"""

from typing import List, Optional
import sys
import os
# Agregar el directorio raíz al path para importar models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from models import Equipo, Jugador, SistemaFutbol as SistemaBase


class JugadorBuilder:
    """Builder para crear jugadores usando fluent interface"""
    
    def __init__(self):
        self.numero: Optional[int] = None
        self.nombre: Optional[str] = None
    
    def con_numero(self, numero: int) -> 'JugadorBuilder':
        """Establece el número de camiseta del jugador"""
        if not isinstance(numero, int) or numero < 1 or numero > 99:
            raise ValueError("El número de camiseta debe ser un entero entre 1 y 99")
        self.numero = numero
        return self
    
    def con_nombre(self, nombre: str) -> 'JugadorBuilder':
        """Establece el nombre del jugador"""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del jugador no puede estar vacío")
        self.nombre = nombre.strip()
        return self
    
    def construir(self) -> Jugador:
        """Construye el jugador con los datos proporcionados"""
        if self.numero is None:
            raise ValueError("Debe especificar el número de camiseta")
        if self.nombre is None:
            raise ValueError("Debe especificar el nombre del jugador")
        
        return Jugador(self.numero, self.nombre)


class EquipoBuilder:
    """Builder para crear equipos usando fluent interface"""
    
    def __init__(self):
        self.nombre: Optional[str] = None
        self.codigo: Optional[str] = None
        self.jugadores: List[Jugador] = []
    
    def con_nombre(self, nombre: str) -> 'EquipoBuilder':
        """Establece el nombre del equipo"""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del equipo no puede estar vacío")
        self.nombre = nombre.strip()
        return self
    
    def con_codigo(self, codigo: str) -> 'EquipoBuilder':
        """Establece el código de 3 letras del equipo"""
        if not codigo or len(codigo.strip()) != 3:
            raise ValueError("El código del equipo debe tener exactamente 3 letras")
        self.codigo = codigo.strip().upper()
        return self
    
    def agregar_jugador(self, numero: int, nombre: str) -> 'EquipoBuilder':
        """Agrega un jugador al equipo"""
        # Verificar que no se repita el número
        if any(jugador.numero == numero for jugador in self.jugadores):
            raise ValueError(f"El número {numero} ya está ocupado en este equipo")
        
        jugador = Jugador(numero, nombre)
        self.jugadores.append(jugador)
        return self
    
    def agregar_jugador_builder(self, jugador_builder: JugadorBuilder) -> 'EquipoBuilder':
        """Agrega un jugador usando un JugadorBuilder"""
        jugador = jugador_builder.construir()
        
        # Verificar que no se repita el número
        if any(j.numero == jugador.numero for j in self.jugadores):
            raise ValueError(f"El número {jugador.numero} ya está ocupado en este equipo")
        
        self.jugadores.append(jugador)
        return self
    
    def construir(self) -> Equipo:
        """Construye el equipo con los datos proporcionados"""
        if self.nombre is None:
            raise ValueError("Debe especificar el nombre del equipo")
        if self.codigo is None:
            raise ValueError("Debe especificar el código del equipo")
        
        equipo = Equipo(self.nombre, self.codigo)
        equipo.jugadores = self.jugadores.copy()
        return equipo


class SistemaFutbol(SistemaBase):
    """Sistema de fútbol con DSL interno para carga de datos"""
    
    def __init__(self):
        super().__init__()
    
    def crear_equipo(self) -> EquipoBuilder:
        """Inicia la creación de un nuevo equipo"""
        return EquipoBuilder()
    
    def crear_jugador(self) -> JugadorBuilder:
        """Inicia la creación de un nuevo jugador"""
        return JugadorBuilder()
    
    def registrar_equipo(self, equipo_builder: EquipoBuilder) -> 'SistemaFutbol':
        """Registra un equipo construido con el builder"""
        equipo = equipo_builder.construir()
        self.agregar_equipo(equipo)
        return self
    
    def mostrar_equipos(self) -> 'SistemaFutbol':
        """Muestra todos los equipos registrados"""
        print("\n" + "="*50)
        print("EQUIPOS REGISTRADOS")
        print("="*50)
        
        if not self.equipos:
            print("No hay equipos registrados.")
        else:
            for codigo, equipo in self.equipos.items():
                print(f"\n{equipo}")
                print(f"Jugadores ({len(equipo.jugadores)}):")
                for jugador in sorted(equipo.jugadores, key=lambda j: j.numero):
                    print(f"  {jugador}")
        
        return self
    
    def mostrar_jugadores_equipo(self, codigo: str) -> 'SistemaFutbol':
        """Muestra los jugadores de un equipo específico"""
        equipo = self.obtener_equipo(codigo)
        if not equipo:
            print(f"No se encontró el equipo con código {codigo}")
            return self
        
        print(f"\nJugadores de {equipo}:")
        for jugador in sorted(equipo.jugadores, key=lambda j: j.numero):
            print(f"  {jugador}")
        
        return self


# Funciones de conveniencia para uso más fluido
def nuevo_equipo() -> EquipoBuilder:
    """Función de conveniencia para crear un nuevo equipo"""
    return EquipoBuilder()


def nuevo_jugador() -> JugadorBuilder:
    """Función de conveniencia para crear un nuevo jugador"""
    return JugadorBuilder()


def sistema_futbol() -> SistemaFutbol:
    """Función de conveniencia para crear un nuevo sistema"""
    return SistemaFutbol()
