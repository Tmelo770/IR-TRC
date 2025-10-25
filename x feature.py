

import pandas as pd
import networkx as nx


file_path = 'Co.xlsx' 
df = pd.read_excel(file_path)

# Define functions to construct the network graph
def build_network(df, periods):
    # 创建一个空的有向图
    G = nx.DiGraph()


    df_selected = df[df['Period'].isin(periods)]

    for _, row in df_selected.iterrows():
        reporter = row['ReporterISO']
        partner = row['PartnerISO']
        qty = row['netWgt']  
        if G.has_edge(reporter, partner):
            G[reporter][partner]['weight'] += qty
        else:
            
            G.add_edge(reporter, partner, weight=qty)

    return G


periods_to_include = list(range(1994, 2024))  # Period 1994-2023


G_combined = build_network(df, periods_to_include)


out_weight = dict(G_combined.out_degree(weight='weight'))  
in_weight = dict(G_combined.in_degree(weight='weight'))    


out_degree_count = dict(G_combined.out_degree())  
in_degree_count = dict(G_combined.in_degree())   


total_weight = {}
for node in set(out_weight.keys()).union(set(in_weight.keys())):
    total_weight[node] = {
        'out_weight': out_weight.get(node, 0),  
        'in_weight': in_weight.get(node, 0),    
        'out_degree': out_degree_count.get(node, 0), 
        'in_degree': in_degree_count.get(node, 0),    
        'total_weight': out_weight.get(node, 0) + in_weight.get(node, 0)  
    }

# save as DataFrame
weight_df = pd.DataFrame.from_dict(total_weight, orient='index')
weight_df.reset_index(inplace=True)
weight_df.columns = ['Node', 'Out Weight', 'In Weight', 'Out Degree', 'In Degree', 'Total Weight']

# 导出结果为Excel文件
weight_df.to_excel('Ni_fea-94-23_node_weights_combined.xlsx', index=False)

print("Save as 'Cu-94-23_node_weights_combined.xlsx' ")
