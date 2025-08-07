import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.stats import chi2_contingency, f_oneway
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
from factor_analyzer import calculate_kmo
from pathlib import Path
from factor_analyzer import FactorAnalyzer
import requests
import streamlit as st
import shap

class DataPipeline:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.territorial_vars = ['CardID', 'RUREG', 'LAT', 'LONG', 'ALT']
        self.territorial_data = None
        self.data = None
        self.artifacts = {}
        self.significance_analyzer = None
        self.multicollinearity_processor = None
        self.kmo_checker = None
        self.factor_analyzer = None
        self.factor_name_generator = None

    def run(self):
        # Этап 0: Загрузка и разделение данных
        raw_data = pd.read_excel(self.input_file)
        self.territorial_data = raw_data[self.territorial_vars]
        self.data = raw_data.drop(columns=self.territorial_vars)

        # Этап 1: Предобработка
        preprocessor = SoilPreprocessor(self.data)
        self.data, self.artifacts['encoding_map'] = preprocessor.process()
        print("\n[Этап 1] Предобработка данных завершена!")

        # Этап 2: Оценка значимости
        self.significance_analyzer = SignificanceAnalyzer(
            target_column='SOIL_ID',
            exclude_columns=self.territorial_vars  # Передаем список переменных для исключения
        )
        self.data, self.artifacts['feature_importances'] = self.significance_analyzer.process(self.data)
        print("\n[Этап 2] Анализ значимости завершен!")
        print("Топ-5 значимых признаков:")
        print(self.artifacts['feature_importances'].head(5))
        print(f"R2 лучшей модели: {max(r['R2'] for r in self.significance_analyzer.results):.2f}")

        # Этап 3: Мультиколлинеарность
        self.multicollinearity_processor = MulticollinearityProcessor()
        self.data, self.artifacts['multicollinearity'] = self.multicollinearity_processor.process(self.data)
        print("\n[Этап 3] Обработка мультиколлинеарности завершена!")
        print(f"Удалено признаков: {len(self.artifacts['multicollinearity']['removed_features'])}")
        print(f"Максимальный VIF после обработки: {self.artifacts['multicollinearity']['vif_report']['VIF'].max():.1f}")

        # Этап 4: Оценка KMO
        self.kmo_checker = KMOChecker()
        self.data, self.artifacts['kmo'] = self.kmo_checker.process(self.data)
        print("\n[Этап 4] KMO анализ завершен!")
        print(f"Удалено переменных с низким KMO: {len(self.artifacts['kmo']['removed_features'])}")
        print(f"Итоговый KMO: {self.artifacts['kmo']['kmo_model']:.2f}")

        # Этап 5: Факторный анализ
        self.factor_analyzer = FactorAnalyzerProcessor()
        artifacts_factor = self.factor_analyzer.process(self.data, self.output_file)
        self.artifacts['factor_analysis'] = artifacts_factor
        print("\n[Этап 5] Факторный анализ завершен!")

        # Этап 6: Факторные оценки
        self.factor_score_processor = FactorScoreProcessor()
        artifacts_factor_scores = self.factor_score_processor.process(self.data, self.artifacts['factor_analysis']['loadings'])
        self.artifacts['factor_scores'] = artifacts_factor_scores
        print("\n[Этап 6] Факторные оценки рассчитаны!")

        # Этап 7: Добавление листа "Переменные"
        self.factor_name_processor = FactorNameProcessor()
        artifacts_factor_names = self.factor_name_processor.process(self.artifacts['factor_analysis']['loadings'])
        self.artifacts['factor_names'] = artifacts_factor_names
        print("\n[Этап 7] Лист 'Переменные' добавлен!")

        # Этап 8: Генерация названий факторов
        self.factor_name_generator = FactorNameGenerator()
        variables_df = self.artifacts['factor_names']
        communalities_df = self.artifacts['factor_analysis']['communalities']
        self.artifacts['factor_names'] = self.factor_name_generator.process(variables_df, communalities_df)
        print("\n[Этап 8] Названия факторов сгенерированы!")

        # Финальное сохранение
        self.save_results()
        print("\nИтоговое количество признаков:", len(self.data.columns))

    def save_results(self):
        # Создаем папку для отчетов
        report_dir = Path("Отчеты и выводы")
        report_dir.mkdir(exist_ok=True)
        output_path = report_dir / self.output_file

        # Проверка наличия территориальных данных
        if self.territorial_data is not None:
            main_data = pd.concat([
                self.territorial_data.reset_index(drop=True),
                self.data.reset_index(drop=True)
            ], axis=1)
        else:
            main_data = self.data.copy()

        try:
            # Восстанавливаем исходный порядок колонок для основного датасета
            main_data = pd.concat([
                self.territorial_data.reset_index(drop=True),
                self.data.reset_index(drop=True)
            ], axis=1)

            # Создаем новый файл или перезаписываем существующий
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Основные данные
                main_data.to_excel(writer, sheet_name="Данные", index=False)

                # Результаты факторного анализа (если есть)
                if 'factor_analysis' in self.artifacts:
                    self.artifacts['factor_analysis']['loadings'].to_excel(
                        writer, sheet_name="Факторные нагрузки", index_label="Переменная"
                    )
                    self.artifacts['factor_analysis']['communalities'].to_excel(
                        writer, sheet_name="Общности", index_label="Переменная"
                    )

                # Факторные оценки (если есть)
                if 'factor_scores' in self.artifacts:
                    # Добавляем территориальные данные к факторным оценкам
                    factor_scores_with_territory = pd.concat([
                        self.territorial_data.reset_index(drop=True),
                        self.artifacts['factor_scores'].reset_index(drop=True)
                    ], axis=1)

                    factor_scores_with_territory.to_excel(
                        writer, sheet_name="Факторные оценки", index_label="Индекс"
                    )

                # Переменные по факторам (если есть)
                if 'factor_names' in self.artifacts:
                    self.artifacts['factor_names'].to_excel(
                        writer, sheet_name="Переменные", index=False
                    )

                # Название переменных (если есть)
                if 'factor_names' in self.artifacts:
                    self.artifacts['factor_names'].to_excel(
                        writer, sheet_name="Названия факторов", index=False
                    )

        except FileNotFoundError:
            # Если файл не найден, создаем его заново
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                pd.DataFrame().to_excel(writer, sheet_name="Данные")
            self.save_results()  # Рекурсивно повторяем сохранение

        # Обновляем названия факторов в артефактах
        if 'factor_names' in self.artifacts:
            factor_names = self.artifacts['factor_names']
            if 'Ответ' in factor_names.columns:  # Проверяем наличие столбца
                name_mapping = dict(zip(factor_names['Фактор'], factor_names['Ответ']))
            else:
                st.warning("Столбец 'Ответ' отсутствует в factor_names. Названия факторов не обновлены.")
                name_mapping = {}

            if 'factor_analysis' in self.artifacts:
                self.artifacts['factor_analysis']['loadings'].rename(columns=name_mapping, inplace=True)
            if 'factor_scores' in self.artifacts:
                self.artifacts['factor_scores'].rename(columns=name_mapping, inplace=True)

        # Сохраняем CSV-отчеты
        reports = {
            'model_comparison.csv': pd.DataFrame(self.significance_analyzer.results)
            if self.significance_analyzer is not None  # Добавлена проверка на None
               and hasattr(self, 'significance_analyzer')
            else pd.DataFrame(),
            'feature_importances.csv': self.artifacts.get('feature_importances', pd.DataFrame()),
            'vif_report.csv': self.artifacts.get('multicollinearity', {}).get('vif_report', pd.DataFrame()),
            'low_kmo_features.csv': pd.DataFrame(
                {'features': self.artifacts.get('kmo', {}).get('removed_features', [])}),
            'final_correlation.csv': self.artifacts.get('kmo', {}).get('correlation_matrix', pd.DataFrame()),
            'factor_loadings.csv': self.artifacts.get('factor_analysis', {}).get('loadings', pd.DataFrame()),
            'communalities.csv': self.artifacts.get('factor_analysis', {}).get('communalities', pd.DataFrame()),
            'factor_scores.csv': self.artifacts.get('factor_scores', pd.DataFrame()),
            'factor_names.csv': self.artifacts.get('factor_names', pd.DataFrame())
        }

        for filename, data in reports.items():
            file_path = report_dir / filename
            if isinstance(data, pd.DataFrame) and not data.empty:
                data.to_csv(file_path, index=False, encoding='utf-8-sig')

        print(f"\nФинальный результат сохранен в: {output_path}")

    def run_stage(self, stage_num):
        if stage_num == 1:
            # Этап 1: Предобработка
            # Загружаем сырые данные и разделяем до предобработки
            raw_data = pd.read_excel(self.input_file)
            self.territorial_data = raw_data[self.territorial_vars]

            # Создаем предобработчик только для анализируемых данных
            preprocessor = SoilPreprocessor(raw_data.drop(columns=self.territorial_vars))

            # Выполняем предобработку
            self.data, self.artifacts['encoding_map'] = preprocessor.process()
            preprocessor.save_results()

        elif stage_num == 2:
            # Этап 2: Оценка значимости
            self.significance_analyzer = SignificanceAnalyzer()
            self.data, self.artifacts['feature_importances'] = self.significance_analyzer.process(self.data)

        elif stage_num == 3:
            # Этап 3: Мультиколлинеарность
            self.multicollinearity_processor = MulticollinearityProcessor()
            self.data, self.artifacts['multicollinearity'] = self.multicollinearity_processor.process(self.data)

        elif stage_num == 4:
            # Этап 4: KMO анализ
            self.kmo_checker = KMOChecker()
            self.data, self.artifacts['kmo'] = self.kmo_checker.process(self.data)

        elif stage_num == 5:
            # Этап 5: Факторный анализ
            self.factor_analyzer = FactorAnalyzerProcessor()
            self.artifacts['factor_analysis'] = self.factor_analyzer.process(self.data, self.output_file)

        elif stage_num == 6:
            # 🔍 Проверяем, есть ли результаты факторного анализа
            if 'factor_analysis' not in self.artifacts:
                raise ValueError(
                    "⚠️ Ошибка: Этап 6 не может быть выполнен, так как факторный анализ (Этап 5) не был успешно завершён.")

            # Этап 6: Факторные оценки
            self.factor_score_processor = FactorScoreProcessor()
            self.artifacts['factor_scores'] = self.factor_score_processor.process(
                self.data, self.artifacts['factor_analysis']['loadings']
            )

        elif stage_num == 7:
            # Этап 7: Группировка переменных
            self.factor_name_processor = FactorNameProcessor()
            self.artifacts['factor_names'] = self.factor_name_processor.process(
                self.artifacts['factor_analysis']['loadings']
            )

        elif stage_num == 8:
            # Этап 8: Генерация названий
            self.factor_name_generator = FactorNameGenerator()
            variables_df = self.artifacts['factor_names']
            communalities_df = self.artifacts['factor_analysis']['communalities']
            self.artifacts['factor_names'] = self.factor_name_generator.process(variables_df, communalities_df)

        else:
            raise ValueError(f"Неизвестный этап обработки: {stage_num}")

        # Автоматическое сохранение результатов после каждого этапа
        self.save_results()

