from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
import pandas as pd
import numpy as np

# Загружаем данные
file_path = "final_results.xlsx"
df = pd.read_excel(file_path)

# Сохраняем информацию о пропущенных значениях
missing_data = df.isna()

# Заполнение NaN значений в числовых столбцах (например, медианой по столбцу)
df_filled = df.apply(lambda x: x.fillna(x.median()) if x.dtype != 'object' else x, axis=0)

# Теперь можно продолжить с VIF
df_with_const = add_constant(df_filled)

# Рассчитываем VIF для всех переменных
vif_data = pd.DataFrame()
vif_data["Variable"] = df_with_const.columns
vif_data["VIF"] = [variance_inflation_factor(df_with_const.values, i) for i in range(df_with_const.shape[1])]

# Печатаем VIF для всех переменных
print("VIF для всех переменных:")
print(vif_data)

# Убираем переменные с высоким VIF (например, VIF > 5)
high_vif = vif_data[vif_data["VIF"] > 5]
print("Переменные с высоким VIF (> 5):")
print(high_vif)

# Исключаем 'const' из списка переменных для удаления
high_vif_filtered = high_vif[high_vif["Variable"] != "const"]

# Удаляем сильно коррелирующие переменные (если VIF > 5), за исключением 'const'
df_filtered = df_filled.drop(columns=high_vif_filtered["Variable"])

# Восстанавливаем пропуски, исходя из оригинальных данных
df_filtered[missing_data] = np.nan

# Проверяем результат после удаления переменных с высоким VIF
print("Размер после удаления переменных с высоким VIF:")
print(df_filtered.shape)

# Сохраняем новый DataFrame в Excel файл
output_file = "soil_data_encoded_multicollinearity.xlsx"
df_filtered.to_excel(output_file, index=False)
print(f"Новый DataFrame сохранен в {output_file}")
