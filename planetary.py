import numpy as np
from geometry import euclidean_distance, unit_vector, radians_to_degrees


def estimate_planet_radius(surface_refs, positions, centroid):
    dist = 0
    for ref in surface_refs:
        pos = positions[ref]
        dist += abs(euclidean_distance(pos, centroid))
    return dist / len(surface_refs)


def get_planet_vectors(north, centroid):
    north_vector = unit_vector(north - centroid)
    prime_meridian = unit_vector(np.array([-north_vector[1], north_vector[0], 0]))
    parallel_zero = np.cross(prime_meridian, north_vector)
    assert np.linalg.norm(parallel_zero) == 1
    return north_vector, prime_meridian, parallel_zero


def get_planetary_coords(pos, centroid, radius, north_vector, prime_meridian, parallel_zero):
    pos -= centroid
    lat = np.arccos(
        np.dot(pos, north_vector) / (np.linalg.norm(pos) * np.linalg.norm(north_vector))
    )
    lat = -1 * lat + np.pi / 2
    lon = np.arctan2(  # y/x -> arctan2(y, x)
        np.dot(pos, parallel_zero),
        np.dot(pos, prime_meridian),
    )
    alt = euclidean_distance(np.zeros(3), pos)
    alt -= radius
    return np.array([alt, lon, lat])


def surface_distance(a, b, radius):
    '''
    (a, b) are in planetary coords
    '''
    _, lon_a, lat_a = list(a)
    _, lon_b, lat_b = list(b)
    delta_lat = lat_b - lat_a
    delta_lon = lon_b - lon_a
    term_a = np.sin(delta_lat/2) ** 2 + np.cos(lat_a) * np.cos(lat_b) * np.sin(delta_lon / 2) ** 2
    term_c = 2 * np.arctan2(np.sqrt(term_a), np.sqrt(1 - term_a))
    distance = radius * term_c
    return distance


def find_bearing(a, b):
    '''
    (a, b) are in planetary coords
    '''
    _, lon_a, lat_a = list(a)
    _, lon_b, lat_b = list(b)
    bearing = np.arctan2(
        np.cos(lat_b) * np.sin(lon_b - lon_a),
        np.cos(lat_a)*np.sin(lat_b) - np.sin(lat_a) * np.cos(lat_b)*np.cos(lon_b - lon_a)
    )
    return bearing


def get_atmosphere_vector(a, b, radius):
    '''
    (a, b) are in planetary coords
    '''
    bearing = find_bearing(a, b)
    if bearing < 0:
        bearing += 2 * np.pi
    s_distance = surface_distance(a, b, radius)
    alt_a = a[0]
    alt_b = b[0]
    pitch = np.arctan2(alt_b - alt_a, s_distance)
    distance = np.sqrt((alt_b - alt_a) ** 2 + s_distance ** 2)

    vector = np.array(
        [
            distance,
            radians_to_degrees(bearing),
            radians_to_degrees(pitch)
        ]
    )
    return vector
    
    
def find_bearing_projection(a, b, north, center):
    '''
    Input coordinates are absolute 3D
    '''
    # Shift to plantery centroid
    a = np.array(a)
    b = np.array(b)
    north = np.array(north)
    a -= center
    b -= center
    north -= center

    plane_norm = unit_vector(a)
    e1 = unit_vector(np.array([
        -plane_norm[1],
        plane_norm[0],
        0
    ]))
    e2 = unit_vector(np.array([
        -plane_norm[0]*plane_norm[2],
        -plane_norm[1]*plane_norm[2],
        plane_norm[0]**2 + plane_norm[1] ** 2
    ]))
    projection_north = np.array([
        np.dot(e1, north - plane_norm),
        np.dot(e2, north - plane_norm)
    ])
    projection_b = np.array([
        np.dot(e1, b - plane_norm),
        np.dot(e2, b - plane_norm)
    ])
    bearing = np.arccos(
        np.dot(projection_north, projection_b) / (
            np.linalg.norm(projection_north) * np.linalg.norm(projection_b)
            )
    )
    return bearing
