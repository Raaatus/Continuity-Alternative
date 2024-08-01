# Continuity-Alternative
Recevez les notifications de vos réseaux sociaux sur un appareil Android et transmettez-les à votre PC en temps réel. Alternative Iphone - PC.


Nous copions une fonctionnalité continuity apple qui est de recevoir les notifications de votre téléphone sur vous Windows.

Attention ce ne sera pas possible avec un iphone vers un Pc, mais nous avons quand même une potentielle alternative. [ici](./iOs-Iphone-user.md).

[demo ici](./img/demo.mp4)
![demo ici](./img/demo.gif)


## Fonctionnement

On va build un apk qui lit les notifications de toutes les applications. Toutes les notifications récoltées seront envoyées à un serveur préalablement défini en trame HTTP-EN local. Le serveur lancé sur un Windows affichera ce qu'il reçoit via les trames, on choisira les applications à afficher.

Pour le moment ce sont des trames http lisible, dans une prochaine Maj, il sera possible d'utiliser des ssl autos signés, à utiliser en local.

## Get Started


### Rapide
Pour un lancement rapide :

- Android 7.0 or + avec les réseaux supportés
- python3
- pip :
    - flask
    - json
    - Pillow
    - tkinter

```pip install flask pillow```

On va installer l'Apk sur le téléphone voulu.

- Télécharger l'application
- Installer
- Configurer lip local du Windows où vous voulez recevoir les notifications
- Changer le port si changer dans le serveur.

- On peut tester la bonne connexion une fois que le serveur est lancé.

Du coté du Pc on lance l'app.

- Téléchargé les dépendances
- On lance l'app
- On attend la fin du startup

À la prochaine notification d'un réseau supporté, la fente s'affichera avec une opacité max.



## Custom Notification


Pour ajouter une notification custom :

- il faut :
    - le nom du package
    - Une image Png du package

- Récupérer le nom du package :
    - Lancer `get_package_name Py``
    - On provoque une notification 
    - On récupère le package nom

- Pour faire :
    - dans `./serveur/modules/modules.txt` on colle dans une nouvelle ligne le nom du package
    - Dans `./serveur/images` on colle l'image choisie puis en la renomme avec le nom du package

Les notifications de l'application seront affichées.