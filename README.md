# sae301 Projet "Prise Connectée Inteliggente Wifi

## Cahier des charges :

## Dans un premier temps, il vous est demandé :

### 1. De concevoir la carte électronique de cette prise connectée en Wifi (cf. EasyEDA : https://easyeda.com/fr).
Les composants électroniques doivent répondre aux critères suivants (liste non exhaustive et sans ordre de préférence)

>a. Taille de la carte électronique
>
>b. Taille de la prise électrique (estimation)
>
>c. Poids (estimation)
>
>d. Prix global de fabrication
>
>e. Wifi intégré
>
>f. Consommation
>
>g. Etc.


Vous devez justifier votre solution, notamment en énumérant vos critères par ordre de priorité !
### 2. L'allumage ou l'extinction de l'appareil branché sur la prise peut se faire depuis l'unique bouton poussoir (cf. le côté latéral gauche de la photo). Une LED indiquera l'état de l'interrupteur commandé. Noter que l'action sur le bouton poussoir doit être visible sur les interfaces web et Android demandées dans les parties suivantes .

### 3. De réaliser un serveur WEB hébergé par un Raspberry Pi.
  La page WEB doit pouvoir :

>a. Commander au moins 2 prises en ON/OFF avec retour de l'état ON ou OFF de la prise.
>
>b. Activer au moins deux plages horaires journalières sur une des deux prises. Les plages horaires journalières seront programmées en « dur » côté Raspberry (donc pas depuis la page WEB, pour l'instant). La page WEB doit indiquer si la programmation est activée ou non.

  Le Raspberry PI peut indiquer, par des LEDs, pour chacune des prises :

>a. L'état ON ou OFF
>
>b. L'activation des plages horaires.


## Dans un deuxième temps, on vous demande :
1. De réaliser une application Android reprenant les fonctionnalités proposées par la page WEB précédente.
2. De permettre la programmation d'au moins deux plages horaires journalières depuis la page WEB.
3. De sécuriser l'accès à la page WEB.
4. De sécuriser le transfert des données côté internet.

## Dans un troisième temps, on vous demande :

1. D'ajouter sur la page WEB et l'application Android, un bouton qui permet d'allumer ou d'éteindre toutes les LEDs. Si jamais, une de ces deux conditions est satisfaite par des actions individuelles sur chacune des prises, ce bouton doit prendre l'état correspondant !
2. D'indiquer, sur la page WEB et l'application Android, la température mesurée par la prise à partir du capteur DS18B20.
3. De permettre, lors de la première installation de la prise, de choisir le réseau auquel elle doit se connecter. Pour se faire, il faudra qu'elle soit en mode AP (Acces point) avant d'être en STA (STand Alone).
4. De sécuriser l'accès à l'application Android.
5. De permettre la programmation d'au moins deux plages horaires journalières depuis l'application Android.

## Dans un quatrième temps, on vous demande :

1. Faire une notification de changement d'état de la prise.
2. Faire une notification de seuil de température dépassée.
3. Envoyer par mail et SMS un message indiquant que la température a dépassé le seuil préconisé.
