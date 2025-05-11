import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import LineString, Polygon
import pandas as pd
from datetime import datetime
from pvlib import solarposition
import numpy as np  # ייבוא numpy

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
    buildings['height'] = buildings['height'].fillna(
        buildings['building:levels'] * 3)  # חישוב גובה ממספר הקומות (3 מטר לכל קומה)
elif 'building:levels' in buildings.columns:
    buildings['height'] = buildings['building:levels'] * 3  # חישוב גובה ממספר הקומות (3 מטר לכל קומה)

# 10. אם יש עדיין NaN, נניח גובה ברירת מחדל של 10 מטר לכל הבניינים
buildings['height'] = buildings['height'].fillna(10)

# 11. חישוב הצל של בניינים - כאן אנחנו משתמשים בספריית pvlib לחישוב זווית השמש
times = pd.date_range(datetime(2025, 5, 5, 12, 0), periods=1, freq='h')
solar_pos = solarposition.get_solarposition(times, lat1, lon1)


# 12. חישוב אורך הצל
def calculate_shadow_length(building_height, solar_zenith):
    # ווידוא שהערכים הם מספריים
    try:
        building_height = float(building_height)
        solar_zenith = float(solar_zenith)
        # אם הערכים אינם נכונים, נחזיר ערכים ברירת מחדל
        if np.isnan(building_height) or np.isnan(solar_zenith) or solar_zenith == 0:
            return 0
        return building_height / np.tan(np.radians(solar_zenith))
    except (ValueError, TypeError):
        return 0  # אם יש שגיאה בהמרה, נחזיר 0


# 13. בדיקת חפיפת הצל עם המסלול
def check_shadow_intersection(building, shadow_length):
    # אם יש לא מספיק נתונים או שהבניין לא בסביבה, נחזור
    if building['geometry'] is None:
        return False

    # חישוב הקואורדינטות של הצל
    building_geom = building['geometry']
    building_coords = list(building_geom.exterior.coords)

    # יש לוודא שהצל ייווצר ממסלול מספיק רחוק
    shadow_coords = []
    for coord in building_coords:
        # נניח שהצל עובר בנקודה מסוימת
        shadow_coords.append((coord[0] + shadow_length, coord[1]))

    if len(shadow_coords) >= 4:
        shadow_polygon = Polygon(shadow_coords)
        # בדיקה אם הצל חותך את המסלול
        return shadow_polygon.intersects(route_line)
    return False


# 14. חישוב הצל עבור כל בניין וצבירת תוצאות
for index, building in buildings.iterrows():
    building_height = building['height']
    solar_zenith = solar_pos['zenith'].iloc[0]
    shadow_length = calculate_shadow_length(building_height, solar_zenith)

    if check_shadow_intersection(building, shadow_length):
        print(f"Building {index} casts a shadow on the route.")
    else:
        print(f"Building {index} does not cast a shadow on the route.")

# 15. הדפסת תוצאה
print(buildings[['geometry', 'height']].head())
