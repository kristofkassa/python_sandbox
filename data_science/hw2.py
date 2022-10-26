from typing import Iterable

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import io
import sklearn.model_selection, sklearn.metrics

# 1
from pandas.core.generic import NDFrame

olimpia120 = pd.read_csv("./athlete_events.csv").query("Season == 'Summer'")
print(olimpia120.head())

# 2
print(olimpia120.describe())

print(olimpia120.Sport[olimpia120.Height.idxmax()] == 'Basketball')
print(olimpia120.Sport[olimpia120.Height.idxmin()] == 'Gymnastics')
print(olimpia120.Sport[olimpia120.Weight.idxmax()] == 'Weightlifting')
print(olimpia120.Sport[olimpia120.Weight.idxmin()] == 'Gymnastics')
print(olimpia120.Sport[olimpia120.Age.idxmax()] == 'Archery')
print(olimpia120.Sport[olimpia120.Age.idxmin()] == 'Gymnastics')

# 3
sports = ['Basketball', 'Gymnastics', 'Wrestling']
rome_1960 = olimpia120.query("Year == 1960 and Sport in @sports")
london_2012 = olimpia120.query("Year == 2012 and Sport in @sports")

fig, (ax1, ax2) = plt.subplots(2)
sns.scatterplot(data=rome_1960, x='Weight', y='Height', hue='Sport', ax=ax1)
sns.scatterplot(data=london_2012, x='Weight', y='Height', hue='Sport', ax=ax2)

ax1.set_ylim(120, 226)
ax1.set_xlim(25, 214)
ax2.set_ylim(120, 226)
ax2.set_xlim(25, 214)

# 4

filtered_df = olimpia120.filter(items=['NOC', 'Year', 'Medal']).dropna().query("Medal == 'Gold'")

grouped_df = filtered_df.groupby(filtered_df.columns.tolist(), as_index=False).size()

grouped_df.drop(columns=(['Medal']), inplace=True)
grouped_df.rename(columns={"size": "GOLDMEDALS"}, inplace=True)

url = 'https://math.bme.hu/~pinterj/BevAdat1/Adatok/TokyoGold.xlsx'
tokyo_data = requests.get(url).content
tokyo_df = pd.read_excel(io.BytesIO(tokyo_data))

tokyo_aggregated = pd.concat([grouped_df, tokyo_df], join="outer").groupby('NOC', as_index=False).sum()

url = 'https://math.bme.hu/~pinterj/BevAdat1/Adatok/OlympicsPopulation.xlsx'
population_data = requests.get(url).content
population_df = pd.read_excel(io.BytesIO(population_data))
result = tokyo_aggregated.merge(population_df).dropna()

for index, row in result.iterrows():
    if row.GOLDMEDALS > 0:
        res = row.POPULATION / 1_000_000 / row.GOLDMEDALS
        result.loc[index, 'GOLD_PER_CAPITA'] = res

sorted_result = result.sort_values(by='GOLD_PER_CAPITA', ascending=False).nlargest(n=10, columns=['GOLD_PER_CAPITA'])
for index, row in sorted_result.iterrows():
    if row.GOLDMEDALS > 0:
        print(f'NOC: {row.NOC}, aranyérmekszáma / 1 millió fő: {row.GOLD_PER_CAPITA}')

# 5

df_sport_year = olimpia120.query("Medal == 'Gold'").groupby(['Sport', 'Year']).agg({"Medal": "nunique"}).reset_index()
df_sorted = df_sport_year.groupby(['Sport']).size().sort_values(ascending=False)

#### 2

url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
red = requests.get(url)
red_wines = pd.read_csv(url, sep=';')

for index, row in red_wines.iterrows():
    if row.quality < 6.5:
        red_wines.loc[index, 'quality'] = 0
    else:
        red_wines.loc[index, 'quality'] = 1

print(red_wines)


# 2

def most_common(lst):
    np.bincount(lst)


def euclidean(point, data):
    return np.sqrt(np.sum((point - data) ** 2, axis=1))


class MykNN:
    def __init__(self, k, metric=euclidean):
        self.y_train = None
        self.x_train = None
        self.k = k
        self.metric = metric

    def fit(self, x_train, y_train):
        self.x_train = pd.DataFrame(x_train).values
        self.y_train = pd.DataFrame(y_train).values

    def predict(self, x_test):
        neighbors = []
        for x in x_test.values:
            distances = self.metric(x, self.x_train)
            y_sorted = [y for _, y in sorted(zip(distances, self.y_train))]
            neighbors.append(y_sorted[:self.k])
        y_pred = list(map(most_common, neighbors))
        return y_pred


X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(red_wines.drop('quality', axis=1),
                                                                            red_wines.quality, test_size=0.3,
                                                                            random_state=0)

myknn = MykNN(5)
myknn.fit(X_train, y_train)
y_pred = myknn.predict(X_test)

print(f'Accuracy: {round(sklearn.metrics.accuracy_score(y_test, y_pred), 2)}')
print(f'Precision: {round(sklearn.metrics.precision_score(y_test, y_pred), 2)}')
print(f'Recall: {round(sklearn.metrics.recall_score(y_test, y_pred), 2)}')
