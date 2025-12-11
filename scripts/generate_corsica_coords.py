import json
import random

def is_point_in_polygon(lat, lon, polygon):
    """
    Ray Casting algorithm to check if point (lat, lon) is inside the polygon.
    Polygon is a list of (lat, lon) tuples.
    """
    inside = False
    n = len(polygon)
    p1_lat, p1_lon = polygon[0]
    
    for i in range(1, n + 1):
        p2_lat, p2_lon = polygon[i % n]
        
        # Check if point is vertically between p1 and p2
        if min(p1_lon, p2_lon) < lon <= max(p1_lon, p2_lon):
            # Calculate intersection latitude
            if p2_lon != p1_lon:
                xinters = (lon - p1_lon) * (p2_lat - p1_lat) / (p2_lon - p1_lon) + p1_lat
                if p1_lat == p2_lat or lat <= xinters:
                    inside = not inside
        p1_lat, p1_lon = p2_lat, p2_lon
        
    return inside

def generate_corsica_coords(num_points=500):
    # Simplified Polygon of Corsica (Lat, Lon)
    # Traced roughly from map to avoid water
    corsica_polygon = [
        # Start North (Cap Corse)
        (43.018, 9.406), # Cap Corse Tip
        (42.920, 9.450), # Macinaggio
        (42.700, 9.450), # Bastia
        
        # East Coast (Relatively Straight)
        (42.500, 9.530), # South of Bastia
        (42.280, 9.550), # Aleria
        (41.950, 9.400), # Solenzara
        (41.650, 9.350), # Palombaggia
        (41.570, 9.280), # Porto Vecchio
        (41.450, 9.220), # Santa Manza
        (41.370, 9.160), # Bonifacio (South Tip)
        
        # West Coast (Jagged - Gulfs & Capes)
        (41.440, 9.050), # Figari Coast
        (41.490, 8.930), # Cap de Roccapina
        (41.560, 8.900), # Sartene Coast (Campomoro)
        
        # Gulf of Valinco (Go Deep Inside)
        (41.670, 8.950), # Propriano (Inside)
        (41.720, 8.800), # Porto Pollo / Serra-di-Ferro
        
        # Gulf of Ajaccio (Go Deep Inside)
        (41.800, 8.700), # Coti-Chiavari
        (41.920, 8.760), # Ajaccio (City/Port/Airport)
        (41.890, 8.600), # Ponte de la Parata (Sanguinaires)
        
        # Gulf of Sagone & West Promontory
        (42.050, 8.610), # Anse de Sagone
        (42.150, 8.580), # Cargese
        (42.250, 8.530), # Capo Rosso (Piana)
        
        # Gulf of Porto
        (42.270, 8.680), # Porto (Bottom of gulf)
        (42.360, 8.540), # Scandola Reserve
        
        # Balagne
        (42.560, 8.750), # Calvi (Citadel)
        (42.630, 8.930), # Ile Rousse
        (42.650, 9.050), # Agriates Desert Coast
        
        # Gulf of Saint Florent
        (42.680, 9.300), # Saint Florent
        (42.750, 9.330), # Nonza
        (42.950, 9.350), # Northwest Cap Corse
        (43.018, 9.406)  # Close Loop
    ]

    # Bounding Box for random generation
    lat_min = min(p[0] for p in corsica_polygon)
    lat_max = max(p[0] for p in corsica_polygon)
    lon_min = min(p[1] for p in corsica_polygon)
    lon_max = max(p[1] for p in corsica_polygon)
    
    coords = []
    attempts = 0
    while len(coords) < num_points:
        attempts += 1
        lat = random.uniform(lat_min, lat_max)
        lon = random.uniform(lon_min, lon_max)
        
        if is_point_in_polygon(lat, lon, corsica_polygon):
            coords.append({"latitude": round(lat, 6), "longitude": round(lon, 6)})
            
        if attempts > num_points * 100: # Safety break
            print("⚠️ Too many attempts, stopping early.")
            break
            
    print(f"Generated {len(coords)} points after {attempts} attempts.")
    return coords

if __name__ == "__main__":
    data = generate_corsica_coords()
    output_file = "scripts/corsica_gps.json"
    
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"✅ Generated {len(data)} points in {output_file}")
