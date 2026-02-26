import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output folder if not exists
if not os.path.exists("../output"):
    os.makedirs("../output")

# Load datasets
matches = pd.read_csv("../data/matches.csv")
deliveries = pd.read_csv("../data/deliveries.csv")

print("Data Loaded Successfully ✅")

# -------------------------------
# 1️⃣ Most Successful Teams
# -------------------------------

team_wins = matches['winner'].value_counts()

print("\nTop 10 Teams by Wins:")
print(team_wins.head(10))

plt.figure(figsize=(10,6))
team_wins.head(10).plot(kind='bar')
plt.title("Top 10 Teams by Wins in IPL")
plt.xlabel("Team")
plt.ylabel("Number of Wins")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../output/team_wins.png")
plt.close()

# -------------------------------
# 2️⃣ Top 10 Batsmen (Total Runs)
# -------------------------------

batsman_runs = deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False)

print("\nTop 10 Batsmen:")
print(batsman_runs.head(10))

plt.figure(figsize=(10,6))
batsman_runs.head(10).plot(kind='bar')
plt.title("Top 10 Batsmen by Total Runs")
plt.xlabel("Batsman")
plt.ylabel("Total Runs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../output/top_batsmen.png")
plt.close()

# -------------------------------
# 3️⃣ Top 10 Bowlers (Wickets)
# -------------------------------

# Wicket types excluding run out
wickets = deliveries[deliveries['dismissal_kind'].notnull()]
wickets = wickets[wickets['dismissal_kind'] != 'run out']

top_bowlers = wickets['bowler'].value_counts()

print("\nTop 10 Bowlers:")
print(top_bowlers.head(10))

plt.figure(figsize=(10,6))
top_bowlers.head(10).plot(kind='bar')
plt.title("Top 10 Bowlers by Wickets")
plt.xlabel("Bowler")
plt.ylabel("Wickets")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../output/top_bowlers.png")
plt.close()

# -------------------------------
# 4️⃣ Toss Impact Analysis
# -------------------------------

toss_win_match_win = matches[matches['toss_winner'] == matches['winner']]

toss_impact_percentage = (len(toss_win_match_win) / len(matches)) * 100

print("\nToss Impact:")
print(f"{toss_impact_percentage:.2f}% of matches won by team that won the toss")

print("\nAnalysis Completed Successfully 🚀")