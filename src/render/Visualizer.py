import os
from src.core.Simulator import Simulator
from src.render.constants import (SYMBOL_PRIORITY,
                                  SYMBOL_RESTRICTED,
                                  SYMBOL_BLOCKED, SYMBOL_NORMAL,
                                  ANSI_COLORS, COLOR_DEFAULT,
                                  ANSI_RESET, ANSI_BOLD, ANSI_BLACK,
                                  SYMBOL_DRONE, SYMBOL_CONNECTION,
                                  SYMBOL_END, TURN_LIMITS)


class Visualizer:
    """
    Prints the simulation, turn by turn,
    Adding the corresponding colors (if given on the txt file)
    """
    def __init__(self, simulator: Simulator) -> None:
        self.simulator = simulator
        self.zones = simulator.zones
        self.connections = simulator.connections
        self.drones = simulator.create_drones()
        self.simul_result = simulator.simulate_turns()
        self.parser = simulator.parser

    def get_zone_symbol(self, zone: str) -> str:
        """Get the zone symbols from constants.py"""
        if zone.name == self.simulator.end_zone.name:
            return SYMBOL_END
        if zone.zone_type == "priority":
            return SYMBOL_PRIORITY
        if zone.zone_type == "restricted":
            return SYMBOL_RESTRICTED
        if zone.zone_type == "blocked":
            return SYMBOL_BLOCKED
        return SYMBOL_NORMAL
    
    def color_text(self, text: str, color: str) -> str:
        """
        Use the color requested on the txt file
        To print on the terminal
        If none is given, use the default one
        """
        ansi_color = ANSI_COLORS.get(color, COLOR_DEFAULT)
        return f"{ansi_color}{text}{ANSI_RESET}"

    def print_simulation(self) -> None:
        print(f"\n{ANSI_BOLD}══════════════════════════════════════\n"
              "       FLY-IN DRONE SIMULATION\n"
              f"══════════════════════════════════════{ANSI_RESET}")
        for turn, moves in self.simul_result.items():
            print(f"\n\033[44mTurn {turn}{ANSI_RESET}")
            for move in moves:
                drone_id, zone_name = move.split("-")
                zone = self.zones[zone_name]
                colored_zone = self.color_text(zone_name, zone.color)
                zone_symbol = self.get_zone_symbol(zone)
                print(
                f"{SYMBOL_DRONE} "
                f"{drone_id} "
                f"{SYMBOL_CONNECTION} "
                f"{colored_zone}",
                f"{zone_symbol}"
            )
        self.print_exit_report()
    
    def print_exit_report(self) -> None:
        """
        Prints the exit banner with the info
        of how many turns the simulation made, the
        amount of drones, etc.
        """
        path = self.parser.file_path
        file_name = os.path.basename(path).split(".txt")[0]
        folder_name = os.path.basename(os.path.dirname(path))
        total_turns = len(self.simul_result)
        max_turns_allowed = TURN_LIMITS[folder_name][file_name]

        print("\n═════════════════════════════════════════\n"
              f"{ANSI_BOLD} 📌 FLY-IN DRONE SIMULATION REPORT 📌{ANSI_RESET}\n\n"
              f" {ANSI_BLACK}Level: {folder_name}\n"
              f" The path: {file_name}\n"
              " Max turns allowed to hit the target: "
              f"{max_turns_allowed}\n\n{ANSI_RESET}"
              f" There where a total of {len(self.drones)} drones\n"
              f" The simulation did a total of {total_turns} turns\n"
              f"═════════════════════════════════════════\n")
