import pandas as pd
import numpy as np

# Load the dataset
dataset_path = "../US_Crime_DataSet.csv"
df = pd.read_csv(dataset_path, low_memory=False)

# Data Cleaning: Remove rows with missing perpetrator details
df = df.dropna(subset=["Perpetrator Age", "Perpetrator Sex", "Weapon"])  

# Convert necessary columns to appropriate types
df["Perpetrator Age"] = pd.to_numeric(df["Perpetrator Age"], errors="coerce")
df = df.dropna(subset=["Perpetrator Age"])  # Remove invalid ages
df["Perpetrator Age"] = df["Perpetrator Age"].astype(int)  # Convert to integer

# Generate suspect scores based on crime severity
def calculateCrimeScore(row):
    """
    Assigns a risk score to each perpetrator based on:
    - Age (younger criminals tend to be riskier)
    - Use of a weapon (firearm vs. other weapons)
    - Number of victims
    """
    age_factor = max(1, 40 - row["Perpetrator Age"])  
    # Younger criminals = Higher risk
    weapon_factor = 2 if "firearm" in row["Weapon"].lower() else 1  # Guns = Higher risk
    victim_factor = row["Victim Count"]   
    # More victims = Higher risk

    return age_factor + weapon_factor + victim_factor

# Apply crime score function to each perpetrator
df["Crime Score"] = df.apply(calculateCrimeScore, axis=1)
df = df[df["Perpetrator Age"] > 20]
# Select top 400 suspects for analysis based on highest crime scores
suspect_scores = df[["Perpetrator Age", "Crime Score"]].sort_values(by="Crime Score", ascending=False).head(400).reset_index(drop=True)

# Alpha-Beta Pruning Algorithm Application Functin which uses Alpha and Beta
def minimaxAlphaBeta(suspects, depth, alpha, beta, maximizing_player, iteration_limit=150):
    """
    Implements Alpha-Beta Pruning to identify the most dangerous suspect efficiently.
    - Stops execution after reaching iteration_limit.
    - Uses alpha and beta to cut unnecessary evaluations (pruning).
    """
    iteration_count = 0  # Counter to track iterations

    def search(suspects, depth, alpha, beta, maximizing_player, path="Root"):
        nonlocal iteration_count  # Allow function to modify iteration counter
        if iteration_count >= iteration_limit or depth == 0 or suspects.empty:
            return np.mean(suspects["Crime Score"]) if not suspects.empty else 0

        if maximizing_player:
            max_eval = float('-inf')
            for i in range(len(suspects)):
                iteration_count += 1  # Increment iteration count

                new_suspects = suspects.iloc[i+1:].copy()  # Reduce search space
                eval_score = search(new_suspects, depth - 1, alpha, beta, False, f"Suspect {i}")

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                # Apply pruning if beta is less than or equal to alpha
                if beta <= alpha:
                    break

            return max_eval

        else:
            min_eval = float('inf')
            for i in range(len(suspects)):
                iteration_count += 1  # Increment iteration count

                new_suspects = suspects.iloc[i+1:].copy()  # Reduce search space
                eval_score = search(new_suspects, depth - 1, alpha, beta, True, f"Suspect {i}")

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                # Apply pruning if beta is less than or equal to alpha
                if beta <= alpha:
                    break

            return min_eval

    return search(suspects, depth, alpha, beta, maximizing_player)

# Run Alpha-Beta Pruning with a maximum of 150 iterations
best_suspect_score = minimaxAlphaBeta(suspect_scores, depth=5, alpha=float('-inf'), beta=float('inf'), maximizing_player=True, iteration_limit=150)

# Display Results
if best_suspect_score > 0:
    top_suspect = suspect_scores.loc[suspect_scores["Crime Score"].idxmax()]
    print("\n   Investigation Results With Alpha Beta Pruning Using Alpha and Beta for Analysis  ")
    print(f"Most Likely Suspect  : Age {top_suspect['Perpetrator Age']}")
    print(f"Crime Involvement Score  : {round(best_suspect_score, 2)}")
else:
    print("\n   Investigation Results   ")
    print("No strong suspects found. Consider increasing search depth or adjusting the pruning threshold.")
