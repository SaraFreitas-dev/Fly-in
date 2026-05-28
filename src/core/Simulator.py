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
        self.pathfinder.build_connected_zones_map()

        self.drones: list[Drone] = []
        self.current_turn: int = 0
        self.occupied_zones: dict[str, list[Drone]] = {}
        self.occupied_links: dict[str, tuple[str, str], list[Drone]] = {}

    def create_drones(self) -> list[Drone]:
        """
        Generate an id for each drone based
        on the total drone amount
        """
        for i in range(self.nb_drones):
            drone_id = "D" + str(i + 1)
            drone = Drone(drone_id, self.start_zone.name, self.end_zone.name)
            self.drones.append(drone)
        return self.drones
    
    def can_move_to_zone(self, next_zone: str) -> bool:
        """Check if the zone is occupied"""
        zone_object = self.zones[next_zone]
        drones_in_zone = self.occupied_zones.get(next_zone, [])

        if next_zone != self.end_zone.name:
            if len(drones_in_zone) >= zone_object.max_drones:
                return False
        return True
    
    def can_use_link(self, current_zone: str,
                     next_zone: str) -> bool:
        """Check if the connection can be used"""
        link_name = tuple(sorted([current_zone, next_zone]))
        for connection in self.connections:
            connection_link = tuple(
                sorted([connection.zone_a, connection.zone_b]))
            if connection_link == link_name:
                drones_in_link = self.occupied_links.get(link_name, [])
                if len(drones_in_link) >= connection.max_link_capacity:
                    return False
        return True
    
    def handle_waiting(self, drone: Drone) -> bool:
        """Checks if the drone must wait a turn"""
        if drone.waiting_turns > 0:
            print(f"{drone.drone_id} waiting...")
            drone.waiting_turns -= 1
            return True
        return False
    
    def move_drone(self, drone: Drone,
                   next_zone: str) -> None:
        """
        Moves the drone to the next zone
        and updates occupancy states
        """
        # Free previous occupied zone
        if drone.current_zone in self.occupied_zones:
            self.occupied_zones[drone.current_zone].remove(drone)
            if not self.occupied_zones[drone.current_zone]:
                self.occupied_zones.pop(drone.current_zone)

        # Occupy the connection link
        link = tuple(sorted([drone.current_zone, next_zone]))

        if link not in self.occupied_links:
            self.occupied_links[link] = []

        self.occupied_links[link].append(drone)
    
        # Move the drone forward in the path
        drone.current_zone = next_zone

        if next_zone != self.end_zone.name:
            if next_zone not in self.occupied_zones:
                self.occupied_zones[next_zone] = []
            self.occupied_zones[next_zone].append(drone)
        
        # Free previous connection link
        self.occupied_links[link].remove(drone)
        if not self.occupied_links[link]:
            self.occupied_links.pop(link)
    
    def simulate_turns(self) -> dict[int, list[str]]:
        """
        Calls all previous functions and
        Simulates turns for each drone
        Until all are delivered to the end_zone
        """
        simul_result: dict[int, list[str]] = {}

        while not all(drone.delivered for drone in self.drones):
            self.current_turn += 1
            current_turn_moves: list[str] = []

            for drone in self.drones:
                # Check if the drone is delivered
                if drone.delivered:
                    continue
                if drone.current_zone == self.end_zone.name:
                    drone.delivered = True
                    continue
                drone.path = self.pathfinder.dijkstra_shortest_path(
                    drone.current_zone,
                    self.end_zone.name,
                    self.occupied_zones
                )

                if len(drone.path) < 2:
                    drone.delivered = True
                    continue

                next_zone = drone.path[1]

                # Check if the drone must wait
                if self.handle_waiting(drone):
                    continue

                # Check if the zone is occupied
                # And the connection link available
                if not self.can_move_to_zone(next_zone):
                    continue
                if not self.can_use_link(drone.current_zone,
                                         next_zone):
                    continue

                zone_object = self.zones[next_zone]
                if zone_object.zone_type == "restricted":
                    drone.waiting_turns = 1

                self.move_drone(drone, next_zone)

                # ADD movement string to current_turn_moves
                current_turn_moves.append(f"{drone.drone_id}-{next_zone}")

            # ADD each turn into the result
            if current_turn_moves:
                simul_result[self.current_turn] = current_turn_moves
        return simul_result
