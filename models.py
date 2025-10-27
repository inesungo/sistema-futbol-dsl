from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class Jugador:
    """Representa un jugador de fútbol"""
    numero: int
    nombre: str
    
    def __str__(self):
        return f"{self.numero}. {self.nombre}"


@dataclass
class Equipo:
    """Representa un equipo de fútbol"""
    nombre: str
    codigo: str
    jugadores: List[Jugador] = field(default_factory=list)
    
    def agregar_jugador(self, numero: int, nombre: str) -> 'Equipo':
        """Agrega un jugador al equipo verificando que no se repita el número"""
        if any(jugador.numero == numero for jugador in self.jugadores):
            raise ValueError(f"El número {numero} ya está ocupado en el equipo {self.nombre}")
        
        self.jugadores.append(Jugador(numero, nombre))
        return self
    
    def obtener_jugador(self, numero: int) -> Optional[Jugador]:
        """Obtiene un jugador por su número de camiseta"""
        for jugador in self.jugadores:
            if jugador.numero == numero:
                return jugador
        return None
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


@dataclass
class Evento:
    """Representa un evento en un partido (gol, tarjeta, cambio)"""
    tiempo: int
    equipo: str  # código del equipo
    
    def __str__(self):
        return f"Minuto {self.tiempo}"


@dataclass
class Gol(Evento):
    """Representa un gol en el partido"""
    autor: int  # número del jugador
    asistente: Optional[int] = None  # número del jugador asistente
    
    def __str__(self):
        asistente_str = f" (Asistencia: {self.asistente})" if self.asistente else ""
        return f"Gol de {self.autor} para {self.equipo} al minuto {self.tiempo}{asistente_str}"


@dataclass
class Tarjeta(Evento):
    """Representa una tarjeta en el partido"""
    jugador: int  # número del jugador
    color: str  # "Amarilla" o "Roja"
    
    def __str__(self):
        return f"Tarjeta {self.color} para {self.jugador} ({self.equipo}) al minuto {self.tiempo}"


@dataclass
class Cambio(Evento):
    """Representa un cambio de jugador en el partido"""
    jugador_sale: int  # número del jugador que sale
    jugador_entra: int  # número del jugador que entra
    
    def __str__(self):
        return f"Cambio: {self.jugador_sale} sale, {self.jugador_entra} entra ({self.equipo}) al minuto {self.tiempo}"


@dataclass
class Partido:
    """Representa un partido de fútbol completo"""
    fecha: datetime
    equipo_local: str  # código del equipo
    equipo_visitante: str  # código del equipo
    formacion_local: str  # ej: "4-3-3"
    formacion_visitante: str  # ej: "4-4-2"
    titulares_local: List[int]  # números de camiseta
    titulares_visitante: List[int]  # números de camiseta
    banco_local: List[int]  # números de camiseta
    banco_visitante: List[int]  # números de camiseta
    eventos: List[Evento] = field(default_factory=list)
    
    def agregar_gol(self, equipo: str, tiempo: int, autor: int, asistente: Optional[int] = None):
        """Agrega un gol al partido"""
        self.eventos.append(Gol(tiempo, equipo, autor, asistente))
    
    def agregar_tarjeta(self, equipo: str, tiempo: int, jugador: int, color: str):
        """Agrega una tarjeta al partido"""
        self.eventos.append(Tarjeta(tiempo, equipo, jugador, color))
    
    def agregar_cambio(self, equipo: str, tiempo: int, jugador_sale: int, jugador_entra: int):
        """Agrega un cambio al partido"""
        self.eventos.append(Cambio(tiempo, equipo, jugador_sale, jugador_entra))
    
    def obtener_goles_equipo(self, equipo: str) -> int:
        """Obtiene la cantidad de goles de un equipo"""
        return len([evento for evento in self.eventos if isinstance(evento, Gol) and evento.equipo == equipo])
    
    def obtener_resultado(self) -> Dict[str, int]:
        """Obtiene el resultado del partido"""
        goles_local = self.obtener_goles_equipo(self.equipo_local)
        goles_visitante = self.obtener_goles_equipo(self.equipo_visitante)
        
        return {
            'local': goles_local,
            'visitante': goles_visitante,
            'ganador': self.equipo_local if goles_local > goles_visitante else 
                      self.equipo_visitante if goles_visitante > goles_local else None
        }
    
    def obtener_puntos_equipo(self, equipo: str) -> int:
        """Obtiene los puntos que suma un equipo en este partido"""
        resultado = self.obtener_resultado()
        if resultado['ganador'] == equipo:
            return 3
        elif resultado['ganador'] is None:
            return 1
        else:
            return 0
    
    def __str__(self):
        resultado = self.obtener_resultado()
        return f"{self.fecha.strftime('%d/%m/%Y')} - {self.equipo_local} {resultado['local']}-{resultado['visitante']} {self.equipo_visitante}"


