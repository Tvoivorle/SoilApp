# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QGraphicsScene, QGraphicsView, \
    QStyleOptionViewItem
from PySide6.QtGui import QStandardItemModel, QStandardItem, QBrush, QPainter, QFont
from Factors import Ui_MainWindow
from factor_analyzer import FactorAnalyzer
import pandas as pd
import  numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class FactorApp(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Df_choice_button.clicked.connect(self.load_dataset)
        self.ui.Elbow_build_button.clicked.connect(self.plot_elbow_method)
        self.ui.Newvalue_button.clicked.connect(self.calculate_new_values)
        self.ui.Matrix_build_button.clicked.connect(self.calculate_factor_loadings)  # Исправлено
        self.ui.Save_button.clicked.connect(self.save_to_excel)

        self.scene = QGraphicsScene(self)
        self.ElbowView = self.ui.ElbowView
        self.ui.ElbowView.setScene(self.scene)

        self.df = None
        self.n_factors = None
        self.loadings = None
        self.df_fa = None

    def load_dataset(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Excel Files (*.xlsx)")
        if filepath:
            self.df = pd.read_excel(filepath)
            self.show_dataframe_in_tableview()

    def show_dataframe_in_tableview(self):
        model = QStandardItemModel(self.df.shape[0], self.df.shape[1])
        for row in range(self.df.shape[0]):
            for column in range(self.df.shape[1]):
                item = QStandardItem()
                item.setData('{:.3f}'.format(self.df.iat[row, column]), Qt.DisplayRole)
                model.setItem(row, column, item)

        model.setHorizontalHeaderLabels(self.df.columns)
        self.ui.ValueView.setModel(model)

    def plot_elbow_method(self):
        if not hasattr(self, 'df'):
            return

        fa = FactorAnalyzer()
        fa.fit(self.df)
        ev, v = fa.get_eigenvalues()

        plt.scatter(range(1, self.df.shape[1] + 1), ev)
        plt.plot(range(1, self.df.shape[1] + 1), ev)
        plt.xlabel('Количество факторов')
        plt.axhline(y=1, c='k')
        self.show_matplotlib_plot()

    def show_matplotlib_plot(self):
        self.scene.clear()
        canvas = FigureCanvas(plt.gcf())
        canvas.setGeometry(0, 0, self.ElbowView.width(), self.ElbowView.height())
        self.scene.addWidget(canvas)

    def calculate_new_values(self):
        n_factors_str = self.ui.Factor_input.text()
        try:
            self.n_factors = int(n_factors_str)
            fa = FactorAnalyzer(n_factors=self.n_factors, rotation='varimax')
            fa.fit(self.df)
            self.loadings = fa.loadings_
            new_vals = fa.transform(self.df)
            self.show_new_values_in_tableview(new_vals)
            self.df_fa = pd.DataFrame(new_vals, columns=[f'Factor {i + 1}' for i in range(self.n_factors)])
        except ValueError:
            print("Введите целое число для количества факторов")

    def calculate_factor_loadings(self):
        try:
            if self.df is None:
                print("Ошибка: Данные не загружены.")
                return

            num_factors_str = self.ui.Factor_input.text()
            try:
                num_factors = int(num_factors_str)
            except ValueError:
                print("Ошибка: Введите целое число для количества факторов.")
                return

            fa = FactorAnalyzer(n_factors=num_factors)  # Указание количества факторов
            fa.fit(self.df)
            self.loadings = fa.loadings_

            self.display_factor_matrix()

        except Exception as e:
            print(f"Ошибка при расчете факторных нагрузок: {e}")

    def show_new_values_in_tableview(self, new_vals):
        model = QStandardItemModel(len(new_vals), len(new_vals[0]))

        for row in range(len(new_vals)):
            for column in range(len(new_vals[0])):
                formatted_value = "{:.3f}".format(new_vals[row][column])
                item = QStandardItem(formatted_value)
                model.setItem(row, column, item)

        model.setHorizontalHeaderLabels([f"Factor {i + 1}" for i in range(len(new_vals[0]))])
        self.ui.ValueView.setModel(model)

    def display_factor_matrix(self):
        try:
            if self.loadings is None:
                print("Ошибка: Матрица компонентов не была рассчитана.")
                return

            num_factors_str = self.ui.Factor_input.text()
            try:
                num_factors = int(num_factors_str)
            except ValueError:
                print("Ошибка: Введите целое число для количества факторов.")
                return

            num_rows, num_cols = self.loadings.shape

            if num_factors > num_cols:
                print("Ошибка: Количество введенных факторов больше, чем количество столбцов в матрице компонентов.")
                return

            model = QStandardItemModel(num_rows, num_factors + 1)
            for row in range(num_rows):
                variable_name = self.df.columns[row]
                item = QStandardItem(variable_name)
                model.setItem(row, 0, item)

                for col in range(num_factors):  # Заменено на num_factors
                    value = self.loadings[row, col]  # Заменено на [row, col]
                    if isinstance(value, (int, float)):
                        formatted_value = "{:.3f}".format(value)
                    else:
                        formatted_value = str(value)
                    item = QStandardItem(formatted_value)
                    model.setItem(row, col + 1, item)

            header_labels = ['Variable'] + ['Factor{}'.format(i) for i in range(1, num_factors + 1)]
            model.setHorizontalHeaderLabels(header_labels)

            self.ui.MatrixView.setModel(model)
        except Exception as e:
            print(f"Ошибка: {e}")

    def save_to_excel(self):
        if self.df is None or self.loadings is None or self.df_fa is None:
            print("Ошибка: Нет данных для сохранения.")
            return

        filepath, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Excel Files (*.xlsx)")
        if filepath:
            try:
                # Добавляем расширение .xlsx, если оно отсутствует
                if not filepath.lower().endswith('.xlsx'):
                    filepath += '.xlsx'

                with pd.ExcelWriter(filepath) as writer:
                    # Сохраняем исходные значения
                    if self.df is not None:
                        self.df.to_excel(writer, sheet_name='Исходные значения', index=False)
                    # Сохраняем матрицу компонентов
                    if self.loadings is not None:
                        # Создаем DataFrame для матрицы компонентов с добавлением заголовков
                        loadings_df = pd.DataFrame(self.loadings, columns=['Factor{}'.format(i + 1) for i in
                                                                           range(self.loadings.shape[1])])
                        loadings_df.insert(0, 'Variable', self.df.columns)
                        loadings_df.to_excel(writer, sheet_name='Матрица компонентов', index=False)
                    # Сохраняем новые значения
                    if self.df_fa is not None:
                        self.df_fa.to_excel(writer, sheet_name='Новые значения', index=False)
                print("Данные успешно сохранены в файл:", filepath)
            except Exception as e:
                print("Ошибка при сохранении данных:", e)

    def create_descript_table(self):
        try:
            if self.loadings is None:
                print("Ошибка: Матрица компонентов не была рассчитана.")
                return

            num_factors_str = self.ui.Factor_input.text()
            try:
                num_factors = int(num_factors_str)
            except ValueError:
                print("Ошибка: Введите целое число для количества факторов.")
                return

            descript_model = QStandardItemModel()

            for col in range(num_factors):
                factor_name = 'Factor{}'.format(col + 1)
                factor_loadings = self.loadings[:, col]
                variable_names = [self.df.columns[row] for row, loading in enumerate(factor_loadings) if loading > 0.5]

                # Создание заголовка столбца - название фактора
                descript_model.setHorizontalHeaderItem(col, QStandardItem(factor_name))

                # Добавление значений столбца - имена переменных
                for row, variable_name in enumerate(variable_names):
                    descript_model.setItem(row, col, QStandardItem(variable_name))

            # Установка модели в таблицу DescriptTable
            self.ui.DescriptTable.setModel(descript_model)

        except Exception as e:
            print(f"Ошибка: {e}")

class NewValuesTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(round(self._data[index.row()][index.column()], 3))
        return None

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._data.columns[section]
            if orientation == Qt.Vertical:
                return self._data.index[section]
        return None


if __name__ == "__main__":
    app = QApplication([])
    window = FactorApp()
    window.show()
    app.exec()
