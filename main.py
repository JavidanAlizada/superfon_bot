import json

from qrcode import QRCode, constants
from telebot import TeleBot

from bot.credentials import bot_token
from bot.request import Request
from bot.virtual_card import VirtualCard

request = Request()


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
                 box_size=4, border=0):
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


def __get_msg():
    return json.load(open("bot/messages.json"))


@bot.message_handler(commands=['start', 'help'])
def start_or_help(message):
    msg_data = __get_msg()['start_message']
    bot.send_message(message.chat.id, f"{msg_data}")


@bot.message_handler(regexp=r"(A)(ZE\d|A)(\d{7})$")
def by_serial_number(message):
    data = message.text
    msg_data = __get_msg()['waiting_message']
    resp = request.get_user_data_by_serial_num(data)
    bot.send_message(message.chat.id, f"{msg_data}")
    body = resp['body']
    if body:
        state.set_user(message.from_user.username)
        if body['status'] == '0' or body['status'] == 0:
            qrcode = QRCodeGenerate(body['qrCodeContent'])
            image = qrcode.get_image()
            resp_update = request.update_query_status(serialNumber=body['serialNumber'],
                                                      status=1)
            if resp_update['body']['status']:
                card = VirtualCard(name=body['fullName'], password=body['password'], qr_code=image)
                image = card.generate_virtual_card()
                bot.send_photo(message.chat.id, image, caption="")
                msg_data = __get_msg()['password']
                password = body['password']
                bot.send_message(message.chat.id, f"{msg_data}{password}")
        else:
            msg_data = __get_msg()['password_exists']
            bot.send_message(message.chat.id, f"{msg_data}")
    else:
        msg_data = __get_msg()['error_message_serial_num']
        bot.send_message(message.chat.id,
                         f" {msg_data} ")


@bot.message_handler(regexp=r"^[0-9]{1}[a-z]{1}[0-9]{1}[a-z]{1}[0-9]{1}[a-z]{1}$")
def by_password(message):
    data = message.text
    msg_data = __get_msg()['waiting_message']
    resp = request.get_user_data_by_password(data)
    bot.send_message(message.chat.id, f"{msg_data}")
    body = resp['body']
    if body:
        state.set_user(message.from_user.username)
        qrcode = QRCodeGenerate(body['qrCodeContent'])
        image = qrcode.get_image()
        card = VirtualCard(name=body['fullName'], password=body['password'], qr_code=image)
        image = card.generate_virtual_card()
        bot.send_photo(message.chat.id, image, caption="")
    else:
        msg_data = __get_msg()['error_message_password']
        bot.send_message(message.chat.id,
                         f" {msg_data} ")


bot.polling(none_stop=True)
