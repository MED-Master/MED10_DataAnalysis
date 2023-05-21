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
SSQOL_only_questions.reset_index(drop=True, inplace=True)
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



# filter out user 3
SSQOL_without3 = SSQOL_only_questions.loc[SSQOL['user_id'] != 3]

# t-test for reflective and example question answers
grouped = SSQOL_without3.groupby('condition')['answer']
reflectiveQuestions = grouped.get_group('R')
exampleQuestions = grouped.get_group('E')

#variance
#guideline called the "Rule of Thumb" that suggests the ratio of the larger variance to the smaller variance should be less than 4 or 5 for the assumption of equal variances to hold.
# #This means that if the larger variance is no more than 4 or 5 times the smaller variance, the variances can be considered approximately equal.
print("variance reflective questions: ", np.var(reflectiveQuestions))
print("variance example questions: ", np.var(exampleQuestions))
# mean  and standard diviation
print("reflective questions mean:" ,np.mean(reflectiveQuestions), ",standard deviation : ", np.std(reflectiveQuestions))
print("example mean:" ,np.mean(exampleQuestions), ",standard deviation : ", np.std(exampleQuestions))

t_statistic, p_value = stats.ttest_ind(reflectiveQuestions, exampleQuestions)
print("t-statistic = ", t_statistic)
print("p-value = ", p_value)

# sum of answers per user
sumOfAnswersPerUser = SSQOL_only_questions.groupby('user_id')['answer'].sum()
print("SSQOL Scores per participant: ", sumOfAnswersPerUser)

# mean and standard diviation of answers per user
meanOfAnswersPerUser = SSQOL_only_questions.groupby('user_id')['answer'].mean()
sdOfAnswersPerUser = SSQOL_only_questions.groupby('user_id')['answer'].std()
print("SSQOL mean Scores per participant: ", meanOfAnswersPerUser)
print("SSQOL standard deviation Scores per participant: ", sdOfAnswersPerUser)

# total time per user
totalTimePerUser = SSQOL_only_questions.groupby('user_id')['Cumulative_duration_minutes'].max()
print("SSQOL total time per participant: ", totalTimePerUser)

# mean and standard deviation time per item
meanTimePerItem = SSQOL_only_questions.groupby('user_id')['seconds-per-item'].mean()
sdTimePerItem = SSQOL_only_questions.groupby('user_id')['seconds-per-item'].std()
print("SSQOL mean time per item per participant: ", meanTimePerItem)
print("SSQOL standard deviation time per item per participant: ", sdTimePerItem)

print(SSQOL_only_questions.groupby('user_id')['duration_seconds'].head(5))
#print second value of duration_seconds
print('test')
print('not work', SSQOL_only_questions['duration_seconds'].loc[1])

# SSQOL as excel
SSQOL_only_questions.to_excel('preprocessedata.xlsx')

# descriptive statistics of SSQOL per user and condition
print(SSQOL_only_questions.groupby(['user_id', 'condition'])['answer'].describe())

#display(SSQOL_only_questions)