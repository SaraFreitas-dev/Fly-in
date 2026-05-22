from src.core.models import Zone, Connection
from src.render.constants import MOVEMENT_COSTS
import heapq


class PathFinderError(Exception):
    """Custom error class for the PathFinder class"""
    pass


class PathFinder():
    """
    Uses get_connected_zones to see the near connections / neighbors
    Uses BFS to find the shortest valid path
    between the start and end zones.
    Stores and returns discovered paths
    Returns the shortest one (valid path)
    To later be used on the Visualizer class
    """
    def __init__(self, zones: dict[str, Zone],
                 connections: list[Connection]) -> None:
        self.zones = zones
        self.connections = connections

    def build_connected_zones_map(self) -> dict[str, list[str]]:
        """
        Checks for each zone which paths it can take
        For example:
            hub: ["roof1", "corridorA"],
            roof1: ["hub", "roof2"]
        """
        connected_zones: dict[str, list[str]] = {}

        for connection in self.connections:
            zone_a, zone_b = connection.zone_a, connection.zone_b

            if zone_a not in connected_zones:
                connected_zones[zone_a] = []
            if zone_b not in connected_zones:
                connected_zones[zone_b] = []
            
            connected_zones[zone_a].append(zone_b)
            connected_zones[zone_b].append(zone_a)
            self.connected_zones = connected_zones
        return self.connected_zones
    
    def get_connected_zones(self, zone: str) -> list[str]:
        """
        Return all reachable zones connected to one zone meaning it
        Returns all its connected neighbors
        """
        if zone not in self.connected_zones:
            raise PathFinderError(f"The zone {zone} does not exist.")
        zone_lst: list[str] = []
        for value in self.connected_zones[zone]:
            zone_lst.append(value)
        return zone_lst

    def get_zone_cost(self, neighbor: str) -> int:
        """Checks the cost to move to the next zone"""
        if neighbor not in self.zones:
                raise PathFinderError(f"The zone {neighbor} does not exist.")
        neighbor_zone: Zone = self.zones[neighbor]
        return MOVEMENT_COSTS[neighbor_zone.zone_type]

    def dijkstra_shortest_path(self, start: str, end: str) -> dict[str, str]:
        """
        Calculate the shortest path from the start to the end zone
        taking into considerantion the least cost possible
        returns a dict of the directions taken (A -> B, B -> C, etc.)
        """
        try:
            queue: list[tuple[int, str]] = []  # stores future possible routes
            visited: set[str] = set()
            parent: dict[str, str] = {}  # stores the prev and current nodes
            costs: dict[str, int] = {}  # stores the cost of each neighbor for comparison

            heapq.heappush(queue, (0, start))

            costs[start] = 0
            while queue:
                current_cost, current_zone = heapq.heappop(queue)
                if current_zone in visited:
                    continue
                neighbors = self.get_connected_zones(current_zone)
                visited.add(current_zone)

                for neighbor in neighbors:
                    zone_object = self.zones[neighbor]
                    move_cost = MOVEMENT_COSTS[zone_object.zone_type]
                    new_cost = current_cost + move_cost

                    if (neighbor not in costs) or (new_cost < costs[neighbor]):
                        costs[neighbor] = new_cost
                        parent[neighbor] = current_zone
                        heapq.heappush(queue, (new_cost, neighbor))

                if current_zone == end:
                    break
                return parent
    
        except PathFinderError:
            raise PathFinderError("dijkstra_shortest_path error.")
            
