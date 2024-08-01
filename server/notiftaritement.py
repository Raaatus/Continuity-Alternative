import json
from datetime import datetime
import os
import notification
script_dir = os.path.dirname(os.path.abspath(__file__))


# Fonction pour mettre à jour la notification depuis le script principal
def update_notification(title, message):
    notification.update_notification(title, message)


def checker(data):
    try:
        # Accéder aux champs spécifiques du JSON
        name = data.get('packageName')
        Texte = data.get('tickerText')
        #Time = data.get('timestamp')

        file_path = os.path.join(script_dir, 'modules', 'modules.txt')

        if name and os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                packages = file.read().splitlines()

            if name in packages:
                update_notification(name, Texte)

        

    except Exception as e:
        print(f"Error processing notification: {e}")
        