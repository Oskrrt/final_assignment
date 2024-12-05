from geopy.distance import geodesic

def calculate_distance(point_a, point_b):
    # made up coordinates, as this was not defined in the task assignment
    distance = geodesic(point_a, point_b).km
    return distance

### calculates the total distance tarjan needs to travel if he were to visit the relatives in chronological order.
def calculate_total_distance(relative_coordinates):
    tarjan_home_coordinates = (37.4890, 127.0014)
    total_distance = 0
    longitudes = relative_coordinates[0]
    latitudes = relative_coordinates[1]
    initial_distance = calculate_distance(tarjan_home_coordinates, (latitudes[0], longitudes[0]))
    i = 1
    while i < len(longitudes):
        point_a = (latitudes[i-1], longitudes[i-1])
        point_b = (latitudes[i], longitudes[i])
        total_distance += calculate_distance(point_a, point_b)
        i += 1
    total_distance = initial_distance + total_distance
    return total_distance

def calculate_price(transport_methods, relative_coordinates):
    price = 0
    total_distance = calculate_total_distance(relative_coordinates)
    print(f"total distance tarjan needs to travel if he to visits all relatives in chronological order: {total_distance} km")
    ## calculate price based on distance, route and travel method
    return price
