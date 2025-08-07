import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="ticks")
import os
os.getcwd()

# Будем анализировать данные только на обучающей выборке
data = pd.read_csv('datatraining.txt', sep=",")

# Первые 5 строк датасета
data.head()

# Размер датасета - 8143 строк, 7 колонок
data.shape

total_count = data.shape[0]
print('Всего строк: {}'.format(total_count))

# Список колонок
data.columns

# Список колонок с типами данных
data.dtypes

# Проверим наличие пустых значений
# Цикл по колонкам датасета
for col in data.columns:
    # Количество пустых значений - все значения заполнены
    temp_null_count = data[data[col].isnull()].shape[0]
    print('{} - {}'.format(col, temp_null_count))

# Основные статистические характеристки набора данных
data.describe()

# Определим уникальные значения для целевого признака
data['Occupancy'].unique()

fig, ax = plt.subplots(figsize=(10,10))
sns.scatterplot(ax=ax, x='Humidity', y='HumidityRatio', data=data)
plt.show()

fig, ax = plt.subplots(figsize=(10,10))
sns.scatterplot(ax=ax, x='Humidity', y='HumidityRatio', data=data, hue='Occupancy')
plt.show()

fig, ax = plt.subplots(figsize=(10,10))
sns.displot(data['Humidity'])
plt.show()

sns.jointplot(x='Humidity', y='HumidityRatio', data=data)
plt.show()

sns.jointplot(x='Humidity', y='HumidityRatio', data=data, kind="hex")
plt.show()

sns.jointplot(x='Humidity', y='HumidityRatio', data=data, kind="kde")
plt.show()

sns.pairplot(data)
plt.show()

sns.pairplot(data, hue="Occupancy")
plt.show()

sns.boxplot(x=data['Humidity'])
plt.show()

sns.boxplot(y=data['Humidity'])
plt.show()

sns.boxplot(x='Occupancy', y='Humidity', data=data)
plt.show()

sns.violinplot(x=data['Humidity'])
plt.show()

fig, ax = plt.subplots(2, 1, figsize=(10,10))
sns.violinplot(ax=ax[0], x=data['Humidity'])
sns.displot(data['Humidity'], ax=ax[1])
plt.show()

sns.violinplot(x='Occupancy', y='Humidity', data=data)
plt.show()

sns.catplot(y='Humidity', x='Occupancy', data=data, kind="violin", split=True)
plt.show()

data.corr()
sns.heatmap(data.corr())
plt.show()

sns.heatmap(data.corr(), annot=True, fmt='.3f')
plt.show()

sns.heatmap(data.corr(), cmap='YlGnBu', annot=True, fmt='.3f')
plt.show()

mask = np.zeros_like(data.corr(), dtype=np.bool)
mask[np.tril_indices_from(mask)] = True
sns.heatmap(data.corr(), mask=mask, annot=True, fmt='.3f')
plt.show()
