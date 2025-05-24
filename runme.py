# My AI Detective Agent with CSV file Integrated
# This program runs search algorithms with Prolog KB for crime detection
# Note: Place suspects.csv, US_Crime_DataSet.csv, kb.pl, and all Python scripts in the same folder
# Run manually with `python3 runme.py`; file changes reflect immediately

import pandas as pd
from pyswip import Prolog
import importlib.util
import sys
import uuid
import os

def run_agent():
    try:
        # Initialize Prolog and consult kb.pl
        prolog = Prolog()
        print("Consulting Prolog file: kb.pl")
        prolog.consult('kb.pl')

        # Load suspects CSV
        dataset_path = "suspects.csv"
        print(f"Loading suspects CSV: {dataset_path}")
        df = pd.read_csv(dataset_path)

        # Function to query Prolog for suspect prioritization
        def should_investigate(suspect, crime_type, location):
            location_norm = location.lower()  # Normalize to lowercase
            query = f"suspects_by_location('{crime_type}', '{location_norm}', '{suspect}', Reasons)"
            result = list(prolog.query(query))
            return bool(result), result

        # Create crime_dict for BFS and A*
        print("Building crime dictionary from suspects.csv")
        crime_dict = {}
        for _, row in df.iterrows():
            city = str(row["Location"]).strip().lower()  # Normalize to lowercase
            crime_type = str(row["CommittedMurder"]).strip() == 'yes' and 'murder' or 'other'
            if city and crime_type:
                if city not in crime_dict:
                    crime_dict[city] = set()
                should, reasons = should_investigate(row["Name"], 'murder', city)
                if should:
                    crime_dict[city].add(crime_type)
                    print(f"Suspect {row['Name']} in {city} flagged for {crime_type}: {reasons}")

        # Function to load and run a Python script
        def run_script(script_name, function_name, *args):
            print(f"Running script: {script_name}")
            spec = importlib.util.spec_from_file_location(script_name[:-3], script_name)
            module = importlib.util.module_from_spec(spec)
            sys.modules[script_name[:-3]] = module
            spec.loader.exec_module(module)
            func = getattr(module, function_name)
            return func(*args)

        # Function to query Prolog for path between cities
        def find_path(start_city, goal_city, use_heuristic=False):
            start_city_norm = start_city.lower()  # Normalize to lowercase
            goal_city_norm = goal_city.lower()    # Normalize to lowercase
            if not use_heuristic:
                query = f"path_between('{start_city_norm}', '{goal_city_norm}', Path)"
                result = list(prolog.query(query))
                if result:
                    print(f"BFS Path from {start_city_norm} to {goal_city_norm}: {result[0]['Path']}")
                    return result[0]['Path']
                else:
                    print(f"No BFS path found from {start_city_norm} to {goal_city_norm}")
                    return None
            else:
                query = f"path_with_hueristic('{start_city_norm}', '{goal_city_norm}', Path, Cost)"
                print(f"Executing A* query: {query}")
                result = list(prolog.query(query))
                if result:
                    print(f"A* Path from {start_city_norm} to {goal_city_norm}: {result[0]['Path']} (Cost: {result[0]['Cost']})")
                    return result[0]['Path']
                else:
                    print(f"No A* path found from {start_city_norm} to {goal_city_norm}")
                    return None

        # Function to add new suspect to Prolog KB
        def add_suspect_to_kb(name, has_gun, has_anger_issues, committed_murder, criminal_record, smokes_cigarette, reported_in_burglary, has_motive, in_debt, has_faked_id, location):
            location_norm = location.lower()  # Normalize to lowercase
            prolog.assertz(f"suspect('{name}', '{has_gun}', '{has_anger_issues}', '{committed_murder}', '{criminal_record}', '{smokes_cigarette}', '{reported_in_burglary}', '{has_motive}', '{in_debt}', '{has_faked_id}', '{location_norm}')")
            if has_gun == 'yes':
                prolog.assertz(f"hasGun('{name}')")
            if has_anger_issues == 'yes':
                prolog.assertz(f"hasAngerIssues('{name}')")
            if committed_murder == 'yes':
                prolog.assertz(f"haveCommittedMurder('{name}')")
            if criminal_record == 'yes':
                prolog.assertz(f"criminalRecord('{name}')")
            if smokes_cigarette == 'yes':
                prolog.assertz(f"smokeCigarette('{name}')")
            if reported_in_burglary == 'yes':
                prolog.assertz(f"reportedInBurglary('{name}')")
            if has_motive == 'yes':
                prolog.assertz(f"hasMotive('{name}')")
            if in_debt == 'yes':
                prolog.assertz(f"inDebt('{name}')")
            if has_faked_id == 'yes':
                prolog.assertz(f"hasFakedID('{name}')")
            prolog.assertz(f"location('{name}', '{location_norm}')")

        # Wrapper to run BFS with Prolog guidance
        def run_bfs_with_prolog(start_city, crime_dict):
            print("\nRunning BFS with Prolog Guidance")
            start_city_norm = start_city.lower()  # Normalize to lowercase
            run_script("bfs.py", "bfsSearch", crime_dict, start_city_norm)

        # Wrapper to run A* with Prolog guidance
        def run_astar_with_prolog(start_city, goal_city, crime_dict):
            print("\nRunning A* with Prolog Guidance")
            start_city_norm = start_city.lower()  # Normalize to lowercase
            goal_city_norm = goal_city.lower()    # Normalize to lowercase
            path = find_path(start_city_norm, goal_city_norm, use_heuristic=True)
            if path:
                print(f"Prolog-guided A* path: {path}")
            else:
                print("Falling back to aStar.py")
                run_script("aStar.py", "aStarSearch", crime_dict, start_city_norm, goal_city_norm)

        # Wrapper to run Genetic Algorithm with Prolog guidance
        def run_genetic_with_prolog(df):
            print("\nRunning Genetic Algorithm with Prolog Guidance")
            run_script("geneticAlgorithim.py", "geneticAlgorithm", df)

        # Main agent logic
        print("\nRunning AI Detective Agent")
        print("Fetching facts from the Prolog KB")
        new_suspect = f"suspect_{uuid.uuid4().hex[:8]}"
        add_suspect_to_kb(new_suspect, 'yes', 'yes', 'yes', 'no', 'no', 'no', 'yes', 'yes', 'no', 'Chicago')
        print(f"Added new suspect {new_suspect} to KB")
        prolog.query("sortAllSuspects.")
        print("\nFinding path from Chicago to Miami with no heuristic (BFS)")
        find_path('Chicago', 'Miami', use_heuristic=False)
        print("\nFinding path from Chicago to Miami with heuristic (A*)")
        find_path('Chicago', 'Miami', use_heuristic=True)
        run_bfs_with_prolog('Chicago', crime_dict)
        run_astar_with_prolog('Chicago', 'Miami', crime_dict)
        run_genetic_with_prolog(df)
        print("Integrated facts from CSV with algorithms")

    except Exception as e:
        print(f"Error running agent: {e}")
        raise  # Raise for debugging

if __name__ == "__main__":
    run_agent()