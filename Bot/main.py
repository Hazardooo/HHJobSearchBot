from core import Bot
from config import ReadConfig

if __name__ == '__main__':
    config = ReadConfig()
    config.read_config()
    token = config.get_token()
    bot = Bot(token)
    bot.start()