import unittest
from handler import Handler
from state_machine import StateMachine


class TestHandler(unittest.TestCase):
    def setUp(self):
        self.handler = Handler()
        self.chat_id = '12345'
        self.handler.get_or_create_state(self.chat_id)
        self.storage = self.handler.storage

    def test_start(self):
        self.storage[self.chat_id]['state'] = StateMachine('start_state')
        self.assertEqual(
            self.handler.get_response(self.chat_id, '/start'),
            'Какую вы хотите пиццу? Большую или маленькую?'
        )

    def test_wrong_food_size(self):
        self.storage[self.chat_id]['state'] = StateMachine('food_size')
        self.assertEqual(
            self.handler.get_response(self.chat_id, 'Какое-то сообщение'),
            'Введите размер: большую или маленькую.'
        )

    def test_correct_food_size(self):
        self.storage[self.chat_id]['state'] = StateMachine('food_size')
        self.assertEqual(
            self.handler.get_response(self.chat_id, 'Маленькую'),
            'Как будете оплачивать? Наличкой или безналичкой?'
        )

    def test_wrong_payment_form(self):
        self.storage[self.chat_id]['state'] = StateMachine('payment_form')
        self.assertEqual(
            self.handler.get_response(self.chat_id, 'Какое то сообщение'),
            'Введите способ оплаты: наличкой или безналичкой.'
        )

    def test_correct_payment_form(self):
        self.storage[self.chat_id]['state'] = StateMachine('payment_form')
        self.storage[self.chat_id]['size'] = 'маленькую'
        self.storage[self.chat_id]['payment'] = 'безналичкой'
        self.assertEqual(
            self.handler.get_response(self.chat_id, 'безналичкой'),
            f"Вы хотите {self.storage[self.chat_id]['size']} пиццу, оплата {self.storage[self.chat_id]['payment']}?",
        )

    def test_wrong_checking(self):
        self.storage[self.chat_id]['state'] = StateMachine('checking')
        self.assertEqual(
            self.handler.get_response(self.chat_id, 'не знаю'),
            'Ответьте: Да или Нет.'
        )

    def test_negative_checking(self):
        self.storage[self.chat_id]['state'] = StateMachine('checking')
        self.assertEqual(
            self.handler.get_response(self.chat_id, 'нет'),
            'Начните заказ по новой с команды /start.'
        )

    def test_positive_checking(self):
        self.storage[self.chat_id]['state'] = StateMachine('checking')
        self.assertEqual(
            self.handler.get_response(self.chat_id, 'да'),
            'Спасибо за заказ.'
        )

    def test_reset(self):
        self.assertEqual(
            self.handler.get_response(self.chat_id, '/reset'),
            'Начните заказ по новой с команды /start.'
        )

    def test_default_answer(self):
        self.storage[self.chat_id]['state'] = StateMachine('start_state')
        self.assertEqual(
            self.handler.get_response(self.chat_id, 'Привет!'),
            'Сделайте заказ с помощью команды /start.'
        )


if __name__ == "__main__":
    unittest.main()