class SoilPreprocessor:
    def __init__(self, df, target_column='SOIL_ID', threshold_ratio=0.1):
        self.df = df.copy()
        self.target_column = target_column
        self.threshold = threshold_ratio * len(self.df)
        self.encoding_map = {}
        self.scaler = StandardScaler()
        self.original_numeric_columns = None  # Сохраняем исходные числовые столбцы
        self.encoded_columns = []  # Список закодированных категориальных столбцов
        self.processed_df = None
        self.report_dir = Path("Отчеты и выводы")
        self.report_dir.mkdir(exist_ok=True)

    @staticmethod
    def evaluate_column_significance(df, column, target_column):
        if np.issubdtype(df[column].dtype, np.number):
            if target_column in df.columns:
                groups = [group.dropna() for _, group in df.groupby(target_column)[column]]
                if len(groups) > 1:
                    _, p_value = f_oneway(*groups)
                    return p_value
        else:
            if target_column in df.columns:
                contingency_table = pd.crosstab(df[column].dropna(), df[target_column].dropna())
                if contingency_table.size > 0:
                    _, p_value, _, _ = chi2_contingency(contingency_table)
                    return p_value
        return None

    def _reorder_columns(self):
        categorical = self.df.select_dtypes(exclude='number').columns.tolist()
        numerical = self.df.select_dtypes(include='number').columns.tolist()
        self.df = self.df[categorical + numerical]

    def _filter_columns(self):
        columns_to_remove = [col for col in self.df.columns if self.df[col].count() < self.threshold]
        significant_columns = []

        for col in columns_to_remove:
            p_value = self.evaluate_column_significance(self.df, col, self.target_column)
            if p_value is not None and p_value < 0.05:
                significant_columns.append(col)

        self.df = self.df.drop(columns=[col for col in columns_to_remove if col not in significant_columns])

    def _replace_missing(self):
        for col in self.df.columns:
            if col == self.target_column:
                continue

            if np.issubdtype(self.df[col].dtype, np.number):
                self.df[col] = self.df.groupby(self.target_column)[col].transform(
                    lambda x: x.fillna(x.mean() if x.isnull().mean() < 0.5 else x.median()))
            else:
                self.df[col] = self.df.groupby(self.target_column)[col].transform(
                    lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan))

    def _encode_text_columns(self):
        text_columns = self.df.select_dtypes(exclude='number').columns.difference([self.target_column])
        self.encoded_columns = list(text_columns)  # Сохраняем список закодированных столбцов

        for col in text_columns:
            unique_values = self.df[col].astype(str).unique()
            encoding_dict = {value: idx for idx, value in enumerate(sorted(unique_values))}
            self.df[col] = self.df[col].astype(str).map(encoding_dict)
            self.encoding_map[col] = encoding_dict

    def _normalize(self):
        # Сохраняем исходные числовые столбцы (исключая целевые и закодированные)
        exclude = [self.target_column] + self.encoded_columns
        self.original_numeric_columns = self.df.select_dtypes(include='number').columns.difference(exclude)

        # Нормализуем только исходные числовые столбцы
        if not self.original_numeric_columns.empty:
            self.df[self.original_numeric_columns] = self.scaler.fit_transform(self.df[self.original_numeric_columns])

    def process(self):
        self._reorder_columns()
        self._filter_columns()
        self._replace_missing()
        self._encode_text_columns()
        self._normalize()
        self.processed_df = self.df
        return self.processed_df, self.encoding_map

    def save_results(self, output_excel="этап 1 предобработка.xlsx", output_txt="encoding_mapping.txt"):
        # Изменяем пути сохранения
        output_excel = self.report_dir / output_excel
        output_txt = self.report_dir / output_txt

        # Сохранение Excel файла
        self.processed_df.to_excel(output_excel, index=False)

        # Сохранение информации о кодировании с сортировкой
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write("Полная расшифровка кодирования текстовых признаков:\n\n")
            for column, mapping in self.encoding_map.items():
                f.write(f"Столбец: {column}\n")
                sorted_mapping = sorted(mapping.items(), key=lambda x: x[1])
                for text, code in sorted_mapping:
                    f.write(f"  '{text}' → {code}\n")
                f.write("-" * 50 + "\n")

        print("\nЭтап предобработки завершен!")
        print(f"Результаты этапа сохранены в: {output_excel}")
        print(f"Файл с кодированием: {output_txt}")

