import os
from PIL import Image, ImageDraw, ImageFont
from src.core.Simulator import Simulator
from src.render.constants import (PIL_COLORS, PIL_SYMBOLS)
from src.render.constants import TURN_LIMITS

IMG_WIDTH = 1400
IMG_HEIGHT = 900
REPORT_HEIGHT = 150


class ImageGenerator:
    """
    This class uses Pillow to convert
    each turn on the simulation into a single frame
    Then, converts the full simulation frames
    into a gif for animation - All stores in assets/img
    """
    def __init__(self, simulator: Simulator) -> None:
        self.drones = simulator.drones
        self.nb_drones = simulator.nb_drones
        self.zones = simulator.zones
        self.connections = simulator.connections
        self.start = simulator.start_zone
        self.end = simulator.end_zone
        self.simul_res = simulator.simulate_turns()
        self.turn_states = simulator.turn_states

        self.map_name = os.path.splitext(
            os.path.basename(simulator.parser.file_path))[0]
        self.folder_name = os.path.basename(
            os.path.dirname(simulator.parser.file_path))
        
    def get_scale(self) -> tuple[float, int, int, int, int]:
        """
        Get the correct scale,
        to be able to fit all zones into the frame
        """
        min_x = min(zone.x for zone in self.zones.values())
        max_x = max(zone.x for zone in self.zones.values())

        min_y = min(zone.y for zone in self.zones.values())
        max_y = max(zone.y for zone in self.zones.values())

        width = max(max_x - min_x, 1)
        height = max(max_y - min_y, 1)

        scale_x = (IMG_WIDTH - 200) / width
        scale_y = (IMG_HEIGHT - REPORT_HEIGHT - 100) / height

        scale = min(scale_x, scale_y)

        return scale, min_x, max_x, min_y, max_y

    def draw_title(self, draw: ImageDraw) -> None:
        """Show a simple title of the project"""
        title_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            24)
        title = "FLY-IN SIMULATION"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = bbox[2] - bbox[0]
        
        draw.text(((IMG_WIDTH - title_width) / 2, 20),
                  title,
                  fill="white",
                  font=title_font)
        draw.line([(100, 40), (500, 40)],
                  fill=(80, 80, 80),
                  width=1)
        draw.line([(900, 40), (1300, 40)],
                  fill=(80, 80, 80),
                  width=1)

    def draw_card(self,
                  draw: ImageDraw,
                  x: int, y: int,
                  width: int, height: int,
                  title: str, value: int | str,
                  title_font: ImageFont,
                  value_font: ImageFont):
        draw.rounded_rectangle((x, y,
                                x + width, y + height),
                                radius=10,
                                outline=(80, 80, 80),
                                width=2)
        draw.text((x + 15, y + 12),
                title,
                fill=(180, 180, 180),
                font=title_font)

        draw.text((x + 15, y + 50),
                str(value),
                fill="white",
                font=value_font)

    def draw_report(self, draw: ImageDraw, state: dict[str, int]) -> None:
        """
        Shows the simulation report banner
        With info such as number of turns and status
        """
        draw.rectangle((0,
                        IMG_HEIGHT - REPORT_HEIGHT,
                        IMG_WIDTH,
                        IMG_HEIGHT),
                        fill=(20, 20, 20))
        padding = 20
        gap = 20

        available_width = IMG_WIDTH - (padding * 2)
        card_width = int((available_width - gap * 3) / 4)
        card_height = REPORT_HEIGHT - 40
        card_y = IMG_HEIGHT - REPORT_HEIGHT + 20

        drones_delivered = state.get(self.end.name, 0)
        max_turns_allowed = TURN_LIMITS[self.folder_name][self.map_name]

        cards = [
            ("LEVEL", self.folder_name),
            ("MAP", self.map_name),
            ("DRONES DELIVERED", f"{drones_delivered} / {self.nb_drones}"),
            ("TURNS", f"{len(self.simul_res)} / {max_turns_allowed} MAX"),]

        title_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            12)

        value_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            18)

        for i, (title, value) in enumerate(cards):
            x = padding + i * (card_width + gap)

            self.draw_card(
                draw, x, card_y,
                card_width, card_height,
                title, value,
                title_font, value_font
            )
    
    def draw_drones(self, draw: ImageDraw,
                    drone_count: int,
                    radius: int, x: int, y: int) -> None:
        """
        For each zone that has at least 1 drone,
        draw the drone amount on the corresponding circle
        """
        if drone_count > 0:
            count_font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                radius)
            text = str(drone_count)

            bbox = draw.textbbox(
                (0, 0),
                text,
                font=count_font)

            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            draw.text((x - text_width / 2,
                       y - text_height / 2),
                       text,
                       fill="black",
                       font=count_font)

    def draw_all(self) -> None:
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
        offset_y = (IMG_HEIGHT - REPORT_HEIGHT - map_height) / 2    

        for turn, state in self.turn_states.items():
            # Create the frame base
            img = Image.new(
                "RGB",(1400, 900), (25, 25, 35)
            )
            draw = ImageDraw.Draw(img)

            # Title
            self.draw_title(draw)

            # Report banner
            self.draw_report(draw, state)

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

                # Lines - connections
                draw.line([start_point, end_point], fill=(180, 180, 180), width=4)

            # Draw zones
            for zone in self.zones.values():
                zone_symbols = PIL_SYMBOLS.get(zone.zone_type, "X")
                x = (zone.x - min_x) * scale + offset_x
                y = (zone.y - min_y) * scale + offset_y

                # Circles - zones
                zone_count = len(self.zones)
                if zone_count <= 10:
                    radius = 35
                elif zone_count <= 25:
                    radius = 25
                else:
                    radius = 15

                draw.ellipse(
                    (x - radius, y - radius,
                    x + radius, y + radius),
                    fill=PIL_COLORS.get(zone.color, "white"),
                    outline="white",
                    width=3
                )

                # Zone names and their types
                font_size = max(
                    12,
                    min(20, int(radius * 0.6)))
                font = ImageFont.truetype(
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                    font_size)

                if zone_count <= 15:
                    label = f"[{zone_symbols}] {zone.name}"
                elif zone_count <= 30:
                    label = f"[{zone_symbols}] {zone.name[:8]}..."
                else:
                    label = f"[{zone_symbols}]"

                bbox = draw.textbbox((0, 0), label, font=font)
                text_width = bbox[2] - bbox[0]

                if zone == self.start or zone == self.end:
                    color = "green"
                else:
                    color = "white"
                draw.text(
                    (x - text_width / 2, y - radius - 30),
                    label,
                    fill=color,
                    font=font
                )

                # Draw drones per turn
                drone_count = state.get(zone.name, 0)
                self.draw_drones(draw,
                                drone_count,
                                radius,
                                x, y)
                
            
            self.save_frames(img, f"frame_{turn:03d}")

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
