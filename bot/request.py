import requests
import json


class Request:

    def __init__(self):
        pass

    def get_user_data_by_serial_num(self, serial_num):
        data = requests.get(f"http://127.0.0.1:8080/api/v1/customer/bySerialNumber?serialNumber={serial_num}")
        return json.loads(data.content)

    def get_all_users(self):
        data = requests.get(f"http://127.0.0.1:8080/api/v1/customer/all")
        return json.loads(data.content)