class SistemaFutbol:
    """Sistema principal para gestionar equipos y partidos"""
    
    def __init__(self):
        self.equipos: Dict[str, Equipo] = {}
        self.partidos: List[Partido] = []
    
    def agregar_equipo(self, equipo: Equipo):
        """Agrega un equipo al sistema"""
        self.equipos[equipo.codigo] = equipo
    
    def obtener_equipo(self, codigo: str) -> Optional[Equipo]:
        """Obtiene un equipo por su código"""
        return self.equipos.get(codigo)
    
    def agregar_partido(self, partido: Partido):
        """Agrega un partido al sistema"""
        self.partidos.append(partido)
    
    def obtener_tabla_posiciones(self) -> List[Dict]:
        """Obtiene la tabla de posiciones ordenada por puntos"""
        estadisticas = {}
        
        # Inicializar estadísticas de todos los equipos
        for codigo in self.equipos.keys():
            estadisticas[codigo] = {
                'equipo': codigo,
                'partidos_jugados': 0,
                'ganados': 0,
                'empatados': 0,
                'perdidos': 0,
                'goles_a_favor': 0,
                'goles_en_contra': 0,
                'puntos': 0
            }
        
        # Procesar todos los partidos
        for partido in self.partidos:
            resultado = partido.obtener_resultado()
            goles_local = resultado['local']
            goles_visitante = resultado['visitante']
            
            # Estadísticas del equipo local
            estadisticas[partido.equipo_local]['partidos_jugados'] += 1
            estadisticas[partido.equipo_local]['goles_a_favor'] += goles_local
            estadisticas[partido.equipo_local]['goles_en_contra'] += goles_visitante
            
            # Estadísticas del equipo visitante
            estadisticas[partido.equipo_visitante]['partidos_jugados'] += 1
            estadisticas[partido.equipo_visitante]['goles_a_favor'] += goles_visitante
            estadisticas[partido.equipo_visitante]['goles_en_contra'] += goles_local
            
            # Puntos y resultados
            if resultado['ganador'] == partido.equipo_local:
                estadisticas[partido.equipo_local]['ganados'] += 1
                estadisticas[partido.equipo_local]['puntos'] += 3
                estadisticas[partido.equipo_visitante]['perdidos'] += 1
            elif resultado['ganador'] == partido.equipo_visitante:
                estadisticas[partido.equipo_visitante]['ganados'] += 1
                estadisticas[partido.equipo_visitante]['puntos'] += 3
                estadisticas[partido.equipo_local]['perdidos'] += 1
            else:  # empate
                estadisticas[partido.equipo_local]['empatados'] += 1
                estadisticas[partido.equipo_local]['puntos'] += 1
                estadisticas[partido.equipo_visitante]['empatados'] += 1
                estadisticas[partido.equipo_visitante]['puntos'] += 1
        
        # Ordenar por puntos (descendente)
        tabla = list(estadisticas.values())
        tabla.sort(key=lambda x: x['puntos'], reverse=True)
        
        return tabla
    
    def obtener_tabla_goleadores(self) -> List[Dict]:
        """Obtiene la tabla de goleadores"""
        goleadores = {}
        
        for partido in self.partidos:
            for evento in partido.eventos:
                if isinstance(evento, Gol):
                    jugador_num = evento.autor
                    equipo_codigo = evento.equipo
                    
                    # Buscar el jugador en los equipos
                    equipo = self.obtener_equipo(equipo_codigo)
                    if equipo:
                        jugador = equipo.obtener_jugador(jugador_num)
                        if jugador:
                            clave = f"{jugador.nombre} ({equipo_codigo})"
                            if clave not in goleadores:
                                goleadores[clave] = {
                                    'jugador': jugador.nombre,
                                    'equipo': equipo_codigo,
                                    'goles': 0
                                }
                            goleadores[clave]['goles'] += 1
        
        # Ordenar por cantidad de goles (descendente)
        tabla = list(goleadores.values())
        tabla.sort(key=lambda x: x['goles'], reverse=True)
        
        return tabla
