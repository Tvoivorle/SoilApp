import pandas as pd
import numpy as np

# Загрузка данных из файла
file_path = "filtered_soil_data_analiz.xlsx"
df = pd.read_excel(file_path)

# Убедимся, что столбец 'CardID' существует
if 'CardID' not in df.columns:
    raise ValueError("Столбец 'CardID' не найден в данных.")


# Функция для замены пропущенных значений
def replace_missing_values(df, target_column):
    # Разделение данных на группы по 'Soil_ID'
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
df = replace_missing_values(df, 'CardID')

# Сохранение результата в новый файл
output_file = "soil_data_with_imputed_values_CardID.xlsx"
df.to_excel(output_file, index=False)

print("Замена пропущенных значений завершена. Результат сохранен в файл:", output_file)
