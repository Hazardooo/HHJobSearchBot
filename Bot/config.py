from os import listdir


class ReadConfig:
    """Класс чтобы считывать токен с config.txt"""
    def __init__(self):
        self.TOKEN = None

    def create_config(self):
        with open("config.txt", "w", encoding="UTF-8") as config:
            config.write(f"Specify your Bot Token here.\n\nToken: ")

    def read_config(self):
        if self.check_exist_config():
            with open("config.txt", "r", encoding="UTF-8") as config:
                self.token = config.readlines()[-1].split()[-1]
        else:
            self.create_config()

    def check_exist_config(self):
        return "config.txt" in listdir()

    def get_token(self):
        return self.token