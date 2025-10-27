#!/usr/bin/env python3
"""
Sistema de Gestión de Partidos de Fútbol
Entregable 3 - DSL Interno y Externo
"""

from src.menu import MenuPrincipal
from src.dsl_interno import SistemaFutbol

def main():
    """Función principal del sistema"""
    print("=" * 60)
    print("    SISTEMA DE GESTIÓN DE PARTIDOS DE FÚTBOL")
    print("=" * 60)
    
    # Inicializar el sistema
    sistema = SistemaFutbol()
    
    # Crear y ejecutar el menú principal
    menu = MenuPrincipal(sistema)
    menu.ejecutar()

if __name__ == "__main__":
    main()
