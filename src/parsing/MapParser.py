from src.core.models import Connection, Zone
from src.render.constants import (
    ZONE_DEFAULT,
    COLOR_DEFAULT,
    MAX_DRONES_DEFAULT,
    META_MAX_L_CAP_DEFAULT
)


class MapParserError(Exception):
    """Custom error class for parsing"""
    pass


class MapParser:
    """
        Parse the file, check for errors or missing types
        and convert them to the needed type
    """
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path
        self.nb_drones: int = 0
        self.start_zone: Zone | None = None
        self.end_zone: Zone | None = None
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []

    def validate_required_elements(self) -> None:
        """
        Check if all the mandatory keys are present and uncommented
        From the txt file (map)
        """
        if self.nb_drones <= 0:
            raise MapParserError("Missing nb_drones in the map file.")
        if not self.start_zone:
            raise MapParserError("Missing start_hub in the map file.")
        if not self.end_zone:
            raise MapParserError("Missing end_hub in the map file.")

    def parse_map(self) -> None:
        """
        Read and clean (extra spaces, lines that start with #, etc.)
        transform the values of the txt file
        """
        try:
            with open(self.file_path, "r") as file:
                for i, line in enumerate(file, start=1):
                    line = line.strip()

                    # Ignore empty lines and comments
                    if not line or line.startswith('#'):
                        continue

                    if ":" not in line:
                        raise MapParserError(f"Invalid format on line {i}.")

                    # Identify line type
                    if line.startswith("nb_drones:"):
                        self.parse_nb_drones(line)

                    elif (
                        line.startswith("start_hub:")
                        or line.startswith("end_hub:")
                        or line.startswith("hub:")
                    ):
                        self.parse_zone(line)

                    elif line.startswith("connection:"):
                        self.parse_connection(line)

                    else:
                        raise MapParserError(f"Parsing error on line {i}")
            self.validate_required_elements()
        except FileNotFoundError:
            raise MapParserError(f"File '{self.file_path}' was not found.")

    def parse_nb_drones(self, line: str) -> None:
        """
        Parse the number of drones from the map file.
        Validate that:
        - the value exists, is a valid integer and is greater than 0
        """
        if self.nb_drones > 0:
            raise MapParserError("Duplicate nb_drones definition.")

        _, value = line.split(':', 1)  # maxsplit=1
        value = value.strip()
        try:
            nb_drones = int(value)

            if nb_drones <= 0:
                raise MapParserError("nb_drones must be a positive integer.")
            self.nb_drones = nb_drones

        except ValueError:
            raise MapParserError("nb_drones must be an integer.")

    def parse_zone(self, line: str) -> None:
        """
        Parse a zone definition from the map file:
        "hub:" / "start_hub" / "end_hub".
        Validate that:
        - the zone format is correct
        - the zone name is unique
        - the coordinates are valid integers
        - the coordinates are not duplicated
        """
        key, value = line.split(':', 1)  # maxsplit=1
        value = value.strip()

        metadata_dict: dict[str, str] = {}

        if '[' in value:
            main_data, metadata = value.split('[', 1)
            metadata = metadata.replace("]", "")
            metadata_dict = self.parse_metadata(metadata)
        else:
            main_data = value

        try:
            main_data_v = main_data.split()

            if len(main_data_v) != 3:
                raise MapParserError(f"Missing required values for {key}.")

            name, x, y = main_data_v
            x = int(x)
            y = int(y)

            # DUPLICATE NAME
            if name in self.zones:
                raise MapParserError(f"{name} name is duplicated.")

            # DUPLICATE COORDS
            for zone in self.zones.values():
                if zone.x == x and zone.y == y:
                    raise MapParserError("Duplicated coordinates "
                                         f"({x}, {y}).")

            # CREATE ZONE
            # Check for the presence of metadata, else use the default values
            zone_type = metadata_dict.get("zone", ZONE_DEFAULT)
            color = metadata_dict.get("color", COLOR_DEFAULT)
            max_drones = metadata_dict.get("max_drones", MAX_DRONES_DEFAULT)
            zone = Zone(name, x, y, zone_type, color, max_drones)

            # START / END

            if key == "start_hub":
                if self.start_zone is not None:
                    raise MapParserError("Duplicate start_hub definition.")
                self.start_zone = zone

            elif key == "end_hub":
                if self.end_zone is not None:
                    raise MapParserError("Duplicate end_hub definition.")
                self.end_zone = zone

            # STORE
            self.zones[name] = zone

        except ValueError:
            raise MapParserError(f"Invalid coordinates in {key} '{name}'.")

    def parse_connection(self, line: str) -> None:
        """
        Parse a connection between two zones.
        Validate that:
        - the connection format is valid
        - both zones exist
        - self-connections are not allowed
        - duplicate connections are not created
        """
        _, value = line.split(':', 1)  # maxsplit=1
        value = value.strip()

        metadata_dict: dict[str, str] = {}

        if '[' in value:
            c_data, metadata = value.split('[', 1)
            metadata = metadata.replace("]", "")
            metadata_dict = self.parse_metadata(metadata)
        else:
            c_data = value

        c_data = c_data.split('-')

        # ZONE AMOUNT
        if len(c_data) != 2:
            raise MapParserError("Each connection must have "
                                 "exactly two zones.")
        zone_a, zone_b = c_data
        zone_a, zone_b = zone_a.strip(), zone_b.strip()

        # SELF CONNECTION
        if zone_a == zone_b:
            raise MapParserError("Self-connections are "
                                 f"not allowed: '{zone_a}'.")

        # UNKNOWN ZONES
        if zone_a not in self.zones:
            raise MapParserError(f"Unknown zone '{zone_a}'.")
        if zone_b not in self.zones:
            raise MapParserError(f"Unknown zone '{zone_b}'.")

        # DUPLICATE CONNECTIONS
        new_connection = sorted([zone_a, zone_b])

        for connection in self.connections:
            existing = sorted([
                connection.zone_a,
                connection.zone_b
            ])
            if existing == new_connection:
                raise MapParserError(
                    f"Duplicate connection '{zone_a}-{zone_b}'.")

        # Check for the presence of max_link_capacity
        # If not, use the default value 1
        max_link_capacity = int(metadata_dict.get("max_link_capacity",
                                                  META_MAX_L_CAP_DEFAULT))
        if max_link_capacity <= 0:
            raise MapParserError("max_link_capacity must be a "
                                 "positive integer.")
        connection = Connection(zone_a, zone_b, max_link_capacity)
        self.connections.append(connection)

    def parse_metadata(self, line: str) -> dict[str, str | int]:
        """
        Parse metadata and special commands from the map file.
        """
        clean_line = line.split(' ')
        metadata_dict: dict[str, str] = {}

        try:
            for c in clean_line:
                key, value = c.split('=')
                metadata_dict[key] = value
            return metadata_dict

        except Exception as e:
            raise MapParserError(f"parse_metadata() failed at {e}")
