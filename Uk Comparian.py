import pandas as pd
import matplotlib.pyplot as plt

# Load the data from your file
file_path = 'u.csv'  # Use the correct file path
df = pd.read_csv(file_path)

# Set the font to match the original plot
plt.rcParams.update({'font.size': 20})  # Adjust the font size as needed

# Plotting
plt.figure(figsize=(18, 5))  # Adjust the figsize to match the ratio

plt.plot(df['k'], df['Δ=1'], label='Δ = 1')
plt.plot(df['k'], df['Δ=3'], label='Δ = 3')
plt.plot(df['k'], df['Δ=5'], label='Δ = 5')
plt.plot(df['k'], df['Δ=10'], label='Δ = 10')

plt.xlabel('k', fontdict={'fontsize': 30})
plt.ylabel('μ(k, Δ)', fontdict={'fontsize': 30})

# Set y-ticks to be 1, 2, 3, 4, 5
plt.yticks([1, 2, 3, 4, 5])

plt.legend(fontsize=20)
plt.grid(False)  # Disable gridlines
plt.show()
