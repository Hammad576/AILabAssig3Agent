import pandas as pd
from pyswip import Prolog
import re

# Step 3.1.0: Initialize Prolog
print("Step 3.1.0: Initializing Prolog for IDDFS KB operations!")
prolog = Prolog()
prolog.consult('kb.pl')
print("Step 3.1.0: Prolog initialized with kb.pl!")

# Step 3.1.1: Load and process dataset
dataset_path = "US_Crime_DataSet.csv"
try:
    df = pd.read_csv(dataset_path, low_memory=False)
except FileNotFoundError:
    print("Step 3.1.1: Error: US_Crime_DataSet.csv not found!")
    exit()

# Verify required columns
required_columns = {"State", "Victim Race"}
if not required_columns.issubset(df.columns):
    print(f"Step 3.1.1: Error: Dataset must contain {required_columns} columns!")
    exit()

# Clean data and filter necessary columns
df = df[["State", "Victim Race"]].dropna()
df["State"] = df["State"].str.strip()
df["Victim Race"] = df["Victim Race"].str.strip()

# Debug: Print dataset info
print("Step 3.1.1: My Crime Dataset Columns:", df.columns)
print("Step 3.1.1: Unique States:", df["State"].unique()[:10].tolist())
print("Step 3.1.1: Sample Data:", df[["State", "Victim Race"]].head().to_dict())

# Build graph: State -> list of Victim Races
graph = {}
for index, row in df.iterrows():
    state = row["State"]
    race = row["Victim Race"]
    if state not in graph:
        graph[state] = []
    if race not in graph[state]:
        graph[state].append(race)
print("Step 3.1.1: Graph built:", {k: v for k, v in list(graph.items())[:5]})

# Sanitize state and race for Prolog
def sanitize_term(term):
    # Keep alphanumeric and underscores, remove other characters
    sanitized = re.sub(r'[^a-z0-9_]', '_', str(term).lower())
    sanitized = re.sub(r'_+', '_', sanitized).strip('_')
    return sanitized

# Assert victim race to KB
def add_victim_race(state, race):
    print("Step 3.1.4: Adding victim race to KB!")
    try:
        # Clear existing victimRaceFact for this state
        state_norm = sanitize_term(state)
        prolog.query(f"retractall(victimRaceFact('{state_norm}', _))")
        print("Step 3.1.4: Cleared existing victimRaceFact for state")
        race_norm = sanitize_term(race)
        prolog.assertz(f"victimRaceFact('{state_norm}', '{race_norm}')")
        print(f"Step 3.1.4: Added to KB: victimRaceFact('{state_norm}', '{race_norm}')")
        print("Step 3.1.4: Finished adding victim race to KB!")
    except Exception as e:
        print(f"Step 3.1.4: Oops, adding victim race to KB failed: {e}")

# Query KB for victim race
def query_victim_race(state):
    print("Step 3.1.5: Querying KB for victim race!")
    try:
        state_norm = sanitize_term(state)
        facts = list(prolog.query(f"victimRace('{state_norm}', Race)"))
        print(f"Step 3.1.5: Debug: Current victimRace facts: {facts}")
        if facts:
            result = [state_norm, facts[0]['Race']]
            print(f"Step 3.1.5: KB returned: {result}")
        else:
            result = []
            print("Step 3.1.5: No victim race found in KB!")
        print("Step 3.1.5: Finished querying KB!")
        return result
    except Exception as e:
        print(f"Step 3.1.5: Oops, KB query failed: {e}")
        return []

# Depth-Limited DFS
def depthLimitedDFS(graph, target_state, target_race, currentDepth, depth_limit):
    print(f"Step 3.1.2: Starting Depth-Limited DFS at depth {currentDepth} with limit {depth_limit}")
    if target_state not in graph:
        print(f"Step 3.1.2: State '{target_state}' not found in graph!")
        return False

    raceStack = []
    for race in graph[target_state]:
        raceStack.append(race)
    print(f"Step 3.1.2: Race stack for '{target_state}': {raceStack}")

    while raceStack:
        race = raceStack.pop()
        print(f"Step 3.1.2: Checking race '{race}' at depth {currentDepth}")
        if race == target_race:
            print(f"Step 3.1.2: Found '{target_race}' in '{target_state}' at depth {currentDepth}")
            return True
        currentDepth += 1
        if currentDepth > depth_limit:
            print(f"Step 3.1.2: Depth limit {depth_limit} reached, stopping search")
            return False
    print(f"Step 3.1.2: Race '{target_race}' not found in '{target_state}' at depth limit {depth_limit}")
    return False

# IDDFS search
def iddfs_search(target_state, target_race, maxDepth=5):
    print(f"Step 3.1.1: Starting IDDFS to find race '{target_race}' in state '{target_state}'")
    
    found = False
    for depth in range(maxDepth + 1):
        print(f"Step 3.1.2: Searching at Depth Limit: {depth}")
        found = depthLimitedDFS(graph, target_state, target_race, 0, depth)
        if found:
            print("Step 3.1.3: Target found using IDDFS!")
            add_victim_race(target_state, target_race)
            kb_result = query_victim_race(target_state)
            break
    if not found:
        print(f"Step 3.1.3: Race '{target_race}' not found in '{target_state}' within depth {maxDepth}")
        kb_result = []

    print("Step 3.1.3: IDDFS completed!")
    return {
        "State": target_state,
        "Race": target_race,
        "Found": found,
        "KB_Result": kb_result
    }

# For standalone testing
if __name__ == "__main__":
    result = iddfs_search("Michigan", "Black")
    print("IDDFS Result:", result)