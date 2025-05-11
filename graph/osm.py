import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import LineString

# 1. הגדרת מקום
place_name = "Bnei Brak, Israel"

# 2. הורדת גרף דרכים
graph = ox.graph_from_place(place_name, network_type="walk")

# 3. נקודת מוצא ויעד
lat1, lon1 = 32.0736, 34.8324
lat2, lon2 = 32.0800, 34.8500

# 4. מציאת צמתים קרובים
orig_node = ox.distance.nearest_nodes(graph, lon1, lat1)
dest_node = ox.distance.nearest_nodes(graph, lon2, lat2)

# 5. מסלול הקצר ביותר
route = nx.shortest_path(graph, orig_node, dest_node, weight="length")

# 6. קבלת קואורדינטות של המסלול
route_coords = [(graph.nodes[n]['x'], graph.nodes[n]['y']) for n in route]
route_line = LineString(route_coords)

# 7. יצירת buffer סביב המסלול (50 מטר)
buffer = gpd.GeoSeries([route_line], crs="EPSG:4326").to_crs(epsg=3857).buffer(50).to_crs(epsg=4326)

# 8. הורדת בניינים מתוך ה-buffer
tags = {"building": True}
buildings = ox.features_from_polygon(buffer[0], tags)

# 9. הוספת גובה לבניינים, אם קיים
if 'height' in buildings.columns:
    # אם קיימת עמודת 'height', נשתמש בה
    buildings['height'] = buildings['height'].fillna(buildings['building:levels'] * 3)  # חישוב גובה ממספר הקומות (3 מטר לכל קומה)
else:
    # אם אין עמודת 'height', נבדוק אם יש עמודת 'building:levels'
    if 'building:levels' in buildings.columns:
        buildings['height'] = buildings['building:levels'] * 3  # חישוב גובה ממספר הקומות (3 מטר לכל קומה)
    else:
        buildings['height'] = 0  # אם אין נתונים, נתן גובה ברירת מחדל של 0

# 10. הדפסת תוצאה
print(buildings[['geometry', 'height']].head())
# הקוד שנגמר שורה מעל נותן גובה ביניין רק אם יש בOSM אם לא נותן NAN

