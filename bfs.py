import pandas as pd

# Load the dataset  
dataset_path = "../US_Crime_DataSet.csv"

# Store the Data Set content in df
df = pd.read_csv(dataset_path, low_memory=False)

# Displaying my data set Columns
print("Dataset Columns:", df.columns)

# Creating a dictionary where key is city and values are the crimes that occurred in that city
crimeDictionary = {}

if "City" in df.columns and "Crime Type" in df.columns:
    for _, row in df.iterrows():
        city = str(row["City"]).strip()
        crime_type = str(row["Crime Type"]).strip()
        
        # Ensure we only add edges between city and its crime types
        if city and crime_type and city.lower() != crime_type.lower():
            if city not in crimeDictionary:
                crimeDictionary[city] = set()  # Use set to store unique crimes
            crimeDictionary[city].add(crime_type)

# Breadth-First Search (BFS) Implementation
def bfsSearch(graph, start_city):
    visited = set()  # Maintain a separate visited set for each city to capture the unique crime of each city
    queue = [start_city]

    

    while queue:
        node = queue.pop(0)  # Dequeue first element
        if node not in visited:
            print("Exploring:", node)
            visited.add(node)  # Mark node as visited
            
            # Explore unique crimes in this city
            if node in graph:
                for crime in graph[node]:
                    if crime not in visited:
                        queue.append(crime)

# Start BFS for each city separately
for city in crimeDictionary:
    bfsSearch(crimeDictionary, city)
