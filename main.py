import requests
from geopy.geocoders import Nominatim


def get_coordinates(address):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None


# def get_route(source, destination):
#     source_coords = get_coordinates(source)
#     destination_coords = get_coordinates(destination)
#     if not source_coords or not destination_coords:
#         return None
#
#     query = f"""
#     [out:json];
#     way(around:100, {source_coords[0]}, {source_coords[1]}) -> .source;
#     way(around:100, {destination_coords[0]}, {destination_coords[1]}) -> .destination;
#     (
#       .source;
#       .destination;
#     );
#     out body;
#     """
#
#     response = requests.get("http://overpass-api.de/api/interpreter", params={"data": query})
#     return response.json()
#
#
# def get_buildings_nearby(address):
#     coords = get_coordinates(address)
#     if not coords:
#         return None
#
#     query = f"""
#     [out:json];
#     (node[building](around:200, {coords[0]}, {coords[1]});
#      way[building](around:200, {coords[0]}, {coords[1]});
#      relation[building](around:200, {coords[0]}, {coords[1]});
#     );
#     out body;
#     """
#
#     response = requests.get("http://overpass-api.de/api/interpreter", params={"data": query})
#     return response.json()
#
#
# def get_elements_nearby(address):
#     coords = get_coordinates(address)
#     if not coords:
#         return None
#
#     query = f"""
#     [out:json];
#     (
#       node(around:200, {coords[0]}, {coords[1]});
#       way(around:200, {coords[0]}, {coords[1]});
#       relation(around:200, {coords[0]}, {coords[1]});
#     );
#     out body;
#     """
#
#     response = requests.get("http://overpass-api.de/api/interpreter", params={"data": query})
#     return response.json()
#
#
# def get_address_coordinates(address):
#     return get_coordinates(address)

if __name__ =='__main__':
    print(get_coordinates("Tel Aviv, Israel"))




