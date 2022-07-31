# Hurston survey on Sat 23 Jul 2022

origin = "HDMS-Pinewood"

# Distance references, origin will be the first in the list
surface_refs = [
    "HDMS-Pinewood",
    "HDMS-Thedus",
    "HDMS-Stanhope",
    "HDMS-Oparei",
    "HDMS-Edmond",
    "HDMS-Hadley",
]

orbital_refs = [
    "OM-1",
    "OM-2",
    "OM-3",
    "OM-4",
    "OM-5",
    "OM-6",
]

refs = surface_refs + orbital_refs

# All possible measureable distances between points
distances = {
    ("HDMS-Pinewood", "HDMS-Stanhope"): 1739,
    ("HDMS-Stanhope", "HDMS-Edmond"): 1004,
    ("HDMS-Stanhope", "HDMS-Hadley"): 1951,
    ("HDMS-Oparei", "HDMS-Stanhope"): 1589,
    ("HDMS-Stanhope", "HDMS-Thedus"): 1440,

    ("HDMS-Pinewood", "HDMS-Thedus"): 968.898,
    ("HDMS-Hadley", "HDMS-Thedus"): 1610,
    ("HDMS-Edmond", "HDMS-Thedus"): 1852,
    ("HDMS-Oparei", "HDMS-Thedus"): 1671,

    ("HDMS-Oparei", "HDMS-Pinewood"): 1832,
    ("HDMS-Hadley", "HDMS-Pinewood"): 1014,
    ("HDMS-Edmond", "HDMS-Pinewood"): 1583,

    ("HDMS-Edmond", "HDMS-Hadley"): 1465,
    ("HDMS-Edmond", "HDMS-Oparei"): 1614,

    ("HDMS-Hadley", "HDMS-Oparei"): 1324,

    ("OM-1", "HDMS-Edmond"): 1131,
    ("OM-1", "HDMS-Stanhope"): 975.907,
    ("OM-1", "HDMS-Pinewood"): 1623,
    ("OM-1", "HDMS-Thedus"): 1665,
    ("OM-1", "HDMS-Hadley"): 2134,
    ("OM-1", "HDMS-Oparei"): 2333,

    ("OM-5", "HDMS-Edmond"): 1970,
    ("OM-5", "HDMS-Stanhope"): 2220,
    ("OM-5", "HDMS-Pinewood"): 483.913,
    ("OM-5", "HDMS-Thedus"): 1338,
    ("OM-5", "HDMS-Hadley"): 1125,
    ("OM-5", "HDMS-Oparei"): 2159,

    ("OM-3", "HDMS-Edmond"): 2272,
    ("OM-3", "HDMS-Stanhope"): 1579,
    ("OM-3", "HDMS-Pinewood"): 1675,
    ("OM-3", "HDMS-Thedus"): 710.110,
    ("OM-3", "HDMS-Hadley"): 2178,
    ("OM-3", "HDMS-Oparei"): 1809,

    ("OM-6", "HDMS-Edmond"): 1498,
    ("OM-6", "HDMS-Stanhope"): 1095,
    ("OM-6", "HDMS-Pinewood"): 2428,
    ("OM-6", "HDMS-Thedus"): 2083,
    ("OM-6", "HDMS-Hadley"): 2205,
    ("OM-6", "HDMS-Oparei"): 1211,

    ("OM-4", "HDMS-Edmond"): 982.544,
    ("OM-4", "HDMS-Stanhope"): 1906,
    ("OM-4", "HDMS-Pinewood"): 1823,
    ("OM-4", "HDMS-Thedus"): 2372,
    ("OM-4", "HDMS-Hadley"): 1178,
    ("OM-4", "HDMS-Oparei"): 1690,

    ("OM-2", "HDMS-Edmond"): 2201,
    ("OM-2", "HDMS-Stanhope"): 2275,
    ("OM-2", "HDMS-Pinewood"): 1870,
    ("OM-2", "HDMS-Thedus"): 1832,
    ("OM-2", "HDMS-Hadley"): 1255,
    ("OM-2", "HDMS-Oparei"): 827.707,
}

# Headings from orbit points to origin
headings = {
    "OM-1": 125.5,
    "OM-2": 64.5,
    "OM-3": 43.5,
    "OM-4": 150,
    "OM-5": 273,
    "OM-6": 95.5,
    
}

# Pitches from orbit points to origin
pitches = {
    "OM-1": 42,
    "OM-2": -54,
    "OM-3": 12,
    "OM-4": -25,
    "OM-5": -18,
    "OM-6": -6,
}

# North point
north = {
    "HDMS-Pinewood": 1302,
    "HDMS-Stanhope": 715.524,
    "HDMS-Thedus": 1308,
    "HDMS-Oparei": 1913,
    "HDMS-Hadley": 1760,
    "HDMS-Edmond": 912.756,
}

radius = 1000


# NEAR Edmond
# H 25, P -44
