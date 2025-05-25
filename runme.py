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
        print("Step 1: Our detective AI agent is setting up the prolog for the knowledge base KB:  ")
        prolog = Prolog()
        prolog.consult('kb.pl')
        print("Step 1 We have setup the Prolog KB. OUr KB is ready now.")

        # Step 2: Load suspects CSV
        print("Step 2: Our detective AI agent is loading suspects.csv data set file.")
        dataset_path = "suspects.csv"
        df = pd.read_csv(dataset_path)
        print("Step 2: Finished loading suspects.csv. The file is now loaded now. ")

        # Helper to run a Python script
        def run_script(script_name, function_name, *args):
            print(f"Step 3.1: Our detective AI agent is executing {script_name}....")
            try:
                spec = importlib.util.spec_from_file_location(script_name[:-3], script_name)
                module = importlib.util.module_from_spec(spec)
                sys.modules[script_name[:-3]] = module
                spec.loader.exec_module(module)
                func = getattr(module, function_name)
                result = func(*args)
                print(f"Step 3.2: Our detective AI agent finished executing {script_name}...")
                return result
            except Exception as e:
                print(f"Step 3.2:Sorry The agent is facing some errors  {script_name}  {e}. ")
                return None

        # Assert race-based crimes to KB
        def add_race_crimes(race, crimes):
            print("Step 4: Our detective AI agent is adding race Based crimes to KB as per assignment requirement. ")
            try:
                race_norm = race.lower()
                for crime in crimes:
                    crime_norm = crime.lower()
                    prolog.assertz(f"raceCrimeFact('{race_norm}', '{crime_norm}')")
                    print(f"Step 4: Added crime to KB: {race_norm} committed {crime_norm}")
                print("Step 4: Finished adding race-based crimes to KB.")
            except Exception as e:
                print(f"Step 4: Sorry, adding race crimes to KB failed: {e}")

        # Assert search path to KB
        def add_search_path(path):
            print("Step 4: Our detective AI agent is adding search path to KB as per assignment requirement.")
            try:
                for i in range(len(path) - 1):
                    city1 = path[i].lower().replace(' ', '_')
                    city2 = path[i + 1].lower().replace(' ', '_')
                    prolog.assertz(f"connectedCities('{city1}', '{city2}')")
                    print(f"Step 4: Added path segment to KB: {city1} to {city2}")
                print("Step 4: Finished adding search path to KB.")
            except Exception as e:
                print(f"Step 4: Sorry, adding search path to KB failed: {e}")

        # Assert genetic routes to KB
        def add_genetic_route(cities):
            print("Step 4: Our detective AI agent is adding genetic routes to KB as per assignment requirement.")
            try:
                for i in range(len(cities) - 1):
                    city1 = cities[i].lower().replace(' ', '_')
                    city2 = cities[i + 1].lower().replace(' ', '_')
                    prolog.assertz(f"connectedCities('{city1}', '{city2}')")
                    print(f"Step 4: Added route to KB: {city1} to {city2}")
                print("Step 4: Finished adding genetic routes to KB.")
            except Exception as e:
                print(f"Step 4: Sorry, adding genetic route to KB failed: {e}")

        # Assert CSP police units to KB
        def add_police_units(city_units):
            print("Step 4: Our detective AI agent is adding CSP police assignments to KB as per assignment requirement.")
            try:
                for city, units in city_units.items():
                    city_norm = city.lower().replace(' ', '_')
                    prolog.assertz(f"policeAssignment('{city_norm}', {units})")
                    print(f"Step 4: Assigned {units} police units to {city_norm} in KB")
                print("Step 4: Finished adding CSP police assignments to KB.")
            except Exception as e:
                print(f"Step 4: Sorry, adding police units to KB failed: {e}")

        # Assert hill climbing hotspot to KB
        def add_hotspot(city, count):
            print("Step 4: Our detective AI agent is adding crime hotspot to KB as per assignment requirement.")
            try:
                city_norm = city.lower().replace(' ', '_')
                prolog.assertz(f"hotspot('{city_norm}', {count})")
                print(f"Step 4: Added hotspot to KB: {city_norm} with {count} crimes")
                print("Step 4: Finished adding crime hotspot to KB.")
            except Exception as e:
                print(f"Step 4: Sorry, adding hotspot to KB failed: {e}")

        # Assert risky city to KB
        def add_risky_city(city):
            print("Step 4: Our detective AI agent is adding risky city to KB as per assignment requirement.")
            try:
                city_norm = city.lower().replace(' ', '_')
                prolog.assertz(f"riskyCityFact('{city_norm}')")
                print(f"Step 4: Added risky city to KB: {city_norm}")
                print("Step 4: Finished adding risky city to KB.")
            except Exception as e:
                print(f"Step 4: Sorry, adding risky city to KB failed: {e}")

        # Assert victim race to KB
        def add_victim_race(state, race):
            print("Step 4: Our detective AI agent is adding victim race to KB as per assignment requirement.")
            try:
                state_norm = state.lower().replace(' ', '_')
                race_norm = race.lower()
                prolog.assertz(f"victimRaceFact('{state_norm}', '{race_norm}')")
                print(f"Step 4: Added victim race to KB: {race_norm} in {state_norm}")
                print("Step 4: Finished adding victim race to KB.")
            except Exception as e:
                print(f"Step 4: Sorry, adding victim race to KB failed: {e}")

        # Assert alpha-beta suspect score to KB
        def add_suspect_score(age, score):
            print("Step 4: Our detective AI agent is adding suspect score to KB as per assignment requirement.")
            try:
                prolog.assertz(f"suspectScoreFact({age}, {score})")
                print(f"Step 4: Added suspect score to KB: Age {age} with score {score}")
                print("Step 4: Finished adding suspect score to KB.")
            except Exception as e:
                print(f"Step 4: Sorry, adding suspect score to KB failed: {e}")

        # Query KB for race crimes
        def query_race_crimes(race):
            print("Step 5: Our detective AI agent is querying KB for race-based crimes as per assignment requirement.")
            try:
                result = list(prolog.query(f"raceCrime('{race.lower()}', Crime)"))
                if result:
                    print("Step 5: KB returned race crimes:")
                    for r in result:
                        print(f"  - Crime: {r['Crime']}")
                else:
                    print("Step 5: No race crimes found in KB.")
                print("Step 5: Finished querying KB for race crimes.")
                return result
            except Exception as e:
                print(f"Step 5: Sorry, race crime query failed: {e}")
                print("Step 5: Finished querying KB with error.")
                return []

        # Query KB for path
        def query_path(start, goal):
            print("Step 5: Our detective AI agent is querying KB for search path as per assignment requirement.")
            start_norm = start.lower()
            goal_norm = goal.lower()
            try:
                result = list(prolog.query(f"searchPath('{start_norm}', '{goal_norm}', Path)"))
                if result:
                    print("Step 5: KB returned path(s):")
                    for r in result:
                        print(f"  - Path: {r['Path']}")
                    print("Step 5: Finished querying KB for path.")
                    return result[0]['Path'] if result else None
                else:
                    print("Step 5: No path found in KB.")
                    print("Step 5: Finished querying KB for path.")
                    return None
            except Exception as e:
                print(f"Step 5: Sorry, path query failed: {e}")
                print(f"Step 5: Finished querying KB with error.")
                return None

        # Query KB for genetic routes
        def query_genetic_routes():
            print("Step 5: Our detective AI agent is querying KB for genetic routes as per assignment requirement.")
            try:
                result = list(prolog.query("geneticRoute(X, Y)"))
                if result:
                    print("Step 5: KB returned genetic routes:")
                    for r in result:
                        print(f"  - Route: {r['X']} to {r['Y']}")
                else:
                    print("Step 5: No genetic routes found in KB.")
                print("Step 5: Finished querying KB for genetic routes.")
                return result
            except Exception as e:
                print(f"Step 5: Sorry, genetic route query failed: {e}")
                print("Step 5: Finished querying KB with error.")
                return []

        # Query KB for police units
        def query_police_units():
            print("Step 5: Our detective AI agent is querying KB for police assignments as per assignment requirement.")
            try:
                result = list(prolog.query("policeUnits(City, Units)"))
                if result:
                    print("Step 5: KB returned police assignments:")
                    for r in result:
                        print(f"  - {r['City']}: {r['Units']} units")
                else:
                    print("Step 5: No police assignments found in KB.")
                print("Step 5: Finished querying KB for police assignments.")
                return result
            except Exception as e:
                print(f"Step 5: Sorry, police units query failed: {e}")
                print("Step 5: Finished querying KB with error.")
                return []

        # Query KB for hotspots
        def query_hotspots():
            print("Step 5: Our detective AI agent is querying KB for crime hotspots as per assignment requirement.")
            try:
                result = list(prolog.query("crimeHotspot(City, Count)"))
                if result:
                    print("Step 5: KB returned crime hotspots:")
                    for r in result:
                        print(f"  - {r['City']}: {r['Count']} crimes")
                else:
                    print("Step 5: No crime hotspots found in KB.")
                print("Step 5: Finished querying KB for crime hotspots.")
                return result
            except Exception as e:
                print(f"Step 5: Sorry, hotspot query failed: {e}")
                print("Step 5: Finished querying KB with error.")
                return []

        # Query KB for risky cities
        def query_risky_cities():
            print("Step 5: Our detective AI agent is querying KB for risky cities as per assignment requirement.")
            try:
                result = list(prolog.query("riskyCity(City)"))
                if result:
                    print("Step 5: KB returned risky cities:")
                    for r in result:
                        print(f"  - City: {r['City']}")
                else:
                    print("Step 5: No risky cities found in KB.")
                print("Step 5: Finished querying KB for risky cities.")
                return result
            except Exception as e:
                print(f"Step 5: Sorry, risky city query failed: {e}")
                print("Step 5: Finished querying KB with error.")
                return []

        # Query KB for victim races
        def query_victim_races(state):
            print("Step 5: Our detective AI agent is querying KB for victim races as per assignment requirement.")
            state_norm = state.lower()
            try:
                result = list(prolog.query(f"victimRace('{state_norm}', Race)"))
                if result:
                    print("Step 5: KB returned victim races:")
                    for r in result:
                        print(f"  - Race: {r['Race']}")
                else:
                    print("Step 5: No victim races found in KB.")
                print("Step 5: Finished querying KB for victim races.")
                return result
            except Exception as e:
                print(f"Step 5: Sorry, victim race query failed: {e}")
                print("Step 5: Finished querying KB with error.")
                return []

        # Query KB for suspect scores
        def query_suspect_scores():
            print("Step 5: Our detective AI agent is querying KB for suspect scores as per assignment requirement.")
            try:
                result = list(prolog.query("suspectScore(Age, Score)"))
                if result:
                    print("Step 5: KB returned suspect scores:")
                    for r in result:
                        print(f"  - Age {r['Age']}: Score {r['Score']}")
                else:
                    print("Step 5: No suspect scores found in KB.")
                print("Step 5: Finished querying KB for suspect scores.")
                return result
            except Exception as e:
                print(f"Step 5: Sorry, suspect score query failed: {e}")
                print("Step 5: Finished querying KB with error.")
                return []

        # Make decision for race crimes
        def decide_race_crimes(race, crimes):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement.")
            if crimes:
                print(f"Step 6: Decision: Increase patrols in areas where {race} is linked to crimes like {', '.join([r['Crime'] for r in crimes])}.")
            else:
                print(f"Step 6: Decision: No {race} crime data in KB, broaden investigation.")
            print("Step 6: Finished making decision.")

        # Make decision for path
        def decide_path(path):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement.")
            if path:
                print(f"Step 6: Decision: Send agents along path {path} to investigate suspects.")
            else:
                print("Step 6: Decision: No path found, focus on local investigations.")
            print("Step 6: Finished making decision.")

        # Make decision for genetic routes
        def decide_genetic_routes(routes):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement.")
            if routes:
                print(f"Step 6: Decision: Deploy police along routes like {routes[0]['X']} to {routes[0]['Y']}.")
            else:
                print("Step 6: Decision: No routes in KB, optimize local deployments.")
            print("Step 6: Finished making decision.")

        # Make decision for police units
        def decide_police_units(units):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement.")
            if units:
                print(f"Step 6: Decision: Reinforce {units[0]['City']} with {units[0]['Units']} units.")
            else:
                print("Step 6: Decision: No assignments in KB, redistribute police.")
            print("Step 6: Finished making decision.")

        # Make decision for deployment
        def decide_deployment(cities):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement.")
            if cities:
                print(f"Step 6: Decision: Deploy police to high-crime cities: {cities}.")
            else:
                print("Step 6: Decision: No optimal deployment found, analyze more data.")
            print("Step 6: Finished making decision.")

        # Make decision for hotspots
        def decide_hotspots(hotspots):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement.")
            if hotspots:
                print(f"Step 6: Decision: Set up task force in hotspot {hotspots[0]['City']} with {hotspots[0]['Count']} crimes.")
            else:
                print("Step 6: Decision: No hotspots in KB, monitor all cities.")
            print("Step 6: Finished making decision.")

        # Make decision for risky cities
        def decide_risky_cities(cities):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement.")
            if cities:
                print(f"Step 6: Decision: Increase surveillance in risky city {cities[0]['City']}.")
            else:
                print("Step 6: Decision: No risky cities in KB, monitor all cities.")
            print("Step 6: Finished making decision.")

        # Make decision for victim races
        def decide_victim_races(state, races):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement.")
            if races:
                print(f"Step 6: Decision: Interview victims of race {races[0]['Race']} in {state}.")
            else:
                print(f"Step 6: Decision: No victim races in KB for {state}, expand victim interviews.")
            print("Step 6: Finished making decision.")

        # Make decision for suspect scores
        def decide_suspect_scores(scores):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement.")
            if scores:
                print(f"Step 6: Decision: Prioritize suspects with age {scores[0]['Age']} and score {scores[0]['Score']}.")
            else:
                print("Step 6: Decision: No suspect scores in KB, broaden suspect profiling.")
            print("Step 6: Finished making decision.")

         # Make decision for CSP assignments
        def decide_assignments(assignments):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement.")
            if assignments:
                assignment_str = ", ".join([f"{city}: {units} units" for city, units in assignments])
                print(f"Step 6: Decision: Assign police units to cities: {assignment_str}.")
            else:
                print("Step 6: Decision: No valid police assignments found, reassess strategy.")
            print("Step 6: Finished making decision.")

        # Make decision for BFS city-crime relations
        def decide_city_crimes(city, crimes):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement.")
            if crimes:
                print(f"Step 6: Decision: Increase patrols in {city} targeting crimes: {crimes}.")
            else:
                print(f"Step 6: Decision: No crime data for {city} in KB, expand investigation.")
            print("Step 6: Finished making decision.")

        def decide_criminal_city(kb_result):
            print("Step 6: Our detective AI agent is making a decision based on KB knowledge as per assignment requirement.")
            if kb_result and len(kb_result) == 2:
                city, count = kb_result
                print(f"Step 6: Decision: Increase patrols in {city} with {count} crimes.")
            else:
                print("Step 6: Decision: No most criminal city found in KB, analyze more data.")
            print("Step 6: Finished making decision.")

        # Sherlock Holmes Menu
        while True:
            print("\n=====================================")
            print("Respected User, I am the LAB Assignment 3 Agent, an AI detective agent based on the Assignment2 PYthon files.")
            print("Please choose an option to solve the case:")
            print("1. Find special race people involved in crime (DFS):")
            print("2. Find a path between cities (A Star):")
            print("3. Find optimal police deployment cities (Genetic Algorithm):")
            print("4. Assign police units to high-crime cities (CSP):")
            print("5. Explore crimes by city (BFS):")
            print("6. Find a path between cities (Greedy Best-First):")
            print("7. Find the city with most crimes (Hill Climbing):")
            print("8. Find risky cities for criminals (MinMax):")
            print("9. Find victim race in a state (IDDFS):")
            print("10. Identify high-risk suspects (Alpha-Beta Pruning):")
            print("11. Exit the program.")
            print("=====================================")
            choice = input("Enter your choice (1-11): ")

            if choice == '1':
                print("\nStep 3: Our detective AI agent is running DFS to find race-based crimes as per assignment requirement.")
                race = "Black"
                result = run_script("dfs.py", "dfs_search", race)
                if result and isinstance(result, dict) and "Crimes" in result and "KB_Crimes" in result:
                    crimes = result["Crimes"]
                    kb_crimes = result["KB_Crimes"]
                    print(f"Step 3: DFS found crimes for {race}: {crimes}")
                    decide_race_crimes(race, kb_crimes)
                else:
                    print("Step 3: DFS failed to find race-based crimes.")
                    decide_race_crimes(race, [])


            elif choice == '2':
                print("\nStep 3: Our detective AI agent is running A* to find a path between cities as per assignment requirement.")
                start_city = "juneau"
                goal_city = "bethel"
                result = run_script("aStar.py", "aStarSearch", start_city, goal_city)
                if result and isinstance(result, dict) and "Path" in result and "KB_Path" in result:
                    path = result["Path"]
                    kb_path = result["KB_Path"]
                    print(f"Step 3: A* found path: {path}")
                    decide_path(kb_path)
                else:
                    print("Step 3: A* failed to find a path.")
                    decide_path(None)

            elif choice == '3':
                print("\nStep 3: Our detective AI agent is running Genetic Algorithm to find optimal police deployment cities as per assignment requirement.")
                result = run_script("geneticAlgorithim.py", "genetic_algorithm")
                if result and isinstance(result, dict) and "Strategy" in result and "KB_Strategy" in result:
                    strategy = result["Strategy"]
                    kb_strategy = result["KB_Strategy"]
                    print(f"Step 3: Genetic Algorithm found deployment strategy: {strategy}")
                    decide_deployment(kb_strategy)
                else:
                    print("Step 3: Genetic Algorithm failed to find a deployment strategy.")
                    decide_deployment([])

            elif choice == '4':
                print("\nStep 3: Our detective AI agent is running CSP to assign police units to high-crime cities as per assignment requirement.")
                result = run_script("csp.py", "csp_solver")
                if result and isinstance(result, dict) and "Assignments" in result and "KB_Assignments" in result:
                    assignments = result["Assignments"]
                    kb_assignments = result["KB_Assignments"]
                    print(f"Step 3: CSP found assignments: {assignments}")
                    decide_assignments(kb_assignments)
                else:
                    print("Step 3: CSP failed to find police assignments.")
                    decide_assignments([])

            elif choice == '5':
                print("\nStep 3: Our detective AI agent is running BFS to explore crimes by city as per assignment requirement.")
                start_city = "anchorage"
                result = run_script("bfs.py", "bfs_explore", start_city)
                if result and isinstance(result, dict) and "CityCrimes" in result and "KB_CityCrimes" in result:
                    city_crimes = result["CityCrimes"]
                    kb_crimes = result["KB_CityCrimes"]
                    city = next(iter(city_crimes), "Unknown")
                    print(f"Step 3: BFS found crimes for {city}: {city_crimes.get(city, [])}")
                    decide_city_crimes(city, kb_crimes)
                else:
                    print("Step 3: BFS failed to find city-crime relations.")
                    decide_city_crimes("Chicago", [])

            elif choice == '6':
                print("\nStep 3: Our detective AI agent is running Greedy Best-First to find a path between cities as per assignment requirement.")
                start_city = "anchorage"
                goal_city = "juneau"
                result = run_script("greedyFirstSearch.py", "greedy_best_first_search", start_city, goal_city)
                if result and isinstance(result, dict) and "Path" in result and "KB_Path" in result:
                    path = result["Path"]
                    kb_path = result["KB_Path"]
                    print(f"Step 3: Greedy Best-First found path: {path}")
                    decide_path(kb_path)
                else:
                    print("Step 3: Greedy Best-First failed to find a path.")
                    decide_path([])

            elif choice == '7':
                print("\nStep 3: Our detective AI agent is running Hill Climbing to find the city with most crimes as per assignment requirement.")
                result = run_script("hillClimbing.py", "hill_climbing_search")
                if result and isinstance(result, dict) and "City" in result and "KB_Result" in result:
                    city = result["City"]
                    crime_count = result["CrimeCount"]
                    kb_result = result["KB_Result"]
                    print(f"Step 3: Hill Climbing found most criminal city: {city} with {crime_count} crimes")
                    decide_criminal_city(kb_result)
                else:
                    print("Step 3: Hill Climbing failed to find the most criminal city.")
                    decide_criminal_city([])

            elif choice == '8':
                print("\nStep 3: Our detective AI agent is running MinMax to find risky cities for criminals as per assignment requirement.")
                result = run_script("minMax.py", "min_max_search")
                if result and isinstance(result, dict) and "City" in result and "KB_Result" in result:
                    city = result["City"]
                    risk_score = result["RiskScore"]
                    kb_result = result["KB_Result"]
                    print(f"Step 3: MinMax found riskiest city: {city} with risk score: {risk_score}")
                    decide_deployment([kb_result] if kb_result else [])
                else:
                    print("Step 3: MinMax failed to find risky cities.")
                    decide_deployment([])

            elif choice == '9':
                print("\nStep 3: Our detective AI agent is running IDDFS to find victim races as per assignment requirement.")
                state = "Michigan"
                race = "Black"
                result = run_script("iddfs.py", "iddfs_search", state, race)
                if result and isinstance(result, dict) and "State" in result and "KB_Result" in result:
                    state = result["State"]
                    race = result["Race"]
                    found = result["Found"]
                    kb_result = result["KB_Result"]
                    print(f"Step 3: IDDFS {'found' if found else 'did not find'} victim race: {race} in {state}")
                    if found:
                        add_victim_race(state, race)
                    kb_races = query_victim_races(state)
                    decide_victim_races(state, kb_races)
                else:
                    print("Step 3: IDDFS failed to find victim race.")
                    decide_victim_races(state, [])

            elif choice == '10':
                print("\nStep 3: Our detective AI agent is running Alpha-Beta for suspects as per assignment requirement.")
                # Load and prepare suspect data
                try:
                    crime_df = pd.read_csv("US_Crime_DataSet.csv", low_memory=False)
                    crime_df = crime_df.dropna(subset=["Perpetrator Age", "Perpetrator Sex", "Weapon"])
                    crime_df["Perpetrator Age"] = pd.to_numeric(crime_df["Perpetrator Age"], errors="coerce")
                    crime_df = crime_df.dropna(subset=["Perpetrator Age"])
                    crime_df["Perpetrator Age"] = crime_df["Perpetrator Age"].astype(int)
                    crime_df = crime_df[crime_df["Perpetrator Age"] > 20]
                    def calculateCrimeScore(row):
                        age_factor = max(1, 40 - row["Perpetrator Age"])
                        weapon_factor = 2 if "firearm" in row["Weapon"].lower() else 1
                        victim_factor = row["Victim Count"]
                        return age_factor + weapon_factor + victim_factor
                    crime_df["Crime Score"] = crime_df.apply(calculateCrimeScore, axis=1)
                    suspect_scores = crime_df[["Perpetrator Age", "Crime Score"]].sort_values(by="Crime Score", ascending=False).head(400).reset_index(drop=True)
                    print("Step 3: Prepared suspect scores:", suspect_scores.head().to_dict())
                except Exception as e:
                    print(f"Step 3: Failed to prepare suspect data: {e}")
                    suspect_scores = pd.DataFrame()
                # Run Alpha-Beta
                result = run_script("alphaBetaPruning.py", "minimax_alpha_beta", suspect_scores)
                if result and isinstance(result, dict) and "Age" in result and "KB_Result" in result:
                    age = result["Age"]
                    score = result["Score"]
                    kb_result = result["KB_Result"]
                    print(f"Step 3: Alpha-Beta found suspect score: {score} for age {age}")
                    if score > 0:
                        add_suspect_score(age, score)
                    kb_scores = query_suspect_scores()
                    decide_suspect_scores(kb_scores)
                else:
                    print("Step 3: Alpha-Beta failed to find suspect score.")
                    decide_suspect_scores([])

            elif choice == '11':
                print("\nStep 7: Our detective AI agent is signing off. Case closed.")
                break

            else:
                print("\nStep 7: Sorry, invalid choice. Pick a number from 1 to 11.")

    except Exception as e:
        print(f"Step 7: Oh no, our detective AI agent tripped: {e}")
        raise

if __name__ == "__main__":
    run_agent()