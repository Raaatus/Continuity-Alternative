from flask import Flask, request, jsonify

import signal
from datetime import datetime
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

import threading
import time
import notification  # Importer le module de notification

# Démarrer le thread de notification
notification_thread = threading.Thread(target=notification.start_notification_thread, daemon=True)
notification_thread.start()

# Fonction pour mettre à jour la notification depuis le script principal
def update_notification(title, message, img):
    notification.update_notification(title, message, img)

# Exemple d'utilisation
update_notification("Démarrage", "Ca démarre", "wait.png")

time.sleep(2)
update_notification("OK", "Projet démarré.", "ready.png")







def checker(data):
    try:
        # Accéder aux champs spécifiques du JSON
        name = data.get('packageName')
        Texte = data.get('tickerText')
        Titre= data.get('Titre')
        #Time = data.get('timestamp')
        #print(name)
        file_path = os.path.join(script_dir, 'modules', 'modules.txt')

        if name and os.path.isfile(file_path) and Texte and Titre :
            with open(file_path, 'r') as file:
                packages = file.read().splitlines()

            if name in packages:
                update_notification(Titre, Texte, name+".png")

        

    except Exception as e:
        print(f"Error processing notification: {e}")





app = Flask(__name__)

@app.route('/notification', methods=['POST'])
def notification_process():
    data = request.json
    checker(data)
    print(data)
    return jsonify({"status": "success"}), 200

@app.route('/', methods=['GET'])
def checkonline():
    print(f"Test check serveur ONLINE")
    return jsonify({"status": "success"}), 200

@app.route('/close', methods=['GET'])
def exit_this():
    print(f"Closing the server...")
    os.kill(os.getpid(), signal.SIGTERM)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



