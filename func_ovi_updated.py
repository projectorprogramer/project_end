from geopy.geocoders import Nominatim
# בדיקת Nominatim
geolocator = Nominatim(user_agent="geoapi")
location = geolocator.geocode("Tel Aviv, Israel")

print(location)  # צריך להחזיר מידע על תל אביב
if location:
   print(location.latitude, location.longitude)  # צריך להדפיס קואורדינטות
# אם זה עובד, המשיכי עם שאר הקוד שלך

# import requests
# from geopy.geocoders import Nominatim
#
#
# def get_coordinates(address):
#     geolocator = Nominatim(user_agent="geoapi")
#     location = geolocator.geocode(address)
#     if location:
#         return location.latitude, location.longitude
#     return None
#
# #מחזירה את המסלול בין שתי כתובות
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
# # מחזירה את כל הבניינים שבקרבת הכתובת.
# def get_buildings_nearby(address):
#     coords = get_coordinates(address)
#     print(coords)
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
# # מחזירה את כל האלמנטים (בניינים, דרכים וכו') שבקרבת הכתובת.
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
#  #מחזירה את קווי האורך והרוחב של כתובת נתונה.
# def get_address_coordinates(address):
#     return get_coordinates(address)
#
# # print(get_address_coordinates("Jerusalem, Israel"))
# data = get_buildings_nearby("Herzl Street, Tel Aviv, Israel")
# print(data)
# # for b in data["elements"]:
# #     print(b)
# # print(get_elements_nearby("Tel Aviv, Israel"))
# # data = get_elements_nearby("Tel Aviv, Israel")
# # for b in data["elements"]:
# #     print(b)
#
