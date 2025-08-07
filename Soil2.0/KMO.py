import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from factor_analyzer import calculate_kmo

# Загрузка данных
file_path = "Output.xlsx"
df = pd.read_excel(file_path)

# Разделение данных на числовые и категориальные
numerical_df = df.select_dtypes(include=['number'])
categorical_df = df.select_dtypes(exclude=['number'])

# Рассчитываем корреляционную матрицу для всех данных
correlation_matrix = df.corr()

# Порог для удаления слабых корреляций (например, если корреляция ниже 0.3)
correlation_threshold = 0.3

# Создаем маску для корреляций, которые выше порога
correlation_mask = correlation_matrix.abs() >= correlation_threshold

# Проверка, является ли correlation_mask DataFrame
if isinstance(correlation_mask, pd.DataFrame):
    # Выводим первые несколько строк для отладки
    print(correlation_mask.head())
else:
    raise TypeError("correlation_mask должен быть DataFrame.")

# Применяем фильтрацию столбцов: оставляем те, которые имеют хотя бы одну корреляцию > порога по строкам
filtered_columns = correlation_matrix.columns[correlation_mask.any(axis=0)].tolist()

# Применяем отфильтрованные столбцы к исходному DataFrame
filtered_df = df[filtered_columns]

# Функция для замены NaN на медианные значения
def replace_nan_with_median(df):
    # Для каждой колонки заменяем NaN на медиану
    return df.apply(lambda x: x.fillna(x.median()), axis=0)

# Заменяем NaN в числовых данных медианными значениями
numerical_filled = replace_nan_with_median(numerical_df)

# Рассчитываем KMO только для числовых значений
numerical_correlation_matrix = numerical_filled.corr()
kmo_all, kmo_model = calculate_kmo(numerical_correlation_matrix.values)

# Порог для KMO (например, 0.5)
kmo_threshold = 0.5

# Индексы переменных с низким KMO
low_kmo_vars = np.where(kmo_all < kmo_threshold)[0]

# Выводим переменные с низким KMO для проверки
print(f"Переменные с низким KMO (менее {kmo_threshold}):")
print(numerical_df.columns[low_kmo_vars])

# Удаляем переменные с низким KMO из числовых данных
numerical_filtered = numerical_filled.drop(numerical_df.columns[low_kmo_vars], axis=1)

# Создаем финальный DataFrame, объединяя категориальные данные с обработанными числовыми
final_df = pd.concat([categorical_df, numerical_filtered], axis=1)

# Рассчитываем новую корреляционную матрицу для всех данных
final_correlation_matrix = final_df.corr()

# Визуализируем тепловую карту для отфильтрованных данных
num_groups = 4
group_size = len(final_correlation_matrix) // num_groups
for i in range(num_groups):
    start = i * group_size
    end = (i + 1) * group_size if i != num_groups - 1 else len(final_correlation_matrix)
    group_corr = final_correlation_matrix.iloc[start:end, start:end]

    # Визуализация тепловой карты для группы
    plt.figure(figsize=(8, 6))
    sns.heatmap(group_corr, annot=False, cmap="coolwarm", fmt='.2f', linewidths=0.5)
    plt.title(f"Группа {i + 1}")
    plt.show()

# Проверяем, является ли матрица положительно определенной
def is_positive_definite(matrix):
    try:
        np.linalg.cholesky(matrix)
        return True
    except np.linalg.LinAlgError:
        return False

if not is_positive_definite(final_correlation_matrix):
    raise ValueError("Корреляционная матрица не является положительно определенной. Проверьте данные.")

# Вычисляем KMO для финальной числовой матрицы
numerical_correlation_values = numerical_filtered.corr().values
numerical_correlation_values[np.isnan(numerical_correlation_values)] = 0  # Заменяем NaN на 0 только для вычисления KMO
kmo_all, kmo_model = calculate_kmo(numerical_correlation_values)
print(f"KMO тест (для модели): {kmo_model}")
print(f"KMO тест (для всех переменных): {kmo_all}")

# Сохраняем новый DataFrame в Excel файл
output_file = "Output.xlsx"
final_df.to_excel(output_file, index=False)

print(f"Новый DataFrame сохранен в файл {output_file}")
