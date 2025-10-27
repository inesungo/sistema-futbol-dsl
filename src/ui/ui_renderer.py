"""
Módulo de UI/UX Profesional
Sistema de colores, estilos y utilidades visuales
"""

import os
import sys
import time
from typing import List, Dict, Any, Optional

# Códigos de colores ANSI para terminal
class Colors:
    """Códigos de colores ANSI para terminal"""
    
    # Colores básicos
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    # Colores de texto
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Colores brillantes
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Colores de fondo
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Colores de fondo brillantes
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'


class UITheme:
    """Tema de colores para la interfaz"""
    
    def __init__(self):
        # Colores principales
        self.primary = Colors.BRIGHT_BLUE
        self.secondary = Colors.BRIGHT_CYAN
        self.success = Colors.BRIGHT_GREEN
        self.warning = Colors.BRIGHT_YELLOW
        self.error = Colors.BRIGHT_RED
        self.info = Colors.BRIGHT_MAGENTA
        
        # Colores de texto
        self.text_primary = Colors.WHITE
        self.text_secondary = Colors.BRIGHT_WHITE
        self.text_muted = Colors.BRIGHT_BLACK
        
        # Colores de fondo
        self.bg_primary = Colors.BG_BLACK
        self.bg_secondary = Colors.BG_BRIGHT_BLACK
        self.bg_success = Colors.BG_GREEN
        self.bg_warning = Colors.BG_YELLOW
        self.bg_error = Colors.BG_RED
        
        # Emojis temáticos
        self.icons = {
            'soccer': '⚽',
            'trophy': '🏆',
            'chart': '📊',
            'team': '👥',
            'calendar': '📅',
            'goal': '🥅',
            'card': '🟨',
            'substitution': '🔄',
            'star': '⭐',
            'fire': '🔥',
            'check': '✅',
            'cross': '❌',
            'warning': '⚠️',
            'info': '💡',
            'help': '❓',
            'settings': '⚙️',
            'home': '🏠',
            'arrow': '➤',
            'bullet': '•',
            'dash': '─',
            'pipe': '│',
            'corner_tl': '┌',
            'corner_tr': '┐',
            'corner_bl': '└',
            'corner_br': '┘',
            'cross_h': '┬',
            'cross_v': '├',
            'cross_b': '┴',
            'cross_c': '┼'
        }


