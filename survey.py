import sys
import numpy as np
from optimize import optimize_distances, optimize_angles, find_planet_centroid, get_coords
from utils import load_positions, save_positions, validate
from planetary import get_planet_vectors
from survey_data.hurston import (
    refs,
    orbital_refs,
    distances,
    headings,
    pitches,
    origin,
    north,
    radius
)


def initialize_positions():
    positions = {
        ref: (np.random.rand(3) * 10).astype(np.longdouble)
        for ref in refs[1:]
    }
    positions[refs[0]] = np.array([0, 0, 0])
    return positions


def command_distances(n):
    np.random.seed(1)
    positions = initialize_positions()
    dist_err, angle_err = validate(positions, distances, headings, pitches)
    print(f"Initialized -- Distance error: {dist_err} -- Angle error: {angle_err}")
    optimize_distances(positions, distances, origin, n)
    dist_err, angle_err = validate(positions, distances, headings, pitches, True)
    print(f"Distance optimized -- Distance error: {dist_err} -- Angle error: {angle_err}")
    save_positions(positions, "maps/hurston_distance.pickle")
    return positions


def command_angles(n):
    positions = load_positions("maps/hurston_distance.pickle")
    dist_err, angle_err = validate(positions, distances, headings, pitches)
    print(f"Initials -- Distance error: {dist_err} -- Angle error: {angle_err}")
    optimize_angles(positions, distances, headings, pitches, origin, n)
    dist_err, angle_err = validate(positions, distances, headings, pitches, True)
    print(f"Angle optimized -- Distance error: {dist_err} -- Angle error: {angle_err}")
    save_positions(positions, "maps/hurston_angle.pickle")
    return positions


def command_add_planet_data():
    positions = load_positions("maps/hurston_angle.pickle")
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
    
    data = {
        "positions": positions,
        "planet": {
            "centroid": centroid,
            "radius": radius,
            "north_vector": north_vector,
            "prime_meridian": prime_meridian,
            "parallel_zero": parallel_zero,
        }
    }
    save_positions(data, "maps/hurston.pickle")
    

def command_make_map():
    pass


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "distances":
        n = int(sys.argv[2])
        command_distances(n)
    elif command == "angles":
        n = int(sys.argv[2])
        command_angles(n)
    elif command == "planet":
        command_add_planet_data()
    elif command == "map":
        command_make_map()
