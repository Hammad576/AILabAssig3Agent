# we need to find the most criminal city using Hill climbing
import pandas as pd
import random

# Step 1: Load the dataset
dataset_path = "../US_Crime_DataSet.csv"  # Adjust the path if needed
df = pd.read_csv(dataset_path, low_memory=False)

# Step 2: Ensure required columns exist
if "City" not in df.columns or "Crime Type" not in df.columns:
    print("Error: Required columns (City, Crime Type) not found in dataset.")
    exit()

# Step 3: Create a dictionary where cities are mapped to their crime count
crime_data = df.groupby("City")["Crime Type"].count().to_dict()

# Step 4: Define the Hill Climbing function
def hill_climbing(start_city):
    current_city = start_city  # Start from a random city
    current_crime_count = crime_data.get(current_city, 0)

    #printing our current city and crimes of city
    print(f"Starting at: {current_city} with {current_crime_count} crimes")

    while True:
        # Step 5: Find neighboring cities (random selection for simplicity)
        neighbors = random.sample(list(crime_data.keys()), min(5, len(crime_data)))  # Pick 5 random neighbors
        best_neighbor = current_city
        best_crime_count = current_crime_count
    # Here we got 5 neighbors for our ease
    # But in simple Hill Climbing we will iterate through each niehgbor
    # and find teh less heuristic neighbor
        for neighbor in neighbors:
            neighbor_crime_count = crime_data.get(neighbor, 0)
            if neighbor_crime_count > best_crime_count:  # Move to a city with a higher crime rate
                best_neighbor = neighbor
                best_crime_count = neighbor_crime_count

        # Step 6: If no better neighbor is found, stop (local maximum reached)
        if best_neighbor == current_city:
            print(f"Local maximum reached at: {current_city} with {current_crime_count} crimes")
            return current_city, current_crime_count

        # Step 7: Move to the best neighbor
        print(f"Moving to: {best_neighbor} with {best_crime_count} crimes")
        current_city = best_neighbor
        current_crime_count = best_crime_count

# Step 8: Pick a random starting city using random python function
random_start_city = random.choice(list(crime_data.keys()))
hill_climbing(random_start_city)
