from abc import ABC, abstractmethod
from typing import List
class IWriter(ABC):
    @abstractmethod
    def send_data(self,data:str,machine_name_str):
        pass