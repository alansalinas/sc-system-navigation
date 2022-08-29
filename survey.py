import sys
import importlib
import numpy as np
import pandas as pd
from optimize import optimize_distances, optimize_angles, find_planet_centroid, get_coords
from utils import load_positions, save_positions, validate
from planetary import get_planet_vectors, get_xyz_vectors

refs = None
orbital_refs = None
distances = None
headings = None
pitches = None
origin = None
north = None
radius = None


def load_survey_data(planet):
    global refs
    global orbital_refs
    global distances
    global headings
    global pitches
    global origin
    global north
    global radius
    planet = importlib.import_module(f"survey_data.{planet}")
    refs = planet.refs
    orbital_refs = planet.orbital_refs
    distances = planet.distances
    headings = planet.headings
    pitches = planet.pitches
    origin = planet.origin
    north = planet.north
    radius = planet.radius
    return True


def initialize_positions():
    positions = {
        ref: (np.random.rand(3) * 10).astype(np.longdouble)
        for ref in refs[1:]
    }
    positions[refs[0]] = np.array([0, 0, 0])
    return positions


def command_distances(planet, n, seed):
    load_survey_data(planet)
    np.random.seed(seed)
    positions = initialize_positions()
    dist_err, angle_err = validate(positions, distances, headings, pitches)
    print(f"Initialized -- Distance error: {dist_err} -- Angle error: {angle_err}")
    optimize_distances(positions, distances, origin, n)
    dist_err, angle_err = validate(positions, distances, headings, pitches, True)
    print(f"Distance optimized -- Distance error: {dist_err} -- Angle error: {angle_err}")
    save_positions(positions, f"maps/{planet}_distance.pickle")
    return positions


def command_angles(planet, n):
    load_survey_data(planet)
    positions = load_positions(f"maps/{planet}_distance.pickle")
    dist_err, angle_err = validate(positions, distances, headings, pitches)
    print(f"Initials -- Distance error: {dist_err} -- Angle error: {angle_err}")
    optimize_angles(positions, distances, headings, pitches, origin, n)
    dist_err, angle_err = validate(positions, distances, headings, pitches, True)
    print(f"Angle optimized -- Distance error: {dist_err} -- Angle error: {angle_err}")
    save_positions(positions, f"maps/{planet}_angle.pickle")
    return positions


def command_add_planet_data(planet):
    load_survey_data(planet)
    positions = load_positions(f"maps/{planet}_angle.pickle")
    # Get planet's center
    centroid = find_planet_centroid(10000, orbital_refs, positions)
    print("Found planetary center:", centroid)
    print("Defined planetary radius:", radius)
    # Get north position
    north_pos = get_coords(positions, north)
    print("North position:", north_pos)
    # Get planet vectors
    north_vector, prime_meridian, parallel_zero = get_planet_vectors(north_pos, centroid)
    print("North vector:", north_vector)
    x_vector, y_vector, z_vector = get_xyz_vectors(north_vector, prime_meridian, parallel_zero)

    data = {
        "positions": positions,
        "planet": {
            "centroid": centroid,
            "radius": radius,
            "north_vector": north_vector,
            "prime_meridian": prime_meridian,
            "parallel_zero": parallel_zero,
            "x_vector": x_vector,
            "y_vector": y_vector,
            "z_vector": z_vector,
        }
    }
    save_positions(data, f"maps/{planet}.pickle")


def command_write_positions(planet):
    records = list()
    data = load_positions(f"maps/{planet}.pickle")
    positions = data["positions"]
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
    df.to_csv(f"{planet}.csv", index=False)


def command_write_planet_data(planet):
    data = load_positions(f"maps/{planet}.pickle")
    output = np.array([
        np.array([data["planet"]["radius"], 0, 0]),
        data["planet"]["centroid"],
        data["planet"]["north_vector"],
        data["planet"]["prime_meridian"],
        data["planet"]["parallel_zero"],
        data["planet"]["x_vector"],
        data["planet"]["y_vector"],
        data["planet"]["z_vector"],
    ])
    output = np.concatenate([
        np.array(["radius", "centroid", "north_vector", "prime_meridian", "parallel_zero", "x_vector", "y_vector", "z_vector"]).reshape(-1, 1),
        output
    ], axis=1)
    df = pd.DataFrame(output)
    df.to_csv(f"{planet}_data.csv", index=None, header=None)


def command_map(planet):
    command_add_planet_data(planet)
    command_write_positions(planet)
    command_write_planet_data(planet)


def command_add_ref():
    pass


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "distances":
        planet = sys.argv[2]
        n = int(sys.argv[3])
        seed = int(sys.argv[4])
        command_distances(planet, n, seed)
    elif command == "angles":
        planet = sys.argv[2]
        n = int(sys.argv[3])
        command_angles(planet, n)
    elif command == "planet":
        planet = sys.argv[2]
        command_add_planet_data(planet)
    elif command == "map":
        planet = sys.argv[2]
        command_map(planet)
    elif command == "add":
        command_add_ref()
