# My AI Detective Agent with CSV file Integerated
# This runs our cool detective stuff with Prolog and Python
# Note: Put suspects.csv, kb.pl, bfs.py, aStar.py, geneticAlgorithim.py in same folder
# Run with `python3 runme.py`

import pandas as pd
from pyswip import Prolog
import importlib.util
import sys
import uuid
import os

def run_agent():
    try:
        # Start our detective work
        print("Our detective AI agent is now starting the case!")

        # Set up Prolog and load kb.pl
        prolog = Prolog()
        print("Our detective AI agent is reading the Prolog file: kb.pl")
        prolog.consult('kb.pl')

        # Load suspects CSV
        dataset_path = "suspects.csv"
        print(f"Our detective AI agent is checking suspects CSV: {dataset_path}")
        df = pd.read_csv(dataset_path)

        # Check suspects in a city
        def should_investigate(suspect, crime_type, location):
            location_norm = location.lower()
            query = f"suspectsByLocation('{crime_type}', '{location_norm}', '{suspect}', Reasons)"
            print(f"Our detective AI agent is asking Prolog about {suspect} in {location_norm}")
            try:
                result = list(prolog.query(query))
                return bool(result), result
            except Exception as e:
                print(f"Oops, Prolog query went wrong: {e}")
                return False, []

        # Build a crime map for BFS and A*
        print("Our detective AI agent is making a crime map from suspects.csv")
        crime_dict = {}
        for _, row in df.iterrows():
            city = str(row["Location"]).strip().lower()
            crime_type = (str(row["HasMotive"]).strip().lower() == 'yes') and 'murder' or 'other'
            if city and crime_type:
                if city not in crime_dict:
                    crime_dict[city] = set()
                should, reasons = should_investigate(row["Name"], 'murder', city)
                if should:
                    crime_dict[city].add(crime_type)
                    print(f"Suspect {row['Name']} in {city} is fishy for {crime_type}: {reasons}")

        # Run a Python script (like bfs.py or aStar.py)
        def run_script(script_name, function_name, *args):
            print(f"Our detective AI agent is running script: {script_name}")
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

        # Ask Prolog for a path between cities
        def find_path(start_city, goal_city):
            start_city_norm = start_city.lower()
            goal_city_norm = goal_city.lower()
            query = f"pathBetween('{start_city_norm}', '{goal_city_norm}', Path)"
            print(f"Our detective AI agent is asking Prolog for a path from {start_city_norm} to {goal_city_norm}")
            try:
                result = list(prolog.query(query))
                if result:
                    path = result[0]['Path']
                    print(f"Our detective AI agent found a path: {path}")
                    return path
                else:
                    print(f"No path found from {start_city_norm} to {goal_city_norm}, bummer!")
                    return None
            except Exception as e:
                print(f"Oops, path query failed: {e}")
                return None

        # Add a new suspect to Prolog KB
        def add_suspect_to_kb(name, has_gun, has_anger_issues, has_motive, has_alibi, has_record, is_sneaky, is_rich, is_smart, is_fast, location):
            location_norm = location.lower()
            print(f"Our detective AI agent is adding suspect {name} to the case!")
            try:
                prolog.assertz(f"suspect('{name}', {has_gun}, {has_anger_issues}, {has_motive}, {has_alibi}, {has_record}, {is_sneaky}, {is_rich}, {is_smart}, {is_fast}, '{location_norm}')")
                if has_gun == 'yes':
                    prolog.assertz(f"hasGun('{name}')")
                if has_anger_issues == 'yes':
                    prolog.assertz(f"hasAngerIssues('{name}')")
                if has_motive == 'yes':
                    prolog.assertz(f"hasMotive('{name}')")
                if has_alibi == 'yes':
                    prolog.assertz(f"hasAlibi('{name}')")
                if has_record == 'yes':
                    prolog.assertz(f"hasRecord('{name}')")
                if is_sneaky == 'yes':
                    prolog.assertz(f"isSneaky('{name}')")
                if is_rich == 'yes':
                    prolog.assertz(f"isRich('{name}')")
                if is_smart == 'yes':
                    prolog.assertz(f"isSmart('{name}')")
                if is_fast == 'yes':
                    prolog.assertz(f"isFast('{name}')")
                prolog.assertz(f"location('{name}', '{location_norm}')")
            except Exception as e:
                print(f"Oops, adding suspect {name} failed: {e}")

        # Add a route from genetic algorithm
        def add_genetic_route(city1, city2):
            city1_norm = city1.lower()
            city2_norm = city2.lower()
            print(f"Our detective AI agent is adding a route from {city1_norm} to {city2_norm}")
            try:
                prolog.assertz(f"connectedCities('{city1_norm}', '{city2_norm}')")
            except Exception as e:
                print(f"Oops, adding route failed: {e}")

        # Run BFS with Prolog help
        def run_bfs_with_prolog(start_city, crime_dict):
            print("\nOur detective AI agent is chasing leads with BFS!")
            start_city_norm = start_city.lower()
            path = find_path(start_city_norm, 'miami')
            if path:
                print(f"Our detective AI agent found a BFS path: {path}")
            run_script("bfs.py", "bfsSearch", crime_dict, start_city_norm)

        # Run A* with Prolog help
        def run_astar_with_prolog(start_city, goal_city, crime_dict):
            print("\nOur detective AI agent is zooming with A*!")
            start_city_norm = start_city.lower()
            goal_city_norm = goal_city.lower()
            path = find_path(start_city_norm, goal_city_norm)
            if path:
                print(f"Our detective AI agent found an A* path: {path}")
            else:
                print("No A* path, falling back to Python!")
                run_script("aStar.py", "aStarSearch", crime_dict, start_city_norm, goal_city_norm)

        # Run genetic algorithm and save routes
        def run_genetic_with_prolog(df):
            print("\nOur detective AI agent is getting fancy with genetic algorithm!")
            result = run_script("geneticAlgorithim.py", "geneticAlgorithm", df)
            if result:
                # Assume genetic algorithm returns a list of (city1, city2) routes
                print("Our detective AI agent is saving genetic routes!")
                for city1, city2 in result[:2]:  # Save first 2 routes for demo
                    add_genetic_route(city1, city2)

        # Main detective work
        print("\nOur detective AI agent is on the case!")
        new_suspect = f"suspect_{uuid.uuid4().hex[:8]}"
        add_suspect_to_kb(new_suspect, 'yes', 'yes', 'yes', 'no', 'no', 'no', 'yes', 'yes', 'no', 'Chicago')
        print(f"Our detective AI agent added new suspect: {new_suspect}")
        
        print("\nOur detective AI agent is sorting suspects with Prolog!")
        prolog.query("sortAllSuspects.")
        
        print("\nOur detective AI agent is finding a path from Chicago to Miami!")
        find_path('Chicago', 'Miami')
        
        run_bfs_with_prolog('Chicago', crime_dict)
        run_astar_with_prolog('Chicago', 'Miami', crime_dict)
        run_genetic_with_prolog(df)
        
        print("Our detective AI agent cracked the case with CSV and Prolog!")

    except Exception as e:
        print(f"Oh no, our detective AI agent tripped: {e}")
        raise

if __name__ == "__main__":
    run_agent()