# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt, QAbstractTableModel, QSize
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QTableView, QVBoxLayout, QGraphicsScene, QMessageBox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from SoilAPP import Ui_MainWindow
from Info import Ui_Dialog
import pandas as pd

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isExpanded = False  # Состояние окна (расширено/не расширено)
        self.originalSize = self.size()  # Исходный размер окна
        self.expandedSize = QSize(self.width() + 200, self.height())  # Размер расширенного окна
        self.setupUi(self)
        self.DF_choice.clicked.connect(self.load_dataset)
        self.Elbow_BTM.clicked.connect(self.elbow)
        self.Elbow_BTM_2.clicked.connect(self.plot_scatter)
        self.scene = QGraphicsScene()  # Создаем сцену
        self.scene2 = QGraphicsScene()  # Создаем сцену
        self.Clasterization.clicked.connect(self.clusterization)
        self.Clas_Stat.clicked.connect(self.show_cluster_statistics)
        self.Factor_info.clicked.connect(self.showInfoDialog)
        self.dialog = None
        self.Save_btm.clicked.connect(self.save_to_excel)

    def load_dataset(self):
        # Открываем диалоговое окно для выбора файла
        filepath, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Excel Files (*.xlsx)")

        # Загружаем датасет из выбранного файла
        if filepath:
            self.df = pd.read_excel(filepath)
            # Отображаем датасет в tableView
            self.show_dataframe_in_tableview()

    def show_dataframe_in_tableview(self):
        # Создаем модель данных
        model = QStandardItemModel(self.df.shape[0], self.df.shape[1])

        # Заполняем модель данными из датафрейма
        for row in range(self.df.shape[0]):
            for column in range(self.df.shape[1]):
                item = QStandardItem()
                # Форматирование чисел с тремя знаками после запятой
                item.setData('{:.3f}'.format(self.df.iat[row, column]), Qt.DisplayRole)
                model.setItem(row, column, item)

        # Устанавливаем заголовки для столбцов
        model.setHorizontalHeaderLabels(self.df.columns)

        # Устанавливаем модель для tableView
        self.tableView.setModel(model)

    def show_description(self):
        # Открываем диалоговое окно для выбора файла
        filepath = "../description.xlsx"
        # Загружаем описание из выбранного файла
        if filepath:
            description_df = pd.read_excel(filepath)
            # Отображаем описание в текстовом поле или другом виде
            # Например, если вы хотите использовать диалоговое окно для отображения описания:
            dialog = DescriptionDialog(description_df)
            dialog.exec_()

    def plot_scatter(self):
        # Получаем имена переменных из Factor1_INPUT и Factor2_INPUT
        factor1_name = self.Factor1_INPUT.text()
        factor2_name = self.Factor2_INPUT.text()

        # Проверяем, что имена переменных существуют в загруженном датасете
        if factor1_name in self.df.columns and factor2_name in self.df.columns:
            # Получаем данные по именам переменных из загруженного датасета
            factor1_data = self.df[factor1_name]
            factor2_data = self.df[factor2_name]

            # Создаем новый график рассеивания
            fig, ax = plt.subplots()
            ax.scatter(factor1_data, factor2_data)
            ax.set_xlabel(factor1_name)
            ax.set_ylabel(factor2_name)
            ax.set_title('Scatter Plot')

            # Создаем холст Matplotlib
            canvas = FigureCanvas(fig)

            # Очищаем сцену для отображения нового графика
            self.scene.clear()

            # Добавляем холст на QGraphicsView
            self.graphicsView.setScene(self.scene)
            self.scene.addWidget(canvas)

            # Устанавливаем размеры холста равными размерам QGraphicsView
            canvas.setGeometry(0, 0, self.graphicsView.width(), self.graphicsView.height())

            # Обновляем холст для отображения графика
            canvas.draw()
        else:
            # Выводим сообщение об ошибке, если имена переменных не найдены в датасете
            QMessageBox.warning(self, "Warning", "One or both factor names not found in the dataset.")

    def elbow(self):
        # Получаем данные x для метода локтя
        data_x = self.df.iloc[:, 3:5]
        x_array = np.array(data_x)

        # Нормализация данных
        scaler = MinMaxScaler()
        x_scaled = scaler.fit_transform(x_array)

        # Метод локтя
        Sum_of_squared_distances = []
        K = range(1, 15)
        for k in K:
            km = KMeans(n_clusters=k)
            km.fit(x_scaled)
            Sum_of_squared_distances.append(km.inertia_)

        # Создаем новый график
        fig, ax = plt.subplots()
        ax.plot(K, Sum_of_squared_distances, marker='o', linestyle='-')
        ax.set_title('Elbow Method For Optimal k')
        ax.set_xlabel('Number of clusters')
        ax.set_ylabel('Sum of squared distances')
        ax.grid(True)

        # Создаем холст Matplotlib
        canvas = FigureCanvas(fig)

        # Очищаем сцену
        if self.scene2:
            self.scene2.clear()
        else:
            self.scene2 = QGraphicsScene()

        # Добавляем холст на сцену
        self.scene2.addWidget(canvas)

        # Устанавливаем размеры холста равными размерам виджета
        canvas.setGeometry(0, 0, self.Elbow_graph.width(), self.Elbow_graph.height())

        # Добавляем сцену на Elbow_graph
        self.Elbow_graph.setScene(self.scene2)

        # Обновляем холст
        canvas.draw()

    def clear_scene(self, scene):
        # Удаляем все элементы из сцены
        if scene is not None:
            for item in scene.items():
                scene.removeItem(item)

    def clusterization(self):
        # Читаем количество кластеров, введенное пользователем
        n_clusters = int(self.Elbow_INPUT.text())

        # Выбираем колонки для кластеризации
        x_column = self.Factor1_INPUT.text()
        y_column = self.Factor2_INPUT.text()

        # Подготавливаем данные
        numerics = self.df[[x_column, y_column]].copy()
        scaler = MinMaxScaler()
        for i in numerics.columns:
            numerics[i] = scaler.fit_transform(numerics[[i]])

        # Применяем кластеризацию
        km = KMeans(n_clusters=n_clusters)
        y_predicted = km.fit_predict(numerics)

        # Добавляем результат кластеризации в DataFrame
        self.df["Cluster"] = y_predicted

        # Создаем фигуру для графика
        fig, ax = plt.subplots(figsize=(12, 8))

        # Визуализация результатов кластеризации
        for i in range(n_clusters):
            df_cluster = self.df[self.df.Cluster == i]
            ax.scatter(df_cluster[x_column], df_cluster[y_column], label=f'Cluster {i + 1}')

        ax.set_title('Clustering Result', fontweight='bold', fontsize=20)
        ax.set_xlabel(x_column, fontsize=15)
        ax.set_ylabel(y_column, fontsize=15)
        ax.legend(fontsize=15)
        ax.grid(True)

        # Создаем холст Matplotlib и отображаем его в graphicsView
        canvas = FigureCanvas(fig)
        self.scene = QGraphicsScene()  # Предполагается, что self.scene уже объявлен. Если нет, его нужно инициализировать.
        self.scene.clear()  # Очистка предыдущих графиков
        self.graphicsView.setScene(
            self.scene)  # Предполагается, что graphicsView - это ваш виджет для отображения графиков.
        self.scene.addWidget(canvas)
        # Устанавливаем размеры холста равными размерам QGraphicsView
        canvas.setGeometry(0, 0, self.graphicsView.width(), self.graphicsView.height())
        canvas.draw()

    def show_cluster_statistics(self):
        # Проверяем, есть ли данные для анализа
        if hasattr(self, 'df') and 'Cluster' in self.df.columns:
            # Рассчитываем средние значения и количество элементов в каждом кластере
            res = self.df.groupby('Cluster').mean()
            res['Количество'] = self.df.groupby('Cluster').size().values

            # Отображаем результаты в tableView
            model = PandasModel(res)
            self.tableView.setModel(model)
        else:
            QMessageBox.warning(self, "Warning", "Please perform clustering first.")

    def save_to_excel(self):
        # Проверяем, есть ли данные в модели
        if hasattr(self, 'tableView') and self.tableView.model() is not None:
            # Получаем DataFrame из модели
            model = self.tableView.model()
            df = model._data  # предполагается, что PandasModel хранит данные в _data

            # Записываем DataFrame в файл Excel
            try:
                filepath = QFileDialog.getSaveFileName(self, 'Save File', '', 'Excel files (*.xlsx)')
                if filepath[0]:
                    df.to_excel(filepath[0], index=False)
                    QMessageBox.information(self, "Success", "Data has been saved to Excel successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", "Failed to save data to Excel.\n" + str(e))
        else:
            QMessageBox.warning(self, "Warning", "No data to save.")

    def showInfoDialog(self):
        if self.dialog is None:  # Проверяем, создан ли диалог
            # Создаем экземпляр диалогового окна
            self.dialog = QDialog(self)
            # Создаем экземпляр Ui_Dialog и применяем настройки интерфейса
            dialog_ui = Ui_Dialog()
            dialog_ui.setupUi(self.dialog)
            self.dialog.finished.connect(self.onDialogClosed)  # Соединяем сигнал завершения с обработчиком
        self.dialog.show()  # Показываем диалог в немодальном режиме

    def onDialogClosed(self):
        # Обработчик закрытия диалога. Очищаем ссылку на диалог, чтобы можно было создать его заново
        self.dialog = None

class PandasModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                value = self._data.values[index.row()][index.column()]
                # Округляем значения до трех знаков после запятой
                return '{:.3f}'.format(value)
            # Отображаем заголовки столбцов
            elif role == Qt.TextAlignmentRole:
                return Qt.AlignCenter
            elif role == Qt.DecorationRole:
                return None
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                # Получаем названия столбцов из данных
                return str(self._data.columns[section])
            elif orientation == Qt.Vertical:
                # Нумерация строк начинается с 1
                return str(section + 1)
        return None
class DescriptionDialog(QDialog):
    def __init__(self, description_df):
        super().__init__()
        self.setWindowTitle("Description")
        self.setGeometry(100, 100, 600, 400)

        # Создаем модель данных
        model = QStandardItemModel(description_df.shape[0], description_df.shape[1])

        # Заполняем модель данными из датафрейма
        for row in range(description_df.shape[0]):
            for column in range(description_df.shape[1]):
                item = QStandardItem()
                item.setData(str(description_df.iloc[row, column]), Qt.DisplayRole)
                model.setItem(row, column, item)

        # Создаем и отображаем таблицу в диалоговом окне
        self.tableView = QTableView()
        self.tableView.setModel(model)

        layout = QVBoxLayout()
        layout.addWidget(self.tableView)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()
