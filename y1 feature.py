import pandas as pd
import networkx as nx

file_path = 'Co.xlsx'  
df = pd.read_excel(file_path)

def build_network(df, periods):
    G = nx.DiGraph()

    df_selected = df[df['Period'].isin(periods)]

    for _, row in df_selected.iterrows():
        reporter = row['ReporterISO']
        partner = row['PartnerISO']

        if G.has_edge(reporter, partner):
            G[reporter][partner]['weight'] += 1
        else:
            G.add_edge(reporter, partner, weight=1)

    return G

periods_to_include = list(range(1994, 2024))  
G_combined = build_network(df, periods_to_include)

out_degree = dict(G_combined.out_degree(weight='weight'))  
in_degree = dict(G_combined.in_degree(weight='weight'))    

node_degrees = {}
for node in set(out_degree.keys()).union(set(in_degree.keys())):
    node_degrees[node] = {'out_degree': out_degree.get(node, 0), 'in_degree': in_degree.get(node, 0)}

degree_df = pd.DataFrame.from_dict(node_degrees, orient='index')
degree_df.reset_index(inplace=True)
degree_df.columns = ['Node', 'Out Degree', 'In Degree']

degree_df.to_excel('Co94-26y_node_degrees_combined.xlsx', index=False)

print("Save in 'node_degrees_combined.xlsx' ")
