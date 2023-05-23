import pandas as pd
from IPython.display import display
import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

df = pd.read_excel('plotdata.xlsx')



# Creating a custom color palette
custom_palette = sns.color_palette(['#569FE6', '#f9ba55', 'black'])


# Plot the rushing
dfrush = df[df['seconds-per-item'] !=0]
rushingPlot = sns.lineplot(x='question', y='seconds-per-item', hue='user_id', data=dfrush, legend=True, palette=custom_palette)
# Access the legend object
legend = rushingPlot.legend_
# Change the legend title
legend.set_title("Participants")
plt.xlabel('SSQOL Question')
plt.ylabel('Seconds per item')
plt.savefig('rushingPlot.png', dpi=1300)
plt.show()

# Power law of learning
powerLawPlot = sns.lineplot(x='question', y='Power_Law_Of_Learning', hue='user_id', data=df, legend=True, palette=custom_palette)
plt.xlabel('SSQOL Question')
plt.ylabel('Time completion(seconds)')
# Access the legend object
legend = powerLawPlot.legend_
# Change the legend title
legend.set_title("Participants")
plt.savefig('learningPlot.png')
plt.show()

# kdeplot
kdePlot = sns.kdeplot(data=df, x='answer', hue='condition', palette=custom_palette, fill=True, alpha=.3, linewidth=0)
plt.xlabel('SSQOL Question')
plt.ylabel('Density')
# Access the legend object
legend = kdePlot.legend_
# Change the legend title
legend.set_title("Conditions")
plt.xlim(1, 5)
plt.xticks(range(1, 6))
plt.savefig('DensityCondition.png')
plt.show()


# Violinplots
Violinplots = sns.violinplot(data=df, x='answer', y='condition', palette=custom_palette, inner='quartile')
plt.xlabel('SSQOL Question')
plt.ylabel('Condition')
plt.xlim(1, 5)
plt.xticks(range(1, 6))
plt.savefig('ViolinplotsCondition.png')
plt.show()

# Violinplots
#ViolinplotsPerParticipant = sns.violinplot(data=df, x='user_id', y='condition',  palette=custom_palette, inner='quartile', linewidth=2, hue='condition')
ViolinplotsPerParticipant = sns.violinplot(data=df, x="user_id", y="answer", hue="condition",
               split=True, inner="quart", linewidth=2,
               palette=custom_palette)
sns.despine(left=True)
plt.xlabel('Participant')
plt.ylabel('Answers')
plt.ylim(1, 5)
# Access the legend object
legend = ViolinplotsPerParticipant.legend_
# Change the legend title
legend.set_title("Conditions")
plt.yticks(range(1, 6))
plt.savefig('ViolinplotsPerParticipant.png', dpi=300)
plt.show()
# Plot the time
#sns.lineplot(x='question', y='Cumulative_duration_minutes', hue='user_id', data=df)
#ax2 = plt.twinx()
#sns.lineplot(x='question', y='duration_seconds', hue='user_id', data=df, ax=ax2, legend=False
#plt.show()

# Plot answers distribution by condition using histplot
answerDistributionHistplot = sns.histplot(data=df, x='answer', hue='condition', bins=5, multiple='stack', kde=True)
plt.title('Distribution of Answers by Condition')
plt.xlabel('Answer')
plt.ylabel('Count')
#plt.show()

# Plot answers distribution by condition using boxplot
answerDistributionBoxplot = sns.boxplot(data=df, x='answer', y="condition", orient='h')
answerDistributionSwarnPlot = sns.swarmplot(data=df, x='answer', y="condition", orient='h', color='black', size=5, alpha=0.5)
plt.title('Distribution of Answers by Condition')
plt.xlabel('SSQOL Answer')
plt.ylabel('Condition')
#plt.savefig('answerDistributionPrConditionBoxplot.png')
#plt.show()

# Plot answers per user id
answerDistributionBoxplot = sns.boxplot(data=df, x='answer', y="user_id", orient='h')
answerDistributionSwarnPlot = sns.swarmplot(data=df, x='answer', y="user_id", orient='h', color='black', size=5, alpha=0.5)
plt.title('Distribution of Answers by Paricipant')
plt.xlabel('SSQOL Answer')
plt.ylabel('Participant')
plt.savefig('answerDistributionBoxplot.png')
#plt.show()

# 2nd plot for answers per user id
#sns.lineplot(x='question', y='answer', hue='user_id', data=df)
#plt.show()