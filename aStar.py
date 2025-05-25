import pandas as pd

# Load the dataset
dataset_path = "US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)

# Display dataset columns
print("My Crime Dataset Columns:", df.columns)

# Creating a graph where cities are linked based on crime data
crimeGraph = {}
heuristic = {}

# Step 1: Build the Graph
if "City" in df.columns and "State" in df.columns:
    city_state_map = {}
    for _, row in df.iterrows():
        city = str(row["City"]).strip()
        state = str(row["State"]).strip()
        if city and state:
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

# Debugging
print("Cities added to crimeGraph:", list(crimeGraph.keys())[:10])

# Step 2: A* Search Algorithm
def aStarSearch(graph, start, goal):
    openSet = [(0, start)]  # (f(n), city)
    came_from = {}
    gScore = {city: float('inf') for city in graph}
    gScore[start] = 0
    iteration = 0

    while openSet:
        openSet.sort()
        current_cost, current = openSet.pop(0)
        print(f"Iteration {iteration}: Exploring {current} with cost {current_cost}")

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            print("Path found from", start, "to", goal)
            print("Path:", " → ".join(path))
            return path  # Return the path

        if current not in graph:
            continue

        for neighbor in graph[current]:
            temp_gScore = gScore[current] + graph[current][neighbor]
            if temp_gScore < gScore[neighbor]:
                gScore[neighbor] = temp_gScore
                priority = temp_gScore + heuristic.get(neighbor, 0)
                openSet.append((priority, neighbor))
                came_from[neighbor] = current

        iteration += 1
        if iteration > 500:
            print("Stopping: Too many iterations (possible infinite loop)")
            break

    print("No path found from", start, "to", goal)
    return None

# Note: Removed redundant execution, path is returned by function