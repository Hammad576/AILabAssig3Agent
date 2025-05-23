import pandas as pd
#For greedy fn=h(n). only heuristic consider
# Load the dataset
dataset_path = "../US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)

# Display dataset columns
print("My Crime Dataset Columns:", df.columns)

# Creating a graph where cities are linked based on crime data
crimeGraph = {}

# Step 1: Build the Graph
# -------------------------
# This part ensures that cities within the same state are linked together.

if "City" in df.columns and "State" in df.columns:
    city_state_map = {}

    # Group cities by state
    for _, row in df.iterrows():
        city = str(row["City"]).strip()
        state = str(row["State"]).strip()

        if city and state:
            if state not in city_state_map:
                city_state_map[state] = set()
            city_state_map[state].add(city)

    # Link cities within the same state
    for state, cities in city_state_map.items():
        for city in cities:
            if city not in crimeGraph:
                crimeGraph[city] = {}

            for neighbor in cities:
                if city != neighbor:
                    crimeGraph[city][neighbor] = 1  # Assign dummy distance of 1

# Debugging: Print sample cities added to graph
print("Cities added to crimeGraph:", list(crimeGraph.keys())[:10])


# Step 2: Greedy Best-First Search (GBFS) Algorithm
# ------------------------------------------------
# This function finds the shortest path using GBFS.

def greedyBestFirstSearch(graph, start, goal):
    openSet = [start]  # List-based priority queue (only stores nodes to explore)
    came_from = {}  # Dictionary to store path history
    
    iteration = 0  # Track loop iterations

    while openSet:
        current = openSet.pop(0)  # Always pick the first node (greedy approach)

        print(f"Iteration {iteration}: Exploring {current}")  # Debugging

        # If goal is reached, reconstruct and print the path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()  # Reverse the path to show it from start to goal
            
            print(" Path found from", start, "to", goal)
            print(" Path:", " → ".join(path))
            return

        # If no neighbors, continue
        if current not in graph:
            continue  

        # Explore neighbors (Greedy approach - pick first available)
        # In our case we are picking the first availible neighbor
        # consider that it has the best availible huerisitc
        # no track of where we came from 
        for neighbor in graph[current]:
            if neighbor not in came_from:  # Avoid cycles
                openSet.append(neighbor)
                came_from[neighbor] = current  # Track the path

        iteration += 1
        if iteration > 500:  # Stop if too many iterations (possible infinite loop) due to my pc limitations
            print("Stopping: Too many iterations (possible infinite loop)")
            break

    print(" No path found from", start, "to", goal)


# Step 3: Run GBFS Algorithm with Example Cities
# ----------------------------------------------
start_city = "Anchorage"
goal_city = "Jefferson"

if start_city in crimeGraph and goal_city in crimeGraph:
    greedyBestFirstSearch(crimeGraph, start_city, goal_city)
else:
    print(f"Error: One or both cities not found in dataset: {start_city}, {goal_city}")
