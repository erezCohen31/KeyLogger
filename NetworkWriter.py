import requests
import json
from IWriter import IWriter


class NetworkWriter(IWriter):

    def send_data(self, data, name_machine):
        try:
            response = requests.post(name_machine, json=data)  # Envoi direct du JSON

            if response.status_code == 200:
                print("sent with success !")
            else:
                print(f"error : {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"fail to connect : {e}")


# Tester l'envoi
writer = NetworkWriter()
json_data = {"nom": "Alice", "age": 25, "ville": "Lyon"}
writer.send_data(json_data, "http://127.0.0.1:5000/upload")