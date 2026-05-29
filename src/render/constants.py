"""
constants.py
Global constants used across the Fly-in project.
"""

from __future__ import annotations

# =========================================================
# DEFAULT VALUES
# =========================================================

ZONE_DEFAULT: str = "normal"
COLOR_DEFAULT: str = "white"
META_MAX_L_CAP_DEFAULT: int = 1
MAX_DRONES_DEFAULT: int = 1

# =========================================================
# ZONE TYPES
# =========================================================

ZONE_NORMAL: str = "normal"
ZONE_RESTRICTED: str = "restricted"
ZONE_PRIORITY: str = "priority"
ZONE_BLOCKED: str = "blocked"

# =========================================================
# MOVEMENT COSTS
# =========================================================

MOVEMENT_COSTS: dict[str, int] = {
    ZONE_NORMAL: 1,
    ZONE_PRIORITY: 1,
    ZONE_RESTRICTED: 2,
    ZONE_BLOCKED: -1,
    ZONE_DEFAULT: 1
}


# =========================================================
# ANSI COLORS
# =========================================================

ANSI_RESET: str = "\033[0m"
ANSI_RED: str = "\33[0;31m"
ANSI_GREEN: str = "\033[32m"
ANSI_YELLOW: str = "\033[33m"
ANSI_BLUE: str = "\033[38;2;80;160;255m"
ANSI_PURPLE: str = "\033[35m"
ANSI_WHITE: str = "\033[37m"
ANSI_BOLD: str = "\033[1m"
ANSI_BLACK: str = "\33[38;5;16m"
ANSI_BROWN: str = "\033[38;2;139;69;19m"
ANSI_ORANGE: str = "\033[38;2;255;165;0m"
ANSI_MAROON: str = "\033[38;2;128;0;0m"
ANSI_GOLD: str = "\033[38;2;255;215;0m"
ANSI_DARK_RED: str = "\033[38;2;255;70;70m"
ANSI_CRIMSON: str = "\033[38;2;200;40;80m"

# =========================================================
# VISUAL COLORS
# =========================================================

COLOR_RED: str = "red"
COLOR_GREEN: str = "green"
COLOR_YELLOW: str = "yellow"
COLOR_BLUE: str = "blue"
COLOR_PURPLE: str = "purple"
COLOR_WHITE: str = "white"
COLOR_GRAY: str = "gray"
COLOR_BLACK: str = "black"
COLOR_BROWN: str = "brown"
COLOR_ORANGE: str = "orange"
COLOR_MAROON: str = "maroon"
COLOR_GOLD: str = "gold"
COLOR_DARK_RED: str = "darkred"
COLOR_CRIMSON: str = "crimson"

# =========================================================
# COLOR TO ANSI MAP
# =========================================================

ANSI_COLORS: dict[str, str] = {
    COLOR_RED: ANSI_RED,
    COLOR_GREEN: ANSI_GREEN,
    COLOR_YELLOW: ANSI_YELLOW,
    COLOR_BLUE: ANSI_BLUE,
    COLOR_PURPLE: ANSI_PURPLE,
    COLOR_WHITE: ANSI_WHITE,
    COLOR_GRAY: ANSI_WHITE,
    COLOR_BLACK: ANSI_BLACK,
    COLOR_BROWN: ANSI_BROWN,
    COLOR_ORANGE: ANSI_ORANGE,
    COLOR_MAROON: ANSI_MAROON,
    COLOR_GOLD: ANSI_GOLD,
    COLOR_DARK_RED: ANSI_DARK_RED,
    COLOR_CRIMSON: ANSI_CRIMSON
}

# =========================================================
# TERMINAL SYMBOLS - UNICODE
# =========================================================

SYMBOL_DRONE: str = "🛸"
SYMBOL_END: str = "🏁"

SYMBOL_NORMAL: str = "⛶ N"
SYMBOL_PRIORITY: str = "⚠  P"
SYMBOL_RESTRICTED: str = "⛞  R"
SYMBOL_BLOCKED: str = "⛔"

SYMBOL_CONNECTION: str = "➤"
SYMBOL_WAIT: str = "⏳ Waiting..."
SYMBOL_ERROR: str = "💀"
SYMBOL_SUCCESS: str = "✅"

# =========================================================
# TURN LIMITS (MAX LIMITS PERMITED BY 42)
# =========================================================

TURN_LIMITS: dict[str, dict[str, int]] = {
    "easy": {
        "01_linear_path": 6,
        "02_simple_fork": 8,
        "03_basic_capacity": 6,
    },
    "medium": {
        "01_dead_end_trap": 12,
        "02_circular_loop": 15,
        "03_priority_puzzle": 12,
    },
    "hard": {
        "01_maze_nightmare": 30,
        "02_capacity_hell": 35,
        "03_ultimate_challenge": 45,
    },
    "challenger": {
        "01_the_impossible_dream": 45,
    }
}
