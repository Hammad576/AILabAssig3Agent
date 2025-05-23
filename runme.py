# My AI Detective Agent with CSV file Integerated
# This progarm watches ALL files in folder and reruns when any file changes
# NOte: Place suspects.csv, kb.pl, and all Python scripts in the same folder
# Changes to any file (py, pl, csv, etc.) reflect immediately

import pandas as pd
from pyswip import Prolog
import importlib.util
import sys
import uuid
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# File watching class to rerun on any file change
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        self.last_run = 0
        self.debounce = 1  # Seconds to wait before rerunning

    def on_modified(self, event):
        if not event.is_directory:
            current_time = time.time()
            if current_time - self.last_run > self.debounce:
                print(f"\nFile changed: {event.src_path}. Rerunning agent...")
                self.callback(event.src_path)
                self.last_run = current_time

# Core agent logic
def run_agent(changed_file=None):
    try:
        # Initialize Prolog and reload kb.pl if it changed
        prolog = Prolog()
        if changed_file and os.path.basename(changed_file) == 'kb.pl':
            print("Reloading kb.pl due to change...")
        prolog.consult('kb.pl')

        # Load suspects CSV
        dataset_path = "suspects.csv"
        df = pd.read_csv(dataset_path)

        # Function to load and run a Python script
        def run_script(script_name, function_name, *args):
            spec = importlib.util.spec_from_file_location(script_name[:-3], script_name)
            module = importlib.util.module_from_spec(spec)
            sys.modules[script_name[:-3]] = module
            spec.loader.exec_module(module)
            func = getattr(module, function_name)
            return func(*args)

        # Function to query Prolog for suspect prioritization
        def should_investigate(suspect, crime_type, location):
            query = f"suspects_by_location('{crime_type}', '{location}', '{suspect}', Reasons)"
            result = list(prolog.query(query))
            return bool(result), result

        # Function to query Prolog for path between cities
        def find_path(start_city, goal_city, use_heuristic=False):
            if not use_heuristic:
                query = f"path_between('{start_city}', '{goal_city}', Path)"
                result = list(prolog.query(query))
                if result:
                    print(f"BFS Path from {start_city} to {goal_city}: {result[0]['Path']}")
                    return result[0]['Path']
                else:
                    print(f"No BFS path found from {start_city} to {goal_city}")
                    return None
            else:
                query = f"path_with_hueristic('{start_city}', '{goal_city}', Path, Cost)"
                result = list(prolog.query(query))
                if result:
                    print(f"A* Path from {start_city} to {goal_city}: {result[0]['Path']} (Cost: {result[0]['Cost']})")
                    return result[0]['Path']
                else:
                    print(f"No A* path found from {start_city} to {goal_city}")
                    return None

        # Function to add new suspect to Prolog KB
        def add_suspect_to_kb(name, has_gun, has_anger_issues, committed_murder, criminal_record, smokes_cigarette, reported_in_burglary, has_motive, in_debt, has_faked_id, location):
            prolog.assertz(f"suspect('{name}', '{has_gun}', '{has_anger_issues}', '{committed_murder}', '{criminal_record}', '{smokes_cigarette}', '{reported_in_burglary}', '{has_motive}', '{in_debt}', '{has_faked_id}', '{location}')")
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
            prolog.assertz(f"location('{name}', '{location}')")

        # Wrapper to run BFS with Prolog guidance
        def run_bfs_with_prolog(start_city):
            print("\nRunning BFS with Prolog Guidance")
            crime_dict = {}
            for _, row in df.iterrows():
                city = str(row["Location"]).strip()
                crime_type = str(row["CommittedMurder"]).strip() == 'yes' and 'murder' or 'other'
                if city and crime_type:
                    if city not in crime_dict:
                        crime_dict[city] = set()
                    should, _ = should_investigate(row["Name"], 'murder', city)
                    if should:
                        crime_dict[city].add(crime_type)
            run_script("bfs.py", "bfsSearch", crime_dict, start_city)

        # Wrapper to run A* with Prolog guidance
        def run_astar_with_prolog(start_city, goal_city):
            print("\nRunning A* with Prolog Guidance")
            path = find_path(start_city, goal_city, use_heuristic=True)
            if path:
                print(f"Prolog-guided A* path: {path}")
            else:
                run_script("aStar.py", "aStarSearch", crime_dict, start_city, goal_city)

        # Wrapper to run Genetic Algorithm with Prolog guidance
        def run_genetic_with_prolog():
            print("\nRunning Genetic Algorithm with Prolog Guidance")
            run_script("geneticAlgorithim.py", "geneticAlgorithm", df)

        # Main agent logic
        print(f"\nRunning agent (triggered by {changed_file or 'initial run'})")
        print("Our AI AGent Now fetching FActs From the KB")
        new_suspect = f"suspect_{uuid.uuid4().hex[:8]}"
        add_suspect_to_kb(new_suspect, 'yes', 'yes', 'yes', 'no', 'no', 'no', 'yes', 'yes', 'no', 'Chicago')
        print(f"Added new suspect {new_suspect} to KB")
        prolog.query("sortAllSuspects.")
        print("\nFinding path from Chicago to Miami with no hueristic (BFS)")
        find_path('chicago', 'miami', use_heuristic=False)
        print("\nFinding path from Chicago to Miami with hueristic (A*)")
        find_path('chicago', 'miami', use_heuristic=True)
        run_bfs_with_prolog('chicago')
        run_astar_with_prolog('chicago', 'miami')
        run_genetic_with_prolog()
        print("We get the facts from the CSV file and integerated with algorithms")

    except Exception as e:
        print(f"Error running agent: {e}")

# Main function with file watching
def main():
    print("Starting AI Detective Agent with file watching for ALL files...")
    event_handler = FileChangeHandler(run_agent)
    observer = Observer()
    observer.schedule(event_handler, path='/app', recursive=False)
    observer.start()
    try:
        run_agent()  # Initial run
        while True:
            time.sleep(1)  # Keep container running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()