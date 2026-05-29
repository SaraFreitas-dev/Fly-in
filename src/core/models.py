from src.render.constants import (
    ZONE_DEFAULT,
    COLOR_DEFAULT,
    MAX_DRONES_DEFAULT,
    META_MAX_L_CAP_DEFAULT
)


class Zone:
    """
    Receive the names and types from each zone
    from the txt file (after parsing)
    """
    def __init__(self, name: str,
                 x: int, y: int,
                 zone_type: str = ZONE_DEFAULT,
                 color: str = COLOR_DEFAULT,
                 max_drones: int = MAX_DRONES_DEFAULT) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type  # Default is normal
        self.color = color  # Default is white
        self.max_drones = max_drones  # Default is 1


class Connection:
    """
    Connections are defined using connection:
    <name1>-<name2> [metadata]
    Defines a bidirectional connection (edge) between two zones.
    """
    def __init__(self, zone_a: str, zone_b: str,
                 max_link_capacity: int = META_MAX_L_CAP_DEFAULT) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity  # default is 1


class Drone:
    """Represents one drone moving through the map"""
    def __init__(
        self,
        drone_id: str,
        start_zone: str,
        end_zone: str
    ) -> None:

        self.drone_id = drone_id
        self.start_zone = start_zone
        self.end_zone = end_zone
        self.current_zone = start_zone
        self.path: list[str] = []
        self.waiting_turns: int = 0
        self.delivered: bool = False
