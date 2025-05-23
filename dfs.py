import pandas as pd

# Load the dataset 
dataset_path = "../US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)  

# Display All my dataset Columns
print("My Crime Dataset Columns:", df.columns)

# Creating a dictionary where only 'Black' race is linked to detailed crime information   ss
crime_graph = {}

# Ensure required columns exist
if "Perpetrator Race" in df.columns and "Crime Type" in df.columns and "Weapon" in df.columns and "Crime Solved" in df.columns:
    for _, row in df.iterrows():
        suspect_race = str(row["Perpetrator Race"]).strip()
        crime_type = str(row["Crime Type"]).strip()
        weapon_used = str(row["Weapon"]).strip()
        crime_solved = str(row["Crime Solved"]).strip()
        
        if suspect_race == "Black" and crime_type and weapon_used and crime_solved:
            if suspect_race not in crime_graph:
                crime_graph[suspect_race] = {
                    "Crimes": set(),
                    "Weapons Used": set(),
                    "Crime Solved Status": {"Yes": 0, "No": 0}
                }
            
            crime_graph[suspect_race]["Crimes"].add(crime_type)
            crime_graph[suspect_race]["Weapons Used"].add(weapon_used)
            
            if crime_solved == "Yes":
                crime_graph[suspect_race]["Crime Solved Status"]["Yes"] += 1
            else:
                crime_graph[suspect_race]["Crime Solved Status"]["No"] += 1

# Depth-First Search (DFS) Implementation using Stack
def dfs_search(graph, start_node):
    visited = set()
    stack = [start_node]
    
    print(f"Finding detailed crime information for suspect Race: {start_node} using DFS:\n")
    
    while stack:
        node = stack.pop()  # Removing the last added element (LIFO - Stack behavior)
        if node not in visited:
            print("Exploring Suspect Race:", node)
            visited.add(node)
            
            if node in graph:
                print("\nTypes of Crimes Committed:", ", ".join(graph[node]["Crimes"]))
                print("Weapons Used:", ", ".join(graph[node]["Weapons Used"]))
                print("Crime Solved Status:")
                print("   - Solved:", graph[node]["Crime Solved Status"]["Yes"])
                print("   - Unsolved:", graph[node]["Crime Solved Status"]["No"])
                print("-------------------------------------------------")
                
                for neighbor in graph.keys():
                    if neighbor not in visited:
                        stack.append(neighbor)

# Example usage: Track crimes committed by 'Black' race
suspectRace = "Black" 

if suspectRace in crime_graph:
    dfs_search(crime_graph, suspectRace)
else:
    print("Error: No crimes found for suspect Race:", suspectRace)
