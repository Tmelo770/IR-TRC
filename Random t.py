# -*- coding: utf-8 -*-

#Generate a randomized network (after randomizing the timestamps, 
#determine the difference from the original data to see if there is randomness)

import pandas as pd
import random
import os

# data path
input_file_path = r'***\data\Co.xlsx'
df = pd.read_excel(input_file_path)

# Create a dictionary
ij_times = {}

# Generate random times
for index, row in df.iterrows():
    i, j = row['i'], row['j']
    t = random.randint(0, 29)
    
    # Ensure unique times for each (i, j) pair.
    while (i, j) in ij_times and t in ij_times[(i, j)]:
        t = random.randint(0, 29)
    
    
    if (i, j) not in ij_times:
        ij_times[(i, j)] = []
    
    # Add the time to the corresponding (i, j) pair.
    ij_times[(i, j)].append(t)
    df.at[index, 't'] = t


output_file_path = r'***\data\Ni_random.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Randomized network connections generated {output_file_path}")
