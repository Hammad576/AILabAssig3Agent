import pandas as pd
from pyswip import Prolog
import re

# Initialize Prolog
print("Step 3.1.0: Initializing Prolog for GBFS KB operations!")
prolog = Prolog()
prolog.consult('kb.pl')
print("Step 3.1.0: Prolog initialized with kb.pl!")

# Load the dataset
dataset_path = "US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)

# Display dataset columns
print("My Crime Dataset Columns:", df.columns)

# Debug: Print unique City and State values
print("Unique Cities:", df['City'].str.strip().str.lower().unique()[:10])
print("Unique States:", df['State'].str.strip().str.lower().unique()[:10])

# Build the Graph
crimeGraph = {}
city_state_map = {}
if "City" in df.columns and "State" in df.columns:
    for _, row in df.iterrows():
        city = str(row["City"]).strip().lower()
        state = str(row["State"]).strip().lower()
        if not city or not state:
            print(f"Debug: Skipping row - City: {city}, State: {state}")
            continue
        if city not in city_state_map:
            city_state_map[city] = state
        else:
            print(f"Debug: Duplicate city {city}: existing state {city_state_map[city]}, new state {state}")
            # Prioritize Alaska for known cities
            if city in ['anchorage', 'juneau'] and state == 'alaska':
                city_state_map[city] = state
else:
    print("Error: 'City' or 'State' column missing!")

# Link cities within the same state
state_city_map = {}
for city, state in city_state_map.items():
    if state not in state_city_map:
        state_city_map[state] = set()
    state_city_map[state].add(city)

for state, cities in state_city_map.items():
    for city in cities:
        if city not in crimeGraph:
            crimeGraph[city] = {}
        for neighbor in cities:
            if city != neighbor:
                crimeGraph[city][neighbor] = 1  # Dummy distance

# Debug: Print city_state_map and crimeGraph samples
print("City-State Map Sample:", {k: v for k, v in list(city_state_map.items())[:5]})
print("Crime Graph Sample:", {k: list(v.keys())[:5] for k, v in list(crimeGraph.items())[:5]})
print(f"Debug: anchorage state: {city_state_map.get('anchorage')}")
print(f"Debug: juneau state: {city_state_map.get('juneau')}")

# Sanitize city names for Prolog
def sanitize_city(city):
    # Keep alphanumeric and underscores, remove other characters
    sanitized = re.sub(r'[^a-z0-9_]', '_', city.lower())
    # Ensure no double underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    return sanitized

# Assert path cities to KB
def add_path_cities(path):
    print("Step 3.1.4: Adding path cities to KB!")
    try:
        # Clear existing pathCity facts
        prolog.query("retractall(pathCity(_, _))")
        print("Step 3.1.4: Cleared existing pathCity facts")
        for i in range(len(path) - 1):
            city1 = sanitize_city(path[i])
            city2 = sanitize_city(path[i + 1])
            prolog.assertz(f"pathCity('{city1}', '{city2}')")
            print(f"Step 3.1.4: Added to KB: {city1} → {city2}")
        print("Step 3.1.4: Finished adding path cities to KB!")
    except Exception as e:
        print(f"Step 3.1.4: Oops, adding path cities to KB failed: {e}")

# Query KB for path
def query_path(start_city, goal_city):
    print("Step 3.1.5: Querying KB for path!")
    start_norm = sanitize_city(start_city)
    goal_norm = sanitize_city(goal_city)
    query = f"searchPath('{start_norm}', '{goal_norm}', Path)"
    print(f"Step 3.1.5: Debug: start_norm={start_norm}, goal_norm={goal_norm}, query={query}")
    try:
        # Debug: List all pathCity facts
        path_city_facts = list(prolog.query("pathCity(X, Y)"))
        print(f"Step 3.1.5: Debug: Current pathCity facts: {path_city_facts}")
        result = list(prolog.query(query))
        if result:
            path = result[0]['Path']
            print("Step 3.1.5: KB returned path:", path)
        else:
            path = []
            print("Step 3.1.5: No path found in KB!")
        print("Step 3.1.5: Finished querying KB!")
        return path
    except Exception as e:
        print(f"Step 3.1.5: Oops, path query failed: {e}")
        return []

# Greedy Best-First Search
def greedyBestFirstSearch(graph, start, goal):
    print(f"Step 3.1.2: Starting GBFS from {start} to {goal}")
    openSet = [start]
    came_from = {}
    visited = set()  # Track all visited nodes to prevent cycles
    iteration = 0
    max_iterations = 100  # Limit to prevent crashes
    max_path_length = 10  # Cap path length

    while openSet:
        current = openSet.pop(0)
        print(f"Step 3.1.2: Iteration {iteration}: Exploring {current}, openSet size: {len(openSet)}")

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            path = []
            path_length = 0
            while current in came_from:
                path.append(current)
                current = came_from[current]
                path_length += 1
                if path_length > max_path_length:
                    print("Step 3.1.2: Path too long, abandoning")
                    return []
            path.append(start)
            path.reverse()
            print(f"Step 3.1.2: Path found: {' → '.join(path)}")
            return path

        if current not in graph:
            print(f"Step 3.1.2: No neighbors for {current}")
            continue

        # Sort neighbors alphabetically for deterministic greedy choice
        neighbors = sorted(graph[current].keys())
        for neighbor in neighbors:
            if neighbor not in visited and neighbor not in came_from:
                openSet.append(neighbor)
                came_from[neighbor] = current
                print(f"Step 3.1.2: Added neighbor {neighbor}")

        iteration += 1
        if iteration >= max_iterations:
            print(f"Step 3.1.2: Stopping: Reached max iterations ({max_iterations})")
            return []

    print(f"Step 3.1.2: No path found from {start} to {goal}")
    return []

# GBFS Search Wrapper
def greedy_best_first_search(start_city="anchorage", goal_city="juneau"):
    print(f"Step 3.1.1: Starting GBFS to find path from {start_city} to {goal_city}!")
    start_city = start_city.lower()
    goal_city = goal_city.lower()

    # Check if cities are in the same state
    start_state = city_state_map.get(start_city)
    goal_state = city_state_map.get(goal_city)
    if start_state != goal_state:
        print(f"Step 3.1.1: Warning: {start_city} ({start_state}) and {goal_city} ({goal_state}) are in different states!")
        # Fallback to cities in Alaska
        alaska_cities = [city for city, state in city_state_map.items() if state == 'alaska']
        if len(alaska_cities) >= 2:
            start_city, goal_city = sorted(alaska_cities)[:2]
            print(f"Step 3.1.1: Fallback to cities in Alaska: {start_city} → {goal_city}")
        else:
            print("Step 3.1.1: Error: Not enough cities in Alaska for fallback")
            return {"Path": [], "KB_Path": []}

    if start_city not in crimeGraph or goal_city not in crimeGraph:
        print(f"Step 3.1.3: Error: One or both cities not in crimeGraph: {start_city}, {goal_city}")
        return {"Path": [], "KB_Path": []}

    path = greedyBestFirstSearch(crimeGraph, start_city, goal_city)
    
    if path:
        add_path_cities(path)
        kb_path = query_path(start_city, goal_city)
    else:
        kb_path = []

    print("Step 3.1.3: GBFS completed!")
    return {"Path": path, "KB_Path": kb_path}

# For standalone testing
if __name__ == "__main__":
    result = greedy_best_first_search()
    print("GBFS Result:", result)