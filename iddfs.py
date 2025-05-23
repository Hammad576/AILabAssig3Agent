import pandas as pd

# Load dataset
dataset_path = "../US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)

# Clean data and filter necessary columns
df = df[["State", "Victim Race"]].dropna()
df["State"] = df["State"].str.strip()
df["Victim Race"] = df["Victim Race"].str.strip()

# Group data by State -> list of Victim Races
graph = {}
for index, row in df.iterrows():
    state = row["State"]
    race = row["Victim Race"]
    if state not in graph:
        graph[state] = []
    if race not in graph[state]:
        graph[state].append(race)

print("After executing this, our Graph Looks like this:", graph)

# The function to implement IDDFS
def depthLimitedDFS(graph, targetState, target_race, currentDepth, depth_limit):
   
    
       
    raceStack =[]
    for race in graph[targetState]:
            # Create a quee of  target State Races
            #Implementing the IDDFS by DFS with depth Limit Restriction
        raceStack.append(race)
            
        print("The Race Stack of the Target State is:",raceStack)
    while raceStack:
        race=raceStack.pop()
        print("We are at depth: ",currentDepth)    
        if race == target_race:
            print(f"Found '{target_race}' in '{targetState}' at depth {currentDepth}")
            return True
            
            print("Current Depth:",currentDepth)
            print("The maximum Depth is:",depth_limit)
        currentDepth+=1 
        if currentDepth>depth_limit:
               
            print("We did not found the particular Race at depth Limit. TRy to increase the depth") 

       
       

    return False

# IDDFS function
def iddfs(graph, target_state, target_race,currentDepth, maxDepth):
    for depth in range(maxDepth + 1):
        print(f"\n--- Searching at Depth Limit: {depth} ---")
        found = depthLimitedDFS(graph, target_state, target_race, currentDepth, depth)
        if found:
            print("Target found using IDDFS.")
            return
    print("Target not found within the given depth. Try increasing depth.")

# Run the IDDFS search
target_state = "Michigan"
target_race = "Black"
currentDepth=0
maxDepth = 5
iddfs(graph, target_state, target_race,currentDepth, maxDepth)
