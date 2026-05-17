from src.render.constants import COLOR_DEFAULT


class Zone:
    """
    Receive the names and types from each zone
    from the txt file (after parsing)
    """
    def __init__(self, name: str,
                 x: int, y: int,
                 zone_type: str = "normal",
                 color: str = COLOR_DEFAULT,
                 max_drones: int = 1) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones  # default is 1


class Connection:
    """
    Connections are defined using connection:
    <name1>-<name2> [metadata]
    Defines a bidirectional connection (edge) between two zones.
    """
    def __init__(self, zone_a: str, zone_b: str,
                 max_link_capacity: int = 1) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity  # default is 1


class Drone:
    pass
