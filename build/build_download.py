import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import LineString

# שלב 1: בניית הגרף והמסלול
place_name = "Bnei Brak, Israel"
graph = ox.graph_from_place(place_name, network_type='all')
lat1, lon1 = 32.0736, 34.8324
lat2, lon2 = 32.0800, 34.8500
orig = ox.distance.nearest_nodes(graph, X=lon1, Y=lat1)
dest = ox.distance.nearest_nodes(graph, X=lon2, Y=lat2)
route = nx.shortest_path(graph, orig, dest, weight='length')

# שלב 2: יצירת LineString של המסלול
route_nodes = [graph.nodes[n] for n in route]
route_coords = [(n['x'], n['y']) for n in route_nodes]
route_line = LineString(route_coords)

# שלב 3: יצירת buffer סביב המסלול (במטרים)
buffer_width = 25  # רוחב האזור שמעניין אותך (למשל 25 מטר מכל צד)
route_gdf = gpd.GeoDataFrame(geometry=[route_line], crs='EPSG:4326')
route_gdf = route_gdf.to_crs(epsg=3857)  # שינוי קואורדינטות ליחידות מטר
buffer = route_gdf.buffer(buffer_width).to_crs(epsg=4326).iloc[0]

# שלב 4: הורדת בניינים רק באזור ה-buffer
tags = {'building': True}
buildings = ox.features_from_polygon(buffer, tags)

# סינון רק בניינים עם צורה גיאומטרית
buildings = buildings[buildings.geometry.notnull()]

# הדפסה לדוגמה
print(buildings[['geometry', 'building']].head())

