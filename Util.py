import math
import sys
import os

cwd = os.getcwd()
sys.path.insert(0, os.path.join(cwd, "..", "classes"))

def calculate_distance(location_1, location_2):
    try:
        x1, y1, z1 = (
            round(location_1["x"], 4),
            round(location_1["y"], 4),
            round(location_1["z"], 4),
        )
        x2, y2, z2 = (
            round(location_2["x"], 4),
            round(location_2["y"], 4),
            round(location_2["z"], 4),
        )
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    except OverflowError:
        print("Numerical result out of range")
        return None
    return distance


def calculate_distance_2D(location_1, location_2):
    x1, y1 = location_1["x"], location_1["y"]
    x2, y2 = location_2["x"], location_2["y"]
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