class UIRenderer:
    """Renderizador de UI profesional"""
    
    def __init__(self):
        self.theme = UITheme()
        self.width = 80  # Ancho por defecto
    
    def clear_screen(self):
        """Limpia la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def set_width(self, width: int):
        """Establece el ancho de la interfaz"""
        self.width = width
    
    def print_header(self, title: str, subtitle: str = "", icon: str = "⚽"):
        """Imprime un encabezado profesional"""
        print(f"\n{self.theme.primary}{Colors.BOLD}")
        print("═" * self.width)
        
        # Título principal
        title_line = f"{icon} {title}"
        if subtitle:
            title_line += f" - {subtitle}"
        
        # Centrar el título
        padding = (self.width - len(title_line)) // 2
        print(" " * padding + title_line)
        print("═" * self.width)
        print(f"{Colors.RESET}")
    
    def print_section(self, title: str, icon: str = "📋"):
        """Imprime una sección"""
        print(f"\n{self.theme.secondary}{Colors.BOLD}")
        print(f"{icon} {title}")
        print("─" * len(f"{icon} {title}"))
        print(f"{Colors.RESET}")
    
    def print_status(self, status: str, status_type: str = "info"):
        """Imprime un estado con color"""
        colors = {
            "success": self.theme.success,
            "warning": self.theme.warning,
            "error": self.theme.error,
            "info": self.theme.info
        }
        
        icons = {
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "info": "💡"
        }
        
        color = colors.get(status_type, self.theme.info)
        icon = icons.get(status_type, "💡")
        
        print(f"{color}{icon} {status}{Colors.RESET}")
    
    def print_table(self, headers: List[str], rows: List[List[str]], 
                   title: str = "", align: str = "left"):
        """Imprime una tabla profesional"""
        if not rows:
            return
        
        # Calcular anchos de columna
        col_widths = []
        for i, header in enumerate(headers):
            max_width = len(header)
            for row in rows:
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])))
            col_widths.append(min(max_width + 2, 20))  # Máximo 20 caracteres
        
        # Imprimir título si existe
        if title:
            self.print_section(title, "📊")
        
        # Imprimir encabezado
        print(f"{self.theme.primary}{Colors.BOLD}")
        print("┌" + "┬".join("─" * width for width in col_widths) + "┐")
        
        header_row = "│"
        for i, header in enumerate(headers):
            header_row += f" {header:<{col_widths[i]-1}}│"
        print(header_row)
        
        print("├" + "┼".join("─" * width for width in col_widths) + "┤")
        print(f"{Colors.RESET}")
        
        # Imprimir filas
        for row_idx, row in enumerate(rows):
            color = self.theme.text_primary if row_idx % 2 == 0 else self.theme.text_secondary
            print(f"{color}")
            
            row_str = "│"
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    cell_str = str(cell)[:col_widths[i]-1]  # Truncar si es muy largo
                    if align == "right":
                        row_str += f" {cell_str:>{col_widths[i]-1}}│"
                    else:
                        row_str += f" {cell_str:<{col_widths[i]-1}}│"
            print(row_str)
            print(f"{Colors.RESET}")
        
        # Imprimir pie
        print(f"{self.theme.primary}{Colors.BOLD}")
        print("└" + "┴".join("─" * width for width in col_widths) + "┘")
        print(f"{Colors.RESET}")
    
    def print_menu(self, title: str, options: List[Dict[str, str]], 
                  current_state: Dict[str, Any] = None):
        """Imprime un menú profesional"""
        self.print_header(title, "Sistema de Gestión de Fútbol", "⚽")
        
        # Mostrar estado actual si se proporciona
        if current_state:
            self.print_status_section(current_state)
        
        print(f"\n{self.theme.text_primary}{Colors.BOLD}📋 OPCIONES DISPONIBLES:{Colors.RESET}")
        print()
        
        for option in options:
            icon = option.get('icon', '•')
            text = option.get('text', '')
            description = option.get('description', '')
            
            print(f"{self.theme.primary}{icon} {text}{Colors.RESET}")
            if description:
                print(f"   {self.theme.text_muted}{description}{Colors.RESET}")
            print()
    
    def print_status_section(self, state: Dict[str, Any]):
        """Imprime una sección de estado"""
        print(f"\n{self.theme.info}{Colors.BOLD}📊 ESTADO ACTUAL:{Colors.RESET}")
        
        # Estadísticas básicas
        equipos = state.get('equipos', 0)
        partidos = state.get('partidos', 0)
        
        print(f"   {self.theme.text_secondary}Equipos registrados: {equipos}{Colors.RESET}")
        print(f"   {self.theme.text_secondary}Partidos cargados: {partidos}{Colors.RESET}")
        
        # Mensajes de estado
        if equipos == 0:
            self.print_status("No hay equipos registrados", "warning")
            self.print_status("Debe crear equipos antes de cargar partidos", "info")
            self.print_status("Use la opción 5 para gestionar equipos", "info")
        elif partidos == 0:
            self.print_status("No hay partidos cargados", "info")
            self.print_status("Use la opción 1 para cargar partidos", "info")
        else:
            self.print_status("Sistema listo para usar", "success")
    
    def print_card(self, title: str, content: str, icon: str = "📄"):
        """Imprime una tarjeta de información"""
        print(f"\n{self.theme.secondary}{Colors.BOLD}")
        print("┌" + "─" * (self.width - 2) + "┐")
        
        # Título
        title_line = f"{icon} {title}"
        padding = (self.width - 2 - len(title_line)) // 2
        print(f"│{' ' * padding}{title_line}{' ' * (self.width - 2 - padding - len(title_line))}│")
        
        print("├" + "─" * (self.width - 2) + "┤")
        
        # Contenido
        lines = content.split('\n')
        for line in lines:
            if len(line) > self.width - 4:
                line = line[:self.width - 7] + "..."
            padding = (self.width - 2 - len(line)) // 2
            print(f"│{' ' * padding}{line}{' ' * (self.width - 2 - padding - len(line))}│")
        
        print("└" + "─" * (self.width - 2) + "┘")
        print(f"{Colors.RESET}")
    
    def print_progress(self, current: int, total: int, label: str = ""):
        """Imprime una barra de progreso"""
        if total == 0:
            return
        
        percentage = (current / total) * 100
        bar_width = 30
        filled_width = int((current / total) * bar_width)
        
        bar = "█" * filled_width + "░" * (bar_width - filled_width)
        
        print(f"\r{self.theme.info}{label} [{bar}] {percentage:.1f}%{Colors.RESET}", end="", flush=True)
        
        if current == total:
            print()  # Nueva línea al completar
    
    def print_loading(self, message: str = "Cargando..."):
        """Imprime un indicador de carga"""
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        for i in range(10):
            print(f"\r{self.theme.info}{chars[i % len(chars)]} {message}{Colors.RESET}", end="", flush=True)
            time.sleep(0.1)
        print("\r" + " " * (len(message) + 3) + "\r", end="")
    
    def print_separator(self, char: str = "─", color: str = None):
        """Imprime un separador"""
        color_code = getattr(self.theme, color, self.theme.text_muted) if color else self.theme.text_muted
        print(f"{color_code}{char * self.width}{Colors.RESET}")
    
    def print_centered(self, text: str, color: str = None):
        """Imprime texto centrado"""
        color_code = getattr(self.theme, color, self.theme.text_primary) if color else self.theme.text_primary
        padding = (self.width - len(text)) // 2
        print(f"{color_code}{' ' * padding}{text}{Colors.RESET}")
    
    def input_prompt(self, prompt: str, color: str = "primary"):
        """Solicita input con estilo"""
        color_code = getattr(self.theme, color, self.theme.text_primary)
        return input(f"{color_code}{prompt}{Colors.RESET}")
    
    def pause(self, message: str = "Presione Enter para continuar..."):
        """Pausa con mensaje estilizado"""
        self.input_prompt(f"\n{self.theme.text_muted}{message}{Colors.RESET}")


# Instancia global del renderizador
ui = UIRenderer()
