import numpy as np
import copy


def euclidean_distance(a, b):
    return np.linalg.norm(a-b)


def to_spherical(p, degree=False):
    R = np.linalg.norm(p)
    lat = np.arcsin(p[2] / R)
    lon = np.arctan2(p[1], p[0])
    if lon < 0:
        lon = 2 * np.pi + lon
    if degree:
        lat = radians_to_degrees(lat)
        lon = radians_to_degrees(lon)
    return np.array((R, lon, lat))


def to_rectangular(p):
    R, lon, lat = p
    x = np.cos(lat) * np.cos(lon) * R
    y = np.cos(lat) * np.sin(lon) * R
    z = np.sin(lat) * R
    return np.array((x, y, z))


def get_direction(a, b):
    return b - a


def invert_heading(theta, degree=True):
    if degree:
        delta = 180
    else:
        delta = np.pi
    theta += delta
    if theta >= delta * 2:
        theta -= delta * 2
    return theta


def invert_pitch(theta):
    return theta * -1


def degrees_to_radians(theta):
    return theta * (np.pi / 180)


def radians_to_degrees(theta):
    return theta * (180 / np.pi)


def unit_vector(v):
    return v / np.linalg.norm(v)


def rotate_on_vector(k, v, theta):
    """
    Rotate vector v around vector k by angle theta
    :param k: Axis of rotation vector
    :param v: Vector to rotate around k
    :param theta: Angle to rotate in radians
    """
    cos = np.cos(theta)
    sin = np.sin(theta)
    v_rot = v * cos + np.cross(k, v) * sin + k * np.dot(k, v) * (1 - cos)
    # Rotation should preserve magnitude
    assert np.isclose(np.linalg.norm(v), np.linalg.norm(v_rot))
    return v_rot


def rotate_positions(positions, k, theta, origin, in_place=False):
    if not in_place:
        positions = copy.copy(positions)
    for ref in positions:
        if ref == origin:
            continue
        v = positions[ref]
        positions[ref] = rotate_on_vector(k, v, theta)
    return positions


def shift_to_center(positions, center):
    for ref in positions:
        positions[ref] = positions[ref] - center
    return positions 
