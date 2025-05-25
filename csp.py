import pandas as pd
from pyswip import Prolog

# Initialize Prolog
print("Step 3.1.0: Initializing Prolog for CSP KB operations!")
prolog = Prolog()
prolog.consult('kb.pl')
print("Step 3.1.0: Prolog initialized with kb.pl!")

# Load Crime Data
dataset_path = "US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)

# Display dataset columns
print("My Crime Dataset Columns:", df.columns)

# Ensure required columns
required_columns = {"City", "Crime Solved"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Dataset must contain {required_columns} columns.")

# Debug: Print unique City values
print("Unique Cities:", df['City'].str.strip().str.lower().unique()[:10])

# Group data by city and count unsolved crimes
crime_stats = df.groupby("City").agg(
    unsolved_crimes=("Crime Solved", lambda x: (x.str.lower() == "no").sum())
).reset_index()

# Debug: Print crime_stats summary
print("Crime Stats Summary:", crime_stats.head().to_dict())

# Sort cities by crime severity
crime_stats = crime_stats.sort_values(by="unsolved_crimes", ascending=False)
top_cities = crime_stats.head(5)["City"].tolist()
print("Step 3.1.1: Top 5 high-crime cities:", top_cities)

# Define Domains: Each city can have 1 to 5 police units
domains = {city: list(range(1, 6)) for city in top_cities}

# Define Constraints: Neighboring cities
neighboring_cities = [
    (top_cities[0], top_cities[1]),
    (top_cities[1], top_cities[2]),
    (top_cities[2], top_cities[3]),
    (top_cities[3], top_cities[4])
]

# Constraint: Higher crime cities must have more police
crime_ranking = {city: i for i, city in enumerate(top_cities)}

# Assert police assignments to KB
def add_police_assignments(assignments):
    print("Step 3.1.4: Adding police assignments to KB!")
    try:
        for city, units in assignments.items():
            city_norm = city.lower().replace(' ', '_')
            prolog.assertz(f"policeAssignment('{city_norm}', {units})")
            print(f"Step 3.1.4: Added assignment to KB: {city_norm} with {units} units")
        print("Step 3.1.4: Finished adding police assignments to KB!")
    except Exception as e:
        print(f"Step 3.1.4: Oops, adding police assignments to KB failed: {e}")

# Query KB for assignments
def query_assignments():
    print("Step 3.1.5: Querying KB for police assignments!")
    try:
        result = list(prolog.query("optimalAssignment(City, Units)"))
        if result:
            assignments = [(r['City'], r['Units']) for r in result]
            print("Step 3.1.5: KB returned assignments:", assignments)
        else:
            assignments = []
            print("Step 3.1.5: No assignments found in KB!")
        print("Step 3.1.5: Finished querying KB!")
        return assignments
    except Exception as e:
        print(f"Step 3.1.5: Oops, assignment query failed: {e}")
        return []

# Check if assignment satisfies constraints
def isValidAssignment(city, value, assignment):
    print(f"Step 3.1.2: Checking validity for {city} with {value} units")
    for neighbor in neighboring_cities:
        if city in neighbor:
            other_city = neighbor[0] if neighbor[1] == city else neighbor[1]
            if other_city in assignment and assignment[other_city] == value:
                print(f"  - Invalid: {city} and {other_city} have same units ({value})")
                return False
    for other_city, _ in crime_ranking.items():
        if other_city in assignment:
            if crime_ranking[city] < crime_ranking[other_city] and value <= assignment[other_city]:
                print(f"  - Invalid: {city} (rank {crime_ranking[city]}) has {value} units, less than or equal to {other_city} (rank {crime_ranking[other_city]}) with {assignment[other_city]} units")
                return False
    print(f"  - Valid: {city} with {value} units")
    return True

# Backtracking Algorithm for CSP
def backtrack(assignment):
    print(f"Step 3.1.2: Backtracking with assignment: {assignment}")
    if len(assignment) == len(top_cities):
        return assignment
    city = next(c for c in top_cities if c not in assignment)
    for value in domains[city]:
        if isValidAssignment(city, value, assignment):
            assignment[city] = value
            result = backtrack(assignment)
            if result:
                return result
            del assignment[city]
    return None

# CSP Solver
def csp_solver():
    print("Step 3.1.1: Starting CSP Solver for police deployment...")
    solution = backtrack({})
    if solution:
        print("Step 3.1.3: Optimal Police Deployment Strategy:")
        for city, units in solution.items():
            print(f"  - {city}: {units} police units")
        add_police_assignments(solution)
        kb_assignments = query_assignments()
    else:
        print("Step 3.1.3: No valid police deployment strategy found.")
        kb_assignments = []
    print("Step 3.1.3: CSP Solver completed!")
    return {"Assignments": solution if solution else {}, "KB_Assignments": kb_assignments}

# For standalone testing
if __name__ == "__main__":
    result = csp_solver()
    print("CSP Result:", result)