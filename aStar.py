import pandas as pd
from pyswip import Prolog

# Initialize Prolog
print("Step 3.1.0: Initializing Prolog for A* KB operations!")
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
print("Unique States:", df['State'].str.strip().str.lower().unique())

# Creating a graph where cities are linked based on crime data
crimeGraph = {}
heuristic = {}

# Step 1: Build the Graph
if "City" in df.columns and "State" in df.columns:
    city_state_map = {}
    for _, row in df.iterrows():
        city = str(row["City"]).strip().lower()
        state = str(row["State"]).strip().lower()
        if not city or not state:
            print(f"Debug: Skipping row - City: {city}, State: {state}")
            continue
        if state not in city_state_map:
            city_state_map[state] = set()
        city_state_map[state].add(city)
    for state, cities in city_state_map.items():
        for city in cities:
            if city not in crimeGraph:
                crimeGraph[city] = {}
                heuristic[city] = len(state)  # Example heuristic
            for neighbor in cities:
                if city != neighbor:
                    crimeGraph[city][neighbor] = 1  # Dummy distance
else:
    print("Error: 'City' or 'State' column missing!")

# Debugging
print("Cities added to crimeGraph:", list(crimeGraph.keys())[:10])

# Assert search path to KB
def add_search_path(path):
    print("Step 3.1.4: Adding search path to KB!")
    try:
        for i in range(len(path) - 1):
            city1 = path[i].lower().replace(' ', '_')
            city2 = path[i + 1].lower().replace(' ', '_')
            prolog.assertz(f"connectedCities('{city1}', '{city2}')")
            print(f"Step 3.1.4: Added path segment to KB: {city1} to {city2}")
        print("Step 3.1.4: Finished adding search path to KB!")
    except Exception as e:
        print(f"Step 3.1.4: Oops, adding search path to KB failed: {e}")

# Query KB for path
def query_path(start, goal):
    print("Step 3.1.5: Querying KB for search path!")
    start_norm = start.lower()
    goal_norm = goal.lower()
    try:
        result = list(prolog.query(f"searchPath('{start_norm}', '{goal_norm}', Path)"))
        if result:
            print("Step 3.1.5: KB returned path(s):")
            for r in result:
                print(f"  - Path: {r['Path']}")
            print("Step 3.1.5: Finished querying KB for path!")
            return result[0]['Path'] if result else None
        else:
            print("Step 3.1.5: No path found in KB!")
            print("Step 3.1.5: Finished querying KB for path!")
            return None
    except Exception as e:
        print(f"Step 3.1.5: Oops, path query failed: {e}")
        return None

# Step 2: A* Search Algorithm
def aStarSearch(start, goal):
    print(f"Step 3.1.1: Starting A* search from {start} to {goal}!")
    
    start = start.lower()
    goal = goal.lower()
    
    if start not in crimeGraph or goal not in crimeGraph:
        print(f"Step 3.1.2: Error: Start ({start}) or Goal ({goal}) not in crimeGraph!")
        return None
    
    openSet = [(0, start)]  # (f(n), city)
    came_from = {}
    gScore = {city: float('inf') for city in crimeGraph}
    gScore[start] = 0
    iteration = 0

    while openSet:
        openSet.sort()
        current_cost, current = openSet.pop(0)
        print(f"Step 3.1.2: Iteration {iteration}: Exploring {current} with cost {current_cost}")

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            print(f"Step 3.1.3: Path found: {' → '.join(path)}")
            
            # Add path to KB and query
            add_search_path(path)
            kb_path = query_path(start, goal)
            
            print(f"Step 3.1.3: A* search completed!")
            return {"Path": path, "KB_Path": kb_path}
        
        for neighbor in crimeGraph[current]:
            temp_gScore = gScore[current] + crimeGraph[current][neighbor]
            if temp_gScore < gScore[neighbor]:
                gScore[neighbor] = temp_gScore
                priority = temp_gScore + heuristic.get(neighbor, 0)
                openSet.append((priority, neighbor))
                came_from[neighbor] = current

        iteration += 1
        if iteration > 500:
            print("Step 3.1.3: Stopping: Too many iterations!")
            break

    print(f"Step 3.1.3: No path found from {start} to {goal}!")
    return None

# For standalone testing
if __name__ == "__main__":
    start_city = "juneau"
    goal_city = "bethel"
    result = aStarSearch(start_city, goal_city)
    if result:
        print("A* Result:", result)