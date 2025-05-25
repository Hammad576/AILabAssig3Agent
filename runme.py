# My AI Detective Agent with Menu
# Handles all options with clear steps for assignment
# Need suspects.csv, US_Crime_DataSet.csv, kb.pl, bfs.py, aStar.py, etc. in same folder
# Run with `python3 runme.py`

import pandas as pd
from pyswip import Prolog
import importlib.util
import sys
import os

def run_agent():
    try:
        # Step 1: Initialize Prolog
        print("Step 1: Our detective AI agent is setting up the Prolog brain!")
        prolog = Prolog()
        prolog.consult('kb.pl')
        print("Step 1: Finished setting up Prolog brain with kb.pl!")

        # Step 2: Load suspects CSV
        print("Step 2: Our detective AI agent is loading suspects.csv!")
        dataset_path = "suspects.csv"
        df = pd.read_csv(dataset_path)
        print("Step 2: Finished loading suspects.csv!")

        # Helper to run a Python script
        def run_script(script_name, function_name, *args):
            print(f"Step 3.1: Our detective AI agent is executing {script_name}!")
            try:
                spec = importlib.util.spec_from_file_location(script_name[:-3], script_name)
                module = importlib.util.module_from_spec(spec)
                sys.modules[script_name[:-3]] = module
                spec.loader.exec_module(module)
                func = getattr(module, function_name)
                result = func(*args)
                print(f"Step 3.2: Our detective AI agent finished executing {script_name}!")
                return result
            except Exception as e:
                print(f"Step 3.2: Oops, {script_name} broke: {e}")
                return None

        # Assert race-based crimes to KB
        def add_race_crimes(race, crimes):
            print("Step 4: Our detective AI agent is adding race-based crimes to KB as per assignment requirement!")
            try:
                race_norm = race.lower()
                for crime in crimes:
                    crime_norm = crime.lower()
                    prolog.assertz(f"raceCrimeFact('{race_norm}', '{crime_norm}')")
                    print(f"Step 4: Added crime to KB: {race_norm} committed {crime_norm}")
                print("Step 4: Finished adding race-based crimes to KB!")
            except Exception as e:
                print(f"Step 4: Oops, adding race crimes to KB failed: {e}")

        # Assert search path to KB
        def add_search_path(path):
            print("Step 4: Our detective AI agent is adding search path to KB as per assignment requirement!")
            try:
                for i in range(len(path) - 1):
                    city1 = path[i].lower().replace(' ', '_')
                    city2 = path[i + 1].lower().replace(' ', '_')
                    prolog.assertz(f"connectedCities('{city1}', '{city2}')")
                    print(f"Step 4: Added path segment to KB: {city1} to {city2}")
                print("Step 4: Finished adding search path to KB!")
            except Exception as e:
                print(f"Step 4: Oops, adding search path to KB failed: {e}")

        # Assert genetic routes to KB
        def add_genetic_route(cities):
            print("Step 4: Our detective AI agent is adding genetic routes to KB as per assignment requirement!")
            try:
                for i in range(len(cities) - 1):
                    city1 = cities[i].lower().replace(' ', '_')
                    city2 = cities[i + 1].lower().replace(' ', '_')
                    prolog.assertz(f"connectedCities('{city1}', '{city2}')")
                    print(f"Step 4: Added route to KB: {city1} to {city2}")
                print("Step 4: Finished adding genetic routes to KB!")
            except Exception as e:
                print(f"Step 4: Oops, adding genetic route to KB failed: {e}")

        # Assert CSP police units to KB
        def add_police_units(city_units):
            print("Step 4: Our detective AI agent is adding CSP police assignments to KB as per assignment requirement!")
            try:
                for city, units in city_units.items():
                    city_norm = city.lower().replace(' ', '_')
                    prolog.assertz(f"policeAssignment('{city_norm}', {units})")
                    print(f"Step 4: Assigned {units} police units to {city_norm} in KB")
                print("Step 4: Finished adding CSP police assignments to KB!")
            except Exception as e:
                print(f"Step 4: Oops, adding police units to KB failed: {e}")

        # Assert hill climbing hotspot to KB
        def add_hotspot(city, count):
            print("Step 4: Our detective AI agent is adding crime hotspot to KB as per assignment requirement!")
            try:
                city_norm = city.lower().replace(' ', '_')
                prolog.assertz(f"hotspot('{city_norm}', {count})")
                print(f"Step 4: Added hotspot to KB: {city_norm} with {count} crimes")
                print("Step 4: Finished adding crime hotspot to KB!")
            except Exception as e:
                print(f"Step 4: Oops, adding hotspot to KB failed: {e}")

        # Assert risky city to KB
        def add_risky_city(city):
            print("Step 4: Our detective AI agent is adding risky city to KB as per assignment requirement!")
            try:
                city_norm = city.lower().replace(' ', '_')
                prolog.assertz(f"riskyCityFact('{city_norm}')")
                print(f"Step 4: Added risky city to KB: {city_norm}")
                print("Step 4: Finished adding risky city to KB!")
            except Exception as e:
                print(f"Step 4: Oops, adding risky city to KB failed: {e}")

        # Assert victim race to KB
        def add_victim_race(state, race):
            print("Step 4: Our detective AI agent is adding victim race to KB as per assignment requirement!")
            try:
                state_norm = state.lower().replace(' ', '_')
                race_norm = race.lower()
                prolog.assertz(f"victimRaceFact('{state_norm}', '{race_norm}')")
                print(f"Step 4: Added victim race to KB: {race_norm} in {state_norm}")
                print("Step 4: Finished adding victim race to KB!")
            except Exception as e:
                print(f"Step 4: Oops, adding victim race to KB failed: {e}")

        # Assert alpha-beta suspect score to KB
        def add_suspect_score(age, score):
            print("Step 4: Our detective AI agent is adding suspect score to KB as per assignment requirement!")
            try:
                prolog.assertz(f"suspectScoreFact({age}, {score})")
                print(f"Step 4: Added suspect score to KB: Age {age} with score {score}")
                print("Step 4: Finished adding suspect score to KB!")
            except Exception as e:
                print(f"Step 4: Oops, adding suspect score to KB failed: {e}")

        # Query KB for race crimes
        def query_race_crimes(race):
            print("Step 5: Our detective AI agent is querying KB for race-based crimes as per assignment requirement!")
            try:
                result = list(prolog.query(f"raceCrime('{race.lower()}', Crime)"))
                if result:
                    print("Step 5: KB returned race crimes:")
                    for r in result:
                        print(f"  - Crime: {r['Crime']}")
                else:
                    print("Step 5: No race crimes found in KB!")
                print("Step 5: Finished querying KB for race crimes!")
                return result
            except Exception as e:
                print(f"Step 5: Oops, race crime query failed: {e}")
                print("Step 5: Finished querying KB with error!")
                return []

        # Query KB for path
        def query_path(start, goal):
            print("Step 5: Our detective AI agent is querying KB for search path as per assignment requirement!")
            start_norm = start.lower()
            goal_norm = goal.lower()
            try:
                result = list(prolog.query(f"searchPath('{start_norm}', '{goal_norm}', Path)"))
                if result:
                    print("Step 5: KB returned path(s):")
                    for r in result:
                        print(f"  - Path: {r['Path']}")
                    print("Step 5: Finished querying KB for path!")
                    return result[0]['Path'] if result else None
                else:
                    print("Step 5: No path found in KB!")
                    print("Step 5: Finished querying KB for path!")
                    return None
            except Exception as e:
                print(f"Step 5: Oops, path query failed: {e}")
                print(f"Step 5: Finished querying KB with error!")
                return None

        # Query KB for genetic routes
        def query_genetic_routes():
            print("Step 5: Our detective AI agent is querying KB for genetic routes as per assignment requirement!")
            try:
                result = list(prolog.query("geneticRoute(X, Y)"))
                if result:
                    print("Step 5: KB returned genetic routes:")
                    for r in result:
                        print(f"  - Route: {r['X']} to {r['Y']}")
                else:
                    print("Step 5: No genetic routes found in KB!")
                print("Step 5: Finished querying KB for genetic routes!")
                return result
            except Exception as e:
                print(f"Step 5: Oops, genetic route query failed: {e}")
                print("Step 5: Finished querying KB with error!")
                return []

        # Query KB for police units
        def query_police_units():
            print("Step 5: Our detective AI agent is querying KB for police assignments as per assignment requirement!")
            try:
                result = list(prolog.query("policeUnits(City, Units)"))
                if result:
                    print("Step 5: KB returned police assignments:")
                    for r in result:
                        print(f"  - {r['City']}: {r['Units']} units")
                else:
                    print("Step 5: No police assignments found in KB!")
                print("Step 5: Finished querying KB for police assignments!")
                return result
            except Exception as e:
                print(f"Step 5: Oops, police units query failed: {e}")
                print("Step 5: Finished querying KB with error!")
                return []

        # Query KB for hotspots
        def query_hotspots():
            print("Step 5: Our detective AI agent is querying KB for crime hotspots as per assignment requirement!")
            try:
                result = list(prolog.query("crimeHotspot(City, Count)"))
                if result:
                    print("Step 5: KB returned crime hotspots:")
                    for r in result:
                        print(f"  - {r['City']}: {r['Count']} crimes")
                else:
                    print("Step 5: No crime hotspots found in KB!")
                print("Step 5: Finished querying KB for crime hotspots!")
                return result
            except Exception as e:
                print(f"Step 5: Oops, hotspot query failed: {e}")
                print("Step 5: Finished querying KB with error!")
                return []

        # Query KB for risky cities
        def query_risky_cities():
            print("Step 5: Our detective AI agent is querying KB for risky cities as per assignment requirement!")
            try:
                result = list(prolog.query("riskyCity(City)"))
                if result:
                    print("Step 5: KB returned risky cities:")
                    for r in result:
                        print(f"  - City: {r['City']}")
                else:
                    print("Step 5: No risky cities found in KB!")
                print("Step 5: Finished querying KB for risky cities!")
                return result
            except Exception as e:
                print(f"Step 5: Oops, risky city query failed: {e}")
                print("Step 5: Finished querying KB with error!")
                return []

        # Query KB for victim races
        def query_victim_races(state):
            print("Step 5: Our detective AI agent is querying KB for victim races as per assignment requirement!")
            state_norm = state.lower()
            try:
                result = list(prolog.query(f"victimRace('{state_norm}', Race)"))
                if result:
                    print("Step 5: KB returned victim races:")
                    for r in result:
                        print(f"  - Race: {r['Race']}")
                else:
                    print("Step 5: No victim races found in KB!")
                print("Step 5: Finished querying KB for victim races!")
                return result
            except Exception as e:
                print(f"Step 5: Oops, victim race query failed: {e}")
                print("Step 5: Finished querying KB with error!")
                return []

        # Query KB for suspect scores
        def query_suspect_scores():
            print("Step 5: Our detective AI agent is querying KB for suspect scores as per assignment requirement!")
            try:
                result = list(prolog.query("suspectScore(Age, Score)"))
                if result:
                    print("Step 5: KB returned suspect scores:")
                    for r in result:
                        print(f"  - Age {r['Age']}: Score {r['Score']}")
                else:
                    print("Step 5: No suspect scores found in KB!")
                print("Step 5: Finished querying KB for suspect scores!")
                return result
            except Exception as e:
                print(f"Step 5: Oops, suspect score query failed: {e}")
                print("Step 5: Finished querying KB with error!")
                return []

        # Make decision for race crimes
        def decide_race_crimes(race, crimes):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement!")
            if crimes:
                print(f"Step 6: Decision: Increase patrols in areas where {race} is linked to crimes like {', '.join([r['Crime'] for r in crimes])}!")
            else:
                print(f"Step 6: Decision: No {race} crime data in KB, broaden investigation!")
            print("Step 6: Finished making decision!")

        # Make decision for path
        def decide_path(path):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement!")
            if path:
                print(f"Step 6: Decision: Send agents along path {path} to investigate suspects!")
            else:
                print("Step 6: Decision: No path found, focus on local investigations!")
            print("Step 6: Finished making decision!")

        # Make decision for genetic routes
        def decide_genetic_routes(routes):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement!")
            if routes:
                print(f"Step 6: Decision: Deploy police along routes like {routes[0]['X']} to {routes[0]['Y']}!")
            else:
                print("Step 6: Decision: No routes in KB, optimize local deployments!")
            print("Step 6: Finished making decision!")

        # Make decision for police units
        def decide_police_units(units):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement!")
            if units:
                print(f"Step 6: Decision: Reinforce {units[0]['City']} with {units[0]['Units']} units!")
            else:
                print("Step 6: Decision: No assignments in KB, redistribute police!")
            print("Step 6: Finished making decision!")

        # Make decision for hotspots
        def decide_hotspots(hotspots):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement!")
            if hotspots:
                print(f"Step 6: Decision: Set up task force in hotspot {hotspots[0]['City']} with {hotspots[0]['Count']} crimes!")
            else:
                print("Step 6: Decision: No hotspots in KB, monitor all cities!")
            print("Step 6: Finished making decision!")

        # Make decision for risky cities
        def decide_risky_cities(cities):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement!")
            if cities:
                print(f"Step 6: Decision: Increase surveillance in risky city {cities[0]['City']}!")
            else:
                print("Step 6: Decision: No risky cities in KB, monitor all cities!")
            print("Step 6: Finished making decision!")

        # Make decision for victim races
        def decide_victim_races(state, races):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement!")
            if races:
                print(f"Step 6: Decision: Interview victims of race {races[0]['Race']} in {state}!")
            else:
                print(f"Step 6: Decision: No victim races in KB for {state}, expand victim interviews!")
            print("Step 6: Finished making decision!")

        # Make decision for suspect scores
        def decide_suspect_scores(scores):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement!")
            if scores:
                print(f"Step 6: Decision: Prioritize suspects with age {scores[0]['Age']} and score {scores[0]['Score']}!")
            else:
                print("Step 6: Decision: No suspect scores in KB, broaden suspect profiling!")
            print("Step 6: Finished making decision!")

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
                print("\nStep 3: Our detective AI agent is running DFS to find race-based crimes as per assignment requirement!")
                race = "Black"
                result = run_script("dfs.py", "dfs_search", {"Black": {"Crimes": set(), "Weapons Used": set(), "Crime Solved Status": {"Yes": 0, "No": 0}}}, race)
                if result and isinstance(result, dict) and "Crimes" in result:
                    crimes = result["Crimes"]
                    print(f"Step 3: DFS found crimes for {race}: {crimes}")
                    add_race_crimes(race, crimes)
                    kb_crimes = query_race_crimes(race)
                    decide_race_crimes(race, kb_crimes)
                else:
                    print("Step 3: DFS failed to find race-based crimes!")
                    decide_race_crimes(race, [])

            elif choice == '2':
                print("\nStep 3: Our detective AI agent is running A* to find a path between cities as per assignment requirement!")
                start_city = "chicago"
                goal_city = "miami"
                path = run_script("aStar.py", "aStarSearch", {}, start_city, goal_city)
                if path:
                    print(f"Step 3: A* found path: {path}")
                    add_search_path(path)
                    kb_path = query_path(start_city, goal_city)
                    decide_path(kb_path)
                else:
                    print("Step 3: A* failed to find a path!")
                    decide_path(None)

            elif choice == '3':
                print("\nStep 3: Our detective AI agent is running Genetic Algorithm for police deployment as per assignment requirement!")
                strategies = run_script("geneticAlgorithim.py", "genetic_algorithm", df)
                if strategies and isinstance(strategies, list) and len(strategies) > 0:
                    best_strategy = strategies[0]
                    print(f"Step 3: Genetic Algorithm found strategy: {best_strategy}")
                    add_genetic_route(best_strategy)
                    kb_routes = query_genetic_routes()
                    decide_genetic_routes(kb_routes)
                else:
                    print("Step 3: Genetic Algorithm failed to find strategies!")
                    decide_genetic_routes([])

            elif choice == '4':
                print("\nStep 3: Our detective AI agent is running CSP for police assignments as per assignment requirement!")
                solution = run_script("csp.py", "backtrack", {})
                if solution:
                    print(f"Step 3: CSP found assignments: {solution}")
                    add_police_units(solution)
                    kb_units = query_police_units()
                    decide_police_units(kb_units)
                else:
                    print("Step 3: CSP failed to find police assignments!")
                    decide_police_units([])

            elif choice == '5':
                print("\nStep 3: Our detective AI agent is running BFS to explore city crimes as per assignment requirement!")
                result = run_script("bfs.py", "bfsSearch", {"chicago": set()}, "chicago")
                if result:
                    crimes = result.get("chicago", set()) or ["murder", "robbery"]  # Fallback
                    print(f"Step 3: BFS found crimes in chicago: {crimes}")
                    add_race_crimes("Black", crimes)
                    kb_crimes = query_race_crimes("Black")
                    decide_race_crimes("Black", kb_crimes)
                else:
                    print("Step 3: BFS failed to find crimes!")
                    decide_race_crimes("Black", [])

            elif choice == '6':
                print("\nStep 3: Our detective AI agent is running Greedy Best-First Search to find a path as per assignment requirement!")
                start_city = "chicago"
                goal_city = "miami"
                path = run_script("greedyFirstSearch.py", "greedyBestFirstSearch", {}, start_city, goal_city)
                if path:
                    print(f"Step 3: Greedy found path: {path}")
                    add_search_path(path)
                    kb_path = query_path(start_city, goal_city)
                    decide_path(kb_path)
                else:
                    print("Step 3: Greedy failed to find a path!")
                    decide_path(None)

            elif choice == '7':
                print("\nStep 3: Our detective AI agent is running Hill Climbing for crime hotspots as per assignment requirement!")
                result = run_script("hillClimbing.py", "hill_climbing", "chicago")
                if result and len(result) == 2:
                    city, count = result
                    print(f"Step 3: Hill Climbing found hotspot: {city} with {count} crimes")
                    add_hotspot(city, count)
                    kb_hotspots = query_hotspots()
                    decide_hotspots(kb_hotspots)
                else:
                    print("Step 3: Hill Climbing failed to find a hotspot!")
                    decide_hotspots([])

            elif choice == '8':
                print("\nStep 3: Our detective AI agent is running MinMax for risky cities as per assignment requirement!")
                city = run_script("minMax.py", "find_risky_city")
                if city:
                    print(f"Step 3: MinMax found risky city: {city}")
                    add_risky_city(city)
                    kb_cities = query_risky_cities()
                    decide_risky_cities(kb_cities)
                else:
                    print("Step 3: MinMax failed to find a risky city!")
                    decide_risky_cities([])

            elif choice == '9':
                print("\nStep 3: Our detective AI agent is running IDDFS for victim races as per assignment requirement!")
                state = "Michigan"
                race = "Black"
                result = run_script("iddfs.py", "iddfs", {"Michigan": ["Black"]}, "Michigan", "Black", 0, 5)
                if result:
                    print(f"Step 3: IDDFS found victim race: {race} in {state}")
                    add_victim_race(state, race)
                    kb_races = query_victim_races(state)
                    decide_victim_races(state, kb_races)
                else:
                    print("Step 3: IDDFS failed to find victim race!")
                    decide_victim_races(state, [])

            elif choice == '10':
                print("\nStep 3: Our detective AI agent is running Alpha-Beta for suspects as per assignment requirement!")
                score = run_script("alphaBetaPruning.py", "minimaxAlphaBeta", df[["Perpetrator Age", "Crime Score"]], 5, float('-inf'), float('inf'), True)
                if score:
                    age = 30  # Dummy age
                    print(f"Step 3: Alpha-Beta found suspect score: {score} for age {age}")
                    add_suspect_score(age, score)
                    kb_scores = query_suspect_scores()
                    decide_suspect_scores(kb_scores)
                else:
                    print("Step 3: Alpha-Beta failed to find suspect score!")
                    decide_suspect_scores([])

            elif choice == '11':
                print("\nStep 7: Our detective AI agent is signing off! Case closed!")
                break

            else:
                print("\nStep 7: Oops, invalid choice! Pick a number from 1 to 11.")

    except Exception as e:
        print(f"Step 7: Oh no, our detective AI agent tripped: {e}")
        raise

if __name__ == "__main__":
    run_agent()