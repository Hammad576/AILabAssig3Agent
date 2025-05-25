import pandas as pd
from pyswip import Prolog
import random
import re

# Step 3.1.0: Initialize Prolog
print("Step 3.1.0: Initializing Prolog for Hill Climbing KB operations!")
prolog = Prolog()
prolog.consult('kb.pl')
print("Step 3.1.0: Prolog initialized with kb.pl!")

# Step 3.1.1: Load the dataset
dataset_path = "US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)

# Verify required columns
if "City" not in df.columns or "Crime Type" not in df.columns:
    print("Step 3.1.1: Error: Required columns (City, Crime Type) not found in dataset!")
    exit()

# Create dictionary of city crime counts (lowercase keys)
crime_data = df.groupby(df["City"].str.lower())["Crime Type"].count().to_dict()

# Debug: Print dataset info
print("Step 3.1.1: My Crime Dataset Columns:", df.columns)
print("Step 3.1.1: Unique Cities:", list(crime_data.keys())[:10])
print("Step 3.1.1: Crime Count Sample:", {k: v for k, v in list(crime_data.items())[:5]})

# Sanitize city names for Prolog
def sanitize_city(city):
    # Keep alphanumeric and underscores, remove other characters
    sanitized = re.sub(r'[^a-z0-9_]', '_', str(city).lower())
    sanitized = re.sub(r'_+', '_', sanitized).strip('_')
    return sanitized

# Assert most criminal city to KB
def add_criminal_city(city, count):
    print("Step 3.1.4: Adding most criminal city to KB!")
    try:
        # Clear existing mostCriminalCity facts
        prolog.query("retractall(mostCriminalCity(_, _))")
        print("Step 3.1.4: Cleared existing mostCriminalCity facts")
        city_norm = sanitize_city(city)
        prolog.assertz(f"mostCriminalCity('{city_norm}', {count})")
        print(f"Step 3.1.4: Added to KB: mostCriminalCity('{city_norm}', {count})")
        print("Step 3.1.4: Finished adding most criminal city to KB!")
    except Exception as e:
        print(f"Step 3.1.4: Oops, adding most criminal city to KB failed: {e}")

# Query KB for most criminal city
def query_criminal_city():
    print("Step 3.1.5: Querying KB for most criminal city!")
    try:
        # Debug: List all mostCriminalCity facts
        facts = list(prolog.query("mostCriminalCity(City, Count)"))
        print(f"Step 3.1.5: Debug: Current mostCriminalCity facts: {facts}")
        if facts:
            result = [facts[0]['City'], facts[0]['Count']]
            print(f"Step 3.1.5: KB returned: {result}")
        else:
            result = []
            print("Step 3.1.5: No most criminal city found in KB!")
        print("Step 3.1.5: Finished querying KB!")
        return result
    except Exception as e:
        print(f"Step 3.1.5: Oops, KB query failed: {e}")
        return []

# Hill Climbing algorithm
def hill_climbing(start_city):
    print(f"Step 3.1.2: Starting Hill Climbing from {start_city}")
    current_city = start_city.lower()
    current_crime_count = crime_data.get(current_city, 0)
    iteration = 0
    max_iterations = 50  # Prevent infinite loops

    print(f"Step 3.1.2: Iteration {iteration}: At {current_city} with {current_crime_count} crimes")

    while iteration < max_iterations:
        # Get neighbors (random sample for simplicity, max 5)
        neighbors = random.sample(list(crime_data.keys()), min(5, len(crime_data)))
        best_neighbor = current_city
        best_crime_count = current_crime_count

        # Evaluate neighbors
        for neighbor in neighbors:
            neighbor = neighbor.lower()
            neighbor_crime_count = crime_data.get(neighbor, 0)
            if neighbor_crime_count > best_crime_count:
                best_neighbor = neighbor
                best_crime_count = neighbor_crime_count

        # Check if local maximum reached
        if best_neighbor == current_city:
            print(f"Step 3.1.2: Local maximum reached at {current_city} with {current_crime_count} crimes")
            return current_city, current_crime_count

        # Move to best neighbor
        iteration += 1
        current_city = best_neighbor
        current_crime_count = best_crime_count
        print(f"Step 3.1.2: Iteration {iteration}: Moving to {current_city} with {current_crime_count} crimes")

    print(f"Step 3.1.2: Stopped: Reached max iterations ({max_iterations})")
    return current_city, current_crime_count

# Main Hill Climbing function
def hill_climbing_search(start_city=None):
    print("Step 3.1.1: Starting Hill Climbing to find the most criminal city!")
    # Pick random start city if none provided
    if start_city is None:
        start_city = random.choice(list(crime_data.keys()))
    start_city = start_city.lower()
    print(f"Step 3.1.1: Debug: Selected start city: {start_city}")

    if start_city not in crime_data:
        print(f"Step 3.1.3: Error: Start city {start_city} not in crime data!")
        return {"City": None, "CrimeCount": 0, "KB_Result": []}

    # Run Hill Climbing
    city, crime_count = hill_climbing(start_city)

    if city:
        add_criminal_city(city, crime_count)
        kb_result = query_criminal_city()
    else:
        kb_result = []

    print("Step 3.1.3: Hill Climbing completed!")
    return {"City": city, "CrimeCount": crime_count, "KB_Result": kb_result}

# For standalone testing
if __name__ == "__main__":
    result = hill_climbing_search()
    print("Hill Climbing Result:", result)