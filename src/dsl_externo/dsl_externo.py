"""
DSL Externo con PLY para gestión de partidos de fútbol
Permite procesar comandos desde archivos de texto o consola
"""

import ply.lex as lex
import ply.yacc as yacc
from datetime import datetime
from typing import List, Dict, Optional, Any
import sys
import os
# Agregar el directorio raíz al path para importar models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from models import Partido, SistemaFutbol


# Tokens del lexer
tokens = (
    'FECHA',
    'EQUIPO_LOCAL',
    'EQUIPO_VISITANTE', 
    'FORMACION_LOCAL',
    'FORMACION_VISITANTE',
    'TITULARES_LOCAL',
    'TITULARES_VISITANTE',
    'BANCO_LOCAL',
    'BANCO_VISITANTE',
    'GOL',
    'TARJETA',
    'CAMBIO',
    'NUMERO',
    'CODIGO_EQUIPO',
    'COLOR',
    'TIEMPO',
    'COMA',
    'GUION',
    'DOS_PUNTOS',
    'PUNTO_COMA',
    'PARENTESIS_ABRE',
    'PARENTESIS_CIERRA',
    'CADENA',
    'NUEVA_LINEA'
)

# Reglas de tokens simples
t_COMA = r','
t_GUION = r'-'
t_DOS_PUNTOS = r':'
t_PUNTO_COMA = r';'
t_PARENTESIS_ABRE = r'\('
t_PARENTESIS_CIERRA = r'\)'
t_NUEVA_LINEA = r'\n'

# Reglas de tokens complejos
def t_FECHA(t):
    r'FECHA\s*:'
    return t

def t_EQUIPO_LOCAL(t):
    r'EQUIPO\s+LOCAL\s*:'
    return t

def t_EQUIPO_VISITANTE(t):
    r'EQUIPO\s+VISITANTE\s*:'
    return t

def t_FORMACION_LOCAL(t):
    r'FORMACION\s+LOCAL\s*:'
    return t

def t_FORMACION_VISITANTE(t):
    r'FORMACION\s+VISITANTE\s*:'
    return t

def t_TITULARES_LOCAL(t):
    r'TITULARES\s+LOCAL\s*:'
    return t

def t_TITULARES_VISITANTE(t):
    r'TITULARES\s+VISITANTE\s*:'
    return t

def t_BANCO_LOCAL(t):
    r'BANCO\s+LOCAL\s*:'
    return t

def t_BANCO_VISITANTE(t):
    r'BANCO\s+VISITANTE\s*:'
    return t

def t_GOL(t):
    r'GOL\s*:'
    return t

def t_TARJETA(t):
    r'TARJETA\s*:'
    return t

def t_CAMBIO(t):
    r'CAMBIO\s*:'
    return t

def t_CODIGO_EQUIPO(t):
    r'[A-Z]{3}'
    return t

def t_COLOR(t):
    r'(AMARILLA|ROJA)'
    return t

def t_TIEMPO(t):
    r'\d{1,3}'
    t.value = int(t.value)
    return t

def t_NUMERO(t):
    r'\d{1,2}'
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Remover comillas
    return t

def t_COMMENT(t):
    r'\#.*'
    pass  # Ignorar comentarios

def t_WHITESPACE(t):
    r'[ \t]+'
    pass  # Ignorar espacios y tabs

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
    t.lexer.skip(1)


# Reglas de gramática
def p_partido(p):
    '''partido : FECHA fecha
               | EQUIPO_LOCAL CODIGO_EQUIPO
               | EQUIPO_VISITANTE CODIGO_EQUIPO
               | FORMACION_LOCAL formacion
               | FORMACION_VISITANTE formacion
               | TITULARES_LOCAL lista_numeros
               | TITULARES_VISITANTE lista_numeros
               | BANCO_LOCAL lista_numeros
               | BANCO_VISITANTE lista_numeros
               | evento'''
    pass

