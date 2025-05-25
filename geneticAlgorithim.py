import numpy as np
import pandas as pd
import random
from pyswip import Prolog

# Initialize Prolog
print("Step 3.1.0: Initializing Prolog for Genetic Algorithm KB operations!")
prolog = Prolog()
prolog.consult('kb.pl')
print("Step 3.1.0: Prolog initialized with kb.pl!")

# Load Dataset
dataset_path = "US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)

# Display dataset columns
print("My Crime Dataset Columns:", df.columns)

# Check required columns
required_columns = {"City", "Incident", "Crime Type", "Crime Solved"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Dataset must contain {required_columns} columns.")

# Debug: Print unique City values
print("Unique Cities:", df['City'].str.strip().str.lower().unique()[:10])

# Group data by City to analyze crime frequency
crime_stats = df.groupby("City").agg(
    total_incidents=("Incident", "count"),
    unsolved_crimes=("Crime Solved", lambda x: (x.str.lower() == "no").sum())
).reset_index()

# Debug: Print crime_stats summary
print("Crime Stats Summary:", crime_stats.head().to_dict())

# Define Genetic Algorithm parameters
POPULATION_SIZE = 10
MUTATION_RATE = 0.1
GENERATIONS = 10

# Step 1: Generate Initial Population
def generate_population():
    print("Step 3.1.2: Generating Initial Population...")
    population = [random.sample(list(crime_stats["City"]), 5) for _ in range(POPULATION_SIZE)]
    for i, individual in enumerate(population):
        print(f"  - Strategy {i+1}: {individual}")
    return population

# Step 2: Fitness Function
def fitness(solution):
    total_unsolved = sum(crime_stats[crime_stats["City"].isin(solution)]["unsolved_crimes"])
    return 1 / (total_unsolved + 1)

# Step 3: Selection
def select_parents(population):
    print("Step 3.1.2: Selecting Best Parents...")
    sorted_population = sorted(population, key=fitness, reverse=True)
    parents = sorted_population[:2]
    print(f"  - Parent 1: {parents[0]} (Fitness: {fitness(parents[0]):.6f})")
    print(f"  - Parent 2: {parents[1]} (Fitness: {fitness(parents[1]):.6f})")
    return parents

# Step 4: Crossover
def crossover(parent1, parent2):
    print("Step 3.1.2: Performing Crossover...")
    split = len(parent1) // 2
    child1 = parent1[:split] + parent2[split:]
    child2 = parent2[:split] + parent1[split:]
    print(f"  - Child 1: {child1}")
    print(f"  - Child 2: {child2}")
    return child1, child2

# Step 5: Mutation
def mutate(child):
    if random.random() < MUTATION_RATE:
        index = random.randint(0, len(child) - 1)
        available_cities = list(set(crime_stats["City"]) - set(child))
        if available_cities:
            old_city = child[index]
            new_city = random.choice(available_cities)
            child[index] = new_city
            print(f"  - Mutation: {old_city} → {new_city}")
    return child

# Assert deployment cities to KB
def add_deployment_cities(cities):
    print("Step 3.1.4: Adding deployment cities to KB!")
    try:
        for city in cities:
            city_norm = city.lower().replace(' ', '_')
            prolog.assertz(f"deploymentCity('{city_norm}')")
            print(f"Step 3.1.4: Added city to KB: {city_norm}")
        print("Step 3.1.4: Finished adding deployment cities to KB!")
    except Exception as e:
        print(f"Step 3.1.4: Oops, adding deployment cities to KB failed: {e}")

# Query KB for deployment cities
def query_deployment():
    print("Step 3.1.5: Querying KB for optimal deployment!")
    try:
        result = list(prolog.query("optimalDeployment(City)"))
        if result:
            cities = [r['City'] for r in result]
            print("Step 3.1.5: KB returned deployment cities:", cities)
        else:
            cities = []
            print("Step 3.1.5: No deployment cities found in KB!")
        print("Step 3.1.5: Finished querying KB!")
        return cities
    except Exception as e:
        print(f"Step 3.1.5: Oops, deployment query failed: {e}")
        return []

# Genetic Algorithm Execution
def genetic_algorithm():
    print("Step 3.1.1: Starting Genetic Algorithm Execution...")
    population = generate_population()

    for generation in range(GENERATIONS):
        print(f"\nStep 3.1.2: Generation {generation+1} =================")
        parents = select_parents(population)
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            child1, child2 = crossover(parents[0], parents[1])
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))
        population = new_population[:POPULATION_SIZE]

        print("\nStep 3.1.2: Population Fitness Scores:")
        for i, individual in enumerate(population):
            print(f"  - Strategy {i+1}: {individual} (Fitness: {fitness(individual):.6f})")

    best_strategy = max(population, key=fitness)
    print("\nStep 3.1.3: Final Optimal Police Deployment Strategy:")
    print(f"Best Cities to Deploy Police: {best_strategy}")
    print(f"Best Strategy Fitness Score: {fitness(best_strategy):.6f}")

    # Add to KB and query
    add_deployment_cities(best_strategy)
    kb_strategy = query_deployment()

    print("Step 3.1.3: Genetic Algorithm completed!")
    return {"Strategy": best_strategy, "KB_Strategy": kb_strategy}

# For standalone testing
if __name__ == "__main__":
    result = genetic_algorithm()
    print("Genetic Algorithm Result:", result)