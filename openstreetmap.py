import osrm
from geopy.distance import geodesic

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters

def is_point_close_to_route(route, point, threshold=100):  # threshold in meters
    for step in route['routes'][0]['legs'][0]['steps']:
        for intersection in step['intersections']:
            route_point = (intersection['location'][1], intersection['location'][0])  # (lat, lon)
            distance = calculate_distance(route_point, point)
            if distance <= threshold:
                return True
    return False

def check_proximity_to_point(start, waypoint, end, threshold=100):
    client = osrm.Client(host='http://router.project-osrm.org')
    
    # Route from start to end
    route_1_to_3 = client.route(
        coordinates=[start, end],
        overview=osrm.overview.full,
        steps=True
    )
    
    # Route from waypoint to end
    route_2_to_3 = client.route(
        coordinates=[waypoint, end],
        overview=osrm.overview.full,
        steps=True
    )
    
    # Check if waypoint is close to route from start to end
    pass_close_to_waypoint_1_to_3 = is_point_close_to_route(route_1_to_3, waypoint, threshold)
    
    # Check if start is close to route from waypoint to end
    pass_close_to_start_2_to_3 = is_point_close_to_route(route_2_to_3, start, threshold)
    
    return pass_close_to_waypoint_1_to_3, pass_close_to_start_2_to_3

# Example usage
point_1 = (13.388860, 52.517037)  # Example: Berlin
point_2 = (13.397634, 52.529407)  # Example: Berlin
point_3 = (13.428555, 52.523219)  # Example: Berlin

threshold_distance = 100  # Define the proximity threshold in meters

# Check proximity
pass_close_to_waypoint_1_to_3, pass_close_to_start_2_to_3 = check_proximity_to_point(point_1, point_2, point_3, threshold_distance)

print(f"Route from point 1 to 3 passes close to point 2: {pass_close_to_waypoint_1_to_3}")
print(f"Route from point 2 to 3 passes close to point 1: {pass_close_to_start_2_to_3}")
