import requests
from IWriter import IWriter


class NetworkWriter(IWriter):

    def send_data(self, data, name_machine):
        print(type(data))
        try:
            if isinstance(data, dict):
                response = requests.post(name_machine, json=data)
                if response.status_code == 200:
                    print("Sent with success!")
                else:
                    print(f"Error: {response.status_code} - {response.text}")
            else:
                print("Data is not a valid dictionary!")
                print(type(data))

        except requests.exceptions.RequestException as e:
            print(f"Failed to connect: {e}")
