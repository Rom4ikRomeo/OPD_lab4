import unittest
from convertor import app


class TestCurrencyConverter(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client() # создаёт тестовый клиент Flask, который позволяет отправлять запросы без запуска реального сервера
        self.app.testing = True # включает тестовый режим

    def test_homepage_loads(self):
        #Проверяем, что главная страница загружается
        response = self.app.get('/') # Отправляем GET-запрос на /
        self.assertEqual(response.status_code, 200) # Проверяем, что сервер отвечает

    def test_valid_conversion(self):
        #Проверяем, что при правильных данных получаем корректный результат
        response = self.app.post('/', data={ # Отправляем POST-запрос на / с корректными данными
            'base_currency': 'USD',
            'target_currency': 'EUR',
            'amount': '100'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Результат:'.encode('utf-8'), response.data) # Проверяем, что в ответе есть фраза "Результат:"

    def test_invalid_currency(self):
        #Проверяем обработку некорректной валюты
        response = self.app.post('/', data={ # Отправляем запрос с несуществующими валютами
            'base_currency': 'XXX',
            'target_currency': 'YYY',
            'amount': '100'
        })
        self.assertEqual(response.status_code, 200) # Проверяем, что сервер не упал, а обработал ошибку корректно
        self.assertIn('Неверная валюта'.encode('utf-8'), response.data) # Проверяем, что в ответе есть текст "Неверная валюта"

    def test_invalid_amount(self):
        #Проверяем обработку некорректного числа
        response = self.app.post('/', data={
            'base_currency': 'USD',
            'target_currency': 'EUR',
            'amount': 'abc'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ошибка получения данных'.encode('utf-8'), response.data)


if __name__ == '__main__':
    unittest.main()