class SignificanceAnalyzer:
    def __init__(self, target_column='SOIL_ID', importance_threshold=0.01, exclude_columns = None):
        self.target_column = target_column
        self.threshold = importance_threshold
        self.exclude_columns = exclude_columns or []
        # Добавляем принудительное исключение LAT
        self.exclude_columns.extend(['LAT', 'LONG', 'ALT', 'CardID', 'RUREG'])
        self.results = []
        # Новый словарь для хранения feature_importances по моделям
        self.feature_importances_dict = {}
        self.best_model = None

    def process(self, df):
        # Дополнительная проверка на наличие исключаемых колонок
        valid_exclude = [col for col in self.exclude_columns if col in df.columns]
        X = df.drop(columns=[self.target_column] + valid_exclude)
        y = df[self.target_column]

        # Заполнение пропусков
        X_filled = X.fillna(0)

        # Оценка моделей
        models = {
            "Random Forest": RandomForestRegressor(n_estimators=95, random_state=42),
            "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
            "Support Vector Regressor (SVR)": SVR(kernel='rbf', C=100, gamma='scale'),
            "K-Nearest Neighbors (KNN)": KNeighborsRegressor(n_neighbors=5)
        }

        self.results = []
        for model_name, model in models.items():
            model.fit(X_filled, y)
            y_pred = model.predict(X_filled)

            mae = mean_absolute_error(y, y_pred)
            mse = mean_squared_error(y, y_pred)
            r2 = r2_score(y, y_pred)

            self.results.append({
                "Model": model_name,
                "MAE": mae,
                "MSE": mse,
                "R2": r2
            })

            # Если модель поддерживает feature_importances, сохраняем её
            if hasattr(model, "feature_importances_"):
                fi_df = pd.DataFrame({
                    'Feature': X.columns,
                    'Importance': model.feature_importances_
                }).sort_values('Importance', ascending=False)
                self.feature_importances_dict[model_name] = fi_df

        results_df = pd.DataFrame(self.results).sort_values(by="R2", ascending=False)
        best_model_name = results_df.iloc[0]["Model"]
        self.best_model = models[best_model_name]

        # Теперь возвращаем исходный DataFrame и словарь с важностями
        return df, self.feature_importances_dict

    def _save_feature_importance_plot(self, model_name):
        """Сохраняет график важности признаков в PNG файл"""
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=self.feature_importances_dict[model_name].head(10),
            x="Importance",
            y="Feature",
            palette="viridis"
        )
        plt.title(f"Топ-10 значимых признаков ({model_name})")
        plt.xlabel("Importance")
        plt.ylabel("Feature")
        plt.tight_layout()
        plot_path = Path("Отчеты и выводы") / f"significant_top_10_features_{model_name}.png"
        plt.savefig(plot_path)
        plt.close()


