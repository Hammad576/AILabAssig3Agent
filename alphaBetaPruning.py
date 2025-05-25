import pandas as pd
import numpy as np
from pyswip import Prolog
import re

# Step 3.1.0: Initialize Prolog
print("Step 3.1.0: Initializing Prolog for Alpha-Beta KB operations!")
prolog = Prolog()
prolog.consult('kb.pl')
print("Step 3.1.0: Prolog initialized with kb.pl!")

# Step 3.1.1: Load and process dataset
dataset_path = "US_Crime_DataSet.csv"
try:
    df = pd.read_csv(dataset_path, low_memory=False)
except FileNotFoundError:
    print("Step 3.1.1: Error: US_Crime_DataSet.csv not found!")
    exit()

# Verify required columns
required_columns = {"Perpetrator Age", "Perpetrator Sex", "Weapon", "Victim Count"}
if not required_columns.issubset(df.columns):
    print(f"Step 3.1.1: Error: Dataset must contain {required_columns} columns!")
    exit()

# Data Cleaning
df = df.dropna(subset=["Perpetrator Age", "Perpetrator Sex", "Weapon"])
df["Perpetrator Age"] = pd.to_numeric(df["Perpetrator Age"], errors="coerce")
df = df.dropna(subset=["Perpetrator Age"])
df["Perpetrator Age"] = df["Perpetrator Age"].astype(int)
df = df[df["Perpetrator Age"] > 20]

# Debug: Print dataset info
print("Step 3.1.1: My Crime Dataset Columns:", df.columns)
print("Step 3.1.1: Unique Ages:", df["Perpetrator Age"].unique()[:10].tolist())
print("Step 3.1.1: Sample Data:", df[["Perpetrator Age", "Weapon", "Victim Count"]].head().to_dict())

# Calculate suspect scores
def calculateCrimeScore(row):
    age_factor = max(1, 40 - row["Perpetrator Age"])  # Younger = higher risk
    weapon_factor = 2 if "firearm" in row["Weapon"].lower() else 1  # Guns = higher risk
    victim_factor = row["Victim Count"]  # More victims = higher risk
    return age_factor + weapon_factor + victim_factor

df["Crime Score"] = df.apply(calculateCrimeScore, axis=1)
suspect_scores = df[["Perpetrator Age", "Crime Score"]].sort_values(by="Crime Score", ascending=False).head(400).reset_index(drop=True)
print("Step 3.1.1: Top suspects:", suspect_scores.head().to_dict())

# Sanitize for Prolog
def sanitize_term(term):
    sanitized = re.sub(r'[^a-z0-9_]', '_', str(term).lower())
    sanitized = re.sub(r'_+', '_', sanitized).strip('_')
    return sanitized

# Assert suspect score to KB
def add_suspect_score(age, score):
    print("Step 3.1.4: Adding suspect score to KB!")
    try:
        prolog.query(f"retractall(suspectScoreFact({age}, _))")
        print("Step 3.1.4: Cleared existing suspectScoreFact for age")
        prolog.assertz(f"suspectScoreFact({age}, {score})")
        print(f"Step 3.1.4: Added to KB: suspectScoreFact({age}, {score})")
        print("Step 3.1.4: Finished adding suspect score to KB!")
    except Exception as e:
        print(f"Step 3.1.4: Oops, adding suspect score to KB failed: {e}")

# Query KB for suspect score
def query_suspect_score(age):
    print("Step 3.1.5: Querying KB for suspect score!")
    try:
        facts = list(prolog.query(f"suspectScore({age}, Score)"))
        print(f"Step 3.1.5: Debug: Current suspectScore facts: {facts}")
        if facts:
            result = [age, facts[0]['Score']]
            print(f"Step 3.1.5: KB returned: {result}")
        else:
            result = []
            print("Step 3.1.5: No suspect score found in KB!")
        print("Step 3.1.5: Finished querying KB!")
        return result
    except Exception as e:
        print(f"Step 3.1.5: Oops, KB query failed: {e}")
        return []

# Alpha-Beta Pruning
def minimax_alpha_beta(suspects, depth=5, iteration_limit=150):
    print(f"Step 3.1.2: Starting Alpha-Beta Pruning to find high-risk suspect")
    iteration_count = 0

    def search(suspects, depth, alpha, beta, maximizing_player, path="Root"):
        nonlocal iteration_count
        if iteration_count >= iteration_limit or depth == 0 or suspects.empty:
            score = np.mean(suspects["Crime Score"]) if not suspects.empty else 0
            print(f"Step 3.1.2: Leaf node reached at {path}, score: {score}")
            return score

        if maximizing_player:
            max_eval = float('-inf')
            for i in range(len(suspects)):
                iteration_count += 1
                if iteration_count >= iteration_limit:
                    print(f"Step 3.1.2: Iteration limit {iteration_limit} reached")
                    return max_eval
                new_suspects = suspects.iloc[i+1:].copy()
                eval_score = search(new_suspects, depth - 1, alpha, beta, False, f"Suspect {i}")
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    print(f"Step 3.1.2: Pruning at {path}, beta {beta} <= alpha {alpha}")
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(len(suspects)):
                iteration_count += 1
                if iteration_count >= iteration_limit:
                    print(f"Step 3.1.2: Iteration limit {iteration_limit} reached")
                    return min_eval
                new_suspects = suspects.iloc[i+1:].copy()
                eval_score = search(new_suspects, depth - 1, alpha, beta, True, f"Suspect {i}")
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    print(f"Step 3.1.2: Pruning at {path}, beta {beta} <= alpha {alpha}")
                    break
            return min_eval

    best_score = search(suspects, depth, float('-inf'), float('inf'), True)
    if best_score > 0:
        top_suspect = suspects.loc[suspects["Crime Score"].idxmax()]
        age = int(top_suspect["Perpetrator Age"])
        score = round(best_score, 2)
        print(f"Step 3.1.2: Alpha-Beta found suspect: Age {age}, Score {score}")
        add_suspect_score(age, score)
        kb_result = query_suspect_score(age)
    else:
        print("Step 3.1.2: No strong suspects found")
        age, score, kb_result = 0, 0, []

    print("Step 3.1.3: Alpha-Beta completed!")
    return {
        "Age": age,
        "Score": score,
        "KB_Result": kb_result
    }

# For standalone testing
if __name__ == "__main__":
    result = minimax_alpha_beta(suspect_scores)
    print("Alpha-Beta Result:", result)