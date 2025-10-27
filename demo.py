#!/usr/bin/env python3
"""
Script de demostración completa del Sistema de Fútbol
Muestra el uso de DSL Interno y Externo
"""

from src.dsl_interno import SistemaFutbol
from src.dsl_externo import procesar_archivo_partidos

def main():
    print("=" * 80)
    print("DEMO COMPLETA DEL SISTEMA DE GESTIÓN DE PARTIDOS DE FÚTBOL")
    print("=" * 80)
    
    # Inicializar sistema
    sistema = SistemaFutbol()
    
    # ========================================
    # PASO 1: Crear equipos con DSL Interno
    # ========================================
    print("\n📋 PASO 1: Creando equipos con DSL Interno...")
    print("-" * 80)
    
    # Barcelona
    barcelona = sistema.crear_equipo()
    barcelona.con_nombre("FC Barcelona").con_codigo("BAR")
    
    jugadores_bar = [
        (1, "Ter Stegen"), (2, "Dest"), (3, "Piqué"), (4, "Araujo"),
        (5, "Busquets"), (6, "Pedri"), (7, "Dembélé"), (8, "De Jong"),
        (9, "Lewandowski"), (10, "Ansu Fati"), (11, "Ferran Torres"),
        (12, "Peña"), (13, "Iñaki Peña"), (14, "Kessié"), 
        (15, "Christensen"), (16, "Raphinha"), (17, "Marcos Alonso")
    ]
    
    for numero, nombre in jugadores_bar:
        barcelona.agregar_jugador(numero, nombre)
    
    sistema.registrar_equipo(barcelona)
    print(f"✅ Equipo creado: Barcelona (BAR) - {len(jugadores_bar)} jugadores")
    
    # Real Madrid
    real_madrid = sistema.crear_equipo()
    real_madrid.con_nombre("Real Madrid").con_codigo("RMA")
    
    jugadores_rma = [
        (1, "Courtois"), (2, "Carvajal"), (3, "Militao"), (4, "Alaba"),
        (5, "Tchouameni"), (6, "Nacho"), (7, "Vinicius Jr"), (8, "Kroos"),
        (9, "Benzema"), (10, "Modric"), (11, "Asensio"),
        (12, "Lunin"), (13, "Vallejo"), (14, "Casemiro"),
        (15, "Valverde"), (16, "Rodrygo"), (17, "Lucas Vázquez")
    ]
    
    for numero, nombre in jugadores_rma:
        real_madrid.agregar_jugador(numero, nombre)
    
    sistema.registrar_equipo(real_madrid)
    print(f"✅ Equipo creado: Real Madrid (RMA) - {len(jugadores_rma)} jugadores")
    
    # ========================================
    # PASO 2: Mostrar equipos registrados
    # ========================================
    print("\n📊 PASO 2: Equipos registrados en el sistema")
    print("-" * 80)
    sistema.mostrar_equipos()
    
    # ========================================
    # PASO 3: Cargar partidos con DSL Externo
    # ========================================
    print("\n⚽ PASO 3: Cargando partidos desde archivo...")
    print("-" * 80)
    
    if procesar_archivo_partidos("ejemplos/partidos_ejemplo.txt", sistema):
        print(f"\n📈 Total de partidos en el sistema: {len(sistema.partidos)}")
    else:
        print("❌ Error cargando partidos")
        return
    
    # ========================================
    # PASO 4: Mostrar resultados
    # ========================================
    print("\n🏆 PASO 4: Resultados de los partidos")
    print("=" * 80)
    
    for i, partido in enumerate(sistema.partidos, 1):
        resultado = partido.obtener_resultado()
        print(f"\nPartido {i}:")
        print(f"  {partido}")
        print(f"  Formaciones: {partido.formacion_local} vs {partido.formacion_visitante}")
        
        if partido.eventos:
            print(f"  Eventos ({len(partido.eventos)}):")
            for evento in sorted(partido.eventos, key=lambda e: e.tiempo):
                print(f"    - {evento}")
    
    # ========================================
    # PASO 5: Tabla de posiciones
    # ========================================
    print("\n📊 PASO 5: Tabla de Posiciones")
    print("=" * 80)
    
    tabla = sistema.obtener_tabla_posiciones()
    
    print(f"\n{'Pos':<5} {'Equipo':<15} {'PJ':<5} {'G':<5} {'E':<5} {'P':<5} {'GF':<5} {'GC':<5} {'Pts':<5}")
    print("-" * 80)
    
    for i, stats in enumerate(tabla, 1):
        print(f"{i:<5} {stats['equipo']:<15} {stats['partidos_jugados']:<5} "
              f"{stats['ganados']:<5} {stats['empatados']:<5} {stats['perdidos']:<5} "
              f"{stats['goles_a_favor']:<5} {stats['goles_en_contra']:<5} {stats['puntos']:<5}")
    
    # ========================================
    # PASO 6: Tabla de goleadores
    # ========================================
    print("\n🥅 PASO 6: Tabla de Goleadores")
    print("=" * 80)
    
    goleadores = sistema.obtener_tabla_goleadores()
    
    if goleadores:
        print(f"\n{'Pos':<5} {'Jugador':<30} {'Equipo':<10} {'Goles':<5}")
        print("-" * 80)
        
        for i, goleador in enumerate(goleadores, 1):
            print(f"{i:<5} {goleador['jugador']:<30} {goleador['equipo']:<10} {goleador['goles']:<5}")
    else:
        print("No hay goles registrados")
    
    print("\n" + "=" * 80)
    print("✅ DEMO COMPLETADA EXITOSAMENTE")
    print("=" * 80)

if __name__ == "__main__":
    main()