class MulticollinearityProcessor:
    def __init__(self, vif_threshold=5):
        self.vif_threshold = vif_threshold
        self.vif_data = None
        self.removed_features = []

    def process(self, df):
        # Сохраняем оригинальные пропуски
        missing_data = df.isna()

        # Заполнение пропусков медианой
        df_filled = df.apply(lambda x: x.fillna(x.median()) if np.issubdtype(x.dtype, np.number) else x)

        # Расчет VIF
        df_with_const = add_constant(df_filled)
        vif_df = pd.DataFrame()
        vif_df["Variable"] = df_with_const.columns
        vif_df["VIF"] = [variance_inflation_factor(df_with_const.values, i)
                         for i in range(df_with_const.shape[1])]

        # Фильтрация переменных
        high_vif = vif_df[(vif_df["VIF"] > self.vif_threshold) & (vif_df["Variable"] != "const")]
        self.removed_features = high_vif["Variable"].tolist()

        # Удаление признаков
        df_filtered = df_filled.drop(columns=self.removed_features)

        # Восстанавливаем оригинальные пропуски
        df_filtered[missing_data] = np.nan

        # Сохраняем артефакты
        self.vif_data = vif_df

        return df_filtered, {
            "vif_report": vif_df,
            "removed_features": self.removed_features
        }
