# initial imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import re

data = pd.read_csv("countryLyrics.csv", sep='#')

# Removing unwanted columns
data = data.drop(columns = ['artist','title','url'])

# Deleting rows with missing values
data.dropna(inplace=True)
data.reset_index(drop=True, inplace=True)

for i in range(0,len(data['lyrics'])):
    if(re.findall(r'\d+.*Embed.*', data['lyrics'][i])!=[]):
        data['lyrics'][i] = data['lyrics'][i].split(re.findall(r'\d+.*Embed.*', data['lyrics'][i])[0])[0]

    if (re.findall(r'\bLyrics\b', data['lyrics'][i])!=[]):
        data['lyrics'][i] = data['lyrics'][i].split('Lyrics')[1]
    data['lyrics'][i] = data['lyrics'][i].lower()

print("Number of songs grouped by genre of music:",data.groupby('genre').count()['lyrics'])
ax = plt.subplots()
ax = sns.countplot(x="genre", data = data, palette= "Set1")
ax.set_title("Number of songs by genre")
plt.show()