class DataPipeline:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.data = None
        self.artifacts = {}
        self.significance_analyzer = None
        self.multicollinearity_processor = None
        self.kmo_checker = None
        self.factor_analyzer = None
        self.factor_name_generator = None

    def run(self):
        # Этап 1: Предобработка
        preprocessor = SoilPreprocessor(self.input_file)
        self.data, self.artifacts['encoding_map'] = preprocessor.process()
        preprocessor.save_results()
        print("\n[Этап 1] Предобработка данных завершена!")
        print(f"Сохранилось признаков: {len(self.data.columns)}")

        # Этап 2: Оценка значимости
        self.significance_analyzer = SignificanceAnalyzer()
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

        try:
            # Создаем новый файл или перезаписываем существующий
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Основные данные
                self.data.to_excel(writer, sheet_name="Данные", index=False)

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
                    self.artifacts['factor_scores'].to_excel(
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
            name_mapping = dict(zip(factor_names['Фактор'], factor_names['Ответ']))

            if 'factor_analysis' in self.artifacts:
                self.artifacts['factor_analysis']['loadings'].rename(columns=name_mapping, inplace=True)
            if 'factor_scores' in self.artifacts:
                self.artifacts['factor_scores'].rename(columns=name_mapping, inplace=True)

        # Сохраняем CSV-отчеты
        reports = {
            'model_comparison.csv': pd.DataFrame(self.significance_analyzer.results)
            if hasattr(self, 'significance_analyzer')
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
            preprocessor = SoilPreprocessor(self.input_file)
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