def p_fecha(p):
    '''fecha : CADENA'''
    p[0] = p[1]

def p_formacion(p):
    '''formacion : NUMERO GUION NUMERO GUION NUMERO'''
    p[0] = f"{p[1]}-{p[3]}-{p[5]}"

def p_lista_numeros(p):
    '''lista_numeros : NUMERO
                     | NUMERO COMA lista_numeros'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_evento(p):
    '''evento : gol
              | tarjeta
              | cambio'''
    p[0] = p[1]

def p_gol(p):
    '''gol : GOL CODIGO_EQUIPO COMA TIEMPO COMA NUMERO COMA NUMERO
           | GOL CODIGO_EQUIPO COMA TIEMPO COMA NUMERO'''
    if len(p) == 8:
        p[0] = {
            'tipo': 'gol',
            'equipo': p[2],
            'tiempo': p[4],
            'autor': p[6],
            'asistente': p[8]
        }
    else:
        p[0] = {
            'tipo': 'gol',
            'equipo': p[2],
            'tiempo': p[4],
            'autor': p[6],
            'asistente': None
        }

def p_tarjeta(p):
    '''tarjeta : TARJETA CODIGO_EQUIPO COMA TIEMPO COMA NUMERO COMA COLOR'''
    p[0] = {
        'tipo': 'tarjeta',
        'equipo': p[2],
        'tiempo': p[4],
        'jugador': p[6],
        'color': p[8]
    }

def p_cambio(p):
    '''cambio : CAMBIO CODIGO_EQUIPO COMA TIEMPO COMA NUMERO COMA NUMERO'''
    p[0] = {
        'tipo': 'cambio',
        'equipo': p[2],
        'tiempo': p[4],
        'jugador_sale': p[6],
        'jugador_entra': p[8]
    }

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' en línea {p.lineno}")
    else:
        print("Error de sintaxis al final del archivo")


class ParserFutbol:
    """Parser para comandos de partidos de fútbol"""
    
    def __init__(self, sistema: SistemaFutbol):
        self.sistema = sistema
        self.lexer = lex.lex()
        self.parser = yacc.yacc()
        self.partido_actual: Optional[Dict[str, Any]] = None
    
    def procesar_linea(self, linea: str) -> Optional[Dict[str, Any]]:
        """Procesa una línea de comando"""
        try:
            resultado = self.parser.parse(linea.strip(), lexer=self.lexer)
            return resultado
        except Exception as e:
            print(f"Error procesando línea: {linea}")
            print(f"Error: {e}")
            return None
    
    def procesar_comando(self, comando: str) -> bool:
        """Procesa un comando completo"""
        partes = comando.split(':', 1)
        if len(partes) != 2:
            print(f"Formato de comando inválido: {comando}")
            return False
        
        tipo_comando = partes[0].strip().upper()
        datos = partes[1].strip()
        
        try:
            if tipo_comando == 'FECHA':
                self._procesar_fecha(datos)
            elif tipo_comando == 'EQUIPO LOCAL':
                self._procesar_equipo_local(datos)
            elif tipo_comando == 'EQUIPO VISITANTE':
                self._procesar_equipo_visitante(datos)
            elif tipo_comando == 'FORMACION LOCAL':
                self._procesar_formacion_local(datos)
            elif tipo_comando == 'FORMACION VISITANTE':
                self._procesar_formacion_visitante(datos)
            elif tipo_comando == 'TITULARES LOCAL':
                self._procesar_titulares_local(datos)
            elif tipo_comando == 'TITULARES VISITANTE':
                self._procesar_titulares_visitante(datos)
            elif tipo_comando == 'BANCO LOCAL':
                self._procesar_banco_local(datos)
            elif tipo_comando == 'BANCO VISITANTE':
                self._procesar_banco_visitante(datos)
            elif tipo_comando == 'GOL':
                self._procesar_gol(datos)
            elif tipo_comando == 'TARJETA':
                self._procesar_tarjeta(datos)
            elif tipo_comando == 'CAMBIO':
                self._procesar_cambio(datos)
            else:
                print(f"Comando desconocido: {tipo_comando}")
                return False
            
            return True
        except Exception as e:
            print(f"Error procesando comando '{comando}': {e}")
            return False
    
    def _procesar_fecha(self, datos: str):
        """Procesa la fecha del partido"""
        try:
            fecha = datetime.strptime(datos.strip(), '%d/%m/%Y')
            if self.partido_actual is None:
                self.partido_actual = {}
            self.partido_actual['fecha'] = fecha
        except ValueError:
            raise ValueError(f"Formato de fecha inválido: {datos}. Use DD/MM/YYYY")
    
    def _procesar_equipo_local(self, datos: str):
        """Procesa el equipo local"""
        codigo = datos.strip().upper()
        if len(codigo) != 3:
            raise ValueError("El código del equipo debe tener 3 letras")
        
        if self.sistema.obtener_equipo(codigo) is None:
            raise ValueError(f"El equipo {codigo} no está registrado")
        
        if self.partido_actual is None:
            self.partido_actual = {}
        self.partido_actual['equipo_local'] = codigo
    
    def _procesar_equipo_visitante(self, datos: str):
        """Procesa el equipo visitante"""
        codigo = datos.strip().upper()
        if len(codigo) != 3:
            raise ValueError("El código del equipo debe tener 3 letras")
        
        if self.sistema.obtener_equipo(codigo) is None:
            raise ValueError(f"El equipo {codigo} no está registrado")
        
        if self.partido_actual is None:
            self.partido_actual = {}
        self.partido_actual['equipo_visitante'] = codigo
    
    def _procesar_formacion_local(self, datos: str):
        """Procesa la formación local"""
        formacion = datos.strip()
        if self.partido_actual is None:
            self.partido_actual = {}
        self.partido_actual['formacion_local'] = formacion
    
    def _procesar_formacion_visitante(self, datos: str):
        """Procesa la formación visitante"""
        formacion = datos.strip()
        if self.partido_actual is None:
            self.partido_actual = {}
        self.partido_actual['formacion_visitante'] = formacion
    
    def _procesar_titulares_local(self, datos: str):
        """Procesa los titulares locales"""
        numeros = [int(x.strip()) for x in datos.split(',')]
        if len(numeros) != 11:
            raise ValueError("Debe haber exactamente 11 titulares")
        
        # Validar que los jugadores existan en el equipo
        if 'equipo_local' in self.partido_actual:
            equipo = self.sistema.obtener_equipo(self.partido_actual['equipo_local'])
            if equipo:
                for num in numeros:
                    if not equipo.obtener_jugador(num):
                        raise ValueError(f"El jugador #{num} no existe en el equipo {equipo.codigo}")
        
        if self.partido_actual is None:
            self.partido_actual = {}
        self.partido_actual['titulares_local'] = numeros
    
    def _procesar_titulares_visitante(self, datos: str):
        """Procesa los titulares visitantes"""
        numeros = [int(x.strip()) for x in datos.split(',')]
        if len(numeros) != 11:
            raise ValueError("Debe haber exactamente 11 titulares")
        
        # Validar que los jugadores existan en el equipo
        if 'equipo_visitante' in self.partido_actual:
            equipo = self.sistema.obtener_equipo(self.partido_actual['equipo_visitante'])
            if equipo:
                for num in numeros:
                    if not equipo.obtener_jugador(num):
                        raise ValueError(f"El jugador #{num} no existe en el equipo {equipo.codigo}")
        
        if self.partido_actual is None:
            self.partido_actual = {}
        self.partido_actual['titulares_visitante'] = numeros
    
    def _procesar_banco_local(self, datos: str):
        """Procesa el banco local"""
        numeros = [int(x.strip()) for x in datos.split(',')]
        
        # Validar que los jugadores existan en el equipo
        if 'equipo_local' in self.partido_actual:
            equipo = self.sistema.obtener_equipo(self.partido_actual['equipo_local'])
            if equipo:
                for num in numeros:
                    if not equipo.obtener_jugador(num):
                        raise ValueError(f"El jugador #{num} no existe en el equipo {equipo.codigo}")
        
        if self.partido_actual is None:
            self.partido_actual = {}
        self.partido_actual['banco_local'] = numeros
    
    def _procesar_banco_visitante(self, datos: str):
        """Procesa el banco visitante"""
        numeros = [int(x.strip()) for x in datos.split(',')]
        
        # Validar que los jugadores existan en el equipo
        if 'equipo_visitante' in self.partido_actual:
            equipo = self.sistema.obtener_equipo(self.partido_actual['equipo_visitante'])
            if equipo:
                for num in numeros:
                    if not equipo.obtener_jugador(num):
                        raise ValueError(f"El jugador #{num} no existe en el equipo {equipo.codigo}")
        
        if self.partido_actual is None:
            self.partido_actual = {}
        self.partido_actual['banco_visitante'] = numeros
    
    def _procesar_gol(self, datos: str):
        """Procesa un gol"""
        partes = [x.strip() for x in datos.split(',')]
        if len(partes) < 3 or len(partes) > 4:
            raise ValueError("Formato de gol inválido. Use: EQUIPO, TIEMPO, AUTOR [, ASISTENTE]")
        
        equipo = partes[0].upper()
        tiempo = int(partes[1])
        autor = int(partes[2])
        asistente = int(partes[3]) if len(partes) == 4 else None
        
        if self.partido_actual is None:
            raise ValueError("Debe configurar el partido antes de agregar eventos")
        
        if 'eventos' not in self.partido_actual:
            self.partido_actual['eventos'] = []
        
        self.partido_actual['eventos'].append({
            'tipo': 'gol',
            'equipo': equipo,
            'tiempo': tiempo,
            'autor': autor,
            'asistente': asistente
        })
    
    def _procesar_tarjeta(self, datos: str):
        """Procesa una tarjeta"""
        partes = [x.strip() for x in datos.split(',')]
        if len(partes) != 4:
            raise ValueError("Formato de tarjeta inválido. Use: EQUIPO, TIEMPO, JUGADOR, COLOR")
        
        equipo = partes[0].upper()
        tiempo = int(partes[1])
        jugador = int(partes[2])
        color = partes[3].upper()
        
        if color not in ['AMARILLA', 'ROJA']:
            raise ValueError("El color debe ser AMARILLA o ROJA")
        
        if self.partido_actual is None:
            raise ValueError("Debe configurar el partido antes de agregar eventos")
        
        if 'eventos' not in self.partido_actual:
            self.partido_actual['eventos'] = []
        
        self.partido_actual['eventos'].append({
            'tipo': 'tarjeta',
            'equipo': equipo,
            'tiempo': tiempo,
            'jugador': jugador,
            'color': color
        })
    
    def _procesar_cambio(self, datos: str):
        """Procesa un cambio"""
        partes = [x.strip() for x in datos.split(',')]
        if len(partes) != 4:
            raise ValueError("Formato de cambio inválido. Use: EQUIPO, TIEMPO, SALE, ENTRA")
        
        equipo = partes[0].upper()
        tiempo = int(partes[1])
        jugador_sale = int(partes[2])
        jugador_entra = int(partes[3])
        
        if self.partido_actual is None:
            raise ValueError("Debe configurar el partido antes de agregar eventos")
        
        if 'eventos' not in self.partido_actual:
            self.partido_actual['eventos'] = []
        
        self.partido_actual['eventos'].append({
            'tipo': 'cambio',
            'equipo': equipo,
            'tiempo': tiempo,
            'jugador_sale': jugador_sale,
            'jugador_entra': jugador_entra
        })
    
    def finalizar_partido(self) -> Optional[Partido]:
        """Finaliza el partido actual y lo agrega al sistema"""
        if self.partido_actual is None:
            return None
        
        # Validar que tenga todos los datos necesarios
        campos_requeridos = ['fecha', 'equipo_local', 'equipo_visitante', 
                           'formacion_local', 'formacion_visitante',
                           'titulares_local', 'titulares_visitante',
                           'banco_local', 'banco_visitante']
        
        for campo in campos_requeridos:
            if campo not in self.partido_actual:
                raise ValueError(f"Falta el campo requerido: {campo}")
        
        # Crear el partido
        partido = Partido(
            fecha=self.partido_actual['fecha'],
            equipo_local=self.partido_actual['equipo_local'],
            equipo_visitante=self.partido_actual['equipo_visitante'],
            formacion_local=self.partido_actual['formacion_local'],
            formacion_visitante=self.partido_actual['formacion_visitante'],
            titulares_local=self.partido_actual['titulares_local'],
            titulares_visitante=self.partido_actual['titulares_visitante'],
            banco_local=self.partido_actual['banco_local'],
            banco_visitante=self.partido_actual['banco_visitante']
        )
        
        # Agregar eventos
        for evento_data in self.partido_actual.get('eventos', []):
            if evento_data['tipo'] == 'gol':
                partido.agregar_gol(
                    evento_data['equipo'],
                    evento_data['tiempo'],
                    evento_data['autor'],
                    evento_data['asistente']
                )
            elif evento_data['tipo'] == 'tarjeta':
                partido.agregar_tarjeta(
                    evento_data['equipo'],
                    evento_data['tiempo'],
                    evento_data['jugador'],
                    evento_data['color']
                )
            elif evento_data['tipo'] == 'cambio':
                partido.agregar_cambio(
                    evento_data['equipo'],
                    evento_data['tiempo'],
                    evento_data['jugador_sale'],
                    evento_data['jugador_entra']
                )
        
        # Agregar al sistema
        self.sistema.agregar_partido(partido)
        
        # Limpiar partido actual
        partido_finalizado = partido
        self.partido_actual = None
        
        return partido_finalizado


def procesar_archivo_partidos(archivo_path: str, sistema: SistemaFutbol) -> bool:
    """Procesa un archivo de partidos - PUEDE CONTENER MÚLTIPLES PARTIDOS"""
    try:
        parser = ParserFutbol(sistema)
        
        with open(archivo_path, 'r', encoding='utf-8') as archivo:
            for num_linea, linea in enumerate(archivo, 1):
                linea = linea.strip()
                if not linea or linea.startswith('#'):
                    continue
                
                # Detectar inicio de nuevo partido
                if linea.upper().startswith('FECHA:'):
                    # Finalizar partido anterior si existe
                    if parser.partido_actual is not None and 'fecha' in parser.partido_actual:
                        try:
                            parser.finalizar_partido()
                            print(f"✅ Partido finalizado correctamente")
                        except Exception as e:
                            print(f"❌ Error finalizando partido anterior: {e}")
                            return False
                
                if not parser.procesar_comando(linea):
                    print(f"❌ Error en línea {num_linea}: {linea}")
                    return False
        
        # Finalizar el último partido si existe
        if parser.partido_actual is not None:
            parser.finalizar_partido()
            print(f"✅ Último partido finalizado correctamente")
        
        return True
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {archivo_path}")
        return False
    except Exception as e:
        print(f"❌ Error procesando archivo: {e}")
        return False


def procesar_comando_partido(comando: str, sistema: SistemaFutbol) -> bool:
    """Procesa un comando de partido desde consola"""
    parser = ParserFutbol(sistema)
    return parser.procesar_comando(comando)