class KMOChecker:
    def __init__(self, correlation_threshold=0.3, kmo_threshold=0.5):
        self.correlation_threshold = correlation_threshold
        self.kmo_threshold = kmo_threshold
        self.low_kmo_vars = []
        self.final_correlation_matrix = None
        self.report_dir = Path("Отчеты и выводы")
        self.report_dir.mkdir(exist_ok=True)

    @staticmethod
    def is_positive_definite(matrix):
        try:
            np.linalg.cholesky(matrix)
            return True
        except np.linalg.LinAlgError:
            return False

    def _save_correlation_plots(self, correlation_matrix):
        num_groups = 4
        group_size = len(correlation_matrix) // num_groups
        for i in range(num_groups):
            plt.figure(figsize=(8, 6))
            start = i * group_size
            end = (i + 1) * group_size if i != num_groups - 1 else len(correlation_matrix)
            group_corr = correlation_matrix.iloc[start:end, start:end]
            sns.heatmap(group_corr, annot=False, cmap="coolwarm", fmt='.2f', linewidths=0.5)
            plt.title(f"Корреляционная матрица (Группа {i + 1})")
            plot_path = self.report_dir / f"correlation_group_{i + 1}.png"
            plt.savefig(plot_path)
            plt.close()

    def process(self, df):
        # Оригинальная логика из KMO.py
        numerical_df = df.select_dtypes(include='number')
        categorical_df = df.select_dtypes(exclude='number')

        # Фильтрация по корреляции
        correlation_matrix = numerical_df.corr()
        correlation_mask = correlation_matrix.abs() >= self.correlation_threshold
        filtered_columns = correlation_matrix.columns[correlation_mask.any(axis=0)].tolist()
        numerical_filtered = numerical_df[filtered_columns]

        # Замена NaN
        numerical_filled = numerical_filtered.apply(lambda x: x.fillna(x.median()))

        # Расчет KMO
        corr_values = numerical_filled.corr().values
        corr_values[np.isnan(corr_values)] = 0
        kmo_all, kmo_model = calculate_kmo(corr_values)

        # Удаление переменных с низким KMO
        self.low_kmo_vars = numerical_filled.columns[np.where(kmo_all < self.kmo_threshold)[0]].tolist()
        numerical_final = numerical_filled.drop(columns=self.low_kmo_vars)

        # Проверка матрицы
        final_corr_matrix = numerical_final.corr()
        if not self.is_positive_definite(final_corr_matrix):
            raise ValueError("Корреляционная матрица не положительно определена!")

        # Визуализация
        self._save_correlation_plots(final_corr_matrix)

        # Сохранение отчетов
        pd.DataFrame({'Признаки': self.low_kmo_vars}).to_csv(
            self.report_dir / "low_kmo_features.csv", index=False, encoding='utf-8-sig'
        )
        pd.DataFrame({'KMO': [kmo_model]}).to_csv(
            self.report_dir / "kmo_score.csv", index=False
        )

        # Итоговый DataFrame
        final_df = pd.concat([categorical_df, numerical_final], axis=1)
        self.final_correlation_matrix = final_corr_matrix

        return final_df, {
            "kmo_model": kmo_model,
            "removed_features": self.low_kmo_vars,
            "correlation_matrix": self.final_correlation_matrix
        }
