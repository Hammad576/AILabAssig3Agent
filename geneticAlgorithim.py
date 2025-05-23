import numpy as np
import pandas as pd
import random

# Load Dataset
dataset_path = "../US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False) 

# Check required columns
required_columns = {"City", "Incident", "Crime Type", "Crime Solved"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Dataset must contain {required_columns} columns.")

# Group data by City to analyze crime frequency
crime_stats = df.groupby("City").agg(
    total_incidents=("Incident", "count"),   # Count total crimes per city
    unsolved_crimes=("Crime Solved", lambda x: (x == "No").sum())  # Count unresolved cases
).reset_index()

# Define Genetic Algorithm parameters (Dummy)
POPULATION_SIZE = 10  # Number of police deployment strategies
MUTATION_RATE = 0.1   # Probability of mutation
GENERATIONS = 10      # Total number of generations

# Step 1: Generate Initial Population (Random Police Deployment Strategies)
def generate_population():
    print("\n Generating Initial Population...")
    population = [random.sample(list(crime_stats["City"]), 5) for _ in range(POPULATION_SIZE)]
    for i, individual in enumerate(population):
        print(f"  - Strategy {i+1}: {individual}")
    return population

# Step 2: Fitness Function (Lower Unsolved Crime = Better Solution)
def fitness(solution):
    total_unsolved = sum(crime_stats[crime_stats["City"].isin(solution)]["unsolved_crimes"])
    return 1 / (total_unsolved + 1)  # Lower unresolved cases = higher fitness

# Step 3: Selection (Choose Best Parents)
def select_parents(population):
    print("\nSelecting Best Parents...")
    sorted_population = sorted(population, key=fitness, reverse=True)
    parents = sorted_population[:2]  # Select top 2 solutions
    print(f"  - Parent 1: {parents[0]} (Fitness: {fitness(parents[0]):.6f})")
    print(f"  - Parent 2: {parents[1]} (Fitness: {fitness(parents[1]):.6f})")
    return parents

# Step 4: Crossover (Mix Strategies to Create New Ones)
def crossover(parent1, parent2):
    print("\nPerforming Crossover...")
    split = len(parent1) // 2
    child1 = parent1[:split] + parent2[split:]
    child2 = parent2[:split] + parent1[split:]
    print(f"  - Child 1: {child1}")
    print(f"  - Child 2: {child2}")
    return child1, child2

# Step 5: Mutation (Introduce Small Changes)
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

# Genetic Algorithm Execution
print("\nStarting Genetic Algorithm Execution...")
population = generate_population()

for generation in range(GENERATIONS):
    print(f"\n================ GENERATION {generation+1} =================")

    # Step 3: Select Parents
    parents = select_parents(population)

    # Step 4 & 5: Crossover & Mutation
    new_population = []
    while len(new_population) < POPULATION_SIZE:
        child1, child2 = crossover(parents[0], parents[1])
        new_population.append(mutate(child1))
        new_population.append(mutate(child2))

    # Ensure population size remains the same
    population = new_population[:POPULATION_SIZE]  

    # Display fitness scores for each strategy
    print("\n Population Fitness Scores:")
    for i, individual in enumerate(population):
        print(f"  - Strategy {i+1}: {individual} (Fitness: {fitness(individual):.6f})")

# Best Strategy Found
best_strategy = max(population, key=fitness)
print("\n FINAL OPTIMAL POLICE DEPLOYMENT STRATEGY:")
print(f"Best Cities to Deploy Police: {best_strategy}")
print(f"Best Strategy Fitness Score: {fitness(best_strategy):.6f}")
