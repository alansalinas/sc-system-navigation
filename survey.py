import sys
import numpy as np
from optimize import optimize_distances, optimize_angles, find_planet_center
from geometry import shift_to_center
from utils import load_positions, save_positions, validate
from survey_data.hurston import (
    refs,
    surface_refs,
    distances,
    headings,
    pitches,
    origin
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


def command_planet_origin():
    positions = load_positions("maps/hurston_angle.pickle")
    center = find_planet_center(1000, surface_refs, positions)
    positions = shift_to_center(positions, center)
    print("Found planetary center:", origin)
    save_positions(positions, "maps/hurston.pickle")
    

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
    elif command == "origin":
        command_planet_origin()
    elif command == "map":
        command_make_map()