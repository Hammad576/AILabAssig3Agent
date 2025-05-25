import pandas as pd
from pyswip import Prolog
import re

# Step 3.1.0: Initialize Prolog
print("Step 3.1.0: Initializing Prolog for MinMax KB operations!")
prolog = Prolog()
prolog.consult('kb.pl')
print("Step 3.1.0: Prolog initialized with kb.pl!")

# Step 3.1.1: Load the dataset
dataset_path = "US_Crime_DataSet.csv"
try:
    df = pd.read_csv(dataset_path, low_memory=False)
except FileNotFoundError:
    print("Step 3.1.1: Error: US_Crime_DataSet.csv not found!")
    exit()

# Verify required columns
required_columns = {"City", "Incident", "Crime Type", "Crime Solved"}
if not required_columns.issubset(df.columns):
    print(f"Step 3.1.1: Error: Dataset must contain {required_columns} columns!")
    exit()

# Debug: Print dataset info
print("Step 3.1.1: My Crime Dataset Columns:", df.columns)
print("Step 3.1.1: Unique Cities:", df["City"].unique()[:10].tolist())
print("Step 3.1.1: Sample Data:", df[["City", "Crime Type", "Crime Solved"]].head().to_dict())

# Sanitize city names for Prolog
def sanitize_city(city):
    # Keep alphanumeric and underscores, remove other characters
    sanitized = re.sub(r'[^a-z0-9_]', '_', str(city).lower())
    sanitized = re.sub(r'_+', '_', sanitized).strip('_')
    return sanitized

# Assert riskiest city to KB
def add_risky_city(city, score):
    print("Step 3.1.4: Adding riskiest city to KB!")
    try:
        # Clear existing riskyCity facts
        prolog.query("retractall(riskyCity(_, _))")
        print("Step 3.1.4: Cleared existing riskyCity facts")
        city_norm = sanitize_city(city)
        prolog.assertz(f"riskyCity('{city_norm}', {score})")
        print(f"Step 3.1.4: Added to KB: riskyCity('{city_norm}', {score})")
        print("Step 3.1.4: Finished adding riskiest city to KB!")
    except Exception as e:
        print(f"Step 3.1.4: Oops, adding riskiest city to KB failed: {e}")

# Query KB for riskiest city
def query_risky_city():
    print("Step 3.1.5: Querying KB for riskiest city!")
    try:
        # Debug: List all riskyCity facts
        facts = list(prolog.query("riskyCity(City, Score)"))
        print(f"Step 3.1.5: Debug: Current riskyCity facts: {facts}")
        if facts:
            result = [facts[0]['City'], facts[0]['Score']]
            print(f"Step 3.1.5: KB returned: {result}")
        else:
            result = []
            print("Step 3.1.5: No riskiest city found in KB!")
        print("Step 3.1.5: Finished querying KB!")
        return result
    except Exception as e:
        print(f"Step 3.1.5: Oops, KB query failed: {e}")
        return []

# MinMax algorithm to find riskiest city
def min_max_search():
    print("Step 3.1.1: Starting MinMax to find the riskiest city!")
    
    # Group data by City
    crime_stats = df.groupby("City").agg(
        total_incidents=("Incident", "count"),
        unsolved_crimes=("Crime Solved", lambda x: (x == "No").sum())
    ).reset_index()

    if crime_stats.empty:
        print("Step 3.1.3: No crime data available for analysis!")
        return {"City": None, "RiskScore": 0, "KB_Result": []}

    # Risk Score Calculation
    crime_stats["risk_score"] = (crime_stats["unsolved_crimes"] * 1.5) + crime_stats["total_incidents"]

    # Find highest risk city
    highest_risk_city_idx = crime_stats["risk_score"].idxmax()
    highest_risk_city = crime_stats.loc[highest_risk_city_idx, "City"]
    highest_risk_score = crime_stats.loc[highest_risk_city_idx, "risk_score"]

    print(f"Step 3.1.2: MinMax found riskiest city: {highest_risk_city} with risk score: {highest_risk_score}")

    # KB Operations
    if highest_risk_city:
        add_risky_city(highest_risk_city, highest_risk_score)
        kb_result = query_risky_city()
    else:
        kb_result = []

    print("Step 3.1.3: MinMax completed!")
    return {
        "City": highest_risk_city,
        "RiskScore": highest_risk_score,
        "KB_Result": kb_result
    }

# For standalone testing
if __name__ == "__main__":
    result = min_max_search()
    print("MinMax Result:", result)