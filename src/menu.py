"""
Menú Principal del Sistema de Gestión de Partidos de Fútbol
"""

import os
from typing import Optional
import sys
import os
# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.dsl_interno import SistemaFutbol
from src.dsl_externo import procesar_archivo_partidos, procesar_comando_partido
from src.ui import ui


class MenuPrincipal:
    """Menú principal del sistema"""
    
    def __init__(self, sistema: SistemaFutbol):
        self.sistema = sistema
    
    def ejecutar(self):
        """Ejecuta el menú principal"""
        while True:
            self._mostrar_menu()
            opcion = ui.input_prompt("\n🔧 Seleccione una opción: ").strip()
            
            if opcion == '1':
                self._menu_carga_partidos()
            elif opcion == '2':
                self._mostrar_tabla_posiciones()
            elif opcion == '3':
                self._mostrar_tabla_goleadores()
            elif opcion == '4':
                self._mostrar_resultados_partidos()
            elif opcion == '5':
                self._menu_gestion_equipos()
            elif opcion == '6':
                self._mostrar_ayuda()
            elif opcion == '0':
                print("\n¡Gracias por usar el sistema!")
                break
            else:
                print("\nOpción inválida. Intente nuevamente.")
    
    def _mostrar_menu(self):
        """Muestra el menú principal"""
        # Preparar opciones del menú
        options = [
            {
                'icon': '⚽',
                'text': '1. Carga de partidos',
                'description': 'Cargar partidos desde archivos o comandos interactivos'
            },
            {
                'icon': '📊',
                'text': '2. Ver tabla de posiciones por puntos',
                'description': 'Mostrar clasificación de equipos por puntos'
            },
            {
                'icon': '🥅',
                'text': '3. Ver tabla de goleadores',
                'description': 'Mostrar estadísticas de goles por jugador'
            },
            {
                'icon': '🏆',
                'text': '4. Listar resultados de todos los partidos',
                'description': 'Ver historial completo de partidos jugados'
            },
            {
                'icon': '👥',
                'text': '5. Gestión de equipos',
                'description': 'Crear y administrar equipos y jugadores'
            },
            {
                'icon': '❓',
                'text': '6. Ayuda y tutorial',
                'description': 'Guía completa del sistema y comandos'
            },
            {
                'icon': '🚪',
                'text': '0. Salir',
                'description': 'Cerrar el sistema'
            }
        ]
        
        # Estado actual del sistema
        current_state = {
            'equipos': len(self.sistema.equipos),
            'partidos': len(self.sistema.partidos)
        }
        
        # Mostrar menú profesional
        ui.print_menu("MENÚ PRINCIPAL", options, current_state)
    
    def _mostrar_estado_sistema(self):
        """Muestra el estado actual del sistema"""
        num_equipos = len(self.sistema.equipos)
        num_partidos = len(self.sistema.partidos)
        
        print(f"\n📊 ESTADO ACTUAL:")
        print(f"   Equipos registrados: {num_equipos}")
        print(f"   Partidos cargados: {num_partidos}")
        
        if num_equipos == 0:
            print("\n⚠️  ATENCIÓN: No hay equipos registrados")
            print("   💡 Debe crear equipos antes de cargar partidos")
            print("   📝 Use la opción 5 para gestionar equipos")
        elif num_partidos == 0:
            print("\n💡 SUGERENCIA: No hay partidos cargados")
            print("   📝 Use la opción 1 para cargar partidos")
        else:
            print("\n✅ Sistema listo para usar")
    
    def _menu_carga_partidos(self):
        """Submenú para carga de partidos"""
        # Verificar que hay equipos registrados
        if len(self.sistema.equipos) == 0:
            print("\n" + "="*60)
            print("⚠️  NO HAY EQUIPOS REGISTRADOS")
            print("="*60)
            print("\nPara cargar partidos, primero debe crear equipos.")
            print("\n💡 OPCIONES:")
            print("1. Crear equipos ahora (opción 5)")
            print("2. Usar demo completo (python demo.py)")
            print("3. Volver al menú principal")
            
            opcion = input("\n¿Qué desea hacer? (1/2/3): ").strip()
            
            if opcion == '1':
                self._menu_gestion_equipos()
            elif opcion == '2':
                print("\n💡 Ejecute: python demo.py")
                input("Presione Enter para continuar...")
            return
        
        while True:
            print("\n" + "-"*40)
            print("CARGA DE PARTIDOS")
            print("-"*40)
            print("a. Carga con comandos")
            print("b. Carga desde archivo")
            print("0. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip().lower()
            
            if opcion == 'a':
                self._carga_por_comandos()
            elif opcion == 'b':
                self._carga_desde_archivo()
            elif opcion == '0':
                break
            else:
                print("\nOpción inválida. Intente nuevamente.")
    
    def _carga_por_comandos(self):
        """Carga de partidos por comandos interactivos"""
        print("\n" + "="*50)
        print("⚽ CARGA DE PARTIDOS POR COMANDOS")
        print("="*50)
        
        print("\n📋 EQUIPOS DISPONIBLES:")
        for codigo, equipo in self.sistema.equipos.items():
            print(f"   {codigo} - {equipo.nombre}")
        
        print("\n💡 COMANDOS DISPONIBLES:")
        print("-" * 30)
        print("FECHA: DD/MM/YYYY")
        print("EQUIPO LOCAL: CODIGO")
        print("EQUIPO VISITANTE: CODIGO")
        print("FORMACION LOCAL: X-Y-Z")
        print("FORMACION VISITANTE: X-Y-Z")
        print("TITULARES LOCAL: 1,2,3,4,5,6,7,8,9,10,11")
        print("TITULARES VISITANTE: 1,2,3,4,5,6,7,8,9,10,11")
        print("BANCO LOCAL: 12,13,14,15,16,17")
        print("BANCO VISITANTE: 12,13,14,15,16,17")
        print("GOL: EQUIPO, TIEMPO, AUTOR [, ASISTENTE]")
        print("TARJETA: EQUIPO, TIEMPO, JUGADOR, COLOR")
        print("CAMBIO: EQUIPO, TIEMPO, SALE, ENTRA")
        
        print("\n📝 INSTRUCCIONES:")
        print("- Escriba 'FIN' para terminar la carga del partido")
        print("- Escriba 'SALIR' para volver al menú")
        print("- Escriba 'AYUDA' para ver comandos nuevamente")
        
        while True:
            comando = input("\n🔧 Comando: ").strip()
            
            if comando.upper() == 'SALIR':
                break
            elif comando.upper() == 'FIN':
                print("✅ Partido cargado exitosamente!")
                break
            elif comando.upper() == 'AYUDA':
                print("\n💡 COMANDOS DISPONIBLES:")
                print("FECHA: DD/MM/YYYY")
                print("EQUIPO LOCAL: CODIGO")
                print("EQUIPO VISITANTE: CODIGO")
                print("FORMACION LOCAL: X-Y-Z")
                print("FORMACION VISITANTE: X-Y-Z")
                print("TITULARES LOCAL: 1,2,3,4,5,6,7,8,9,10,11")
                print("TITULARES VISITANTE: 1,2,3,4,5,6,7,8,9,10,11")
                print("BANCO LOCAL: 12,13,14,15,16,17")
                print("BANCO VISITANTE: 12,13,14,15,16,17")
                print("GOL: EQUIPO, TIEMPO, AUTOR [, ASISTENTE]")
                print("TARJETA: EQUIPO, TIEMPO, JUGADOR, COLOR")
                print("CAMBIO: EQUIPO, TIEMPO, SALE, ENTRA")
            elif comando:
                if procesar_comando_partido(comando, self.sistema):
                    print("✅ Comando procesado correctamente")
                else:
                    print("❌ Error en el comando")
    
    def _carga_desde_archivo(self):
        """Carga de partidos desde archivo"""
        print("\n" + "="*50)
        print("CARGA DE PARTIDOS DESDE ARCHIVO")
        print("="*50)
        
        archivo_path = input("Ingrese la ruta del archivo: ").strip()
        
        if not archivo_path:
            print("Debe especificar una ruta de archivo")
            return
        
        if not os.path.exists(archivo_path):
            print(f"El archivo {archivo_path} no existe")
            return
        
        print(f"Procesando archivo: {archivo_path}")
        
        if procesar_archivo_partidos(archivo_path, self.sistema):
            print("✓ Archivo procesado exitosamente")
        else:
            print("✗ Error procesando el archivo")
    
    def _mostrar_tabla_posiciones(self):
        """Muestra la tabla de posiciones"""
        ui.print_header("TABLA DE POSICIONES", "Clasificación por Puntos", "📊")
        
        if len(self.sistema.equipos) == 0:
            ui.print_status("No hay equipos registrados", "warning")
            ui.print_status("Debe crear equipos antes de ver estadísticas", "info")
            ui.print_status("Use la opción 5 para gestionar equipos", "info")
            ui.pause()
            return
        
        tabla = self.sistema.obtener_tabla_posiciones()
        
        if not tabla or all(stats['partidos_jugados'] == 0 for stats in tabla):
            ui.print_status("No hay partidos jugados aún", "info")
            ui.print_status("Use la opción 1 para cargar partidos", "info")
            ui.pause()
            return
        
        # Preparar datos para la tabla
        headers = ["Pos", "Equipo", "PJ", "G", "E", "P", "GF", "GC", "Pts"]
        rows = []
        
        for i, equipo_stats in enumerate(tabla, 1):
            row = [
                str(i),
                equipo_stats['equipo'],
                str(equipo_stats['partidos_jugados']),
                str(equipo_stats['ganados']),
                str(equipo_stats['empatados']),
                str(equipo_stats['perdidos']),
                str(equipo_stats['goles_a_favor']),
                str(equipo_stats['goles_en_contra']),
                str(equipo_stats['puntos'])
            ]
            rows.append(row)
        
        # Mostrar tabla profesional
        ui.print_table(headers, rows, "Clasificación de Equipos")
        ui.pause()
    
    def _mostrar_tabla_goleadores(self):
        """Muestra la tabla de goleadores"""
        ui.print_header("TABLA DE GOLEADORES", "Estadísticas de Goles", "🥅")
        
        if len(self.sistema.equipos) == 0:
            ui.print_status("No hay equipos registrados", "warning")
            ui.print_status("Debe crear equipos antes de ver estadísticas", "info")
            ui.print_status("Use la opción 5 para gestionar equipos", "info")
            ui.pause()
            return
        
        tabla = self.sistema.obtener_tabla_goleadores()
        
        if not tabla:
            ui.print_status("No hay goles registrados aún", "info")
            ui.print_status("Use la opción 1 para cargar partidos con eventos", "info")
            ui.pause()
            return
        
        # Preparar datos para la tabla
        headers = ["Pos", "Jugador", "Equipo", "Goles"]
        rows = []
        
        for i, goleador in enumerate(tabla, 1):
            row = [
                str(i),
                goleador['jugador'],
                goleador['equipo'],
                str(goleador['goles'])
            ]
            rows.append(row)
        
        # Mostrar tabla profesional
        ui.print_table(headers, rows, "Ranking de Goleadores")
        ui.pause()
    
    def _mostrar_resultados_partidos(self):
        """Muestra todos los resultados de partidos"""
        print("\n" + "="*80)
        print("🏆 RESULTADOS DE TODOS LOS PARTIDOS")
        print("="*80)
        
        if len(self.sistema.equipos) == 0:
            print("\n⚠️  No hay equipos registrados")
            print("💡 Debe crear equipos antes de ver resultados")
            print("📝 Use la opción 5 para gestionar equipos")
            input("\nPresione Enter para continuar...")
            return
        
        if not self.sistema.partidos:
            print("\n💡 No hay partidos registrados aún")
            print("📝 Use la opción 1 para cargar partidos")
            input("\nPresione Enter para continuar...")
            return
        
        for i, partido in enumerate(self.sistema.partidos, 1):
            resultado = partido.obtener_resultado()
            print(f"\n{i}. {partido}")
            
            # Mostrar eventos del partido
            if partido.eventos:
                print("   📋 Eventos:")
                for evento in sorted(partido.eventos, key=lambda e: e.tiempo):
                    print(f"   - {evento}")
            else:
                print("   📋 Sin eventos registrados")
        
        input("\nPresione Enter para continuar...")
    
    def _mostrar_ayuda(self):
        """Muestra ayuda y tutorial del sistema"""
        print("\n" + "="*80)
        print("📚 AYUDA Y TUTORIAL DEL SISTEMA")
        print("="*80)
        
        print("\n🎯 ¿CÓMO FUNCIONA EL SISTEMA?")
        print("-" * 40)
        print("1️⃣ PRIMERO: Crear equipos (obligatorio)")
        print("2️⃣ SEGUNDO: Cargar partidos")
        print("3️⃣ TERCERO: Ver estadísticas")
        
        print("\n📋 PASOS DETALLADOS:")
        print("-" * 40)
        print("1. Use la opción 5 para crear equipos")
        print("   - Cada equipo necesita código de 3 letras")
        print("   - Mínimo 11 jugadores (para titulares)")
        print("   - Números de camiseta únicos")
        
        print("\n2. Use la opción 1 para cargar partidos")
        print("   - Desde archivo de texto")
        print("   - Por comandos interactivos")
        
        print("\n3. Use las opciones 2, 3, 4 para ver estadísticas")
        print("   - Tabla de posiciones")
        print("   - Tabla de goleadores")
        print("   - Resultados de partidos")
        
        print("\n💡 COMANDOS DE PARTIDO:")
        print("-" * 40)
        print("FECHA: DD/MM/YYYY")
        print("EQUIPO LOCAL: CODIGO")
        print("EQUIPO VISITANTE: CODIGO")
        print("FORMACION LOCAL: X-Y-Z")
        print("FORMACION VISITANTE: X-Y-Z")
        print("TITULARES LOCAL: 1,2,3,4,5,6,7,8,9,10,11")
        print("TITULARES VISITANTE: 1,2,3,4,5,6,7,8,9,10,11")
        print("BANCO LOCAL: 12,13,14,15,16,17")
        print("BANCO VISITANTE: 12,13,14,15,16,17")
        print("GOL: EQUIPO, TIEMPO, AUTOR [, ASISTENTE]")
        print("TARJETA: EQUIPO, TIEMPO, JUGADOR, COLOR")
        print("CAMBIO: EQUIPO, TIEMPO, SALE, ENTRA")
        
        print("\n🚀 OPCIONES RÁPIDAS:")
        print("-" * 40)
        print("• python demo.py - Demo completo automático")
        print("• python ejemplo_flujo.py - Ejemplo paso a paso")
        print("• python main.py - Menú interactivo")
        
        print("\n⚠️  REGLAS IMPORTANTES:")
        print("-" * 40)
        print("• Los equipos deben existir antes de crear partidos")
        print("• Exactamente 11 titulares por equipo")
        print("• Códigos de equipo de 3 letras únicos")
        print("• Números de camiseta únicos por equipo")
        print("• Sistema de puntos: Ganador=3, Empate=1, Perdedor=0")
        
        input("\nPresione Enter para continuar...")
    
    def _menu_gestion_equipos(self):
        """Submenú para gestión de equipos"""
        while True:
            print("\n" + "-"*40)
            print("GESTIÓN DE EQUIPOS")
            print("-"*40)
            print("a. Crear nuevo equipo")
            print("b. Mostrar todos los equipos")
            print("c. Mostrar jugadores de un equipo")
            print("0. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip().lower()
            
            if opcion == 'a':
                self._crear_equipo()
            elif opcion == 'b':
                self.sistema.mostrar_equipos()
            elif opcion == 'c':
                self._mostrar_jugadores_equipo()
            elif opcion == '0':
                break
            else:
                print("\nOpción inválida. Intente nuevamente.")
    
    def _crear_equipo(self):
        """Crea un nuevo equipo usando DSL interno"""
        print("\n" + "="*50)
        print("CREAR NUEVO EQUIPO")
        print("="*50)
        
        try:
            nombre = input("Nombre del equipo: ").strip()
            if not nombre:
                print("El nombre del equipo no puede estar vacío")
                return
            
            codigo = input("Código del equipo (3 letras): ").strip().upper()
            if len(codigo) != 3:
                print("El código debe tener exactamente 3 letras")
                return
            
            # Verificar que el código no esté en uso
            if self.sistema.obtener_equipo(codigo):
                print(f"Ya existe un equipo con el código {codigo}")
                return
            
            # Crear equipo usando DSL interno
            equipo_builder = self.sistema.crear_equipo()
            equipo_builder.con_nombre(nombre).con_codigo(codigo)
            
            # Agregar jugadores
            print(f"\nAgregando jugadores para {nombre}:")
            print("(Escriba 'FIN' para terminar)")
            
            while True:
                try:
                    numero_input = input("Número de camiseta (o 'FIN'): ").strip()
                    if numero_input.upper() == 'FIN':
                        break
                    
                    numero = int(numero_input)
                    nombre_jugador = input("Nombre del jugador: ").strip()
                    
                    if not nombre_jugador:
                        print("El nombre del jugador no puede estar vacío")
                        continue
                    
                    equipo_builder.agregar_jugador(numero, nombre_jugador)
                    print(f"✓ Jugador {numero}. {nombre_jugador} agregado")
                    
                except ValueError as e:
                    print(f"Error: {e}")
                except KeyboardInterrupt:
                    print("\nOperación cancelada")
                    return
            
            # Registrar el equipo
            self.sistema.registrar_equipo(equipo_builder)
            print(f"\n✓ Equipo {nombre} ({codigo}) creado exitosamente")
            
        except Exception as e:
            print(f"Error creando equipo: {e}")
    
    def _crear_equipo(self):
        """Crea un nuevo equipo usando DSL interno"""
        print("\n" + "="*50)
        print("⚽ CREAR NUEVO EQUIPO")
        print("="*50)
        
        try:
            print("\n📝 DATOS DEL EQUIPO:")
            nombre = input("Nombre del equipo: ").strip()
            if not nombre:
                print("❌ El nombre del equipo no puede estar vacío")
                input("Presione Enter para continuar...")
                return
            
            codigo = input("Código del equipo (3 letras): ").strip().upper()
            if len(codigo) != 3:
                print("❌ El código debe tener exactamente 3 letras")
                input("Presione Enter para continuar...")
                return
            
            # Verificar que el código no esté en uso
            if self.sistema.obtener_equipo(codigo):
                print(f"❌ Ya existe un equipo con el código {codigo}")
                input("Presione Enter para continuar...")
                return
            
            # Crear equipo usando DSL interno
            equipo_builder = self.sistema.crear_equipo()
            equipo_builder.con_nombre(nombre).con_codigo(codigo)
            
            # Agregar jugadores
            print(f"\n👥 AGREGANDO JUGADORES PARA {nombre.upper()}:")
            print("💡 Debe agregar al menos 11 jugadores (para titulares)")
            print("📝 Escriba 'FIN' para terminar")
            
            jugadores_agregados = 0
            while True:
                try:
                    numero_input = input(f"\nJugador #{jugadores_agregados + 1} - Número de camiseta (o 'FIN'): ").strip()
                    if numero_input.upper() == 'FIN':
                        if jugadores_agregados < 11:
                            print(f"⚠️  Solo tiene {jugadores_agregados} jugadores. Necesita al menos 11.")
                            continuar = input("¿Continuar agregando? (s/n): ").strip().lower()
                            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                                break
                        else:
                            break
                    
                    numero = int(numero_input)
                    nombre_jugador = input("Nombre del jugador: ").strip()
                    
                    if not nombre_jugador:
                        print("❌ El nombre del jugador no puede estar vacío")
                        continue
                    
                    equipo_builder.agregar_jugador(numero, nombre_jugador)
                    jugadores_agregados += 1
                    print(f"✅ Jugador {numero}. {nombre_jugador} agregado")
                    
                except ValueError as e:
                    print(f"❌ Error: {e}")
                except KeyboardInterrupt:
                    print("\n❌ Operación cancelada")
                    return
            
            # Registrar el equipo
            self.sistema.registrar_equipo(equipo_builder)
            print(f"\n🎉 ¡Equipo {nombre} ({codigo}) creado exitosamente!")
            print(f"📊 Total de jugadores: {jugadores_agregados}")
            
        except Exception as e:
            print(f"❌ Error creando equipo: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _mostrar_jugadores_equipo(self):
        """Muestra los jugadores de un equipo específico"""
        print("\n" + "="*50)
        print("👥 JUGADORES DE EQUIPO")
        print("="*50)
        
        if len(self.sistema.equipos) == 0:
            print("\n⚠️  No hay equipos registrados")
            print("💡 Debe crear equipos primero")
            input("\nPresione Enter para continuar...")
            return
        
        print("\n📋 Equipos disponibles:")
        for codigo, equipo in self.sistema.equipos.items():
            print(f"   {codigo} - {equipo.nombre}")
        
        codigo = input("\nCódigo del equipo: ").strip().upper()
        self.sistema.mostrar_jugadores_equipo(codigo)
        input("\nPresione Enter para continuar...")
