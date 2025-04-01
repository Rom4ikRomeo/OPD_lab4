from flask import Flask, render_template, request # Flask – основной фреймворк, render_template – для отображения HTML-страницы, request – для работы с пользовательским вводом.
import requests # requests – для отправки HTTP-запросов

app = Flask(__name__) # создает объект app, который будет управлять сервером.

API_URL = "https://api.exchangerate-api.com/v4/latest/" # Указываем URL API

# Создаем маршрут для главной страницы
@app.route('/', methods=['GET', 'POST']) # указывает, что эта функция отвечает за http://127.0.0.1:5000/, methods – позволяет принимать как GET, так и POST
def index():
    result = None # result будет хранить сумму после конвертации.
    error = None # error будет содержать текст ошибки, если что-то пошло не так.

    if request.method == 'POST': # Проверяем, отправлена ли форма
        base_currency = request.form.get('base_currency').upper() # получаем валюту, из которой конвертируем.
        target_currency = request.form.get('target_currency').upper() # получаем валюту, в которую конвертируем.
        amount = request.form.get('amount') # получаем сумму, введенную пользователем.

        try:
            amount = float(amount) # переводим введенное значение из строки в число с плавающей точкой.
            response = requests.get(API_URL + base_currency) # отправляем HTTP-запрос на нужную валюту
            data = response.json() # превращаем ответ API в словарь (dict), который можно обрабатывать.

            if "rates" in data and target_currency in data["rates"]: # проверяет, вернулись ли курсы валют и проверяет, есть ли в ответе нужная валюта.
                rate = data["rates"][target_currency] # получаем курс.
                result = round(amount * rate, 2) # умножаем сумму на курс и округляем до 2 знаков.
            else:
                error = "Неверная валюта. Попробуйте снова." # Если введена неправильная валюта, выводим сообщение.
        except Exception as e:
            error = "Ошибка получения данных. Проверьте введенные данные." # Если API не работает или пользователь ввел не число – показываем сообщение.

    return render_template("index.html", result=result, error=error) # Передаем result и error


if __name__ == '__main__':
    app.run(debug=True)