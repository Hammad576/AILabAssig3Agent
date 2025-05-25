# AI Lab Assignment 3  
**Supervisor:** [**Dr. Zunaira Rauff**](https://scholar.google.com/citations?user=YOUR_SUPERVISOR_ID_HERE)

## 🧠 Topic: Create AI Agent Integrated with Python

---

## 🔍 Project Details

This project is my AI **crime detection agent**, built to tackle **suspect prioritization** and **path-finding** for crime investigations. It integrates **Python**, **Prolog**, and a **CSV dataset** to make smart decisions, combining **logic-based reasoning** with **search algorithms**.

### 🎯 Goal
Create an AI that processes crime data, identifies key suspects, and finds optimal paths between locations—while being robust and efficient.

---

## 🚀 What It Does

- **Suspect Prioritization:**  
  Uses **Prolog (`kb.pl`)** to query a knowledge base with over **50 facts** and **15+ rules**, pulling data from `suspects.csv` (11 columns: Name, HasGun, etc.) to rank suspects based on crime type and location.

- **Path-Finding:**  
  Implements **BFS** and **A\*** algorithms (`bfs.py`, `aStar.py`) to find paths between cities (e.g., Chicago to Miami), guided by Prolog for accuracy.

- **Genetic Algorithm:**  
  Runs a **genetic algorithm** (`geneticAlgorithim.py`) to optimize suspect selection, integrated with the CSV data.

- **Real-Time Updates:**  
  File changes (e.g., `kb.pl`, `suspects.csv`) are reflected instantly via **Docker volume mounting** (`/app`).

---

## 🧩 Key Components

- `runme.py`: Main script that ties everything together. Loads `suspects.csv`, consults `kb.pl`, adds suspects, and runs BFS, A*, and genetic algorithm.
- `kb.pl`: Prolog knowledge base (50+ facts, 15+ rules), includes predicates like `sortAllSuspects`, `path_between`.
- `suspects.csv`: Dataset with suspect details (Name, HasGun, HasAngerIssues, etc.).
- `bfs.py`, `aStar.py`: Implement **BFS** and **A\*** search for crime path-finding.
- `geneticAlgorithim.py`: Optimizes suspect selection using a **genetic algorithm**.
- Other AI scripts:
  - `alphaBetaPruning.py`
  - `csp.py`
  - `dfs.py`
  - `greedyFirstSearch.py`
  - `hillClimbing.py`
  - `iddfs.py`
  - `minMax.py`

---

## ⚙️ How to Run

### 🐳 Setup via Docker

Ensure all files (`runme.py`, `kb.pl`, `suspects.csv`, etc.) are in the same directory.

```bash
docker run -it -v "$(pwd)":/app my-ai-lab3-agent
```
### Inside the Contianer Docker
apt-get update
apt-get install -y python3 python3-pip libjpeg-dev zlib1g-dev gcc g++ make cmake libgmp-dev libssl-dev libpcre3-dev libyaml-dev libncurses5-dev wget

cd /tmp
wget https://www.swi-prolog.org/download/stable/src/swipl-8.4.3.tar.gz
tar -xzf swipl-8.4.3.tar.gz
cd swipl-8.4.3
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr/local ..
make -j$(nproc)
make install

# Clean up
cd /tmp
rm -rf swipl-8.4.3 swipl-8.4.3.tar.gz

# Install Python dependencies
pip3 install --no-cache-dir pandas numpy pyswip==0.3.0

# Environment variables
export SWI_HOME_DIR=/usr/local/lib/swipl
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH

# HOw to Run The project
cd /app
python3 runme.py

# HOw to run the prolog Queries

swipl kb.pl
sortAllSuspects.
halt.
