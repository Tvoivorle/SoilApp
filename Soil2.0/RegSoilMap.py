import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def load_data():
    """Загружает таблицу с факторными оценками."""
    try:
        data = pd.read_excel(
            r'C:/Users/Stepan/PycharmProjects/Soils/Soil2.0/TestFactMap.xlsx',
            engine='openpyxl'
        )

        # Преобразование координат
        data['LAT'] = data['LAT'].astype(str).str.replace(',', '.').astype(float)
        data['LONG'] = data['LONG'].astype(str).str.replace(',', '.').astype(float)

        return data

    except Exception as e:
        st.error(f"Ошибка загрузки данных: {str(e)}")
        return None


def plot_factors_map(filtered_data, selected_factors, mode):
    """Строит карту с факторными оценками"""
    fig = go.Figure()

    if mode == "Сила выбранных факторов":
        for factor in selected_factors:
            fig.add_trace(go.Scattermapbox(
                lat=filtered_data["LAT"],
                lon=filtered_data["LONG"],
                mode="markers",
                marker=dict(
                    size=8,
                    color=filtered_data[factor],
                    colorscale="viridis",
                    showscale=True,
                    colorbar=dict(title=factor)
                ),
                text=filtered_data["RUREG"],
                name=factor
            ))

    elif mode == "Сильнейший фактор":
        # Определяем сильнейший фактор в каждой строке
        factor_columns = [col for col in filtered_data.columns if "Фактор" in col]
        filtered_data["Max Factor"] = filtered_data[factor_columns].abs().idxmax(axis=1)
        filtered_data["Max Value"] = filtered_data[factor_columns].max(axis=1)

        # Уникальные цвета для каждого фактора
        factor_colors = {factor: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                         for i, factor in enumerate(factor_columns)}

        for factor, color in factor_colors.items():
            subset = filtered_data[filtered_data["Max Factor"] == factor]
            fig.add_trace(go.Scattermapbox(
                lat=subset["LAT"],
                lon=subset["LONG"],
                mode="markers",
                marker=dict(
                    size=8,
                    color=color,
                    showscale=False
                ),
                text=subset["RUREG"] + f" ({factor})",
                name=factor
            ))

    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            zoom=5,
            center=dict(lat=filtered_data["LAT"].mean(), lon=filtered_data["LONG"].mean())
        ),
        margin=dict(r=0, t=0, l=0, b=0)
    )

    return fig


def main():
    st.title("🌍 Визуализация факторных оценок по разрезам")

    data = load_data()
    if data is None:
        return

    # 🎯 **Фильтры**
    col1, col2 = st.columns(2)

    with col1:
        selected_regions = st.multiselect("Выберите регионы", data["RUREG"].unique(), default=data["RUREG"].unique())

    with col2:
        selected_horizon = st.selectbox("Выберите HORNMB", data["HORNMB"].unique())

    # 🔍 **Фильтруем данные**
    filtered_data = data[
        (data["RUREG"].isin(selected_regions)) &
        (data["HORNMB"] == selected_horizon)
    ]

    if filtered_data.empty:
        st.warning("Нет данных для выбранных фильтров.")
        return

    # 🎛️ **Выбор режима отображения**
    mode = st.radio("Выберите режим отображения:", ["Сила выбранных факторов", "Сильнейший фактор"])

    # 🎛️ **Выбор факторов**
    factor_columns = [col for col in data.columns if "Фактор" in col]
    selected_factors = st.multiselect("Выберите факторы для отображения", factor_columns, default=[factor_columns[0]])

    # 🌍 **Построение карты**
    st.markdown("### Карта с факторными оценками")
    fig = plot_factors_map(filtered_data, selected_factors, mode)
    st.plotly_chart(fig, use_container_width=True)

    # 📊 **Вывод таблицы**
    st.markdown("### Таблица факторных оценок")
    st.dataframe(filtered_data[["RUREG", "HORNMB"] + selected_factors])


if __name__ == "__main__":
    main()
