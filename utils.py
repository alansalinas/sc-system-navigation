import pickle
from geometry import (
    euclidean_distance,
    degrees_to_radians,
    invert_heading,
    invert_pitch,
    to_spherical,
)


def save_positions(positions, filename):
    with open(filename, "wb") as f:
        pickle.dump(positions, f)
    return True


def load_positions(filename):
    with open(filename, "rb") as f:
        positions = pickle.load(f)
    return positions


def validate(positions, distances, headings, pitches, full=False):
    avg_error = 0
    for ref in distances:
        x, y = ref
        Px, Py = positions[x], positions[y]
        dist = distances[ref]
        dist_estimated = euclidean_distance(Px, Py)
        dist_error = dist_estimated - dist
        if full:
            print("Dist err", x, y, dist_error)
        avg_error += abs(dist_error)
    dist_err = avg_error / len(distances)
    avg_error = 0
    for aref in headings:
        # Obtain target angles from origin to angle refs
        target_heading = degrees_to_radians(invert_heading(headings[aref]))
        target_pitch = degrees_to_radians(invert_pitch(pitches[aref]))
        # Obtain current angles from origin to angle refs
        curr_pos = to_spherical(positions[aref])
        h_error = target_heading - curr_pos[1]
        p_error = target_pitch - curr_pos[2]
        avg_error += abs(h_error) + abs(p_error)
        if full:
            print("Angle err", aref, abs(h_error) + abs(p_error))
    angle_err = avg_error / len(headings)
    return dist_err, angle_err
