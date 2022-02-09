import pandas as pd
from datetime import timedelta, datetime
import random
import os

data_dir = os.getcwd()+"//Data"

def print_statistics(l, head, occupancy, p=0):
    print('-'*20)
    print(head.upper())
    choose_online = round(p * 100)
    choose_inperson = round(len(l)/len(occupancy) * 100)
    forced_online = 100 - choose_online - choose_inperson
    print('Fraction of instructors who want to be and are online:                        ', choose_online, '%')
    print('Fraction of instructors who want to be and are in-person:                     ', choose_inperson, '%')
    print('Fraction of instructors who want to be in-person but are forced to be online: ', forced_online, '%')
    print('Number of courses: ', len(l),'(', round(len(l)/len(occupancy) * 100), '%)')
    print('Total max enrollment: ', sum(l), '(', round(sum(l)/sum(occupancy)*100), '%)')
    print('Average max course size: ', round(sum(l)/len(l)))


filenames = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
dataframes = []
print("loading data ....")
for filename in filenames:
    if filename.split(".")[1] == "csv":
        file_with_path = os.path.join(data_dir, filename)
        dataframes.append(pd.read_csv(file_with_path))
print("analyzing data ....")
occupancy = []
courses = []
for df in dataframes:
    for index, row in df.iterrows():
        courses.append(row)
        available = row['numCurr']
        total = row['numTot']
        if isinstance(total, (int, float, complex)) and total < 5000:
            occupancy.append(total)

occupancy.sort(reverse = True)
total_max = sum(occupancy)

#print_statistics (occupancy, "No constraints", occupancy)

for constraint in [0.2]:
    for p in [0, 0.3, 0.4, 0.5]:
        all = occupancy.copy()
        remaining = random.sample(occupancy.copy(), round((1-p)*len(occupancy)))
        remaining.sort(reverse = True)
        inperson = []
        done = False
        while remaining != []:
            if remaining[0] < constraint * all[0]:
                inperson.append(remaining[0])
                all.pop(0)
            remaining.pop(0)
        print_statistics(inperson, str(round(constraint*100))+"% "+"capacity constraints, "+str(round(p*100))+"% "+"chooses online", occupancy, p)