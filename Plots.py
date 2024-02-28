import pandas as pd
from IPython.display import display
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
import scipy.stats as stats

df = pd.read_excel('plotdata.xlsx')



# Creating a custom color palette
custom_palette = sns.color_palette(['#569FE6', '#f9ba55', 'black'])


# Plot the rushing
dfrush = df[df['seconds-per-item'] !=0]
user_id_mapping = {1: 2, 3: 6, 4: 4}

# Apply the mapping to the 'user_id' column
dfrush['user_id'] = dfrush['user_id'].map(user_id_mapping)
print(dfrush)
rushingPlot = sns.lineplot(x='question', y='seconds-per-item', hue='user_id', data=dfrush, legend=True, palette=custom_palette)
# Access the legend object
legend = rushingPlot.legend_
# Change the legend title
legend.set_title("Participants")

# Draw the square (rectangle)
rectangle = Rectangle((33, 25), 10, 35,
                       fill=True,
                       color='#fbf5e7', # Use 'lightorange' for light orange color
                       linewidth=0.8, # This is already set to a thinner line
                       alpha=0.8) # Set the alpha value for transparency
plt.gca().add_patch(rectangle)

# Add text label over the square
plt.text(38, 65, 'Problematic questions', fontsize=10, ha='center', va='center')

plt.xlabel('SSQOL Question')
plt.ylabel('Seconds per item')
# Plot the vertical lines
plt.plot([11, 11], [10, 140], '--', color="black", linewidth=0.8, label='Dotted line') # 'k-' specifies black line
plt.plot([25, 25], [10, 140], '--', color="black", linewidth=0.8, label='Dotted line')

# Add text labels for the lines
plt.text(12, 140, "'Evner' prompt", fontsize=10, ha='center', rotation=-10) # ha='center' centers the text horizontally
plt.text(25, 140, 'Mid-questionnaire', fontsize=10, ha='center', rotation=-10)

# Set axis limits if necessary
plt.xlim([0, 50])
plt.ylim([0, 165])

plt.savefig('rushingPlot.png', dpi=1300)
plt.show()
