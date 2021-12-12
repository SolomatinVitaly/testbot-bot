from state_machine import StateMachine


class Handler:


    def __init__(self):
        self.storage = {}


    def get_or_create_state(self, chat_id):
        try:
            return self.storage[chat_id]['state'].state
        except KeyError:
            self.storage.update({
                chat_id: {
                    'state': StateMachine(),
                    'size': None,
                    'payment': None,
                }
            })
            return self.storage[chat_id]['state'].state


    def get_response(self, chat_id, message):
        text = message.lower()
        if self.get_or_create_state(chat_id) == 'start_state' and text == '/start':
            self.storage[chat_id]['state'].next_state()
            return 'Какую вы хотите пиццу? Большую или маленькую?'

        elif text == '/reset':
            self.storage[chat_id]['state'].cancel()
            return 'Начните заказ по новой с команды /start.'

        elif self.get_or_create_state(chat_id) == 'food_size':
            if text in ['большую', 'маленькую']:
                self.storage[chat_id]['size'] = text
                self.storage[chat_id]['state'].next_state()
                return 'Как будете оплачивать? Наличкой или безналичкой?'
            else:
                return 'Введите размер: большую или маленькую.'

        elif self.get_or_create_state(chat_id) == 'payment_form':
            if text in ['наличкой', 'безналичкой']:
                self.storage[chat_id]['payment'] = text
                self.storage[chat_id]['state'].next_state()
                return f"Вы хотите {self.storage[chat_id]['size']} пиццу, оплата {self.storage[chat_id]['payment']}?"
            else:
                return 'Введите способ оплаты: наличкой или безналичкой.'

        elif self.get_or_create_state(chat_id) == 'checking':
            if text == 'да':
                self.storage[chat_id]['state'].next_state()
                return 'Спасибо за заказ.'
            elif text == 'нет':
                self.storage[chat_id]['state'].cancel()
                return 'Начните заказ по новой с команды /start.'
            else:
                return 'Ответьте: Да или Нет.'

        return 'Сделайте заказ с помощью команды /start.'