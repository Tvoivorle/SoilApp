import streamlit as st
import pandas as pd
import numpy as np
import hashlib
from pathlib import Path
import matplotlib.pyplot as plt
from Main import DataPipeline, FactorAnalyzerProcessor  # Импорт основных классов
import seaborn as sns
import requests
import re
import json

# Функция для сохранения данных
def save_user_input(user_input):
    with open("user_input.json", "w", encoding="utf-8") as f:
        json.dump(user_input, f, ensure_ascii=False, indent=4)

# Функция для загрузки данных
def load_user_input():
    try:
        with open("user_input.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Если файла нет, возвращаем пустой словарь
    except json.JSONDecodeError:
        st.error("Ошибка загрузки сохраненных данных.")
        return {}


class RecommendationGenerator:
    def __init__(self, api_key='chad-396a38eb0ffc4d809b11543207ab3ab7moxdetmr'):
        self.api_key = api_key
        self.report_dir = Path("Отчеты и выводы")
    def process(self, factors_df):
        try:
            recommendation_prompts = []
            # Формируем запросы для каждого фактора
            for index, row in factors_df.iterrows():
                prompt = (
                    f"Ты агроном-практик с 20-летним опытом. Сгенерируй конкретные рекомендации для "
                    f"фермера на основе этих данных:\n\n"
                    f"Фактор: «{row['Название_фактора']}»\n"
                    f"Влияние: {row['Влияние']} (шкала 0-100)\n"
                    f"Входящие параметры: {', '.join(parse_variables(row['Фактор']))}\n\n"  # Функция для извлечения переменных
                    "Требования к ответу:\n"
                    "1. Начни сразу с практических шагов без вводных фраз\n"
                    "2. Укажи 3-5 конкретных действий с примерами культур/удобрений\n"
                    "3. Добавь параметры для мониторинга (оптимальные диапазоны значений)\n"
                    "4. Предложи методы коррекции для проблемных значений\n"
                    "5. Избегай общих терминов, ориентируйся на полевое применение\n"
                    "Формат:\n"
                    "1. {Название фактора} | Влияние: {значение}\n"
                    "- Действие 1: ...\n"
                    "- Действие 2: ...\n"
                    "- Контроль: замерять ... (оптимум: X-Y единиц)\n"
                    "- Примеры: культуры А, Б; удобрения В, Г"
                )
                recommendation_prompts.append({"factor": row['Фактор'], "prompt": prompt})
            # Отправка запросов к API
            factors_df['Рекомендации'] = self._get_api_responses(recommendation_prompts)

            # Проверка результатов
            if factors_df['Рекомендации'].str.contains('Ошибка').any():
                st.warning("Некоторые рекомендации не были сгенерированы")

            return factors_df

        except Exception as e:
            st.error(f"Ошибка генерации рекомендаций: {str(e)}")
            factors_df['Рекомендации'] = "Ошибка обработки"
            return factors_df

    def _get_api_responses(self, prompts):
        responses = []
        for item in prompts:
            try:
                # Логирование запроса
                print(f"Sending request to API: {item['prompt'][:50]}...")

                response = requests.post(
                    url='https://ask.chadgpt.ru/api/public/gpt-4o',
                    json={"message": item["prompt"], "api_key": self.api_key},
                    timeout=20
                )

                # Логирование ответа
                print(f"Response status: {response.status_code}")

                if response.status_code == 200:
                    resp_json = response.json()
                    if resp_json.get('is_success', False):
                        clean_response = resp_json['response'].split('```')[0].strip()
                        responses.append(clean_response)
                    else:
                        responses.append(f"API Error: {resp_json.get('message', 'Unknown error')}")
                else:
                    responses.append(f"HTTP Error {response.status_code}")

            except Exception as e:
                responses.append(f"Connection Error: {str(e)}")

        return responses

def parse_variables(factor_str):
    """Извлекает переменные из строки фактора вида 'F1 (var1, var2)'"""
    match = re.search(r'\((.*?)\)', factor_str)
    return match.group(1).split(', ') if match else []

@st.cache_data
def load_variable_descriptions():
    """ Загружает описания переменных """
    try:
        desc_df = pd.read_excel("Отчеты и выводы/naming_of_variables.xlsx")
        return desc_df[['Переменная', 'Описание данных']].dropna()
    except Exception as e:
        st.error(f"Ошибка загрузки файла с описаниями переменных: {str(e)}")
        return pd.DataFrame(columns=['Переменная', 'Описание данных'])

@st.cache_data
def load_factor_names():
    """Загружает названия факторов из файла"""
    path = Path("Отчеты и выводы/soil_analysis_results.xlsx")
    if path.exists():
        try:
            names_df = pd.read_excel(path, sheet_name="Названия факторов")
            return dict(zip(
                [f"Фактор {i+1}" for i in range(len(names_df))],
                names_df["Ответ"].fillna("Без названия").tolist()
            ))
        except:
            return {}
    return {}

def get_file_hash(file):
    """Функция вычисляет хеш (MD5) файла для проверки изменений"""
    file.seek(0)
    return hashlib.md5(file.read()).hexdigest()


# 🎯 Функция загрузки факторных данных
def load_factor_data():
    """Загружает факторные нагрузки, оценки и названия факторов"""
    factor_scores_path = Path("Отчеты и выводы/soil_analysis_results.xlsx")

    factor_names = {}
    factor_loadings = None
    factor_scores = None

    if factor_scores_path.exists():
        with pd.ExcelFile(factor_scores_path) as xls:
            # Загрузка основных данных
            if "Факторные нагрузки" in xls.sheet_names and "Факторные оценки" in xls.sheet_names:
                factor_loadings = pd.read_excel(xls, sheet_name="Факторные нагрузки", index_col=0)
                factor_scores = pd.read_excel(xls, sheet_name="Факторные оценки", index_col=0)

            # Загрузка названий факторов
            if "Названия факторов" in xls.sheet_names:
                names_df = pd.read_excel(xls, sheet_name="Названия факторов")
                factor_names = dict(zip(
                    [f"Фактор {i + 1}" for i in range(len(names_df))],
                    names_df["Ответ"].tolist()
                ))

    return factor_loadings, factor_scores, factor_names

def main():
    st.set_page_config(page_title="Soil Analysis App", layout="wide")

    # 🎯 **Выбор страницы**
    page = st.sidebar.selectbox(
        "Выберите раздел",
        ["Предобработка и факторный анализ", "Анализ почвы"]
    )

    if page == "Предобработка и факторный анализ":
        st.title("📊 Анализ почвенных данных")

        # Инициализация состояния сессии и флагов этапов
        if 'pipeline' not in st.session_state:
            st.session_state.pipeline = None
        if 'file_uploaded' not in st.session_state:
            st.session_state.file_uploaded = False
        if 'file_hash' not in st.session_state:
            st.session_state.file_hash = None

        # Флаги для этапов обработки
        if 'preprocessed' not in st.session_state:
            st.session_state.preprocessed = False
        if 'significance_done' not in st.session_state:
            st.session_state.significance_done = False
        if 'multicollinearity_done' not in st.session_state:
            st.session_state.multicollinearity_done = False
        if 'kmo_done' not in st.session_state:
            st.session_state.kmo_done = False
        if 'factor_analysis_done' not in st.session_state:
            st.session_state.factor_analysis_done = False
        if 'factor_scores_done' not in st.session_state:
            st.session_state.factor_scores_done = False
        if 'factor_names_done' not in st.session_state:
            st.session_state.factor_names_done = False

        temp_path = None  # Инициализация переменной до загрузки файла
        # В основном коде после инициализации:
        variable_descriptions = load_variable_descriptions()

        uploaded_file = st.file_uploader("Загрузите файл данных (Excel)", type=["xlsx"])

        if uploaded_file:
            current_file_hash = get_file_hash(uploaded_file)
            if st.session_state.file_hash is None or st.session_state.file_hash != current_file_hash:
                # Сохранение временного файла и инициализация пайплайна
                temp_path = Path("temp_soil_data.xlsx")
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                st.session_state.pipeline = DataPipeline(
                    input_file=str(temp_path),
                    output_file="soil_analysis_results.xlsx"
                )
                st.session_state.file_uploaded = True
                st.session_state.file_hash = current_file_hash
                # Сброс флагов этапов обработки, так как файл изменился
                st.session_state.preprocessed = False
                st.session_state.significance_done = False
                st.session_state.multicollinearity_done = False
                st.session_state.kmo_done = False
                st.session_state.factor_analysis_done = False
                st.session_state.factor_scores_done = False
                st.session_state.factor_names_done = False
            else:
                st.write("Файл не изменился, пропускаем этапы 1-4.")

        if st.session_state.pipeline:
            pipeline = st.session_state.pipeline
            progress_bar = st.progress(0)
            status = st.empty()

            try:
                # Этап 1: Предобработка
                with st.expander("✅ Этап 1: Предобработка данных", expanded=True):
                    if not st.session_state.preprocessed:
                        status.markdown("**Выполняется предварительная обработка данных...**")
                        pipeline.run_stage(1)
                        st.session_state.preprocessed = True
                        st.success("Предобработка завершена!")
                        st.write(f"Сохранилось признаков: {len(pipeline.data.columns)}")
                        progress_bar.progress(12)
                    else:
                        st.write("Этап предобработки уже выполнен.")
                        progress_bar.progress(12)

                    # Показываем все предобработанные данные с возможностью прокрутки
                    if st.checkbox("Показать предобработанные данные"):
                        st.dataframe(pipeline.data, height=600)  # height можно настроить по необходимости

                # Этап 2: Анализ значимости признаков
                with st.expander("📈 Этап 2: Анализ значимости признаков"):
                    if not st.session_state.significance_done:
                        status.markdown("**Анализ значимости признаков...**")
                        pipeline.run_stage(2)
                        st.session_state.significance_done = True
                        progress_bar.progress(25)
                    else:
                        st.write("Этап анализа значимости уже выполнен.")
                        progress_bar.progress(25)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Выберите модель для отображения важности признаков")
                        if pipeline.artifacts['feature_importances']:
                            model_names = list(pipeline.artifacts['feature_importances'].keys())
                            selected_model = st.selectbox("Модель", model_names, index=0)

                            # Получаем и обогащаем данные описаниями
                            top_features = pipeline.artifacts['feature_importances'][selected_model].head()
                            if not variable_descriptions.empty:
                                top_features = top_features.merge(
                                    variable_descriptions,
                                    left_on='Feature',
                                    right_on='Переменная',
                                    how='left'
                                ).drop('Переменная', axis=1).fillna('Нет описания')

                            st.subheader("Топ-5 значимых признаков")
                            st.dataframe(top_features)
                    with col2:
                        st.subheader("Сравнение моделей")
                        if (pipeline.significance_analyzer is not None and
                            hasattr(pipeline.significance_analyzer, 'results')):
                            models_df = pd.DataFrame(pipeline.significance_analyzer.results)
                            st.dataframe(models_df.sort_values('R2', ascending=False))
                        else:
                            st.warning("Данные анализа значимости недоступны")
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.barplot(
                        data=pipeline.artifacts['feature_importances'][selected_model].head(10),
                        x="Importance",
                        y="Feature",
                        palette="viridis",
                        ax=ax
                    )
                    st.pyplot(fig)

                # Этап 3: Мультиколлинеарность
                with st.expander("📉 Этап 3: Анализ мультиколлинеарности"):
                    if not st.session_state.multicollinearity_done:
                        status.markdown("**Обработка мультиколлинеарности...**")
                        pipeline.run_stage(3)
                        st.session_state.multicollinearity_done = True
                        progress_bar.progress(37)
                    else:
                        st.write("Этап мультиколлинеарности уже выполнен.")
                        progress_bar.progress(37)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Удаленные признаки")
                        removed_features = pipeline.artifacts['multicollinearity']['removed_features']

                        # Добавляем описания для удаленных признаков
                        if not variable_descriptions.empty:
                            removed_df = pd.DataFrame(removed_features, columns=['Переменная'])
                            removed_df = removed_df.merge(
                                variable_descriptions,
                                on='Переменная',
                                how='left'
                            ).fillna('Нет описания')
                            st.dataframe(removed_df)
                        else:
                            st.write(removed_features)
                    with col2:
                        st.subheader("VIF отчет")
                        vif_report = pipeline.artifacts['multicollinearity']['vif_report'].copy()

                        # Добавляем описания в VIF отчет
                        if not variable_descriptions.empty:
                            # Проверяем, есть ли колонка с названиями переменных
                            if 'Variable' in vif_report.columns:
                                # Используем колонку 'Variable' для объединения
                                vif_report['Variable'] = vif_report['Variable'].astype(str).str.strip().str.lower()
                                variable_descriptions['Переменная'] = variable_descriptions['Переменная'].astype(
                                    str).str.strip().str.lower()

                                # Объединяем по колонке 'Variable'
                                vif_report = vif_report.merge(
                                    variable_descriptions,
                                    left_on='Variable',
                                    right_on='Переменная',
                                    how='left'
                                ).drop('Переменная', axis=1).fillna('Нет описания')
                            else:
                                # Если колонки 'Variable' нет, используем индекс
                                vif_report = vif_report.reset_index()
                                vif_report['index'] = vif_report['index'].astype(str).str.strip().str.lower()
                                variable_descriptions['Переменная'] = variable_descriptions['Переменная'].astype(
                                    str).str.strip().str.lower()

                                # Объединяем по индексу
                                vif_report = vif_report.merge(
                                    variable_descriptions,
                                    left_on='index',
                                    right_on='Переменная',
                                    how='left'
                                ).drop('Переменная', axis=1).fillna('Нет описания')

                                # Возвращаем индекс
                                vif_report = vif_report.set_index('index')
                                vif_report.index.name = None

                        st.dataframe(vif_report)

                # Этап 4: KMO анализ
                with st.expander("🔍 Этап 4: KMO анализ"):
                    if not st.session_state.kmo_done:
                        status.markdown("**Проверка адекватности выборки...**")
                        pipeline.run_stage(4)
                        st.session_state.kmo_done = True
                        progress_bar.progress(50)
                    else:
                        st.write("Этап KMO анализа уже выполнен.")
                        progress_bar.progress(50)

                    st.subheader("Результаты KMO")
                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("Общий KMO", f"{pipeline.artifacts['kmo']['kmo_model']:.2f}")
                        st.write("Удаленные переменные:")
                        st.write(pipeline.artifacts['kmo']['removed_features'])

                    with col2:
                        # Получаем список всех корреляционных матриц
                        correlation_images = sorted(Path("Отчеты и выводы").glob("correlation_group_*.png"))

                        # Инициализируем индекс текущего изображения
                        if 'current_corr_image' not in st.session_state:
                            st.session_state.current_corr_image = 0

                        # Создаем кнопки для навигации
                        cols = st.columns([1, 2, 1])
                        with cols[0]:
                            if st.button("← Назад"):
                                st.session_state.current_corr_image = max(0, st.session_state.current_corr_image - 1)
                        with cols[2]:
                            if st.button("Вперед →"):
                                st.session_state.current_corr_image = min(len(correlation_images) - 1,
                                                                          st.session_state.current_corr_image + 1)

                        # Отображаем текущее изображение
                        if correlation_images:
                            current_image = correlation_images[st.session_state.current_corr_image]
                            st.image(str(current_image))
                            st.caption(
                                f"Корреляционная матрица (фрагмент {st.session_state.current_corr_image + 1} из {len(correlation_images)})")
                        else:
                            st.warning("Корреляционные матрицы не найдены")

                    # Рекомендации после KMO-анализа
                    if "factor_analysis_recommendations" not in st.session_state:
                        factor_analyzer = FactorAnalyzerProcessor()
                        recommendations = factor_analyzer.process(pipeline.data, pipeline.output_file, num_factors=None)
                        st.session_state.factor_analysis_recommendations = recommendations

                # 🔥 Этап 5: Факторный анализ
                with st.expander("🧩 Этап 5: Факторный анализ"):
                    status.markdown("**Выполнение факторного анализа...**")

                    # 🔥 Вывод рекомендаций по количеству факторов (сразу после KMO-анализа)
                    st.subheader("📊 Рекомендации по количеству факторов")

                    recs = st.session_state.get("factor_analysis_recommendations", {})
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Критерий Кайзера", recs.get('num_factors_kaiser', 'N/A'))
                    with col2:
                        st.metric("Параллельный анализ", recs.get('num_factors_parallel', 'N/A'))
                    with col3:
                        st.metric("70% дисперсии", recs.get('num_factors_variance', 'N/A'))

                    # 🔥 Отображение графиков (графики теперь тоже загружаются после KMO-анализа)
                    st.subheader("📉 Графики для определения количества факторов")
                    col1, col2 = st.columns(2)
                    with col1:
                        if Path("Отчеты и выводы/scree_plot.png").exists():
                            st.image("Отчеты и выводы/scree_plot.png", caption="График Scree Plot")
                        else:
                            st.warning("График Scree Plot не найден")

                    with col2:
                        if Path("Отчеты и выводы/explained_variance.png").exists():
                            st.image("Отчеты и выводы/explained_variance.png", caption="Объясненная дисперсия")
                        else:
                            st.warning("График не найден")

                    # 🔥 Ввод количества факторов (с кнопкой)
                    st.subheader("⚙️ Выбор количества факторов")
                    num_factors = st.number_input(
                        "Выберите количество факторов",
                        min_value=1,
                        max_value=30,
                        value=3,
                        key="num_factors_input"
                    )

                    # Кнопка для запуска анализа
                    if st.button("🔍 Выполнить факторный анализ"):
                        try:
                            pipeline.factor_analyzer = FactorAnalyzerProcessor()
                            result = pipeline.factor_analyzer.process(
                                pipeline.data,
                                pipeline.output_file,
                                num_factors=num_factors
                            )

                            # Проверка, есть ли результаты факторного анализа
                            if result and "loadings" in result:
                                pipeline.artifacts['factor_analysis'] = result  # Сохранение результата
                                st.session_state.factor_analysis_done = True
                                st.success("Факторный анализ выполнен успешно!")

                                # 📊 Вывод совокупной объясненной дисперсии
                                explained_variance = result.get("cumulative_variance", None)
                                if explained_variance is not None:
                                    st.metric("Совокупная объясненная дисперсия", f"{explained_variance:.2f}%")

                                # Открываем этапы 6, 7 и финальный этап
                                st.session_state.show_stage_6 = True
                                st.session_state.show_stage_7 = True
                                st.session_state.show_final_stage = True

                                progress_bar.progress(62)
                            else:
                                st.error("⚠️ Ошибка: Факторный анализ не вернул результаты.")

                        except Exception as e:
                            st.error(f"🚨 Ошибка факторного анализа: {str(e)}")

                    elif st.session_state.factor_analysis_done:
                        st.success(
                            "Факторный анализ уже выполнен. При необходимости измените параметры и запустите анализ заново."
                        )

                # Этап 6: Факторные оценки (скрыт, пока не выполнен факторный анализ)
                if st.session_state.get("show_stage_6", False):
                    with st.expander("📐 Этап 6: Расчет факторных оценок"):
                        if 'factor_analysis' not in pipeline.artifacts:
                            st.error("⚠️ Ошибка: Перед выполнением Этапа 6 сначала запустите факторный анализ (Этап 5).")
                        else:
                            if not st.session_state.factor_scores_done:
                                status.markdown("**Расчет факторных оценок...**")
                                pipeline.run_stage(6)
                                st.session_state.factor_scores_done = True
                                progress_bar.progress(75)
                            else:
                                st.write("Этап расчета факторных оценок уже выполнен.")
                                progress_bar.progress(75)

                            st.subheader("Факторные оценки")
                            st.dataframe(pipeline.artifacts['factor_scores'].head())

                            # 3D Визуализация, если есть хотя бы 3 фактора
                            if len(pipeline.artifacts['factor_scores'].columns) >= 3:
                                fig = plt.figure(figsize=(10, 6))
                                ax = fig.add_subplot(111, projection='3d')
                                factors = pipeline.artifacts['factor_scores'].iloc[:, :3]
                                ax.scatter(factors.iloc[:, 0], factors.iloc[:, 1], factors.iloc[:, 2])
                                ax.set_xlabel(factors.columns[0])
                                ax.set_ylabel(factors.columns[1])
                                ax.set_zlabel(factors.columns[2])
                                st.pyplot(fig)

                # Этап 7: Группировка переменных и генерация названий (скрыт, пока не выполнен факторный анализ)
                if st.session_state.get("show_stage_7", False):
                    with st.expander("📋 Этап 7: Группировка переменных и генерация названий"):
                        status.markdown("**Формирование групп переменных и автоматическая генерация названий факторов...**")
                        if not st.session_state.factor_names_done:
                            pipeline.run_stage(7)  # Группировка переменных
                            pipeline.run_stage(8)  # Генерация названий
                            st.session_state.factor_names_done = True
                            progress_bar.progress(87)
                        else:
                            progress_bar.progress(87)

                        if 'factor_names' in pipeline.artifacts:
                            st.subheader("Распределение переменных по факторам")
                            st.dataframe(pipeline.artifacts['factor_names'])

                            # Выбор фактора для детального просмотра
                            if 'Фактор' in pipeline.artifacts['factor_names'].columns:
                                selected_factor = st.selectbox(
                                    "Выберите фактор для детального просмотра",
                                    pipeline.artifacts['factor_names']['Фактор'].tolist()
                                )
                                if 'Переменные' in pipeline.artifacts['factor_names'].columns:
                                    factor_vars = pipeline.artifacts['factor_names'][
                                        pipeline.artifacts['factor_names']['Фактор'] == selected_factor
                                        ]['Переменные'].values[0]
                                    st.write(f"Переменные в факторе {selected_factor}: {factor_vars}")
                                else:
                                    st.warning("Столбец 'Переменные' отсутствует в данных.")
                            else:
                                st.warning("Столбец 'Фактор' отсутствует в данных.")
                        else:
                            st.error("Данные о факторах отсутствуют. Убедитесь, что этап группировки выполнен успешно.")

                # Финальный этап (скрыт, пока не выполнен факторный анализ)
                if st.session_state.get("show_final_stage", False):
                    with st.expander("📥 Финальные результаты"):
                        progress_bar.progress(100)
                        st.success("Анализ успешно завершен!")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.download_button(
                                label="Скачать полный отчет Excel",
                                data=open("Отчеты и выводы/soil_analysis_results.xlsx", "rb").read(),
                                file_name="soil_analysis_report.xlsx"
                            )
                        st.subheader("Факторные нагрузки")
                        st.dataframe(pipeline.artifacts['factor_analysis']['loadings'])
                        st.subheader("Факторные оценки")
                        st.dataframe(pipeline.artifacts['factor_scores'])
                        fig = plt.figure(figsize=(12, 6))
                        pipeline.artifacts['factor_scores'].plot(kind='bar')
                        plt.title("Распределение факторных оценок")
                        st.pyplot(fig)

            except Exception as e:
                st.error(f"🚨 Ошибка выполнения: {str(e)}")
                st.exception(e)
            finally:
                progress_bar.empty()

        # Удаляем временный файл только если он существует
        if temp_path is not None and temp_path.exists():
            temp_path.unlink(missing_ok=True)

    elif page == "Анализ почвы":
        st.title("🌱 Анализ почвы по факторным нагрузкам")

        # Инициализация состояния сессии
        if 'top_factors' not in st.session_state:
            st.session_state.top_factors = None
        if 'recommendations' not in st.session_state:
            st.session_state.recommendations = None

        # Загрузка данных ВНЕ блока инициализации состояния
        factor_loadings, factor_scores, factor_names = load_factor_data()
        variable_descriptions = load_variable_descriptions()

        # Загрузка кодировок
        @st.cache_data
        def load_encoding_mapping():
            encoding_mapping = {}
            try:
                with open("Отчеты и выводы/encoding_mapping.txt", "r", encoding="utf-8") as file:
                    current_column = None
                    for line in file:
                        if line.startswith("Столбец:"):
                            current_column = line.split(":")[1].strip()
                            encoding_mapping[current_column] = {}
                        elif "→" in line:
                            key, value = line.split("→")
                            key = key.strip().strip("'")
                            value = int(value.strip())
                            encoding_mapping[current_column][key] = value
            except Exception as e:
                st.error(f"Ошибка загрузки кодировок: {str(e)}")
            return encoding_mapping

        encoding_mapping = load_encoding_mapping()

        # Основной блок интерфейса
        if factor_loadings is not None and factor_scores is not None:
            st.write("🔍 Введите известные характеристики почвы:")

            # Подготовка данных
            variable_descriptions['Переменная'] = variable_descriptions['Переменная'].astype(str).str.strip()
            factor_loadings.index = factor_loadings.index.astype(str).str.strip()
            index_name = factor_loadings.index.name or 'index'
            factor_data = factor_loadings.reset_index().rename(columns={index_name: 'variable'})

            factor_data = factor_data.merge(
                variable_descriptions,
                left_on='variable',
                right_on='Переменная',
                how='left'
            ).drop(columns=["Переменная"]).fillna("Нет описания")

            if 'variable' not in factor_data.columns:
                st.error("Ошибка структуры данных")
                st.stop()

            # 🔄 Загружаем ранее сохраненные значения, если они есть
            loaded_data = load_user_input()

            # 📝 **Генерация полей ввода с предзаполнением сохраненных данных**
            user_input = {}
            for _, row in factor_data.iterrows():
                var_name = row['variable']
                desc = row["Описание данных"]
                label = f"{var_name} - {desc}"

                if var_name in encoding_mapping:
                    options = list(encoding_mapping[var_name].keys())

                    # Определяем сохраненное значение, если оно есть
                    default_value = next(
                        (k for k, v in encoding_mapping[var_name].items() if v == loaded_data.get(var_name, 0)),
                        options[0]
                    )

                    selected = st.selectbox(label, options, key=f"select_{var_name}",
                                            index=options.index(default_value))
                    user_input[var_name] = encoding_mapping[var_name][selected]

                else:
                    user_input[var_name] = st.number_input(label, value=loaded_data.get(var_name, 0.0),
                                                           key=f"num_{var_name}")

            # 🎛️ Кнопки для загрузки и сохранения данных (теперь user_input уже определен)
            col1, col2 = st.columns(2)

            with col1:
                if st.button("📂 Загрузить сохраненные данные"):
                    loaded_data = load_user_input()
                    if loaded_data:
                        st.success("✅ Данные успешно загружены!")
                    else:
                        st.warning("⚠️ Файл данных не найден или пуст.")

            with col2:
                if st.button("💾 Сохранить текущие данные"):
                    save_user_input(user_input)
                    st.success("✅ Данные сохранены!")

            # Управляющие кнопки
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("🔎 Найти релевантные факторы"):
                    input_vector = np.array([user_input[var] for var in factor_data["variable"]])
                    factor_similarity = factor_loadings.T.dot(input_vector)

                    if isinstance(factor_similarity, pd.DataFrame):
                        factor_similarity = factor_similarity.squeeze()

                    st.session_state.top_factors = factor_similarity.abs().sort_values(ascending=False).head(3)
                    st.session_state.recommendations = None

            with col2:
                if st.session_state.top_factors is not None:
                    if st.button("📜 Получить рекомендации"):
                        with st.spinner("Анализируем данные..."):
                            try:
                                recommendations_df = pd.DataFrame({
                                    "Название_фактора": [factor_names.get(f, f) for f in
                                                         st.session_state.top_factors.index],
                                    "Влияние": st.session_state.top_factors.values.round(2),
                                    "Фактор": st.session_state.top_factors.index
                                })

                                generator = RecommendationGenerator()
                                result_df = generator.process(recommendations_df)
                                st.session_state.recommendations = result_df

                            except Exception as e:
                                st.error(f"Ошибка генерации: {str(e)}")

            # Отображение результатов (всегда под полями ввода)
            if st.session_state.top_factors is not None:
                st.subheader("📌 Наиболее релевантные факторы")
                for factor, score in st.session_state.top_factors.items():
                    display_name = factor_names.get(factor, factor)
                    st.write(f"**{display_name}**: влияние {score:.2f}")

                fig, ax = plt.subplots(figsize=(8, 4))
                sns.barplot(x=st.session_state.top_factors.values,
                            y=st.session_state.top_factors.index,
                            ax=ax,
                            palette="viridis")
                ax.set(xlabel="Влияние", ylabel="Фактор", title="Топ факторов влияния")
                st.pyplot(fig)

            if st.session_state.recommendations is not None:
                st.subheader("🚜 Агрономические рекомендации")
                full_text = "\n\n".join(
                    f"### {row['Название_фактора']} (влияние: {row['Влияние']})\n{row['Рекомендации']}"
                    for _, row in st.session_state.recommendations.iterrows()
                )
                st.markdown(full_text)

        else:
            st.warning("Требуется выполнить факторный анализ")


if __name__ == "__main__":
    main()
