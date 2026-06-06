from src.core.models import Zone, Connection
from src.core.models import Drone
from src.render.constants import MOVEMENT_COSTS
import heapq


class PathFinderError(Exception):
    """Custom error class for the PathFinder class"""
    pass


class PathFinder():
    """
    Uses get_connected_zones to see the near connections / neighbors
    Uses Dijkstra to find the shortest valid path
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

    def dijkstra_shortest_path(self, start: str, end: str,
                               occupied_zones: dict[str, list[Drone]]
                               ) -> list[str]:
        """
        Calculate the shortest path from the start to the end zone
        taking into considerantion the least cost possible
        and the priority zones
        Reverses the path (start to end)
        returns a list of the directions taken (A -> B, B -> C, etc.)
        """
        try:
            queue: list[tuple[int, str]] = []  # stores future possible routes
            visited: set[str] = set()
            parent: dict[str, str] = {}  # stores the prev and current nodes
            costs: dict[str, int] = {}  # cost of each neighbor for comparison

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
                    drones_in_zone = len(
                        occupied_zones.get(neighbor, []))
                    move_cost = (MOVEMENT_COSTS[zone_object.zone_type] +
                                 drones_in_zone)
                    new_cost = current_cost + move_cost

                    # Ignore blocked zones
                    if zone_object.zone_type == "blocked":
                        continue

                    # Better route found
                    if (
                        (neighbor not in costs)
                        or
                        (new_cost < costs[neighbor])
                    ):
                        costs[neighbor] = new_cost
                        parent[neighbor] = current_zone
                        heapq.heappush(queue, (new_cost, neighbor))

                    # Same cost but priority zone preferred
                    elif (
                        new_cost == costs[neighbor]
                        and
                        zone_object.zone_type == "priority"
                    ):
                        parent[neighbor] = current_zone
                        heapq.heappush(queue, (new_cost, neighbor))

                if current_zone == end:
                    break
            return self.reconstruct_path(parent, start, end)

        except PathFinderError as e:
            raise PathFinderError(f"dijkstra_shortest_path error: {e}.")

    @staticmethod
    def reconstruct_path(parent: dict[str, str],
                         start: str, end: str) -> list[str]:
        """Reconstruct the path (revert it from start to end)"""
        try:
            current = end
            path: list[str] = []

            if end == start:
                return [start]

            while current != start:
                path.append(current)
                current = parent[current]

            path.append(start)
            # Get the result from the start to the exit point
            path.reverse()
            return path
        except (KeyError, ValueError):
            return []
