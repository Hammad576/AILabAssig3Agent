import pandas as pd
from pyswip import Prolog

# Initialize Prolog
print("Step 3.1.0: Initializing Prolog for BFS KB operations!")
prolog = Prolog()
prolog.consult('kb.pl')
print("Step 3.1.0: Prolog initialized with kb.pl!")

# Load the dataset
dataset_path = "US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)

# Display dataset columns
print("My Crime Dataset Columns:", df.columns)

# Debug: Print unique City and Crime Type values
print("Unique Cities:", df['City'].str.strip().str.lower().unique()[:10])
print("Unique Crime Types:", df['Crime Type'].str.strip().str.lower().unique())

# Create crimeDictionary
crimeDictionary = {}
if "City" in df.columns and "Crime Type" in df.columns:
    for _, row in df.iterrows():
        city = str(row["City"]).strip().lower()
        crime_type = str(row["Crime Type"]).strip().lower()
        if not city or not crime_type:
            print(f"Debug: Skipping row - City: {city}, Crime Type: {crime_type}")
            continue
        if city != crime_type:  # Avoid self-loops
            if city not in crimeDictionary:
                crimeDictionary[city] = set()
            crimeDictionary[city].add(crime_type)
else:
    print("Error: 'City' or 'Crime Type' column missing!")

# Debug: Print crimeDictionary sample
print("Crime Dictionary Sample:", {k: list(v)[:5] for k, v in list(crimeDictionary.items())[:5]})

# Assert city-crime relations to KB
def add_city_crimes(city, crimes):
    print("Step 3.1.4: Adding city-crime relations to KB!")
    try:
        city_norm = city.lower().replace(' ', '_')
        for crime in crimes:
            crime_norm = crime.lower().replace(' ', '_')
            prolog.assertz(f"cityCrime('{city_norm}', '{crime_norm}')")
            print(f"Step 3.1.4: Added to KB: {city_norm} committed {crime_norm}")
        print("Step 3.1.4: Finished adding city-crime relations to KB!")
    except Exception as e:
        print(f"Step 3.1.4: Oops, adding city-crime relations to KB failed: {e}")

# Query KB for city-crime relations
def query_city_crimes(city):
    print("Step 3.1.5: Querying KB for city-crime relations!")
    city_norm = city.lower().replace(' ', '_')
    try:
        result = list(prolog.query(f"cityCrimeRelation('{city_norm}', Crime)"))
        if result:
            crimes = [r['Crime'] for r in result]
            print("Step 3.1.5: KB returned crimes:", crimes)
        else:
            crimes = []
            print("Step 3.1.5: No crimes found in KB for", city_norm)
        print("Step 3.1.5: Finished querying KB!")
        return crimes
    except Exception as e:
        print(f"Step 3.1.5: Oops, city-crime query failed: {e}")
        return []

# Breadth-First Search Implementation
def bfsSearch(graph, start_city):
    print(f"Step 3.1.2: Starting BFS for city: {start_city}")
    visited = set()
    queue = [start_city]
    exploration = []

    while queue:
        node = queue.pop(0)
        if node not in visited:
            print(f"Step 3.1.2: Exploring: {node}")
            visited.add(node)
            exploration.append(node)
            if node in graph:
                for crime in sorted(graph[node]):  # Sort for consistent output
                    if crime not in visited:
                        queue.append(crime)
    print(f"Step 3.1.2: BFS completed for {start_city}")
    return exploration

# BFS Exploration for a single city
def bfs_explore(start_city="anchorage"):
    print(f"Step 3.1.1: Starting BFS exploration for crimes in {start_city}!")
    start_city = start_city.lower()
    if start_city not in crimeDictionary:
        print(f"Step 3.1.3: Error: {start_city} not in crimeDictionary!")
        return {"CityCrimes": {}, "KB_CityCrimes": []}

    exploration = bfsSearch(crimeDictionary, start_city)
    crimes = list(crimeDictionary.get(start_city, set()))
    
    # Add to KB and query
    add_city_crimes(start_city, crimes)
    kb_crimes = query_city_crimes(start_city)

    print(f"Step 3.1.3: BFS exploration completed for {start_city}!")
    return {
        "CityCrimes": {start_city: crimes},
        "KB_CityCrimes": kb_crimes
    }

# For standalone testing
if __name__ == "__main__":
    result = bfs_explore()
    print("BFS Result:", result)