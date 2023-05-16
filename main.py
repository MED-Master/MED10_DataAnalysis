import pandas as pd
from IPython.display import display
import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

motivationQuestionnaire = pd.read_csv('Questionnaire.csv', sep=';')
#SSQOL = pd.read_csv('SSQOL.csv')
SSQOL = pd.read_excel('SSQOL-results.xlsx')
# Remove id column
SSQOL = SSQOL.drop(['id'], axis=1)

# Convert answer column to numeric
SSQOL['answer'] = pd.to_numeric(SSQOL['answer'], errors='coerce')

# Convert timestamp to datetime object
SSQOL['timestamp'] = pd.to_datetime(SSQOL['timestamp'])

# Remove date from timestamp
SSQOL['time'] = SSQOL['timestamp'].dt.strftime('%H:%M:%S')

# Remove rows with user_id = 0
SSQOL_filtered = SSQOL.loc[SSQOL['user_id'] != 0]
# Remove empty rows
SSQOL_only_questions = SSQOL_filtered.dropna()

# Calculate the time difference in seconds between rows for each user
SSQOL_only_questions['duration_seconds'] = SSQOL_only_questions.groupby('user_id')['timestamp'].diff().dt.total_seconds()
# Fill NaN values with 0 as the beginning of each user is NaN
SSQOL_only_questions['duration_seconds'] = SSQOL_only_questions['duration_seconds'].fillna(0)
# Calculate the cumulative sum of the duration_seconds for each user
SSQOL_only_questions['Cumulative_duration_seconds'] = SSQOL_only_questions.groupby('user_id')['duration_seconds'].cumsum()

# Calculates rushing i.g. seconds-per-item(SPI)
def rushing(row):
    if row['question'] > 1:
        return row['Cumulative_duration_seconds'] / (row['question'] - 1)
    else:
        return 0

def secToMin(row):
    return row['Cumulative_duration_seconds'] / 60
# add column with cumulative duration in minutes
SSQOL_only_questions['Cumulative_duration_minutes'] = SSQOL_only_questions.apply(lambda row: secToMin(row), axis=1)

def conditionToNumber(row):
    if row['condition'] == 'R':
        return 1
    else:
        return 0
# add column with condition as number
SSQOL_only_questions['condition_number'] = SSQOL_only_questions.apply(lambda row: conditionToNumber(row), axis=1)
#add column rushing
SSQOL_only_questions['seconds-per-item'] = SSQOL_only_questions.apply(lambda row: rushing(row), axis=1)

# Plot the rushing
rushingPlot = sns.lineplot(x='question', y='seconds-per-item', hue='user_id', data=SSQOL_only_questions)
plt.show()
# Plot the time
sns.lineplot(x='question', y='Cumulative_duration_minutes', hue='user_id', data=SSQOL_only_questions)
#ax2 = plt.twinx()
#sns.lineplot(x='question', y='duration_seconds', hue='user_id', data=SSQOL_only_questions, ax=ax2, legend=False
plt.show()

# Plot answers distribution by condition using histplot
answerDistributionHistplot = sns.histplot(data=SSQOL_only_questions, x='answer', hue='condition', bins=5, multiple='stack', kde=True)
plt.title('Distribution of Answers by Condition')
plt.xlabel('Answer')
plt.ylabel('Count')
plt.show()

# Plot answers distribution by condition using boxplot
answerDistributionBoxplot = sns.boxplot(data=SSQOL_only_questions, x='answer', y="condition", orient='h')
#answerDistributionStripplot = sns.stripplot(data=SSQOL_only_questions, x='answer', y="condition", alpha=0.5, orient='h', jitter=True, color='black', size=4)
answerDistributionSwarnPlot = sns.swarmplot(data=SSQOL_only_questions, x='answer', y="condition", orient='h', color='black', size=5, alpha=0.5)
plt.title('Distribution of Answers by Condition')
plt.xlabel('Answer')
plt.ylabel('Condition')
plt.show()

# Plot answers per user id
answerDistributionBoxplot = sns.boxplot(data=SSQOL_only_questions, x='answer', y="user_id", orient='h')
#answerDistributionStripplot = sns.stripplot(data=SSQOL_only_questions, x='answer', y="condition", alpha=0.5, orient='h', jitter=True, color='black', size=4)
answerDistributionSwarnPlot = sns.swarmplot(data=SSQOL_only_questions, x='answer', y="user_id", orient='h', color='black', size=5, alpha=0.5)
plt.title('Distribution of Answers by user_id')
plt.xlabel('Answer')
plt.ylabel('user_id')
plt.show()

# 2nd plot for answers per user id
sns.lineplot(x='question', y='answer', hue='user_id', data=SSQOL_only_questions)
plt.show()

# t-test for reflective and example question answers
grouped = SSQOL_only_questions.groupby('condition')['answer']
reflectiveQuestions = grouped.get_group('R')
exampleQuestions = grouped.get_group('E')

t_statistic, p_value = stats.ttest_ind(reflectiveQuestions, exampleQuestions)
print("t-statistic = ", t_statistic)
print("p-value = ", p_value)

#display(SSQOL_only_questions)