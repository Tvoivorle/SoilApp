import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Загрузка данных
file_path = "factor_analysis_results.xlsx"
factor_loadings = pd.read_excel(file_path, sheet_name="Факторные нагрузки", index_col=0)

# Настройка стиля визуализации
sns.set(style="whitegrid")

# Параметры разбиения
factors_per_page = 1  # Количество факторов на одной странице
threshold = 0.05  # Порог для исключения переменных с низкими нагрузками
num_pages = math.ceil(len(factor_loadings.columns) / factors_per_page)  # Количество страниц

# Цикл по страницам
for page in range(num_pages):
    plt.figure(figsize=(14, 8 * factors_per_page))  # Увеличиваем размеры для нескольких графиков
    start_factor = page * factors_per_page
    end_factor = min(start_factor + factors_per_page, len(factor_loadings.columns))

    for i, factor in enumerate(factor_loadings.columns[start_factor:end_factor], start=1):
        # Отбираем только переменные с нагрузкой выше порога
        factor_loadings_filtered = factor_loadings[factor][abs(factor_loadings[factor]) >= threshold]
        factor_loadings_sorted = factor_loadings_filtered.sort_values(ascending=False)  # Сортировка по убыванию

        if not factor_loadings_sorted.empty:  # Проверяем, есть ли переменные для отображения
            plt.subplot(factors_per_page, 1, i)  # Создаем отдельный график для каждого фактора
            bar_colors = ['#1f77b4' if abs(val) >= 0.4 else '#ff7f0e' for val in
                          factor_loadings_sorted]  # Цвета на основе порога

            # Построение графика
            factor_loadings_sorted.plot(kind="barh", color=bar_colors, alpha=0.85)
            plt.axvline(x=0, color='black', linewidth=0.8, linestyle="--")  # Линия по центру
            plt.title(f"Распределение нагрузок для {factor}", fontsize=14, weight="bold")
            plt.xlabel("Факторная нагрузка")
            plt.ylabel("Переменные")
            plt.tight_layout()

    # Сохранение текущей страницы
    plt.savefig(f"factor_loadings_page_{page + 1}.png", dpi=300, bbox_inches="tight")
    plt.close()  # Закрываем фигуру, чтобы не показывать графики

print(f"Готово! Графики сохранены в файлы factor_loadings_page_1.png, ..., factor_loadings_page_{num_pages}.png")
