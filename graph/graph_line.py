import matplotlib
matplotlib.use('TkAgg')  # משנה את ה-backend ל-TkAgg
# import matplotlib
# matplotlib.use('Agg')  # אפשר גם להשתמש ב-'TkAgg' אם מדובר בסביבה תומכת GUI
import osmnx as ox
import networkx as nx

# מיקום המקום
place_name = "Bnei Brak, Israel"

# גרף הרחובות
graph = ox.graph_from_place(place_name, network_type='all')

# קואורדינטות נקודת המוצא (נניח שאתה רוצה את הקואורדינטות של בני ברק)
lat1, lon1 = 32.0736, 34.8324  # קואורדינטות לדוגמה

# קואורדינטות נקודת היעד (נניח שאתה רוצה את הקואורדינטות של מקום אחר)
lat2, lon2 = 32.0800, 34.8500  # קואורדינטות לדוגמה

# צומת מקור
orig_node = ox.distance.nearest_nodes(graph, X=lon1, Y=lat1)

# צומת יעד
dest_node = ox.distance.nearest_nodes(graph, X=lon2, Y=lat2)

# לחשב את המסלול הקצר ביותר
route = nx.shortest_path(graph, orig_node, dest_node, weight='length')

# להציג את המסלול
ox.plot_graph_route(graph, route, route_linewidth=6, node_size=0, bgcolor='k')
