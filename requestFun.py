import re
from collections import defaultdict

def parse_week_file(filename, week):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    teams = []
    for i in range(1, len(lines)-1):
        if lines[i].startswith('(') and re.match(r'^\(.*\)$', lines[i]):
            team_name = lines[i-1]
            points_line = lines[i+1]
            if re.match(r'^\d+(\.\d+)?$', points_line):
                points_for = float(points_line)
                teams.append((team_name, points_for, week))
    return teams

all_weeks_data = []
for w in range(1, 15):
    fname = f"week{w}.txt"
    all_weeks_data.extend(parse_week_file(fname, w))

# Group by week
weeks = defaultdict(list)
for team_name, points_for, week_num in all_weeks_data:
    # Create a structure like the original code expected
    weeks[week_num].append({
        'teamName': team_name,
        'pointsFor': points_for
    })

num_teams = 12
max_wins = num_teams - 1
max_losses = num_teams - 1

team_records = defaultdict(lambda: {"wins": 0, "losses": 0})

for wk in sorted(weeks.keys()):
    week_data = weeks[wk]
    week_data.sort(key=lambda x: x['pointsFor'], reverse=True)
    
    for rank, team_row in enumerate(week_data):
        team_name = team_row['teamName']
        wins = max_wins - rank
        losses = rank
        team_records[team_name]['wins'] += wins
        team_records[team_name]['losses'] += losses

sorted_teams = sorted(team_records.items(), key=lambda item: (item[1]['wins'], -item[1]['losses']), reverse=True)
print("fantasy league free for all results")
for team, record in sorted_teams:
    print(f"{team}: {record['wins']}-{record['losses']}")

import matplotlib.pyplot as plt
from collections import defaultdict

# Suppose you have all_weeks_data as a list of tuples: (team_name, points_for, week)
# For example: all_weeks_data = [("Team A", 120.5, 1), ("Team B", 98.7, 1), ("Team A", 130.0, 2), ...]

# Group scores by team
team_scores = defaultdict(list)
for team_name, points_for, week in all_weeks_data:
    team_scores[team_name].append(points_for)

# Prepare data for box plot
data = []
labels = []

for team_name, scores in team_scores.items():
    data.append(scores)
    labels.append(team_name)


# Create the figure and plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.boxplot(data, labels=labels, vert=True)

# Optional: rotate labels if you have many teams
plt.xticks(rotation=45, ha='right')

# Add titles and labels
plt.title("Distribution of Weekly Scores by Team")
plt.xlabel("Team")
plt.ylabel("Points For")

plt.tight_layout()
plt.show()



import numpy as np
from collections import defaultdict

# Compute key statistics for each team incase one wants to see it via the command line
stats = {}
for team, scores in team_scores.items():
    arr = np.array(scores)
    minimum = np.min(arr)
    q1 = np.percentile(arr, 25)
    median = np.percentile(arr, 50)
    q3 = np.percentile(arr, 75)
    maximum = np.max(arr)
    stats[team] = {
        'Min': minimum,
        'Q1': q1,
        'Median': median,
        'Q3': q3,
        'Max': maximum
    }

team_col_width = 15
num_col_width = 10

header = f"{'Team':<{team_col_width}}{'Min':>{num_col_width}}{'Q1':>{num_col_width}}{'Median':>{num_col_width}}{'Q3':>{num_col_width}}{'Max':>{num_col_width}}"


print(header)
print("-" * len(header))

for team, s in stats.items():
    line = (
        f"{team:<{team_col_width}}"
        f"{s['Min']:{num_col_width}.2f}"
        f"{s['Q1']:{num_col_width}.2f}"
        f"{s['Median']:{num_col_width}.2f}"
        f"{s['Q3']:{num_col_width}.2f}"
        f"{s['Max']:{num_col_width}.2f}"
    )
    print(line)


