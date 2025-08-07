import pandas as pd

# Загружаем существующие листы "Факторные нагрузки"
file_path = "factor_analysis_results.xlsx"
factor_loadings = pd.read_excel(file_path, sheet_name="Факторные нагрузки", index_col=0)

# Порог для выбора значений нагрузок
threshold = 0.4

# Создаем словарь для хранения переменных по факторам
factor_structure = {}

for factor in factor_loadings.columns:
    # Выбираем переменные, которые соответствуют данному фактору с учетом порога
    variables = factor_loadings.index[abs(factor_loadings[factor]) >= threshold].tolist()
    factor_structure[factor] = ", ".join(variables)  # Преобразуем список переменных в строку

# Преобразуем словарь в DataFrame
variables_df = pd.DataFrame(list(factor_structure.items()), columns=["Фактор", "Переменные"])

# Сохраняем результат в новой вкладке "Переменные"
with pd.ExcelWriter(file_path, engine="openpyxl", mode="a") as writer:
    variables_df.to_excel(writer, sheet_name="Переменные", index=False)

print("Готово! Лист 'Переменные' успешно добавлен.")
