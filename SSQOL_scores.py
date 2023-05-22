import pandas as pd
from IPython.display import display
import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

df = pd.read_excel('SSQOLComputeCorrect.xlsx')

# compute mean of each user by each Domains and then compute the mean of the means
dfmean = df.groupby(['user_id', 'Domains'])['answer'].mean().reset_index()
dfmean = dfmean.groupby(['user_id'])['answer'].mean().reset_index()
dfmean = dfmean.rename(columns={'answer': 'mean'})
print(dfmean)