import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Загрузка данных из файла
file_path = "soil_data_with_imputed_values_by_cardid.xlsx"
df = pd.read_excel(file_path)

# Заменяем все пропущенные значения (NaN) на 0
df = df.fillna(0)

# Проверяем столбцы, которые содержат текстовые данные
text_columns = df.select_dtypes(include=['object']).columns

# Столбцы, которые не должны подвергаться нормализации
exclude_columns = ['CardID', 'SOIL_ID']  # Идентификаторы, не нормализуем

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
output_file = "soil_data_encoded_normalized.xlsx"
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

print("Кодирование текстовых переменных и нормализация числовых данных завершены. Результат сохранен в файл:", output_file)
print(f"Информация о заменах сохранена в {encoding_info_file}.")
