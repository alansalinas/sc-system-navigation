import pandas as pd
import sys
from geometry import (
    to_spherical,
    get_direction,
    radians_to_degrees,
    euclidean_distance
)
from utils import load_positions
from optimize import get_coords
from planetary import get_atmosphere_vector, get_planetary_coords, get_xyz_vectors
from survey_data.hurston import refs


data = load_positions("maps/hurston.pickle")
positions = data["positions"]
centroid = data["planet"]["centroid"]
radius = data["planet"]["radius"]
north_vector = data["planet"]["north_vector"]
prime_meridian = data["planet"]["prime_meridian"]
parallel_zero = data["planet"]["parallel_zero"]


def command_get_coords(file):
    data = pd.read_csv(file).to_dict(orient="records")
    data = {item["ref"]: item["distance"] for item in data}
    pos = get_coords(positions, data)
    print("Coords", pos)


def command_get_pos_ref(ref):
    print("North", north_vector)
    print(ref, positions[ref])
    print("center", centroid)


def command_get_planetary_coords(file):
    data = pd.read_csv(file).to_dict(orient="records")
    data = {item["ref"]: item["distance"] for item in data}
    pos = get_coords(positions, data)
    coords = get_planetary_coords(pos, centroid, radius, north_vector, prime_meridian, parallel_zero)
    print("Planetary coords")
    print("Longitude:", radians_to_degrees(coords[1]))
    print("Latitude:", radians_to_degrees(coords[2]))
    print("Altitude", coords[0])


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
    pos_a = get_coords(positions, data_a)
    coords_a = get_planetary_coords(pos_a, centroid, radius, north_vector, prime_meridian, parallel_zero)
    pos_b = get_coords(positions, data_b)
    coords_b = get_planetary_coords(pos_b, centroid, radius, north_vector, prime_meridian, parallel_zero)
    vector = get_atmosphere_vector(
        coords_a,
        coords_b,
        radius,
    )
    print("Vector")
    print("Distance:", vector[0])
    print("Heading:", vector[1])
    print("Pitch:", vector[2])


def command_get_nearest_ref(file):
    data = pd.read_csv(file).to_dict(orient="records")
    data = {item["ref"]: item["distance"] for item in data}
    pos = get_coords(positions, data)
    best_dist = 1e6
    for ref in refs:
        dist = abs(euclidean_distance(pos, positions[ref]))
        if dist < best_dist:
            best_dist = dist
            om = ref
    print("Nearest:", om)
    print("Dist", best_dist)
    

def command_write_positions():
    records = list()
    for ref in positions:
        pos = positions[ref]
        r = {
            "ref": ref,
            "x": pos[0],
            "y": pos[1],
            "z": pos[2]
        }
        records.append(r)
    df = pd.DataFrame(records)
    df.to_csv("hurston.csv", index=False)
    
    
def command_planet_data():
    x_vector, y_vector, z_vector = get_xyz_vectors(north_vector, prime_meridian, parallel_zero)
    data = [
        ["radius", radius, 0, 0],
        ["centroid", centroid[0], centroid[1], centroid[2]],
        ["north_vector", north_vector[0], north_vector[1], north_vector[2]],
        ["prime_meridian", prime_meridian[0], prime_meridian[1], prime_meridian[2]],
        ["parallel_zero", parallel_zero[0], parallel_zero[1], parallel_zero[2]],
        ["x_vector", x_vector[0], x_vector[1], x_vector[2]],
        ["y_vector", y_vector[0], y_vector[1], y_vector[2]],
        ["z_vector", z_vector[0], z_vector[1], z_vector[2]],
    ]
    df = pd.DataFrame(data)
    df.to_csv("hurston_data.csv", index=None, header=None)


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "coords":
        file = sys.argv[2]
        command_get_coords(file)
    elif command == "orbital":
        file_a = sys.argv[2]
        file_b = sys.argv[3]
        command_get_orbital_vector(file_a, file_b)
    elif command == "atmo":
        file_a = sys.argv[2]
        file_b = sys.argv[3]
        command_get_atmosphere_vector(file_a, file_b)
    elif command == "pcoords":
        file = sys.argv[2]
        command_get_planetary_coords(file)
    elif command == "nearest":
        file = sys.argv[2]
        command_get_nearest_ref(file)
    elif command == "write":
        command_write_positions()
    elif command == "data":
        command_planet_data()
