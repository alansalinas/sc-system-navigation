import pandas as pd
import sys
from geometry import (
    to_spherical,
    get_direction,
)
from utils import load_positions
from optimize import get_coords

positions = load_positions("maps/hurston_angle.pickle")


def command_get_coords(file):
    data = pd.read_csv(file).to_dict(orient="records")
    data = {item["ref"]: item["distance"] for item in data}
    pos = get_coords(positions)
    print("Coords", pos)


def command_get_orbital_vector(file_a, file_b):
    data_a = pd.read_csv(file_a).to_dict(orient="records")
    data_a = {item["ref"]: item["distance"] for item in data_a}
    data_b = pd.read_csv(file_b).to_dict(orient="records")
    data_b = {item["ref"]: item["distance"] for item in data_b}
    a = get_coords(positions, data_a)
    b = get_coords(positions, data_b)
    vector = to_spherical(get_direction(a, b), degree=True)
    print("Vector", vector)
    

def command_get_atmosphere_vector(file_a, file_b):
    data_a = pd.read_csv(file_a).to_dict(orient="records")
    data_a = {item["ref"]: item["distance"] for item in data_a}
    data_b = pd.read_csv(file_b).to_dict(orient="records")
    data_b = {item["ref"]: item["distance"] for item in data_b}


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "coords":
        file = sys.argv[2]
        command_get_coords(file)
    elif command == "orbital":
        file_a = sys.argv[2]
        file_b = sys.argv[3]
        command_get_orbital_vector(file_a, file_b)
