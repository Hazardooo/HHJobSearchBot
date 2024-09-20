from telebot import TeleBot
from telebot import types
from vacancy_parser import Parser


class Bot:
    
    def __init__(self, token):
        self.bot = TeleBot(token=token)
        self.current_index = 0
        self.job_list = None
        self.job_filter = None

        @self.bot.message_handler(commands=["start"])
        def welcome(message):
            self.bot.send_message(
                message.chat.id,
                f"{message.from_user.first_name}!\nПривет. Я бот по поиску работы",
                reply_markup=self.keyboard_start_search_job())

        @self.bot.message_handler(content_types=["text"])
        def vacancy(message):
            user_id = message.chat.id
            match message.text.lower():
                case "поиск работы":
                    self.generate_job_list()
                    self.bot.send_message(user_id, 'Предлогаемые вакансии:',reply_markup=self.keyboard_next_and_back())
                    self.bot.send_message(user_id, self.get_job())
                case "далее":
                    self.check_job_list()
                    self.del_previous_message(message)
                    self.bot.send_message(user_id,self.get_job())
                    self.current_index += 1
                case "назад":
                    self.check_job_list()
                    self.del_previous_message(message)
                    self.bot.send_message(user_id,self.get_job())
                    self.current_index = self.current_index - 1 if self.current_index > 0 else 0
                case _:
                    self.bot.send_message(user_id, 'Я не знаю таких команд!',reply_markup=self.keyboard_start_search_job())

    def start(self):
        """Функция для запуска бота."""
        self.bot.polling(none_stop=True)

    def keyboard_start_search_job(self):
        """Кнопочка для запуска поиска работы."""
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False,
                                           resize_keyboard=True)
        search_job = types.KeyboardButton('Поиск работы')
        markup.add(search_job)
        return markup

    def keyboard_next_and_back(self):
        """Кнопочки для листания страниц."""
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False,
                                           resize_keyboard=True)
        bck = types.KeyboardButton('Назад')
        nxt = types.KeyboardButton('Далее')
        markup.add(bck, nxt)
        return markup

    def del_previous_message(self,message):
        """Удаление предыдущих сообщений."""
        self.bot.delete_message(message.chat.id, message.message_id)
        self.bot.delete_message(message.chat.id, message.message_id-1)

    def __rasparse(self, dct: dict):
        out = ''
        for _, v in dct.items():
            out += str(v) + "\n"
        return out

    def check_job_list(self):
        """
        Проверяем список на наличие вакансий.
        Если спсок пуст, то генерируем его.
        """
        if not self.job_list:
           self.generate_job_list()

    def get_job(self):
        """Получаем значение из списка в зависимости от нашей страницы (current_index)."""
        return self.__rasparse(self.job_list[self.current_index])

    def generate_job_list(self):
        """Генерируем список ваканский"""
        if self.current_index == 0:
            self.job_list = Parser('Аналитик').info_to_vac_list() #Генерировать вакансии от ввода пользователя

