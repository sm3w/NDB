import csv
from math import *
import pickle
import os

# TODO(jamie): Clean this entire thing up!!!

# TODO(jamie): @Cleanup - we want to init the postcode database once and expose
# one function to call from the application

# Radius of the earth in miles and kilometres
Rm  = float(3953)
Rk  = float(6363)

PI  = 3.14159265359
TAU = 3.14159265359*2


PICKLED_DB = "database/postcode_db.pck"


def write_debug_file(lookup_count, comparison_data):
    with open("compare.txt", 'w') as fp:
        fp.write('\n'.join('{}:  {}, {}'.format(x[0],x[1],x[2]) for x in comparison_data))
    print("Look up count was: {}".format(lookup_count))


def read_csv_data():
    postcode_db = {}
    with open("data/UK-Postcodes.csv", 'r') as csv_file:
        data   = []
        reader = csv.reader(csv_file)
        for count, row in enumerate(reader):
            postcode_db[row[1]] = row[2:4]

    print(postcode_db)
    picklefile = open(PICKLED_DB, "wb")
    pickle.dump(postcode_db, picklefile)

    return(postcode_db)

def init_postcode_db():
    if not os.path.exists(PICKLED_DB):
        postcode_db = read_csv_data()
    else:
        picklefile = open(PICKLED_DB, "rb")
        postcode_db = pickle.load(picklefile)

    return(postcode_db)


def degrees_to_radians(deg):
    radian = deg * PI/180
    return(radian)

# NOTE(jamie): Haversine formula version
def calculate_distance(src_lat, src_lon, dest_lat, dest_lon):
    """

    Haversine formula for reference
    a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    c = 2 ⋅ atan2( √a, √(1−a) )
    d = R ⋅ c

    """
    # NOTE(jamie): This attempts to compensate for the fact our
    # distances between lat/longs are calc'd roughly as the crow flies.
    fudge_factor = 35

    lat_1 = degrees_to_radians(src_lat)
    lon_1 = degrees_to_radians(src_lon)
    lat_2 = degrees_to_radians(dest_lat)
    lon_2 = degrees_to_radians(dest_lon)

    lat_delta = lat_2 - lat_1
    lon_delta = lon_2 - lon_1

    a = (sin(lat_delta/2))**2 + cos(lat_1) * cos(lat_2) * (sin(lon_delta/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    float_dm = c * Rm
    float_dk = c * Rk
    float_dm += (float_dm / 100 * fudge_factor)
    float_dk += (float_dk / 100 * fudge_factor)

    dm = round(float_dm)
    dk = round(float_dk)

    return(float_dm)

# Law of cosines method
def test_radius(src_lat, src_lon, dest_lat, dest_lon):
    earth_radius_miles = float(3953)
    f1 = cos(degrees_to_radians(src_lat))
    f2 = cos(degrees_to_radians(dest_lat))
    f3 = cos(degrees_to_radians(src_lon) - degrees_to_radians(dest_lon))
    f4 = sin(degrees_to_radians(src_lat))
    f5 = sin(degrees_to_radians(dest_lat))
    distance = earth_radius_miles * acos(f1 * f2 * f3 + f4 * f5)
    return(distance)

def test_postcode_distance(postcode_db, postcode, radius):
    ''' Returns a list of postcode prefixes (e.g. SA43) that fall within the radius of the supplied desired postcode'''

    # IMPORTANT(jamie): the leading digits of 'longitude' will always be the same for
    # a given radius (tested up to 25 miles) - ergo, we dont want to bother
    # calculating distances with longitude values that are not == to this
    # number. 

    # IMPORTANT(jamie): Potential gotcha in here if the received radius value is > 25 miles
    # see above todo.

    # TODO(jamie): Check the key is in the db before doing anything else
    if not postcode in postcode_db.keys():
        return -1
    zero_point = postcode_db[postcode]


    zero_lat = float(zero_point[0])
    zero_lon = float(zero_point[1])

    THE_LAT = 0
    THE_LON = 1

    trunc_zero_lon = trunc(zero_lon)

    compare = []
    distance_results = []
    lookup_count = 0

    for key in postcode_db:
       temp_lat = float(postcode_db[key][THE_LAT])
       temp_lon = float(postcode_db[key][THE_LON])
       #if (trunc(temp_lon) != trunc_zero_lon):
       #    continue
       #else:
       distance = calculate_distance(zero_lat, zero_lon, temp_lat, temp_lon)
       lookup_count += 1
       if round(distance) <= float(radius):
           print("Distances are: {}, radius is {}".format(distance, radius))
           k = (key)
           dis = (key, temp_lat, temp_lon)
           distance_results.append(k)
           compare.append(dis)

    print(distance_results)
    return(distance_results)

# @Unused
def get_values(postcode_db, postcode_1, postcode_2):
    location_1 = postcode_db[postcode_1]
    location_2 = postcode_db[postcode_2]

    src_lat  = float(location_1[0])
    src_lon  = float(location_1[1])
    dest_lat = float(location_2[0])
    dest_lon = float(location_2[1])

    test_radius(src_lat, src_lon, dest_lat, dest_lon)

# NOTE(jamie): Testing function calls
def run_test():
    db = init_postcode_db()
    test_postcode_distance(db, "HA4", 5)

db = init_postcode_db()

def get_postcodes(postcode, radius):
    result = test_postcode_distance(db, postcode, radius)
    return(result)

