import pandas as pd
from factor_analyzer import FactorAnalyzer

# Загрузка данных
file_path = "factor_analysis_results.xlsx"

# Загрузка данных и заголовков
df = pd.read_excel(file_path_2)  # Исходные данные с нормализованными значениями
headers = df.columns  # Заголовки переменных

# Загрузка факторных нагрузок
factor_loadings = pd.read_excel(file_path, sheet_name="Факторные нагрузки", index_col=0)

# Проверка соответствия числа переменных
assert df.shape[1] == factor_loadings.shape[0], "Размерность данных и факторных нагрузок не совпадает!"

# Определяем число факторов
n_factors = factor_loadings.shape[1]

# Создание и настройка модели факторного анализа
fa = FactorAnalyzer(n_factors=n_factors, rotation=None, method="principal")
fa.fit(df)

# Расчет факторных оценок
factor_scores = fa.transform(df)

# Преобразуем факторные оценки в DataFrame
factor_scores_df = pd.DataFrame(
    factor_scores,
    columns=[f"Фактор {i+1}" for i in range(n_factors)],
    index=df.index
)

# Сохранение данных в файл
output_file = "factor_analysis_with_scores.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Исходные данные", index=True)
    factor_loadings.to_excel(writer, sheet_name="Факторные нагрузки", index=True)
    factor_scores_df.to_excel(writer, sheet_name="Факторные оценки", index=True)

print(f"Факторные оценки успешно рассчитаны и сохранены в файл {output_file}.")
