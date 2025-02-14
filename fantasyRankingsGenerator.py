import csv
from collections import defaultdict

# Read data
rows = []
with open('extendedFamily.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['pointsFor'] = float(row['pointsFor'])
        rows.append(row)

# Group by week
weeks = defaultdict(list)
for r in rows:
    week_number = int(r['week'])
    weeks[week_number].append(r)

# We assume a fixed number of teams, e.g., 12
num_teams = 12
max_wins = num_teams - 1  
max_losses = num_teams - 1

team_records = defaultdict(lambda: {"wins": 0, "losses": 0})

for wk in range(1, 15):  
    week_data = weeks[wk]

    week_data.sort(key=lambda x: x['pointsFor'], reverse=True)
    
    for rank, team_row in enumerate(week_data):
        team_name = team_row['teamName']
        wins = max_wins - rank
        losses = rank

        team_records[team_name]['wins'] += wins
        team_records[team_name]['losses'] += losses


sorted_teams = sorted(team_records.items(), key=lambda item: (item[1]['wins'], -item[1]['losses']), reverse=True)

for team, record in sorted_teams:
    print(f"{team}: {record['wins']}-{record['losses']}")