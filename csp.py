import pandas as pd

# Load Crime Data (Replace with your actual file path)
dataset_path = "../US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)

# Ensuring columns retrived
required_columns = {"City", "Crime Solved"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Dataset must contain {required_columns} columns.")

# Group data by city and count unsolved crimes
# we will then sort cities by crime rate
crime_stats = df.groupby("City").agg(
    unsolved_crimes=("Crime Solved", lambda x: (x == "No").sum())  # Count unresolved cases
).reset_index()

# Sort cities based on crime severity (higher crime = higher priority)
crime_stats = crime_stats.sort_values(by="unsolved_crimes", ascending=False)
#1St Step is variables, our variables are the cities that are 
#effecting by crimes


top_cities = crime_stats.head(5)["City"].tolist()

#2nd Step is Domains Select the top 5 high-crime cities for the CSP example
# Define Domains: Each city can have 1 to 5 police units
domains = {city: list(range(1, 6)) for city in top_cities}

#3rd Step is Defining Constraints (Neighboring cities should not have the same units)
neighboring_cities = [
    (top_cities[0], top_cities[1]),
    (top_cities[1], top_cities[2]),
    (top_cities[2], top_cities[3]),
    (top_cities[3], top_cities[4])
]

# Constraint: Higher crime cities must have more police
crime_ranking = {city: i for i, city in enumerate(top_cities)}  # Rank cities based on crime


#  Backtracking Algorithm for CSP 
# Next Step is Constraints
# No two Cities can have same number of police units
# The higher crime rates cities should have more police Units
def isValidAssignment(city, value, assignment):
    """Check if assigning 'value' to 'city' satisfies constraints."""
    for neighbor in neighboring_cities:
        if city in neighbor:  
            other_city = neighbor[0] if neighbor[1] == city else neighbor[1]
            if other_city in assignment and assignment[other_city] == value:
                return False  
                # 1St constraint Neighboring cities cannot have the same police count

    # 2nd Constraint higher crime cities get more police
    for other_city, _ in crime_ranking.items():
        if other_city in assignment:
            if crime_ranking[city] < crime_ranking[other_city] and value <= assignment[other_city]:
                return False  # Higher crime city must have more police

    return True


def backtrack(assignment):
    """Recursive backtracking function to find a valid solution."""
    if len(assignment) == len(top_cities):  
        return assignment  # Solution found

    city = next(c for c in top_cities if c not in assignment)  

    for value in domains[city]:  
        if isValidAssignment(city, value, assignment):  
            assignment[city] = value  
            result = backtrack(assignment)  
            if result:
                return result  # Solution found
            del assignment[city]  

    return None  # No valid assignment found


# Solve the CSP
solution = backtrack({})

# Display Result
if solution:
    print("\nOptimal Police Deployment Strategy:")
    for city, units in solution.items():
        print(f"  - {city}: {units} police units")
else:
    print("\nNo valid police deployment strategy found.")
