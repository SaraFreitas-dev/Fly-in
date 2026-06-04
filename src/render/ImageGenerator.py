import os
from PIL import Image, ImageDraw, ImageFont
from src.core.Simulator import Simulator
from src.render.constants import (PIL_COLORS, PIL_SYMBOLS)

IMG_WIDTH = 1400
IMG_HEIGHT = 900


class ImageGenerator:
    """
    This class uses Pillow to convert
    each turn on the simulation into a single frame
    Then, converts the full simulation frames
    into a gif for animation - All stores in assets/img
    """
    def __init__(self, simulator: Simulator) -> None:
        self.zones = simulator.zones
        self.connections = simulator.connections
        self.start = simulator.start_zone
        self.end = simulator.end_zone
        self.simul_res = simulator.simulate_turns()
        
    def get_scale(self) -> tuple[float, int, int, int, int]:
        """
        Get the correct scale,
        to be able to fit all zones into the frame
        """
        min_x = min(zone.x for zone in self.zones.values())
        max_x = max(zone.x for zone in self.zones.values())

        min_y = min(zone.y for zone in self.zones.values())
        max_y = max(zone.y for zone in self.zones.values())

        scale_x = (IMG_WIDTH - 200) / (max_x - min_x)
        scale_y = (IMG_HEIGHT - 200) / (max_y - min_y)
        scale = min(scale_x, scale_y)

        return scale, min_x, max_x, min_y, max_y


    def draw_zones(self) -> None:
        """
        Draw the basics of the frame:
        Zones, Connections as well as their
        description, zone types and names
        """
        # Scale and offset values
        scale, min_x, max_x, min_y, max_y = self.get_scale()
        map_width = (max_x - min_x) * scale
        map_height = (max_y - min_y) * scale
        offset_x = (IMG_WIDTH - map_width) / 2
        offset_y = (IMG_HEIGHT - map_height) / 2    

        # Create the frame base
        img = Image.new(
            "RGB", (1400, 900), (50, 50, 50)
        )
        draw = ImageDraw.Draw(img)

        # Draw connections
        for connection in self.connections:
            zone_a, zone_b = connection.zone_a, connection.zone_b
            zone_a_obj = self.zones[zone_a]
            zone_b_obj = self.zones[zone_b]

            a_x = (zone_a_obj.x - min_x) * scale + offset_x
            b_x = (zone_b_obj.x - min_x) * scale + offset_x
            a_y = (zone_a_obj.y - min_y) * scale + offset_y
            b_y = (zone_b_obj.y - min_y) * scale + offset_y

            start_point = (a_x, a_y)
            end_point = (b_x, b_y)
            draw.line([start_point, end_point], fill="white", width=4)

        # Draw zones
        for zone in self.zones.values():
            zone_symbols = PIL_SYMBOLS.get(zone.zone_type, "X")
            x = (zone.x - min_x) * scale + offset_x
            y = (zone.y - min_y) * scale + offset_y
            draw.ellipse(
                (x - 25, y - 25, x + 25, y + 25),
                fill=PIL_COLORS.get(zone.color, "white")
            )
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
            draw.text(
                (x - 20, y + 30),
                (f"[{zone_symbols}] {zone.name}"),
                fill="black",
                font=font
            )
        
        self.save_frames(img, f"frame")

    def save_frames(self, img: Image, frame_n: str) -> None:
        """
        Checks if the img folder already exists
        on assets, generates and stores each frame
        """
        os.makedirs(
            "assets/frames",
            exist_ok=True
        )
        img.save(f"assets/frames/{frame_n}.png")
