import requests
import pandas as pd

# Укажите ваш API-ключ Chad GPT
CHAD_API_KEY = 'chad-89e316e81eef48f38165b412f6befbc8vclzho9t'

# Читаем листы из файла
variables_df = pd.read_excel(file_path, sheet_name="Переменные")
communalities_df = pd.read_excel(file_path, sheet_name="Общности")

# Создаем словарь с описаниями переменных для быстрого поиска
description_dict = dict(zip(communalities_df['Переменные'], communalities_df['Описание переменной']))

# Создаем список запросов для факторов
factor_prompts = []
for index, row in variables_df.iterrows():
    factor = row['Фактор']
    variables = row['Переменные'].split(', ')  # Предполагаем, что переменные разделены запятыми
    descriptions = []

    # Получаем описание для каждой переменной
    for variable in variables:
        description = description_dict.get(variable, "Описание не найдено")
        descriptions.append(f"{variable}: {description}")

    # Формируем запрос с добавлением описаний переменных
    prompt = (f"Ты ученый почвовед. Придумай краткое и логичное название для фактора, "
              f"содержащего переменные: {', '.join(variables)}. Описание переменных:\n"
              f"{'\n'.join(descriptions)}.\nТебе необходимо коротко, без лишнего текста и пояснения дать в кавычках название для фактора")
    factor_prompts.append({"factor": factor, "prompt": prompt})

# Отправляем запросы к API и сохраняем ответы
factor_responses = []  # Для нового столбца "Ответ"

for item in factor_prompts:
    request_json = {
        "message": item["prompt"],
        "api_key": CHAD_API_KEY
    }

    # Логируем запрос
    print(f"Запрос: {item['prompt']}")

    # Отправляем запрос к Chad GPT API
    response = requests.post(url='https://ask.chadgpt.ru/api/public/gpt-4o-mini', json=request_json)

    # Проверяем успешность запроса
    if response.status_code == 200:
        resp_json = response.json()

        if resp_json['is_success']:
            factor_name = resp_json['response'].strip()
            factor_responses.append(factor_name)
            print(f"Ответ: {factor_name}")
        else:
            error_message = resp_json.get('error_message', 'Неизвестная ошибка')
            print(f"Ошибка: {error_message}")
            factor_responses.append("Ошибка API")
    else:
        print(f"Ошибка! Код http-ответа: {response.status_code}")
        factor_responses.append("Ошибка подключения")

# Добавляем новый столбец "Ответ" в DataFrame
variables_df['Ответ'] = factor_responses

# Сохраняем файл с добавленным столбцом
output_file_path = "factor_analysis_results.xlsx"
with pd.ExcelWriter(output_file_path) as writer:
    variables_df.to_excel(writer, sheet_name="Переменные", index=False)

    # Копируем другие листы из исходного файла
    original_data = pd.read_excel(file_path, sheet_name=None)
    for sheet_name, data in original_data.items():
        if sheet_name != "Переменные":
            data.to_excel(writer, sheet_name=sheet_name)

print(f"Файл с обновленными результатами сохранен: {output_file_path}")
