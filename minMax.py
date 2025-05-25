import numpy as np
import pandas as pd

def find_risky_city():
    print("Step 3.1: Our detective AI agent is executing minMax.py!")
    # Load dataset
    dataset_path = "US_Crime_DataSet.csv"
    df = pd.read_csv(dataset_path, low_memory=False)

    # Check required columns
    required_columns = {"City", "Incident", "Crime Type", "Crime Solved"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Dataset must contain {required_columns} columns.")

    # Group data by City
    crime_stats = df.groupby("City").agg(
        total_incidents=("Incident", "count"),
        unsolved_crimes=("Crime Solved", lambda x: (x == "No").sum())
    ).reset_index()

    if crime_stats.empty:
        print("Step 3.2: No crime data available for analysis!")
        return None

    # Risk Score Calculation
    crime_stats["risk_score"] = (crime_stats["unsolved_crimes"] * 1.5) + crime_stats["total_incidents"]

    # Find highest risk city
    highest_risk_city_idx = crime_stats["risk_score"].idxmax()
    highest_risk_city = crime_stats.loc[highest_risk_city_idx, "City"]

    print(f"Step 3.2: MinMax found highest risk city: {highest_risk_city}")
    print("Step 3.2: Our detective AI agent finished executing minMax.py!")
    return highest_risk_city

# For standalone testing
if __name__ == "__main__":
    result = find_risky_city()
    if result:
        print(f"MinMax Analysis Result: Highest Risk City: {result}")