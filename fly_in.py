import sys
import traceback
from src.parsing.MapParser import MapParser
from src.render.Visualizer import Visualizer
from src.core.Simulator import Simulator
from src.render.ImageGenerator import ImageGenerator


def fly_in() -> None:
    """Main function to call at main, run the program"""
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        print("No .txt file provided.\n"
              "Run the program with one of the following commands:\n"
              "-> python3 fly_in.py <map_path>.<map_name>\n"
              "-> Add the <map_name> on the Makefile and type make run\n")

    try:
        parser = MapParser(file_path)
        parser.parse_map()

        simul = Simulator(parser)

        visualizer = Visualizer(simul)
        visualizer.print_simulation()

        imagegen = ImageGenerator(simul)
        imagegen.draw_zones()

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        print(f"Failed on the function: {tb[-1].name}")
        print(f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    fly_in()
