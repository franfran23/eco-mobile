import osrm
from geopy.distance import geodesic

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters

def is_point_close_to_route(route, point, threshold=200):  # threshold in meters
    # print("Point to check:", point)
    # print("Threshold (meters):", threshold)
    
    for step in route['routes'][0]['legs'][0]['steps']:
        for intersection in step['intersections']:
            route_point = (intersection['location'][1], intersection['location'][0])  # (lat, lon)
            distance = calculate_distance(route_point, point)
            # print("Route point:", route_point, "Distance to point:", distance)
            if distance <= threshold:
                # print("Point is within threshold distance.")
                return True

    # print("Point is not within threshold distance for any route point.")
    return False

def check_proximity_to_point(start, waypoint, end, threshold=200):
    client = osrm.Client(host='http://router.project-osrm.org')
    
    # Route from start to end
    route_1_to_3 = client.route(
        coordinates=[start[::-1], end[::-1]],
        overview=osrm.overview.full,
        steps=True
    )
    # print('route 1 to 3', route_1_to_3)
    
    # Route from waypoint to end
    route_2_to_3 = client.route(
        coordinates=[waypoint[::-1], end[::-1]],
        overview=osrm.overview.full,
        steps=True
    )
    
    # Check if waypoint is close to route from start to end
    pass_close_to_waypoint_1_to_3 = is_point_close_to_route(route_1_to_3, waypoint, threshold)
    
    # Check if start is close to route from waypoint to end
    pass_close_to_start_2_to_3 = is_point_close_to_route(route_2_to_3, start, threshold)
    
    return pass_close_to_waypoint_1_to_3, pass_close_to_start_2_to_3
'''
# Example usage
me = (50.6949544, 3.1511743)
eic = (50.720550200000005, 3.150640888902045)
place = (50.72041815, 3.1528558962092363)

threshold_distance = 200  # Define the proximity threshold in meters

# Check proximity
pass_close_to_waypoint_1_to_3, pass_close_to_start_2_to_3 = check_proximity_to_point(me, place, eic, threshold_distance)

print(f"Route from point 1 to 3 passes close to point 2: {pass_close_to_waypoint_1_to_3}")
print(f"Route from point 2 to 3 passes close to point 1: {pass_close_to_start_2_to_3}")
'''