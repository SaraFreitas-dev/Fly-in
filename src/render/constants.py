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
# STATE
# =========================================================

DELIVERED_STATE = "delivered"
WAITING_STATE = "waiting"
TRANSIT_STATE = "transit"

# =========================================================
# ANSI COLORS
# =========================================================

ANSI_RESET: str = "\033[0m"

ANSI_RED: str = "\033[31m"
ANSI_GREEN: str = "\033[32m"
ANSI_YELLOW: str = "\033[33m"
ANSI_BLUE: str = "\033[34m"
ANSI_CYAN: str = "\033[36m"
ANSI_WHITE: str = "\033[37m"

# =========================================================
# VISUAL COLORS
# =========================================================

COLOR_RED: str = "red"
COLOR_GREEN: str = "green"
COLOR_YELLOW: str = "yellow"
COLOR_BLUE: str = "blue"
COLOR_CYAN: str = "cyan"
COLOR_WHITE: str = "white"
COLOR_GRAY: str = "gray"

# =========================================================
# COLOR TO ANSI MAP
# =========================================================

COLOR_TO_ANSI: dict[str, str] = {
    COLOR_RED: ANSI_RED,
    COLOR_GREEN: ANSI_GREEN,
    COLOR_YELLOW: ANSI_YELLOW,
    COLOR_BLUE: ANSI_BLUE,
    COLOR_CYAN: ANSI_CYAN,
    COLOR_WHITE: ANSI_WHITE,
    COLOR_GRAY: ANSI_WHITE,
}

# ansi_color = COLOR_TO_ANSI.get(color, ANSI_WHITE)
# print(f"{ansi_color}TEXT{ANSI_RESET}")

# =========================================================
# TERMINAL SYMBOLS - UNICODE
# =========================================================

SYMBOL_DRONE: str = "☠"

SYMBOL_START: str = "S ⚐"
SYMBOL_END: str = "E ⚑"

SYMBOL_NORMAL: str = "⛶"
SYMBOL_PRIORITY: str = "⚠"
SYMBOL_RESTRICTED: str = "⛞"
SYMBOL_BLOCKED: str = "⛌ ⛝ ⛔"

SYMBOL_CONNECTION: str = "→  ➤"

SYMBOL_WAIT: str = "W ❗"
SYMBOL_ERROR: str = "💀"
SYMBOL_SUCCESS: str = "✔ ✅"
