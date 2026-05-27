import sys
import traceback
from src.parsing.MapParser import MapParser
from src.core.PathFinder import PathFinder
from src.core.Simulator import Simulator


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

        simul.create_drones()
        simul.assign_paths()

        sim_result = simul.simulate_turns()

        for turn, moves in sim_result.items():
            print(f"Turn {turn}")
            print(" ".join(moves))

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        print(f"Failed on the function: {tb[-1].name}")
        print(f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    fly_in()
