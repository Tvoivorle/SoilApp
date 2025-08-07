import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.feature_selection import SelectKBest, f_regression
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка данных
file_path = "Output.xlsx"
df = pd.read_excel(file_path)

# Определение целевой переменной и предикторов
target_column = 'SOIL_ID'  # Замените на вашу целевую переменную
if target_column not in df.columns:
    raise ValueError(f"Целевая переменная '{target_column}' не найдена в данных.")

# Разделяем данные на целевую переменную и предикторы
X = df.drop(columns=[target_column])  # Независимые переменные
y = df[target_column]  # Целевая переменная

# Заполнение пропусков
X_filled = X.fillna(0)

# --- Выбор моделей для сравнения с оптимальным n_estimators ---
models = {
    "Random Forest": RandomForestRegressor(n_estimators=95, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
    "Support Vector Regressor (SVR)": SVR(kernel='rbf', C=100, gamma='scale'),
    "K-Nearest Neighbors (KNN)": KNeighborsRegressor(n_neighbors=5)
}

# Оценка каждой модели
results = []

for model_name, model in models.items():
    model.fit(X_filled, y)  # Обучение модели
    y_pred = model.predict(X_filled)  # Прогноз

    # Метрики
    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    # Сохраняем результаты
    results.append({
        "Model": model_name,
        "MAE": mae,
        "MSE": mse,
        "R2": r2
    })

    # Вывод метрик для текущей модели
    print(f"\nМодель: {model_name}")
    print(f"MAE (Mean Absolute Error): {mae}")
    print(f"MSE (Mean Squared Error): {mse}")
    print(f"R2 (R-squared): {r2}")

# --- Сравнение моделей ---
results_df = pd.DataFrame(results).sort_values(by="R2", ascending=False)

# Сохраняем результаты в текстовый файл
with open("model_comparison.txt", "w") as f:
    f.write("Сравнение моделей:\n")
    f.write(results_df.to_string(index=False))

# --- Важность признаков и исключение незначимых ---
best_model_name = results_df.iloc[0]["Model"]
best_model = models[best_model_name]

if hasattr(best_model, "feature_importances_"):
    feature_importances = pd.DataFrame({
        'Feature': X.columns,
        'Importance': best_model.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    # Убираем признаки с малой значимостью (Importance < 0.01)
    significant_features = feature_importances[feature_importances['Importance'] >= 0.01]['Feature'].tolist()
    X_significant = X_filled[significant_features]

    # Повторное обучение лучшей модели
    best_model.fit(X_significant, y)
    y_pred_significant = best_model.predict(X_significant)

    # Метрики после исключения
    mae_significant = mean_absolute_error(y, y_pred_significant)
    mse_significant = mean_squared_error(y, y_pred_significant)
    r2_significant = r2_score(y, y_pred_significant)

    print("\nПовторная оценка лучшей модели (только значимые признаки):")
    print(f"MAE (Mean Absolute Error): {mae_significant}")
    print(f"MSE (Mean Squared Error): {mse_significant}")
    print(f"R2 (R-squared): {r2_significant}")

    # Сохраняем важность признаков
    with open(f"significant_features_{best_model_name}.txt", "w") as f:
        f.write("Значимые признаки:\n")
        f.write(feature_importances.to_string(index=False))

    # График значимых признаков
    plt.figure(figsize=(10, 6))
    sns.barplot(data=feature_importances.head(10), x="Importance", y="Feature", palette="viridis")
    plt.title(f"Топ-10 значимых признаков ({best_model_name})")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.savefig(f"significant_top_10_features_{best_model_name}.png")
    plt.show()

# --- Финальный вывод ---
print("\nСравнение моделей:")
print(results_df)
