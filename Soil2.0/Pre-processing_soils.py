import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from scipy.stats import chi2_contingency, f_oneway

# Функция для оценки содержательности столбца
def evaluate_column_significance(df, column):
    # Если столбец числовой, выполняем ANOVA
    if np.issubdtype(df[column].dtype, np.number):
        filled_data = df[column].dropna()
        if 'SOIL_ID' in df.columns:
            groups = [group.dropna() for _, group in df.groupby('SOIL_ID')[column]]
            if len(groups) > 1:
                f_stat, p_value = f_oneway(*groups)
                return p_value
        return None
    else:
        # Для категориальных данных выполняем тест хи-квадрат
        if 'SOIL_ID' in df.columns:
            contingency_table = pd.crosstab(df[column].dropna(), df['SOIL_ID'].dropna())
            chi2, p_value, _, _ = chi2_contingency(contingency_table)
            return p_value
        return None

# Загрузка данных из файла
file_path = "soil_data.xlsx"
df = pd.read_excel(file_path)

# Перестановка категориальных и числовых столбцов
categorical_columns = df.select_dtypes(exclude=['number']).columns.tolist()  # Категориальные столбцы
numerical_columns = df.select_dtypes(include=['number']).columns.tolist()  # Числовые столбцы

# Объединяем в новый порядок: категориальные впереди, числовые после
ordered_columns = categorical_columns + numerical_columns
df = df[ordered_columns]

# Установка минимального порога заполненных значений
threshold = 0.1 * len(df)  # 10% от общего количества строк

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
df = df.drop(columns=final_columns_to_remove)

# Функция для замены пропущенных значений
def replace_missing_values(df, target_column):
    # Разделение данных на группы по 'CardID'
    grouped = df.groupby(target_column)

    # Для каждого столбца в данных
    for column in df.columns:
        if column == target_column:  # Пропускаем целевую переменную
            continue

        # Для числовых данных
        if np.issubdtype(df[column].dtype, np.number):
            # Заменяем пропущенные значения на среднее/медиану для каждой группы
            df[column] = df.groupby(target_column)[column].transform(
                lambda x: x.fillna(x.mean() if x.isnull().mean() < 0.5 else x.median()))

        # Для категориальных данных
        else:
            # Заменяем пропущенные значения на наиболее частое значение для каждой группы
            df[column] = df.groupby(target_column)[column].transform(
                lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan))

    return df

# Применяем замену пропущенных значений
df = replace_missing_values(df, 'SOIL_ID')

# Кодирование текстовых столбцов
text_columns = df.select_dtypes(include=['object']).columns
exclude_columns = ['SOIL_ID']  # Идентификаторы, не нормализуем

# Проверяем столбцы, которые содержат числовые данные, исключая те, которые не должны нормализоваться
numeric_columns = df.select_dtypes(include=['number']).columns.difference(exclude_columns)

# Функция для кодирования текстовых переменных
def encode_text_columns(df, text_columns, encoding_method='label'):
    encoding_map = {}  # Словарь для хранения соответствий текст -> число
    for column in text_columns:
        if encoding_method == 'label':
            # Применение Label Encoding для текстовых переменных
            le = LabelEncoder()
            df[column] = le.fit_transform(df[column].astype(str))

            # Сохраняем соответствие между текстом и числом
            encoding_map[column] = dict(zip(le.classes_, le.transform(le.classes_)))

        elif encoding_method == 'one_hot':
            # Применение One-Hot Encoding
            df = pd.get_dummies(df, columns=[column],
                                drop_first=True)  # drop_first=True чтобы избежать мультиколлинеарности

    return df, encoding_map

# Кодирование текстовых столбцов
df_encoded, encoding_map = encode_text_columns(df, text_columns,
                                               encoding_method='label')  # Выберите 'label' или 'one_hot'

# Нормализация числовых данных с помощью StandardScaler
scaler = StandardScaler()
df_encoded[numeric_columns] = scaler.fit_transform(df_encoded[numeric_columns])

# Сохранение DataFrame в Excel файл
output_file = "этап 1 предобработка файл.xlsx"
df_encoded.to_excel(output_file, index=False)

# Сохранение информации о заменах в текстовый файл
encoding_info_file = "encoding_mapping.txt"
with open(encoding_info_file, 'w') as f:
    f.write("Кодирование текстовых переменных завершено.\n\n")
    for column, mapping in encoding_map.items():
        f.write(f"Столбец: {column}\n")
        for text, label in mapping.items():
            f.write(f"  {text} -> {label}\n")
        f.write("\n")

print("Обработка данных завершена.")
print(f"Результат сохранен в {output_file}.")
print(f"Информация о заменах сохранена в {encoding_info_file}.")

