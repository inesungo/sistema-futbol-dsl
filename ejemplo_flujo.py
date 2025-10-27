#!/usr/bin/env python3
"""
Ejemplo paso a paso del flujo completo del sistema
"""

from src.dsl_interno import SistemaFutbol, nuevo_equipo
from src.dsl_externo import procesar_archivo_partidos

def ejemplo_flujo_completo():
    """Demuestra el flujo completo paso a paso"""
    
    print("=" * 60)
    print("    FLUJO COMPLETO DEL SISTEMA DE FÚTBOL")
    print("=" * 60)
    
    # PASO 1: Crear sistema
    print("\n1️⃣ CREANDO SISTEMA")
    print("-" * 30)
    sistema = SistemaFutbol()
    print("✅ Sistema creado")
    
    # PASO 2: Crear equipos (OBLIGATORIO)
    print("\n2️⃣ CREANDO EQUIPOS (OBLIGATORIO)")
    print("-" * 30)
    
    # Crear Barcelona
    barcelona = (nuevo_equipo()
                .con_nombre("Barcelona")
                .con_codigo("BAR")
                .agregar_jugador(1, "Ter Stegen")
                .agregar_jugador(2, "Sergi Roberto")
                .agregar_jugador(3, "Piqué")
                .agregar_jugador(4, "Araújo")
                .agregar_jugador(5, "Busquets")
                .agregar_jugador(6, "Gavi")
                .agregar_jugador(7, "Pedri")
                .agregar_jugador(8, "De Jong")
                .agregar_jugador(9, "Lewandowski")
                .agregar_jugador(10, "Dembélé")
                .agregar_jugador(11, "Fati")
                .agregar_jugador(12, "Neto")
                .agregar_jugador(13, "García")
                .agregar_jugador(14, "Kessie")
                .agregar_jugador(15, "Torres")
                .agregar_jugador(16, "Raphinha")
                .agregar_jugador(17, "Alba"))
    
    sistema.registrar_equipo(barcelona)
    print("✅ Barcelona (BAR) creado con 17 jugadores")
    
    # Crear Real Madrid
    real_madrid = (nuevo_equipo()
                  .con_nombre("Real Madrid")
                  .con_codigo("RMA")
                  .agregar_jugador(1, "Courtois")
                  .agregar_jugador(2, "Carvajal")
                  .agregar_jugador(3, "Militão")
                  .agregar_jugador(4, "Alaba")
                  .agregar_jugador(5, "Modrić")
                  .agregar_jugador(6, "Casemiro")
                  .agregar_jugador(7, "Benzema")
                  .agregar_jugador(8, "Kroos")
                  .agregar_jugador(9, "Vinicius")
                  .agregar_jugador(10, "Valverde")
                  .agregar_jugador(11, "Rodrygo")
                  .agregar_jugador(12, "Lunin")
                  .agregar_jugador(13, "Camavinga")
                  .agregar_jugador(14, "Tchouaméni")
                  .agregar_jugador(15, "Hazard")
                  .agregar_jugador(16, "Asensio")
                  .agregar_jugador(17, "Mendy"))
    
    sistema.registrar_equipo(real_madrid)
    print("✅ Real Madrid (RMA) creado con 17 jugadores")
    
    # Mostrar equipos creados
    print(f"\n📋 Equipos disponibles: {list(sistema.equipos.keys())}")
    
    # PASO 3: Crear archivo de partido
    print("\n3️⃣ CREANDO ARCHIVO DE PARTIDO")
    print("-" * 30)
    
    contenido_partido = """# Partido Barcelona vs Real Madrid
FECHA: 15/10/2023
EQUIPO LOCAL: BAR
EQUIPO VISITANTE: RMA
FORMACION LOCAL: 4-3-3
FORMACION VISITANTE: 4-4-2
TITULARES LOCAL: 1,2,3,4,5,6,7,8,9,10,11
TITULARES VISITANTE: 1,2,3,4,5,6,7,8,9,10,11
BANCO LOCAL: 12,13,14,15,16,17
BANCO VISITANTE: 12,13,14,15,16,17

# Eventos del partido
GOL: BAR, 25, 9
GOL: RMA, 45, 7
TARJETA: RMA, 30, 7, AMARILLA
"""
    
    with open("partido_ejemplo.txt", "w", encoding="utf-8") as f:
        f.write(contenido_partido)
    
    print("✅ Archivo de partido creado: partido_ejemplo.txt")
    
    # PASO 4: Procesar partido
    print("\n4️⃣ PROCESANDO PARTIDO")
    print("-" * 30)
    
    if procesar_archivo_partidos("partido_ejemplo.txt", sistema):
        print("✅ Partido procesado exitosamente")
        print(f"📊 Total de partidos: {len(sistema.partidos)}")
    else:
        print("❌ Error procesando partido")
        return
    
    # PASO 5: Ver resultados
    print("\n5️⃣ MOSTRANDO RESULTADOS")
    print("-" * 30)
    
    # Tabla de posiciones
    tabla = sistema.obtener_tabla_posiciones()
    print("\n📈 TABLA DE POSICIONES:")
    for i, stats in enumerate(tabla, 1):
        print(f"{i}. {stats['equipo']} - {stats['puntos']} puntos")
    
    # Tabla de goleadores
    goleadores = sistema.obtener_tabla_goleadores()
    print("\n⚽ TABLA DE GOLEADORES:")
    for i, goleador in enumerate(goleadores, 1):
        print(f"{i}. {goleador['jugador']} ({goleador['equipo']}) - {goleador['goles']} goles")
    
    # Resultados de partidos
    print("\n🏆 RESULTADOS DE PARTIDOS:")
    for i, partido in enumerate(sistema.partidos, 1):
        resultado = partido.obtener_resultado()
        print(f"{i}. {partido}")
        for evento in partido.eventos:
            print(f"   - {evento}")
    
    # Limpiar archivo temporal
    import os
    os.remove("partido_ejemplo.txt")
    
    print("\n" + "=" * 60)
    print("    FLUJO COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    print("✅ Equipos creados")
    print("✅ Partido procesado")
    print("✅ Estadísticas calculadas")
    print("\n💡 Ahora puedes usar el menú interactivo:")
    print("   python main.py")

if __name__ == "__main__":
    ejemplo_flujo_completo()
