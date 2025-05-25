# My AI Detective Agent with Menu
# Runs one algorithm at a time based on user choice
# Need suspects.csv, US_Crime_DataSet.csv, kb.pl, bfs.py, aStar.py, etc. in same folder
# Run with `python3 runme.py`

import pandas as pd
from pyswip import Prolog
import importlib.util
import sys
import os

def run_agent():
    try:
        # Initialize Prolog
        print("Step 1: Our detective AI agent is setting up the Prolog brain!")
        prolog = Prolog()
        prolog.consult('kb.pl')

        # Load suspects CSV
        print("Step 2: Our detective AI agent is loading suspects.csv!")
        dataset_path = "suspects.csv"
        df = pd.read_csv(dataset_path)

        # Run a Python script
        def run_script(script_name, function_name, *args):
            print(f"Step 3: Our detective AI agent is running script: {script_name}")
            try:
                spec = importlib.util.spec_from_file_location(script_name[:-3], script_name)
                module = importlib.util.module_from_spec(spec)
                sys.modules[script_name[:-3]] = module
                spec.loader.exec_module(module)
                func = getattr(module, function_name)
                return func(*args)
            except Exception as e:
                print(f"Oops, script {script_name} broke: {e}")
                return None

        # Assert race-based crimes to KB
        def add_race_crimes(race, crimes):
            print("Step 4: Our detective AI agent is adding race-based crimes to KB!")
            try:
                race_norm = race.lower()
                for crime in crimes:
                    crime_norm = crime.lower()
                    prolog.assertz(f"raceCrimeFact('{race_norm}', '{crime_norm}')")
                    print(f"Added crime: {race_norm} committed {crime_norm}")
            except Exception as e:
                print(f"Oops, adding race crimes failed: {e}")

        # Assert genetic routes to KB
        def add_genetic_route(cities):
            print("Step 4: Our detective AI agent is adding genetic routes to KB!")
            try:
                for i in range(len(cities) - 1):
                    city1 = cities[i].lower().replace(' ', '_')
                    city2 = cities[i + 1].lower().replace(' ', '_')
                    prolog.assertz(f"connectedCities('{city1}', '{city2}')")
                    print(f"Added route: {city1} to {city2}")
            except Exception as e:
                print(f"Oops, adding genetic route failed: {e}")

        # Assert CSP police units to KB
        def add_police_units(city_units):
            print("Step 4: Our detective AI agent is adding CSP police assignments to KB!")
            try:
                for city, units in city_units.items():
                    city_norm = city.lower().replace(' ', '_')
                    prolog.assertz(f"policeAssignment('{city_norm}', {units})")
                    print(f"Assigned {units} police units to {city_norm}")
            except Exception as e:
                print(f"Oops, adding police units failed: {e}")

        # Assert A*/Greedy paths to KB
        def add_search_path(path):
            print("Step 4: Our detective AI agent is adding search path to KB!")
            try:
                for i in range(len(path) - 1):
                    city1 = path[i].lower().replace(' ', '_')
                    city2 = path[i + 1].lower().replace(' ', '_')
                    prolog.assertz(f"connectedCities('{city1}', '{city2}')")
                    print(f"Added path segment: {city1} to {city2}")
            except Exception as e:
                print(f"Oops, adding search path failed: {e}")

        # Assert hill climbing hotspot to KB
        def add_hotspot(city, count):
            print("Step 4: Our detective AI agent is adding crime hotspot to KB!")
            try:
                city_norm = city.lower().replace(' ', '_')
                prolog.assertz(f"hotspot('{city_norm}', {count})")
                print(f"Added hotspot: {city_norm} with {count} crimes")
            except Exception as e:
                print(f"Oops, adding hotspot failed: {e}")

        # Assert minimax risky city to KB
        def add_risky_city(city):
            print("Step 4: Our detective AI agent is adding risky city to KB!")
            try:
                city_norm = city.lower().replace(' ', '_')
                prolog.assertz(f"riskyCityFact('{city_norm}')")
                print(f"Added risky city: {city_norm}")
            except Exception as e:
                print(f"Oops, adding risky city failed: {e}")

        # Assert IDDFS victim race to KB
        def add_victim_race(state, race):
            print("Step 4: Our detective AI agent is adding victim race to KB!")
            try:
                state_norm = state.lower().replace(' ', '_')
                race_norm = race.lower()
                prolog.assertz(f"victimRaceFact('{state_norm}', '{race_norm}')")
                print(f"Added victim race: {race_norm} in {state_norm}")
            except Exception as e:
                print(f"Oops, adding victim race failed: {e}")

        # Assert alpha-beta suspect score to KB
        def add_suspect_score(age, score):
            print("Step 4: Our detective AI agent is adding suspect score to KB!")
            try:
                prolog.assertz(f"suspectScoreFact({age}, {score})")
                print(f"Added suspect score: Age {age} with score {score}")
            except Exception as e:
                print(f"Oops, adding suspect score failed: {e}")

        # Sherlock Holmes Menu
        while True:
            print("\n=====================================")
            print("Respected User, I am Sherlock Home, an AI detective agent!")
            print("Please choose an option to solve the case:")
            print("1. Find special race people involved in crime (DFS)")
            print("2. Find a path between cities (A*)")
            print("3. Find optimal police deployment cities (Genetic Algorithm)")
            print("4. Assign police units to high-crime cities (CSP)")
            print("5. Explore crimes by city (BFS)")
            print("6. Find a path between cities (Greedy Best-First)")
            print("7. Find the city with most crimes (Hill Climbing)")
            print("8. Find risky cities for criminals (MinMax)")
            print("9. Find victim race in a state (IDDFS)")
            print("10. Identify high-risk suspects (Alpha-Beta Pruning)")
            print("11. Exit")
            print("=====================================")

            choice = input("Enter your choice (1-11): ")

            if choice == '1':
                # DFS: Find race-based crimes
                print("\nStep 3: Our detective AI agent is running DFS to find race-based crimes!")
                race = "Black"
                result = run_script("dfs.py", "dfs_search", {"Black": {"Crimes": set(), "Weapons Used": set(), "Crime Solved Status": {"Yes": 0, "No": 0}}}, race)
                if result:
                    crimes = result.get("Crimes", set())
                    add_race_crimes(race, crimes)
                    print("Step 5: Our detective AI agent is querying KB for race crimes!")
                    try:
                        result = list(prolog.query(f"raceCrime('{race.lower()}', Crime)"))
                        print(f"KB knows about {race} crimes:")
                        for r in result:
                            print(f"  - Crime: {r['Crime']}")
                        print("Step 6: Our detective AI agent decides: Increase patrols in areas with these crimes!")
                    except Exception as e:
                        print(f"Oops, race crime query failed: {e}")

            elif choice == '2':
                # A*: Find path between cities
                print("\nStep 3: Our detective AI agent is running A* to find a city path!")
                path = run_script("aStar.py", "aStarSearch", {}, "Anchorage", "Jefferson")
                if path:
                    add_search_path(path)
                    print("Step 5: Our detective AI agent is querying KB for paths!")
                    try:
                        result = list(prolog.query("searchPath('anchorage', 'jefferson', Path)"))
                        for r in result:
                            print(f"KB found path: {r['Path']}")
                        print("Step 6: Our detective AI agent decides: Send agents along this path to investigate!")
                    except Exception as e:
                        print(f"Oops, path query failed: {e}")

            elif choice == '3':
                # Genetic Algorithm: Optimal police deployment
                print("\nStep 3: Our detective AI agent is running Genetic Algorithm for police deployment!")
                strategies = run_script("geneticAlgorithim.py", "genetic_algorithm", df)
                if strategies and isinstance(strategies, list) and len(strategies) > 0:
                    best_strategy = strategies[0]
                    add_genetic_route(best_strategy)
                    print("Step 5: Our detective AI agent is querying KB for genetic routes!")
                    try:
                        result = list(prolog.query("geneticRoute(X, Y)"))
                        print("KB knows about genetic routes:")
                        for r in result:
                            print(f"  - Route: {r['X']} to {r['Y']}")
                        print("Step 6: Our detective AI agent decides: Deploy police along these routes!")
                    except Exception as e:
                        print(f"Oops, genetic route query failed: {e}")

            elif choice == '4':
                # CSP: Police unit assignments
                print("\nStep 3: Our detective AI agent is running CSP for police assignments!")
                solution = run_script("csp.py", "backtrack", {})
                if solution:
                    add_police_units(solution)
                    print("Step 5: Our detective AI agent is querying KB for police assignments!")
                    try:
                        result = list(prolog.query("policeUnits(City, Units)"))
                        print("KB knows about police assignments:")
                        for r in result:
                            print(f"  - {r['City']}: {r['Units']} units")
                        print("Step 6: Our detective AI agent decides: Reinforce these cities with more detectives!")
                    except Exception as e:
                        print(f"Oops, police units query failed: {e}")

            elif choice == '5':
                # BFS: Explore crimes by city
                print("\nStep 3: Our detective AI agent is running BFS to explore city crimes!")
                run_script("bfs.py", "bfsSearch", {"Chicago": set()}, "Chicago")
                # Simulate race crimes for BFS
                crimes = ["murder", "robbery"]  # Dummy for demo
                add_race_crimes("Black", crimes)
                print("Step 5: Our detective AI agent is querying KB for race crimes!")
                try:
                    result = list(prolog.query("raceCrime('black', Crime)"))
                    print("KB knows about Black crimes:")
                    for r in result:
                        print(f"  - Crime: {r['Crime']}")
                    print("Step 6: Our detective AI agent decides: Focus investigations on these crime types!")
                except Exception as e:
                    print(f"Oops, race crime query failed: {e}")

            elif choice == '6':
                # Greedy Best-First: Find path
                print("\nStep 3: Our detective AI agent is running Greedy Best-First Search!")
                path = run_script("greedyFirstSearch.py", "greedyBestFirstSearch", {}, "Anchorage", "Jefferson")
                if path:
                    add_search_path(path)
                    print("Step 5: Our detective AI agent is querying KB for paths!")
                    try:
                        result = list(prolog.query("searchPath('anchorage', 'jefferson', Path)"))
                        for r in result:
                            print(f"KB found path: {r['Path']}")
                        print("Step 6: Our detective AI agent decides: Patrol this path for suspects!")
                    except Exception as e:
                        print(f"Oops, path query failed: {e}")

            elif choice == '7':
                # Hill Climbing: Find crime hotspot
                print("\nStep 3: Our detective AI agent is running Hill Climbing for crime hotspots!")
                result = run_script("hillClimbing.py", "hill_climbing", "Chicago")
                if result:
                    city, count = result
                    add_hotspot(city, count)
                    print("Step 5: Our detective AI agent is querying KB for hotspots!")
                    try:
                        result = list(prolog.query("crimeHotspot(City, Count)"))
                        print("KB knows about crime hotspots:")
                        for r in result:
                            print(f"  - {r['City']}: {r['Count']} crimes")
                        print("Step 6: Our detective AI agent decides: Set up a task force in this hotspot!")
                    except Exception as e:
                        print(f"Oops, hotspot query failed: {e}")

            elif choice == '8':
                # MinMax: Risky cities
                print("\nStep 3: Our detective AI agent is running MinMax for risky cities!")
                os.system("python3 minMax.py")
                city = "Chicago"  # Dummy for demo
                add_risky_city(city)
                print("Step 5: Our detective AI agent is querying KB for risky cities!")
                try:
                    result = list(prolog.query("riskyCity(City)"))
                    print("KB knows about risky cities:")
                    for r in result:
                        print(f"  - City: {r['City']}")
                    print("Step 6: Our detective AI agent decides: Increase surveillance in these cities!")
                except Exception as e:
                    print(f"Oops, risky city query failed: {e}")

            elif choice == '9':
                # IDDFS: Victim race in state
                print("\nStep 3: Our detective AI agent is running IDDFS for victim races!")
                run_script("iddfs.py", "iddfs", {"Michigan": ["Black"]}, "Michigan", "Black", 0, 5)
                add_victim_race("Michigan", "Black")
                print("Step 5: Our detective AI agent is querying KB for victim races!")
                try:
                    result = list(prolog.query("victimRace('michigan', Race)"))
                    print("KB knows about victim races:")
                    for r in result:
                        print(f"  - Race: {r['Race']}")
                    print("Step 6: Our detective AI agent decides: Interview victims of this race in Michigan!")
                except Exception as e:
                    print(f"Oops, victim race query failed: {e}")

            elif choice == '10':
                # Alpha-Beta: High-risk suspects
                print("\nStep 3: Our detective AI agent is running Alpha-Beta for suspects!")
                score = run_script("alphaBetaPruning.py", "minimaxAlphaBeta", df[["Perpetrator Age", "Crime Score"]], 5, float('-inf'), float('inf'), True)
                if score:
                    age = 30  # Dummy for demo
                    add_suspect_score(age, score)
                    print("Step 5: Our detective AI agent is querying KB for suspect scores!")
                    try:
                        result = list(prolog.query("suspectScore(Age, Score)"))
                        print("KB knows about suspect scores:")
                        for r in result:
                            print(f"  - Age {r['Age']}: Score {r['Score']}")
                        print("Step 6: Our detective AI agent decides: Prioritize suspects with this profile!")
                    except Exception as e:
                        print(f"Oops, suspect score query failed: {e}")

            elif choice == '11':
                print("\nOur detective AI agent is signing off! Case closed!")
                break

            else:
                print("\nOops, invalid choice! Pick a number from 1 to 11.")

    except Exception as e:
        print(f"Oh no, our detective AI agent tripped: {e}")
        raise

if __name__ == "__main__":
    run_agent()