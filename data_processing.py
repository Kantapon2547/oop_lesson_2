import csv
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))

countries = []
with open(os.path.join(__location__, 'Countries.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        countries.append(dict(r))

titanic = []
with open(os.path.join(__location__, 'Titanic.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        titanic.append(dict(r))

teams = []
with open(os.path.join(__location__, 'Teams.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        teams.append(dict(r))

players = []
with open(os.path.join(__location__, 'Players.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        players.append(dict(r))


class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None


import copy


class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table

    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            temps.append(float(item1[aggregation_key]))
        return function(temps)

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def __str__(self):
        return self.table_name + ':' + str(self.table)


table1 = Table('cities', cities)
table2 = Table('countries', countries)
table3 = Table('titanic', titanic)
table4 = Table('teams', teams)
table5 = Table('players', players)
my_DB = DB()
my_DB.insert(table1)
my_DB.insert(table2)
my_DB.insert(table3)
my_DB.insert(table4)
my_DB.insert(table5)
my_table1 = my_DB.search('cities')

print("Test filter: only filtering out cities in Italy")
my_table1_filtered = my_table1.filter(lambda x: x['country'] == 'Italy')
print(my_table1_filtered)
print()

print("Test select: only displaying two fields, city and latitude, for cities in Italy")
my_table1_selected = my_table1_filtered.select(['city', 'latitude'])
print(my_table1_selected)
print()

print("Calculting the average temperature without using aggregate for cities in Italy")
temps = []
for item in my_table1_filtered.table:
    temps.append(float(item['temperature']))
print(sum(temps) / len(temps))
print()

print("Calculting the average temperature using aggregate for cities in Italy")
print(my_table1_filtered.aggregate(lambda x: sum(x) / len(x), 'temperature'))
print()

print("Test join: finding cities in non-EU countries whose temperatures are below 5.0")
my_table2 = my_DB.search('countries')
my_table3 = my_table1.join(my_table2, 'country')
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'no').filter(lambda x: float(x['temperature']) < 5.0)
print(my_table3_filtered.table)
print()
print("Selecting just three fields, city, country, and temperature")
print(my_table3_filtered.select(['city', 'country', 'temperature']))
print()

print("Print the min and max temperatures for cities in EU that do not have coastlines")
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'yes').filter(lambda x: x['coastline'] == 'no')
print("Min temp:", my_table3_filtered.aggregate(lambda x: min(x), 'temperature'))
print("Max temp:", my_table3_filtered.aggregate(lambda x: max(x), 'temperature'))
print()

print("Print the min and max latitude for cities in every country")
for item in my_table2.table:
    my_table1_filtered = my_table1.filter(lambda x: x['country'] == item['country'])
    if len(my_table1_filtered.table) >= 1:
        print(item['country'], (my_table1_filtered.aggregate(lambda x: min(x), 'latitude'),
                                my_table1_filtered.aggregate(lambda x: max(x), 'latitude')))
print()

print("Filter players who played less than 200 minutes and made more than 100 passes")
# players_table = my_DB.search('players')
filtered_players = table5.filter(lambda x: float(x['minutes']) < 200 and int(x['passes']) > 100)
print("""Filter teams with "ia" in the team name""")
# teams_table = my_DB.search('teams')
filtered_teams = table4.filter(lambda x: "ia" in x['team'])

print("Join the filtered players and teams tables")
joined_data = filtered_players.join(filtered_teams, 'team')

print("Select the required attributes: player surname, team, and position")
result = joined_data.select(['surname', 'team', 'position'])
print(result)
print()

print("Calculate the average number of games played for teams below rank 10")
below_rank_10 = table4.filter(lambda x: int(x['ranking']) < 10)
avg_games_below_rank_10 = below_rank_10.aggregate(lambda x: sum(x) / len(x), 'games')

print("Calculate the average number of games played for teams rank 10 or above")
rank_10_or_above = table4.filter(lambda x: int(x['ranking']) >= 10)
avg_games_rank_10_or_above = rank_10_or_above.aggregate(lambda x: sum(x) / len(x), 'games')

print("Average games played for teams below rank 10:", avg_games_below_rank_10)
print("Average games played for teams rank 10 or above:", avg_games_rank_10_or_above)
print()

print("Calculate the average number of passes made by forwards")
forwards = table5.filter(lambda x: x['position'] == 'Forward')
if len(forwards.table) > 0:
    avg_passes_forwards = forwards.aggregate(lambda x: sum(x) / len(x), 'passes')
else:
    avg_passes_forwards = 0

print("Calculate the average number of passes made by midfielders")
midfielders = table5.filter(lambda x: x['position'] == 'Midfielder')
if len(midfielders.table) > 0:
    avg_passes_midfielders = midfielders.aggregate(lambda x: sum(x) / len(x), 'passes')
else:
    avg_passes_midfielders = 0

print("Average passes made by forwards:", avg_passes_forwards)
print("Average passes made by midfielders:", avg_passes_midfielders)
print()

print("Query 1: Calculate the average fare paid by passengers in the first class versus in the third class.")
print("Filter passengers in the first class.")
first_class_passengers = table3.filter(lambda x: x['class'] == '1')

print("Calculate the average fare for first class passengers.")
average_fare_first_class = first_class_passengers.aggregate(lambda x: sum(x) / len(x), 'fare')

print("Average fare for passengers in the first class:", average_fare_first_class)
print()

print("Filter passengers in the third class.")
third_class_passengers = table3.filter(lambda x: x['class'] == '3')

print("Calculate the average fare for third class passengers.")
average_fare_third_class = third_class_passengers.aggregate(lambda x: sum(x) / len(x), 'fare')

print("Average fare for passengers in the third class:", average_fare_third_class)
print()

print("""Query 2: Calculate the survival rate of male versus female passengers.
Filter male passengers.""")
male_passengers = table3.filter(lambda x: x['gender'] == 'M')

print("Calculate the survival rate for male passengers.")
if len(male_passengers.table) > 0:
    survived_count = sum(1 for passenger in male_passengers.table if passenger['survived'] == 'yes')
    total_count = len(male_passengers.table)
    male_survival_rate = survived_count / total_count
else:
    male_survival_rate = 0
print("Survival rate for male passengers:", male_survival_rate)
print()

print("Filter female passengers.")
female_passengers = table3.filter(lambda x: x['gender'] == 'F')

print("Calculate the survival rate for female passengers.")
if len(female_passengers.table) > 0:
    survived_count = sum(1 for passenger in female_passengers.table if passenger['survived'] == 'yes')
    total_count = len(female_passengers.table)
    female_survival_rate = survived_count / total_count
else:
    female_survival_rate = 0
print("Survival rate for female passengers:", female_survival_rate)
print()

print("Find the total number of male passengers embarked at Southampton")
male_passengers_southampton = table3.filter(lambda x: x['gender'] == 'M' and x['embarked'] == 'Southampton')
total_male_passengers_southampton = len(male_passengers_southampton.table)
print("Total number of male passengers embarked at Southampton:", total_male_passengers_southampton)