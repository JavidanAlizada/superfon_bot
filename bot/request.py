import requests
import json

from bot.credentials import endpoint_url


class Request:

    def __init__(self):
        pass

    def get_user_data_by_serial_num(self, serial_num):
        data = requests.get(f"{endpoint_url}/customer/bySerialNumber?serialNumber={serial_num}")
        return json.loads(data.content)

    def get_user_data_by_password(self, password):
        data = requests.get(f"{endpoint_url}/customer/byPassword?password={password}")
        return json.loads(data.content)

    def get_all_users(self):
        data = requests.get(f"{endpoint_url}/customer/all")
        return json.loads(data.content)

    def update_query_status(self, serialNumber, status):
        headers = {"Content-Type": "application/json", "charset": "UTF-8"}
        url = f"{endpoint_url}/customer/status/{serialNumber}/"
        data = requests.patch(url, json=status, headers=headers)
        return json.loads(data.content)

    def save_qr_code_content(self, serialNumber, qrCode):
        headers = {"Content-Type": "application/json", "charset": "UTF-8"}
        url = f"{endpoint_url}/customer/updateQrCode/{serialNumber}/"
        data = requests.patch(url, json=qrCode, headers=headers)

        return json.loads(data.content)

