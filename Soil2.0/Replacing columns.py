import pandas as pd

# Читаем файл с результатами факторного анализа
file_path = "factor_analysis_results.xlsx"

# Читаем листы "Факторные нагрузки" и "Переменные" из файла, указываем движок
factor_loadings_df = pd.read_excel(file_path, sheet_name="Факторные нагрузки", engine='openpyxl')
variables_df = pd.read_excel(file_path, sheet_name="Переменные", engine='openpyxl')

# Создаем словарь для замены: фактор -> ответ
factor_name_mapping = dict(zip(variables_df['Фактор'], variables_df['Ответ']))

# Заменяем названия факторов в DataFrame "Факторные нагрузки"
# Перебираем все столбцы и заменяем названия
factor_loadings_df.columns = [factor_name_mapping.get(col, col) for col in factor_loadings_df.columns]

# Загружаем остальные листы
all_sheets = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')

# Оставляем нетронутыми все листы, кроме "Факторные нагрузки"
with pd.ExcelWriter("factor_analysis_results_with_updated_factors.xlsx", engine='openpyxl') as writer:
    # Записываем изменённый лист "Факторные нагрузки"
    factor_loadings_df.to_excel(writer, sheet_name="Факторные нагрузки", index=False)

    # Записываем все остальные листы без изменений
    for sheet_name, sheet_data in all_sheets.items():
        if sheet_name != "Факторные нагрузки":
            sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)

print("Файл с обновленными названиями факторов сохранен.")
