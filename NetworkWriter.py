import requests
from IWriter import IWriter


class NetworkWriter(IWriter):


    def send_data(self, data,name_machine):
        """Envoie les données au serveur via une requête POST"""
        try:
            response = requests.post(name_machine, json={"data": data})
            if response.status_code == 200:
                print("sent with success!")
            else:
                print(f"error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"fail to connect: {e}")