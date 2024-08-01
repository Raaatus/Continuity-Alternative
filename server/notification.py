import os, signal
import json
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread, Event
from queue import Queue, Empty

# Obtenir le répertoire contenant le script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construire le chemin complet vers le fichier de position
position_file = os.path.join(script_dir, "config", "notification_position.json")
images_dir = os.path.join(script_dir, "images")  # Dossier contenant les images

def ensure_config_directory():
    """Créer le répertoire config si nécessaire."""
    if not os.path.exists(os.path.dirname(position_file)):
        os.makedirs(os.path.dirname(position_file))

def load_position():
    """Charger la position sauvegardée depuis un fichier."""
    if os.path.exists(position_file):
        with open(position_file, "r") as file:
            return json.load(file)
    return {"x": 0, "y": 0}

def save_position(x, y):
    """Sauvegarder la position actuelle dans un fichier."""
    with open(position_file, "w") as file:
        json.dump({"x": x, "y": y}, file)

# File d'attente pour les mises à jour de notification
notification_queue = Queue()
stop_event = Event()

def show_notification(screen=2):
    # Créer la fenêtre principale
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale

    # Charger la position sauvegardée
    pos = load_position()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Positionner sur l'écran secondaire si nécessaire
    screen_x_offset = screen_width if screen == 2 else 0

    # Créer une fenêtre de notification
    notification_window = tk.Toplevel(root)
    notification_window.title("Notification")
    notification_window.geometry(f"400x150+{screen_x_offset + pos['x']}+{pos['y']}")
    notification_window.attributes("-topmost", True)
    notification_window.overrideredirect(True)

    # Créer un cadre pour le label et l'image
    frame = tk.Frame(notification_window)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Charger une image par défaut
    image_label = tk.Label(frame)
    image_label.pack(side=tk.LEFT, padx=10)

    # Ajouter le titre
    label_title = tk.Label(frame, text="", font=("Arial", 12, "bold"), fg="gray")
    label_title.pack(padx=10, pady=5)

    # Ajouter le message
    label_message = tk.Label(frame, text="", font=("Arial", 10), fg="black", wraplength=250)
    label_message.pack(padx=10, pady=5)

    def load_image(image_name):
        """Charger une image depuis le dossier images."""
        image_path = os.path.join(images_dir, image_name)
        if os.path.isfile(image_path):
            image = Image.open(image_path)
            image = image.resize((40, 40), Image.LANCZOS)  # Redimensionner l'image
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo  # Conserver une référence à l'image
        else:
            image_label.config(image='')  # Effacer l'image si le fichier n'existe pas

    # Initialiser l'opacité basse
    notification_window.attributes("-alpha", 0.1)  # Opacité initiale

    def close_window():
        # Sauvegarder la position avant de fermer
        x = notification_window.winfo_x()
        y = notification_window.winfo_y()
        save_position(x - screen_x_offset, y)
        notification_window.destroy()
        os.kill(os.getpid(), signal.SIGTERM)
        root.quit()  # Quitter la boucle principale

    def show_menu(event):
        menu.post(event.x_root, event.y_root)

    menu = tk.Menu(notification_window, tearoff=0)
    menu.add_command(label="Fermer", command=close_window)
    notification_window.bind("<Button-3>", show_menu)

    # Fonction pour déplacer la fenêtre
    def start_move(event):
        notification_window.x = event.x
        notification_window.y = event.y

    def stop_move(event):
        notification_window.x = None
        notification_window.y = None

    def on_motion(event):
        if notification_window.x is not None and notification_window.y is not None:
            x = notification_window.winfo_x() + (event.x - notification_window.x)
            y = notification_window.winfo_y() + (event.y - notification_window.y)
            notification_window.geometry(f"+{x}+{y}")

    notification_window.bind("<Button-1>", start_move)
    notification_window.bind("<ButtonRelease-1>", stop_move)
    notification_window.bind("<B1-Motion>", on_motion)

    # Mettre à jour le message et le titre en fonction des valeurs de la file d'attente
    def update_notification():
        while not stop_event.is_set():
            try:
                title, message, image_name = notification_queue.get(timeout=1)
                notification_window.title(title)
                label_title.config(text=title)
                label_message.config(text=message)
                load_image(image_name)  # Charger et afficher l'image
                notification_window.attributes("-alpha", 1.0)  # Rendre opaque lors de la mise à jour
                root.after(10000, lambda: notification_window.attributes("-alpha", 0.1))  # Réduire l'opacité après 10 secondes
            except Empty:
                pass

    # Lancer le thread de mise à jour
    update_thread = Thread(target=update_notification, daemon=True)
    update_thread.start()

    # Lancer la boucle principale de Tkinter
    root.mainloop()

def start_notification_thread():
    """Démarrer le thread de notification."""
    ensure_config_directory()
    Thread(target=show_notification, daemon=True).start()

def update_notification(title, message, image_name):
    """Mettre à jour le titre, le message et l'image de la notification en cours."""
    notification_queue.put((title, message, image_name))