class FactorAnalyzerProcessor:
    def __init__(self, naming_file="naming_of_variables.xlsx"):
        self.report_dir = Path("Отчеты и выводы")
        self.report_dir.mkdir(exist_ok=True)  # Создаем папку, если её нет
        self.naming_file_path = self.report_dir / naming_file

        # Проверяем существование файла и создаем его при необходимости
        if not self.naming_file_path.exists():
            default_data = pd.DataFrame({
                "Переменная": [],
                "Описание данных": []
            })
            default_data.to_excel(self.naming_file_path, index=False)
            st.warning(f"Файл {naming_file} не найден. Создан пустой шаблон.")

        # Читаем файл с обработкой ошибок
        try:
            self.naming_df = pd.read_excel(self.naming_file_path)
        except Exception as e:
            st.error(f"Ошибка чтения файла {naming_file}: {str(e)}")
            self.naming_df = pd.DataFrame()

        # Инициализация путей для графиков
        self.scree_plot_path = self.report_dir / "scree_plot.png"
        self.parallel_plot_path = self.report_dir / "parallel_analysis.png"
        self.variance_plot_path = self.report_dir / "explained_variance.png"

    def _save_plots(self, eigenvalues, mean_random_eigenvalues, cumulative_variance_ratio):
        # Scree Plot
        plt.figure(figsize=(8, 6))
        plt.plot(range(1, len(eigenvalues) + 1), eigenvalues, marker='o', linestyle='--')
        plt.title("Scree Plot")
        plt.xlabel("Номер компоненты")
        plt.ylabel("Собственное значение")
        plt.axhline(y=1, color='r', linestyle='-', label="Критерий Кайзера")
        plt.grid()
        plt.legend()
        plt.savefig(self.scree_plot_path)
        plt.close()

        # Параллельный анализ
        plt.figure(figsize=(8, 6))
        plt.plot(range(1, len(eigenvalues) + 1), eigenvalues, marker='o', label="Реальные значения")
        plt.plot(range(1, len(mean_random_eigenvalues) + 1), mean_random_eigenvalues,
                marker='x', label="Случайные значения")
        plt.title("Параллельный анализ")
        plt.xlabel("Номер компоненты")
        plt.ylabel("Собственное значение")
        plt.legend()
        plt.grid()
        plt.savefig(self.parallel_plot_path)
        plt.close()

        # Объясненная дисперсия
        plt.figure(figsize=(8, 6))
        plt.plot(range(1, len(cumulative_variance_ratio) + 1), cumulative_variance_ratio, marker='o')
        plt.axhline(y=0.7, color='r', linestyle='--', label="70% дисперсии")
        plt.title("Кумулятивная объяснённая дисперсия")
        plt.xlabel("Компоненты")
        plt.ylabel("Дисперсия")
        plt.legend()
        plt.grid()
        plt.savefig(self.variance_plot_path)
        plt.close()

    def _create_empty_sheets(self, output_path):
        """Создает пустые листы в файле, если их нет."""
        if not output_path.exists():
            # Создаем новый файл с пустыми листами
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                pd.DataFrame().to_excel(writer, sheet_name="Факторные нагрузки", index=False)
                pd.DataFrame().to_excel(writer, sheet_name="Общности", index=False)

    def process(self, df, output_file, num_factors=None):
        # Оригинальная логика из FactorAnalys.py
        corr_matrix = df.corr().fillna(0)
        eigenvalues, _ = np.linalg.eig(corr_matrix)

        # Параллельный анализ
        random_eigenvalues = []
        for _ in range(100):
            random_data = np.random.normal(size=df.shape)
            rand_eigvals, _ = np.linalg.eig(np.corrcoef(random_data, rowvar=False))
            random_eigenvalues.append(rand_eigvals)

        mean_random_eigenvalues = np.mean(random_eigenvalues, axis=0)
        explained_variance = eigenvalues / eigenvalues.sum()
        cumulative_variance = np.cumsum(explained_variance)

        # Выравнивание размеров массивов
        min_len = min(len(eigenvalues), len(mean_random_eigenvalues))
        eigenvalues_trunc = eigenvalues[:min_len]
        mean_random_trunc = mean_random_eigenvalues[:min_len]

        # Расчет рекомендаций
        num_factors_kaiser = np.sum(eigenvalues_trunc > 1)
        num_factors_parallel = np.sum(eigenvalues_trunc > mean_random_trunc)
        num_factors_variance = np.argmax(cumulative_variance >= 0.7) + 1

        # Вывод рекомендаций в консоль (можно убрать или заменить на логирование)
        print("\n[Этап 5] Рекомендации по количеству факторов:")
        print(f"• По критерию Кайзера: {num_factors_kaiser}")
        print(f"• По параллельному анализу: {num_factors_parallel}")
        print(f"• Для 70% объясненной дисперсии: {num_factors_variance}")

        # Сохранение графиков
        self._save_plots(eigenvalues, mean_random_eigenvalues, cumulative_variance)

        # Если значение количества факторов не передано, используем значение по умолчанию (например, 3)
        if num_factors is None:
            num_factors = 3

        # Факторный анализ
        fa = FactorAnalyzer(n_factors=num_factors, rotation='varimax')
        fa.fit(df.fillna(df.median()))
        # Получаем собственные значения (eigenvalues)
        eigenvalues = fa.get_eigenvalues()[0]
        # Доля объясненной дисперсии каждым фактором
        explained_variance_ratio = eigenvalues / np.sum(eigenvalues)
        # Совокупная доля объясненной дисперсии (в процентах)
        cumulative_variance = np.cumsum(explained_variance_ratio) * 100
        print(f"Объясненная дисперсия выбранными факторами: {cumulative_variance[-1]:.2f}%")
        # Формирование результатов
        loadings = pd.DataFrame(
            fa.loadings_,
            index=df.columns,
            columns=[f"Фактор {i + 1}" for i in range(num_factors)]
        )
        communalities = pd.DataFrame(
            fa.get_communalities(),
            index=df.columns,
            columns=["Общность"]
        ).assign(Описание=df.columns.map(
            dict(zip(self.naming_df['Переменная'], self.naming_df['Описание данных']))
        ))

        # Сохранение в существующий файл
        output_path = self.report_dir / output_file
        self._create_empty_sheets(output_path)  # Создаем пустые листы, если их нет

        with pd.ExcelWriter(output_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            loadings.to_excel(writer, sheet_name="Факторные нагрузки", index_label="Переменная")
            communalities.to_excel(writer, sheet_name="Общности", index_label="Переменная")

        return {
            "num_factors_kaiser": num_factors_kaiser,
            "num_factors_parallel": num_factors_parallel,
            "num_factors_variance": num_factors_variance,
            "loadings": loadings,
            "communalities": communalities
        }

class FactorScoreProcessor:
    def process(self, df, factor_loadings):
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

        return factor_scores_df
class FactorNameProcessor:
    def process(self, factor_loadings, threshold=0.4):
        # Создаем словарь для хранения переменных по факторам
        factor_structure = {}

        for factor in factor_loadings.columns:
            # Выбираем переменные, которые соответствуют данному фактору с учетом порога
            variables = factor_loadings.index[abs(factor_loadings[factor]) >= threshold].tolist()
            factor_structure[factor] = ", ".join(variables)  # Преобразуем список переменных в строку

        # Преобразуем словарь в DataFrame
        variables_df = pd.DataFrame(list(factor_structure.items()), columns=["Фактор", "Переменные"])

        return variables_df


class FactorNameGenerator:
    def __init__(self, api_key='chad-9e746526a1d540a0b1d4dd56970888898jppxdhf'):
        self.api_key = api_key
        self.report_dir = Path("Отчеты и выводы")

    def process(self, variables_df, communalities_df):
        try:
            # Создаем словарь с описаниями переменных (индекс = названия переменных)
            description_dict = dict(zip(communalities_df.index, communalities_df['Описание']))
            factor_prompts = []
            # Формируем запросы для каждого фактора
            for index, row in variables_df.iterrows():
                variables = row['Переменные'].split(', ')
                descriptions = [f"{var}: {description_dict.get(var, 'Описание не найдено')}" for var in variables]
                prompt = (
                    f"Ты ученый почвовед. Придумай краткое и логичное название для фактора, "
                    f"содержащего переменные: {', '.join(variables)}. Описание переменных:\n"
                    f"{'\n'.join(descriptions)}.\nНазвание в кавычках:"
                )
                factor_prompts.append({"factor": row['Фактор'], "prompt": prompt})
            # Отправка запросов к API
            variables_df['Ответ'] = self._get_api_responses(factor_prompts)
            # Проверка результатов
            if variables_df['Ответ'].isnull().any():
                st.warning("Некоторые названия не были сгенерированы")
            return variables_df

        except Exception as e:
            st.error(f"Критическая ошибка генерации: {str(e)}")
            variables_df['Ответ'] = "Ошибка генерации"
            return variables_df

    def _get_api_responses(self, factor_prompts):
        responses = []
        for item in factor_prompts:
            try:
                response = requests.post(
                    url='https://ask.chadgpt.ru/api/public/gpt-4o-mini',
                    json={"message": item["prompt"], "api_key": self.api_key}
                )
                if response.status_code == 200:
                    resp_json = response.json()
                    responses.append(resp_json['response'].strip() if resp_json['is_success'] else "Ошибка API")
                else:
                    responses.append("Ошибка подключения")
            except Exception as e:
                responses.append(f"Ошибка: {str(e)}")
        return responses
# Пример использования
if __name__ == "__main__":
    pipeline = DataPipeline(
        input_file="soil_data2.xlsx",
        output_file="final_results.xlsx"
    )
    pipeline.run()
    print("\nВсе этапы обработки успешно завершены!")

