import pandas as pd

file_path = 'Co94-23.xlsx'
data = pd.read_excel(file_path)

print(data.head())

# Collect unique time points (sorted)
time_points = sorted(data['t'].unique())

# Prepare a results dict
results = {'t': [], 'p_sur': [], 'p_birth': []}

# Compute Eq. (11) and Eq. (12) for each t
for t in time_points:
    E_t  = data[data['t'] == t]         # edges at time t
    E_t1 = data[data['t'] == t + 1]     # edges at time t+1

    # Number of unique nodes at time t (from i and j)
    unique_nodes_t = len(set(E_t['i']).union(set(E_t['j'])))

    # Survival rate (Eq. 11): |E_t ∩ E_{t+1}| / |E_t|
    E_t_set  = set(zip(E_t['i'], E_t['j']))
    E_t1_set = set(zip(E_t1['i'], E_t1['j']))
    intersection = E_t_set & E_t1_set
    p_sur = len(intersection) / len(E_t_set) if len(E_t_set) > 0 else 0

    # Birth rate (Eq. 12): (|E_{t+1}| - |E_t ∩ E_{t+1}|) / [N_t*(N_t-1) - |E_t|]
    denom = unique_nodes_t * (unique_nodes_t - 1) - len(E_t_set)
    p_birth = (len(E_t1_set) - len(intersection)) / denom if denom > 0 else 0

    # Append to results
    results['时间'].append(t)
    results['p_sur'].append(p_sur)
    results['p_birth'].append(p_birth)

# To DataFrame
results_df = pd.DataFrame(results)

# Export to Excel
output_file_path = 'Ni P&B+results.xlsx'
results_df.to_excel(output_file_path, index=False)

# Preview result
results_df.head()
