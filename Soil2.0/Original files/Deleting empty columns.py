import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, f_oneway

# Загрузка данных из файла
file_path = r"C:\Users\Stepan\PycharmProjects\Soils\БД ЕГРПР\soil_data.xlsx"
df = pd.read_excel(file_path)

# Установка минимального порога заполненных значений
threshold = 0.1 * len(df)  # 10% от общего количества строк

# Функция для оценки содержательности столбца
def evaluate_column_significance(df, column):
    # Если столбец числовой, выполняем ANOVA
    if np.issubdtype(df[column].dtype, np.number):
        filled_data = df[column].dropna()
        if 'CardID' in df.columns:
            groups = [group.dropna() for _, group in df.groupby('CardID')[column]]
            if len(groups) > 1:
                f_stat, p_value = f_oneway(*groups)
                return p_value
        return None
    else:
        # Для категориальных данных выполняем тест хи-квадрат
        if 'CardID' in df.columns:
            contingency_table = pd.crosstab(df[column].dropna(), df['CardID'].dropna())
            chi2, p_value, _, _ = chi2_contingency(contingency_table)
            return p_value
        return None

# Выделяем столбцы, которые будут удалены
columns_to_remove = [
    column for column in df.columns
    if df[column].count() < threshold
]

# Оцениваем статистическую значимость удаляемых столбцов
significant_columns = []
for column in columns_to_remove:
    p_value = evaluate_column_significance(df, column)
    if p_value is not None and p_value < 0.05:
        significant_columns.append(column)

# Фильтрация столбцов (исключаем только статистически незначимые)
final_columns_to_remove = [col for col in columns_to_remove if col not in significant_columns]
filtered_df = df.drop(columns=final_columns_to_remove)

# Сохранение результата в новый файл
output_file = "filtered_soil_data_analiz_CardID.xlsx"
filtered_df.to_excel(output_file, index=False)

print("Фильтрация завершена.")
if significant_columns:
    print("Следующие столбцы статистически значимы и не были удалены:", significant_columns)
else:
    print("Все удаленные столбцы были статистически незначимыми.")
