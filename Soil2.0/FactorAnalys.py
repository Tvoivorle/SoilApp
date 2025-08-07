import pandas as pd
import numpy as np
from factor_analyzer import FactorAnalyzer
import matplotlib.pyplot as plt

# Загрузка данных
file_path = "final_results-копия.xlsx"
df = pd.read_excel(file_path)
naming_df = pd.read_excel('naming_of_variables.xlsx')

# Проверяем корреляционную матрицу
correlation_matrix = df.corr()

# Заполняем NaN в корреляционной матрице (например, 0)
correlation_matrix_filled = correlation_matrix.fillna(0)

# Вычисляем собственные значения (eigenvalues) корреляционной матрицы
eigenvalues, _ = np.linalg.eig(correlation_matrix_filled)

# 1. Scree Plot
plt.figure(figsize=(8, 6))
plt.plot(range(1, len(eigenvalues) + 1), eigenvalues, marker='o', linestyle='--')
plt.title("Scree Plot")
plt.xlabel("Номер компоненты")
plt.ylabel("Собственное значение")
plt.axhline(y=1, color='r', linestyle='-', label="Критерий Кайзера")
plt.grid()
plt.legend()
plt.show()

# 1. Критерий Кайзера (eigenvalues > 1)
num_factors_kaiser = sum(eigenvalues > 1)
print(f"Количество факторов по критерию Кайзера: {num_factors_kaiser}")

# 2. Параллельный анализ (ручная реализация)
random_eigenvalues = []
n_iterations = 100  # Количество итераций для генерации случайных матриц
n_samples, n_features = df.shape

for _ in range(n_iterations):
    random_data = np.random.normal(size=(n_samples, n_features))
    random_corr_matrix = np.corrcoef(random_data, rowvar=False)
    rand_eigvals, _ = np.linalg.eig(random_corr_matrix)
    random_eigenvalues.append(rand_eigvals)

random_eigenvalues = np.array(random_eigenvalues)
mean_random_eigenvalues = random_eigenvalues.mean(axis=0)

plt.figure(figsize=(8, 6))
plt.plot(range(1, len(eigenvalues) + 1), eigenvalues, marker='o', linestyle='--', label="Реальные значения")
plt.plot(range(1, len(mean_random_eigenvalues) + 1), mean_random_eigenvalues, marker='x', linestyle='-', label="Случайные значения")
plt.title("Параллельный анализ")
plt.xlabel("Номер компоненты")
plt.ylabel("Собственное значение")
plt.legend()
plt.grid()
plt.show()

# Количество факторов по параллельному анализу
num_factors_parallel = np.sum(eigenvalues > mean_random_eigenvalues)
print(f"Оптимальное количество факторов по параллельному анализу: {num_factors_parallel}")

# 3. Кумулятивная объяснённая дисперсия (например, 70%)
explained_variance_ratio = eigenvalues / eigenvalues.sum()
cumulative_variance_ratio = np.cumsum(explained_variance_ratio)

plt.figure(figsize=(8, 6))
plt.plot(range(1, len(cumulative_variance_ratio) + 1), cumulative_variance_ratio, marker='o', linestyle='--')
plt.axhline(y=0.7, color='r', linestyle='-', label="80% объяснённой дисперсии")
plt.title("Кумулятивная объяснённая дисперсия")
plt.xlabel("Номер компоненты")
plt.ylabel("Объяснённая дисперсия")
plt.legend()
plt.grid()
plt.show()

# Количество факторов для достижения 80% дисперсии
num_factors_variance = np.argmax(cumulative_variance_ratio >= 0.7) + 1
print(f"Количество факторов для 70% объяснённой дисперсии: {num_factors_variance}")

# Запрашиваем количество факторов у пользователя
num_factors = int(input("Введите количество факторов для факторного анализа: "))

# Факторный анализ
fa = FactorAnalyzer(n_factors=num_factors, rotation="varimax")
fa.fit(df.fillna(df.median()))  # Заменяем NaN в данных на медианные значения для факторного анализа

# Факторные нагрузки
factor_loadings = pd.DataFrame(fa.loadings_, index=df.columns, columns=[f"Фактор {i+1}" for i in range(num_factors)])

# Общности
communalities = pd.DataFrame(fa.get_communalities(), index=df.columns, columns=["Общность"])

# Добавление описаний переменных
# Создаем словарь с описаниями из naming_of_variables.xlsx
description_dict = dict(zip(naming_df['Переменная'], naming_df['Описание данных']))

# Добавляем столбец с описанием в общности
communalities['Описание переменной'] = communalities.index.map(description_dict)

# Сохранение результатов
output_file = "factor_analysis_results.xlsx"
with pd.ExcelWriter(output_file) as writer:
    # Указываем имя индекса при сохранении факторных нагрузок
    factor_loadings.to_excel(writer, sheet_name="Факторные нагрузки", index_label="Переменные")
    # Указываем имя индекса при сохранении общностей
    communalities.to_excel(writer, sheet_name="Общности", index_label="Переменные")

print("Результаты факторного анализа сохранены в файл:", output_file)
