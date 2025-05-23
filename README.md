AI Lab Assignment 3
Supervisor: Dr. Zunaira RauffTopic: Create AI Agent Integrated with Python  
Project Details
This project is my AI crime detection agent, built to tackle suspect prioritization and path-finding for crime investigations. It integrates Python, Prolog, and a CSV dataset to make smart decisions, combining logic-based reasoning with search algorithms. The goal was to create an AI that processes crime data, identifies key suspects, and finds optimal paths between locations, all while being robust and efficient.
What It Does

Suspect Prioritization: Uses Prolog (kb.pl) to query a knowledge base with over 50 facts and 15+ rules, pulling data from suspects.csv (11 columns: Name, HasGun, etc.) to rank suspects based on crime type and location.
Path-Finding: Implements BFS and A* algorithms (bfs.py, aStar.py) to find paths between cities (e.g., Chicago to Miami), guided by Prolog for accuracy.
Genetic Algorithm: Runs a genetic algorithm (geneticAlgorithim.py) to optimize suspect selection, integrated with the CSV data.
Real-Time Updates: File changes (e.g., kb.pl, suspects.csv) are reflected instantly via Docker volume mounting (/app).

Key Components

runme.py: The main script that ties everything together. It loads suspects.csv, consults kb.pl, adds new suspects, and runs BFS, A*, and genetic algorithms.
kb.pl: Prolog knowledge base with 50+ facts and 15+ rules for suspect queries (e.g., sortAllSuspects, path_between).
suspects.csv: Dataset with suspect details (Name, HasGun, HasAngerIssues, etc.).
bfs.py, aStar.py: Implement BFS and A* for path-finding, guided by Prolog.
geneticAlgorithim.py: Genetic algorithm for suspect optimization.
Other Scripts: Includes alphaBetaPruning.py, csp.py, dfs.py, etc., for additional AI techniques.

How to Run

Setup:

Ensure all files (runme.py, kb.pl, suspects.csv, etc.) are in the same directory.
Use an Ubuntu-based Docker container with SWI-Prolog 8.4.3 and pyswip==0.3.0 (see below for installation).
Mount the project directory: docker run -it -v "$(pwd)":/app my-ai-lab3-agent.


Install Dependencies (in container’s bash):
apt-get update
apt-get install -y python3 python3-pip libjpeg-dev zlib1g-dev gcc g++ make cmake libgmp-dev libssl-dev libpcre3-dev libyaml-dev libncurses5-dev wget
cd /tmp
wget https://www.swi-prolog.org/download/stable/src/swipl-8.4.3.tar.gz
tar -xzf swipl-8.4.3.tar.gz
cd swipl-8.4.3
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr/local ..
make -j$(nproc)
make install
cd /tmp
rm -rf swipl-8.4.3 swipl-8.4.3.tar.gz
pip3 install --no-cache-dir pandas numpy pyswip==0.3.0
export SWI_HOME_DIR=/usr/local/lib/swipl
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH


Execute:

Run the agent:cd /app
python3 runme.py

This processes suspects.csv, queries kb.pl, and runs BFS, A*, and genetic algorithms.
Run Prolog queries:swipl kb.pl
sortAllSuspects.
halt.





Challenges and Fixes

pyswip Error: Fixed the PL_put_chars error by using SWI-Prolog 8.4.3 and pyswip==0.3.0, avoiding FLI issues with 9.2.9.
File Syncing: Docker volume mounting ensures real-time file updates.
Path Issues: Handled spaces in /home/numberoneuser/AI Lab/LAB Assignment/Lab Assingment3/pythonCodeWithPLIntegeration using escaped paths.

Files

Core: runme.py, kb.pl, suspects.csv, bfs.py, aStar.py, geneticAlgorithim.py
Docs: AILabAss3Report.docx, howToRunTheAgent.docx, projectReport.md
Extras: alphaBetaPruning.py, csp.py, dfs.py, greedyFirstSearch.py, hillClimbing.py, iddfs.py, minMax.py, US_Crime_DataSet.csv

This project shows how AI can combine logic (Prolog), data (CSV), and algorithms (Python) to solve real-world problems like crime detection. It’s my take on building a smart, integrated agent for AI Lab Assignment 3.
