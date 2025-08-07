import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="ticks")
import os
os.getcwd()

# Будем анализировать
data = pd.read_csv('BostonHousing.csv', sep=",")
# Размер датасета
data.shape
total_count = data.shape[0]
print('Всего строк: {}'.format(total_count))
# Список колонок
print(data.columns)

plt.plot(data['rm'], data['medv'], 'o')
# Настройка осей и заголовка графика
plt.xlabel('Количество комнат')
plt.ylabel('Средняя стоимость домов, в 1000 долларах')
plt.title('Взаимосвязь между количеством комнат и стоимостью дома')
# Отображение графика
plt.show()

# Создание графика рассеяния
plt.scatter(data.iloc[:, 5], data['medv'])
plt.xlabel('Количество комнат')
plt.ylabel('Средняя стоимость домов, в 1000 долларах')
plt.title('Взаимосвязь между количеством комнат и стоимостью дома')
plt.show()

# Построение графика bar
plt.bar(data['rad'], data['crim'])
# Настройка осей и заголовка графика
plt.xlabel('индекс доступности к радиальным магистралям')
plt.ylabel('Уровень криминальной опсности')
plt.title('Зависимость уровня преступности от индекса доступности к радиальным магистралям')
# Отображение графика
plt.show()

# Группировка данных по категориям
grouped_data = data.groupby('chas').size()
# Построение графика pie
plt.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%')
# Настройка заголовка графика
plt.title('Распределение по категории CHAS')
# Отображение графика
plt.show()

# Построение графика hist
plt.hist(data['tax'])
# Настройка осей и заголовка графика
plt.xlabel('Налог')
plt.ylabel('Стоимость налога')
# Отображение графика
plt.show()

# Построение графика boxplot для столбца "indus"
plt.boxplot(data['indus'])
plt.title('Boxplot для столбца indus')
plt.ylabel('indus')
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data['crim'], data['zn'], data['tax'])
ax.set_xlabel('crim')
ax.set_ylabel('zn')
ax.set_zlabel('tax')
ax.set_title('3D Scatter Plot для столбца tax')
plt.show()