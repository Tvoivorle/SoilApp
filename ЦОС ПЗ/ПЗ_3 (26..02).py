import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Загрузка данных
data = pd.read_csv('soil_data_usa.csv')

# Предварительная обработка данных (удаление пропущенных значений, стандартизация, и т.д.)

# Выбор признаков для анализа (необходимо удалить идентификаторы и целевые переменные)
X = data.drop(['ID', 'Soil_Type'], axis=1)

# Стандартизация данных
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Применение кластерного анализа
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_scaled)
clusters = kmeans.predict(X_scaled)

# Визуализация результатов (например, с использованием графика парных признаков)
plt.scatter(X['Feature1'], X['Feature2'], c=clusters, cmap='viridis')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Clustering of Soil Samples')
plt.show()
