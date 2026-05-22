from src.core.PathFinder import PathFinder
from src.core.models import Drone
from src.parsing.MapParser import MapParser


class Simulator:
    """Run the simulation based on the map provided"""
    def __init__(self, parser: MapParser) -> None:
        self.parser = parser

        self.zones = parser.zones
        self.connections = parser.connections
        self.start_zone = parser.start_zone
        self.end_zone = parser.end_zone
        self.nb_drones = parser.nb_drones

        self.pathfinder = PathFinder(
            self.zones,
            self.connections
        )

        self.drones: list[Drone] = []
        self.current_turn: int = 0
        self.occupied_zones: dict[str, Drone] = {}

    def create_drones(self) -> list[Drone]:
        """
        Generate an id for each drone based
        on the total drone amount
        """
        for i in range(self.nb_drones):
            drone_id = i + 1
            drone = Drone(drone_id, self.start_zone.name, self.end_zone.name)
            self.drones.append(drone)
        return self.drones

