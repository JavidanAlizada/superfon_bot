from qrcode import QRCode, constants
from telebot import TeleBot

from bot.credentials import bot_token


class State:
    state = {}
    user = None

    def __init__(self):
        pass

    def set_user(self, username):
        self.user = username
        try:
            self.state[username] = self.state[username]
        except:
            self.state[username] = {}

    def get_all_state(self):
        return self.state

    def get_state(self):
        try:
            return self.state[self.user]
        except Exception as e:
            return None

    def add(self, key, value):
        self.state[self.user][key] = value


class QRCodeGenerate:
    def __init__(self, content, version=1, error_correction=constants.ERROR_CORRECT_L,
                 box_size=50, border=6):
        self.qrcode = QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        self.qrcode.add_data(content)
        self.qrcode.make(fit=True)

    def get_image(self):
        return self.qrcode.make_image(fill_color="black", back_color="white")


bot = TeleBot(bot_token)
state = State()


@bot.message_handler(commands=['start', 'help'])
def start_or_help(message):
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name} {message.from_user.last_name}")
    # state.set_user(message.from_user.username)
    # state.add()


@bot.message_handler(commands=['step1'])
def step1(message):
    user_input_data = message.text.replace("/step1", "")
    if not user_input_data:
        return bot.send_message(message.chat.id, "Usage: /step1 your data")

    state.set_user(message.from_user.username)
    state.add("step1", user_input_data)
    bot.send_message(message.chat.id, f"Your data saved to cache")


#
# @bot.message_handler(commands=['step2'])
# def step2(message):
#     bot.send_message(message.chat.id, "Step 2")


@bot.message_handler(commands=['end'])
def end(message):
    state.set_user(message.from_user.username)
    qrcode = QRCodeGenerate(state.get_state())
    image = qrcode.get_image()

    bot.send_photo(message.chat.id, image.get_image(), caption="Data saved to db")


bot.polling(none_stop=True)
