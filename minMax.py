import numpy as np
import pandas as pd

# Load dataset (Your dataset import logic remains unchanged)
dataset_path = "../US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)  

# Check if required columns exist
required_columns = {"City", "Incident", "Crime Type", "Crime Solved"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Dataset must contain {required_columns} columns.")

# Group data by City to analyze crime frequency
crime_stats = df.groupby("City").agg(
    total_incidents=("Incident", "count"),  # Count total crimes per city
    unsolved_crimes=("Crime Solved", lambda x: (x == "No").sum())  
    # Just Counting the  unresolved cases all NO are counted as one
).reset_index()


#We are implementing the MIN Max The Criminals are (Minimizers) try to find the ways to commit crimes
# where polic deployement is less to commit crime
# We Police are (Maximizers). We will increase our Reward
# Check if the dataset contains valid data
if crime_stats.empty:
    print("No crime data available for analysis.")
else:
    # Implementing Min-Max logic
    # Risk Score Calculation: We assign more weight to unresolved crimes to prioritize them
    crime_stats["risk_score"] = (crime_stats["unsolved_crimes"] * 1.5) + (crime_stats["total_incidents"])

    # Find cities based on Minimax logic
    least_policed_city_idx = crime_stats["unsolved_crimes"].idxmax()   # Criminals' best move (Min)
    most_crime_city_idx = crime_stats["total_incidents"].idxmax()       # Police's best move (Max)
    highest_risk_city_idx = crime_stats["risk_score"].idxmax()          # Most dangerous city (considering both factors)

    # Extract city names
    least_policed_city = crime_stats.loc[least_policed_city_idx, "City"]
    most_crime_city = crime_stats.loc[most_crime_city_idx, "City"]
    highest_risk_city = crime_stats.loc[highest_risk_city_idx, "City"]

    # Displaying clear and structured results
    print("\nCrime Prediction and Police Deployment Analysis")
    print(f"1. Predicted Crime City (where criminals may move due to low police action): {least_policed_city}")
    
    print(f"3. Highest Risk City (Due to Unresolved Cases because We Police are Maximizers): {least_policed_city}")
    