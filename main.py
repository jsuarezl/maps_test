import googlemaps
from shapely import Polygon, Point

gmaps = googlemaps.Client(key='key')

# find the nearest route between two points
start_point = (-33.44717904737609, -70.64542083490814)
end_point = (-33.43291721249615, -70.61496167006258)

directions_result = gmaps.directions(start_point, end_point, alternatives=True, avoid='highways')

# mark a blacklist area
area_coordinates = [
    (-33.44506735118542, -70.64628945681663),
    (-33.43661597080002, -70.64768420543484),
    (-33.43692037802916, -70.63598977471295),
    (-33.44194805059744, -70.63029295219013)
]
# Create a Polygon object using the coordinates
area_polygon = Polygon(area_coordinates)

# check if coordinates on the directions collide with our area
index = 0
for directions in directions_result:
    index += 1
    for step in directions['legs'][0]['steps']:
        start_location = step['start_location']
        end_location = step['end_location']

        # Create Point objects for start and end locations
        start_point = Point(start_location['lat'], start_location['lng'])
        end_point = Point(end_location['lat'], end_location['lng'])

        # Check if either point is within the polygon
        if area_polygon.contains(start_point) or area_polygon.contains(end_point):
            print(f"Collision detected on directions {index}")
            break
