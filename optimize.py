import numpy as np
from geometry import (
    euclidean_distance,
    to_spherical,
    to_rectangular,
    invert_heading,
    invert_pitch,
    degrees_to_radians,
    rotate_positions,
)
from utils import validate


def optimize_distances(positions, distances, origin, n, gain=0.001, decay=0.999999999999):
    print("\nDistance optimization:", n)
    prev_err = 1e5
    for i in range(n):
        gain = decay * gain
        avg_error = 0
        # Correct distances
        for ref in distances:
            x, y = ref
            Px, Py = positions[x], positions[y]
            dist = distances[ref]
            dist_estimated = euclidean_distance(Px, Py)
            direction = (Px - Py) / dist_estimated
            dist_error = dist_estimated - dist
            if x != origin:
                Px = Px - gain * (dist_error / 2) * direction
            if y != origin:
                Py = Py + gain * (dist_error / 2) * direction
            positions[x] = Px
            positions[y] = Py
            avg_error += abs(dist_error)
            # if i == n-1:
            #     print(x, y, "dist err", abs(dist_error))
        # Log progress
        prog = ((i+1)/n)*100
        avg_dist_err = avg_error / len(distances)
        log = f"\rProgress {prog:.2f}% - Current error dist: {avg_dist_err:.5f}"
        print(log, end="", flush=True)
        if avg_dist_err < 1.0 and prev_err - avg_dist_err < 1e-20:
            print(f"\nEarly stopping at {prog:.2f}%.", avg_dist_err)
            break
        prev_err = avg_dist_err
    print("")
    return True


def optimize_angles(positions, distances, headings, pitches, origin, n):
    # First step: rotate to set one vector right
    aref = list(headings.keys())[0]
    a = positions[aref]
    b_r = to_spherical(a)[0]
    b_h = degrees_to_radians(invert_heading(headings[aref]))
    b_p = degrees_to_radians(invert_pitch(pitches[aref]))
    b = to_rectangular(np.array([b_r, b_h, b_p]))
    k = np.cross(a, b)
    k = k / np.linalg.norm(k)
    theta = np.arcsin(np.linalg.norm(np.cross(a, b)) / (np.linalg.norm(a) * np.linalg.norm(b)))
    rotate_positions(positions, k, theta, origin, in_place=True)
    dist_err, new_angle_err = validate(positions, distances, headings, pitches)
    assert np.isclose(b, positions[aref]).all()
    print("Initial flip. Dist err:", dist_err, " - Angle err:", new_angle_err)

    # Second step: rotate around good vector to minimze error
    a = positions[aref]
    a = a / np.linalg.norm(a)
    best_angle_err = 10
    best_theta = None
    for i in range(n):
        theta = ((np.pi * 2) / n) * i
        new_positions = rotate_positions(positions, a, theta, origin)
        dist_err, new_angle_err = validate(new_positions, distances, headings, pitches)
        if new_angle_err < best_angle_err:
            best_angle_err = new_angle_err
            best_theta = theta
        # Log progress
        prog = ((i+1)/n)*100
        log = f"\rProgress {prog:.2f}% - Current error dist:{dist_err:.5f} - Current error angle:{best_angle_err:.5f}"
        print(log, end="", flush=True)
    rotate_positions(positions, a, best_theta, origin, in_place=True)


def get_coords(positions, data):
    pos = np.random.rand(3).astype(np.longdouble)
    gain = 0.5
    for i in range(1000):
        for key in data:
            if key not in positions:
                continue
            dist_estimated = euclidean_distance(pos, positions[key])
            direction = (pos - positions[key]) / dist_estimated
            dist_error = dist_estimated - data[key]
            pos = pos - gain * (dist_error / 2) * direction
    assert dist_error < 0.5
    return pos


def find_planet_centroid(n, surface_refs, positions):
    pos = np.random.rand(3).astype(np.longdouble)
    gain = 0.01
    for i in range(n):
        avg_error = list()
        if i == n - 1:
            print("\n")
        for ref_a in surface_refs:
            for ref_b in surface_refs:
                if ref_a == ref_b:
                    continue
            dist_a = euclidean_distance(pos, positions[ref_a])
            direction_a = (pos - positions[ref_a]) / dist_a
            dist_b = euclidean_distance(pos, positions[ref_b])
            direction_b = (pos - positions[ref_b]) / dist_b
            error_a = dist_a - dist_b
            error_b = dist_b - dist_a
            pos = pos - gain * (error_a / 2) * direction_a
            pos = pos - gain * (error_b / 2) * direction_b
            avg_error.append(abs(dist_a - dist_b))
            if i == n-1:
                print(ref_a, ref_b, abs(dist_a - dist_b))
        if i == 0:
            print("Initial error:", np.mean(avg_error), "\n")
        # Log progress
        prog = ((i+1)/n)*100
        avg_error = np.mean(avg_error)
        log = f"\rProgress {prog:.2f}% - Current error dist:{avg_error:.5f}"
        print(log, end="", flush=True)
    print("\n")
    return pos
    
    
