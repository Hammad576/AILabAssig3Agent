import pandas as pd

# Load the dataset
dataset_path = "../US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)

# Display dataset columns
print("My Crime Dataset Columns:", df.columns)

# Creating a graph where cities are linked based on crime data
crimeGraph = {}
heuristic = {}

# Step 1: Build the Graph
# -------------------------
# This part ensures that cities within the same state are linked together.

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
                heuristic[city] = len(state)  # Example heuristic: length of state name

            for neighbor in cities:
                if city != neighbor:
                    crimeGraph[city][neighbor] = 1  # Assign dummy distance of 1

# Debugging Print statement
print("Cities added to crimeGraph:", list(crimeGraph.keys())[:10])


# Step 2: A* Search Algorithm Implementation
# ------------------------------------------
# This part finds the shortest path between two cities using A* search.

def aStarSearch(graph, start, goal):
    openSet = [(0, start)]  # List-based priority queue (f(n), city)
    came_from = {}  # Dictionary to store path history
    gScore = {city: float('inf') for city in graph}  
    # Initialize gScore
    gScore[start] = 0
    
    iteration = 0  # To track loop iterations

    while openSet:
        openSet.sort()  # Sort list to get node with lowest cost (f(n) = g(n) + h(n))
        current_cost, current = openSet.pop(0)  # Get node with lowest cost
        
        print(f"Iteration {iteration}: Exploring {current} with cost {current_cost}")  # Debugging

        # If goal is reached, reconstruct and print the path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()  # Reverse the path to show it from start to goal
            
            print("Path found from", start, "to", goal)
            print("Path:", " → ".join(path))
            return

        # If no neighbors, continue
        if current not in graph:
            continue  

        for neighbor in graph[current]:
            temp_gScore = gScore[current] + graph[current][neighbor]

            if temp_gScore < gScore[neighbor]:  # If a better path is found
                gScore[neighbor] = temp_gScore
                priority = temp_gScore + heuristic.get(neighbor, 0)  # f(n) = g(n) + h(n)
                openSet.append((priority, neighbor))
                came_from[neighbor] = current  # Track the path

        iteration += 1
        if iteration > 500:  # Stop if too many iterations (possible infinite loop)
            print("Stopping: Too many iterations (possible infinite loop)")
            break

    print(" No path found from", start, "to", goal)


# Step 3: Runing A* Algorithm with Example Cities
# --------------------------------------------
start_city = "Anchorage"
goal_city = "Jefferson"

if start_city in crimeGraph and goal_city in crimeGraph:
    aStarSearch(crimeGraph, start_city, goal_city)
else:
    print(f"Error: One or both cities not found in dataset: {start_city}, {goal_city}")
