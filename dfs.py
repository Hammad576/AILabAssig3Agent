import pandas as pd
from pyswip import Prolog

# Initialize Prolog
print("Step 3.1.0: Initializing Prolog for DFS KB operations!")
prolog = Prolog()
prolog.consult('kb.pl')
print("Step 3.1.0: Prolog initialized with kb.pl!")

# Load the dataset 
dataset_path = "US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)  

# Display dataset columns
print("My Crime Dataset Columns:", df.columns)

# Debug: Print unique Perpetrator Race values
print("Unique Perpetrator Race values:", df['Perpetrator Race'].str.strip().str.lower().unique())

# Creating a dictionary for 'Black' race crime information
crime_graph = {}

# Ensure required columns exist
if all(col in df.columns for col in ["Perpetrator Race", "Crime Type", "Weapon", "Crime Solved"]):
    for _, row in df.iterrows():
        suspect_race = str(row["Perpetrator Race"]).strip().lower()
        crime_type = str(row["Crime Type"]).strip()
        weapon_used = str(row["Weapon"]).strip()
        crime_solved = str(row["Crime Solved"]).strip()
        
        # Debug: Print row data if race is 'black'
        if suspect_race == "black":
            print(f"Debug: Row with Black race - Crime: {crime_type}, Weapon: {weapon_used}, Solved: {crime_solved}")
        
        if suspect_race == "black" and crime_type and weapon_used and crime_solved:
            if suspect_race not in crime_graph:
                crime_graph[suspect_race] = {
                    "Crimes": set(),
                    "Weapons Used": set(),
                    "Crime Solved Status": {"Yes": 0, "No": 0}
                }
            
            crime_graph[suspect_race]["Crimes"].add(crime_type)
            crime_graph[suspect_race]["Weapons Used"].add(weapon_used)
            
            if crime_solved.lower() == "yes":
                crime_graph[suspect_race]["Crime Solved Status"]["Yes"] += 1
            else:
                crime_graph[suspect_race]["Crime Solved Status"]["No"] += 1
else:
    print("Error: Required columns missing in dataset!")

# Debug: Print crime_graph
print("Debug: crime_graph after population:", crime_graph)

# Assert race-based crimes to KB
def add_race_crimes(race, crimes):
    print("Step 3.1.4: Adding race-based crimes to KB!")
    try:
        race_norm = race.lower()
        for crime in crimes:
            crime_norm = crime.lower().replace(' ', '_')
            prolog.assertz(f"raceCrimeFact('{race_norm}', '{crime_norm}')")
            print(f"Step 3.1.4: Added crime to KB: {race_norm} committed {crime_norm}")
        print("Step 3.1.4: Finished adding race-based crimes to KB!")
    except Exception as e:
        print(f"Step 3.1.4: Oops, adding race crimes to KB failed: {e}")

# Query KB for race crimes
def query_race_crimes(race):
    print("Step 3.1.5: Querying KB for race-based crimes:")
    try:
        result = list(prolog.query(f"raceCrime('{race.lower()}', Crime)"))
        if result:
            print("Step 3.1.5: KB returned race crimes:")
            for r in result:
                print(f"  - Crime: {r['Crime']}")
        else:
            print("Step 3.1.5: No race crimes found in KB:")
        print("Step 3.1.5: Finished querying KB for race crimes:")
        return result
    except Exception as e:
        print(f"Step 3.1.5: Oops, race crime query failed: {e}")
        return []

# Depth-First Search (DFS) Implementation
def dfs_search(start_node):
    print(f"Step 3.1.1: Starting DFS for suspect Race: {start_node}!")
    
    if start_node.lower() not in crime_graph:
        print(f"Step 3.1.2: Error: No crimes found for suspect Race: {start_node}")
        return None
    
    node = start_node.lower()
    print(f"Step 3.1.2: Exploring Suspect Race: {node}")
    print("Types of Crimes Committed:", ", ".join(crime_graph[node]["Crimes"]))
    print("Weapons Used:", ", ".join(crime_graph[node]["Weapons Used"]))
    print("Crime Solved Status:")
    print("   - Solved:", crime_graph[node]["Crime Solved Status"]["Yes"])
    print("   - Unsolved:", crime_graph[node]["Crime Solved Status"]["No"])
    print("-------------------------------------------------")
    
    # Add crimes to KB
    crimes = list(crime_graph[node]["Crimes"])
    if crimes:
        add_race_crimes(node, crimes)
        kb_crimes = query_race_crimes(node)
    else:
        print("Step 3.1.3: No crimes to add to KB!")
        kb_crimes = []
    
    print(f"Step 3.1.3: DFS completed for suspect Race: {start_node}!")
    return {"Crimes": crimes, "KB_Crimes": kb_crimes}

# For standalone testing
if __name__ == "__main__":
    suspect_race = "Black"
    result = dfs_search(suspect_race)
    if result:
        print("DFS Result:", result)