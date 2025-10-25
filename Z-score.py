

import pandas as pd


file_path = 'Cu F&inf.xlsx'  
df = pd.read_excel(file_path)


df_cleaned = df.dropna()


df_cleaned.iloc[:, 1:] = (df_cleaned.iloc[:, 1:] - df_cleaned.iloc[:, 1:].mean()) / df_cleaned.iloc[:, 1:].std()


df_cleaned.to_excel('Cu F&inf__standardized_data1.xlsx', index=False)
