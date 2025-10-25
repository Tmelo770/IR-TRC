
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('Co P&B+results.xlsx')

t = df.iloc[:, 0]
p_sur = df.iloc[:, 1]
p_birth = df.iloc[:, 2]

fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)  

#  p_sur
ax1.plot(t, p_sur, 'o-', color='blue', label='p_(1→1)')
ax1.set_xlabel('Time (t)')
ax1.set_ylabel('p_(1→1)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

#  p_birth
ax2 = ax1.twinx()
ax2.plot(t, p_birth, 's-', color='red', label='p_(0→1)')
ax2.set_ylabel('p_(0→1)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

ax1.legend(loc='lower left')
ax2.legend(loc='lower right')

ax1.grid(False)
ax2.grid(False)


fig.tight_layout()
plt.show()

