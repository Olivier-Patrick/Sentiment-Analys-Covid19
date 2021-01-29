# Sentiment-Analys-Covid19

## INTRODUCTION 

Dans ce projet de l’unité d’enseignement Analyse des réseaux sociaux , notre objectif est de collecter les Tweetes comportant le hashtags #COVID19 à l’aide de Tweepy puis les stocker dans une base de données  MongoDB en local en suite pré-traiter et analyser
les données avec python et stocker les résultats dans les bases de données Mysql et InfluxDB selon la visualisation avec Grafana. Il est claire de souligner 
que grafana est un puissant outils de visualisation, pour l’utiliser je l’ai paramétré aux base de données Mysql et InfluxDB.
Ci dessous on peut voir l’architecture de ce projet :
<img src="https://github.com/Olivier-Patrick/Sentiment-Analys-Covid19/blob/master/Image%20Analyse%20des%20reseaux%20socio/Architecture%20Projet%20Analyse%20des%20Sentiments%20(autre%20copie).png" width="800px" height="auto">

Commençons par la collection des Tweetes.

## COLLECTIONS
Nous collectionnons les Tweetes comportant des hashtag #COVID19 en utilisant Tweepy puis nous
les stockons dans une base de données mongoDB. Tweepy permet de faciliter l’utilisation de l’API
de streaming Twitter en gérant l’authentification, la connexion, la création et la destruction de la
session, la lecture des messages entrant et le routage partiel des messages.Ci dessous nous
importons les librairies et définissons les clés d’acces de notre application crée sur Twitter.
Le fichier config.py contient les clés d’authentifications de l’application crée dans mon compte
Twitter développeur pour avoir acces à l’API de streaming Twitter.

L’ API de streaming Twitter est utilisé pour télécharger les messages Twitter en temps réel.
Dans la librairie Tweepy , une instance de tweepy.Stream établit une session de streaming et
achemine les messages vers l’instance StreamListerner. 

La méthode on_data() d’un écouteur de
flux reçoit tous les messages et appelle des fonctions en fonction du type de message.
La méthode on_data() reçoit tout les messages puis les charges en json par la suite on insert les
données en format json dans la base de données COVID dans une collection appelée Tweets. Nous
sommes maintenant à mesure de créer notre objet flux en utilisant un filtre pour diffuser tous les
messages contenant: corona, coronavirus, covid, covid-19.

Après exécutions nous pouvons voir les tweets: 
<img src="https://github.com/Olivier-Patrick/Sentiment-Analys-Covid19/blob/master/Image%20Analyse%20des%20reseaux%20socio/donn%C3%A9es%20dans%20la%20bd%20covid.png" width="800px" height="auto">

On connecte en paramétrant la base de donnée InfluxDB et Mysql à Grafana pour visualiser la position de chaque personne qui a twitté.
Voici la localisation des utilisateurs qui ont twitté sur le covid19 lors de l’extraction :
On peut voir que plus d’utilisateurs en Amérique, Brésil et en Inde ont twitté sur le covid à cet
instant.

<img src="https://github.com/Olivier-Patrick/Sentiment-Analys-Covid19/blob/master/Image%20Analyse%20des%20reseaux%20socio/distributions%20sur%20la%20carte%20du%20monde%20.png" width="800px" height="auto">

Après pré-traitement des données et en appliquant la fonction du nuage des mots sur les tweets on a :

<img src="https://github.com/Olivier-Patrick/Sentiment-Analys-Covid19/blob/master/Image%20Analyse%20des%20reseaux%20socio/world_cloud.png" width="800px" height="auto">

Les figures ci dessous montre le taux de chaque classe , on peut remarquer qu'il y a plus de tweetes
neutres cela se justifie par le faites que nous avons considéré que la langue anglaise dans notre étude,
ainsi la plupart des tweetes qui ne sont pas en anglais ont été considérés comme neutres.Aussi il est
important de remarquer qu’il y a plus de tweetes négatifs que positifs sur le covid19.

<img src="https://github.com/Olivier-Patrick/Sentiment-Analys-Covid19/blob/master/Image%20Analyse%20des%20reseaux%20socio/Bar%20Jauge%20(copie).png" width="800px" height="auto">

<img src="https://github.com/Olivier-Patrick/Sentiment-Analys-Covid19/blob/master/Image%20Analyse%20des%20reseaux%20socio/pie%20chart%20(copie).png" width="800px" height="auto">

<img src="https://github.com/Olivier-Patrick/Sentiment-Analys-Covid19/blob/master/Image%20Analyse%20des%20reseaux%20socio/Label%20des%20avant.png" width="800px" height="auto">

<img src="https://github.com/Olivier-Patrick/Sentiment-Analys-Covid19/blob/master/Image%20Analyse%20des%20reseaux%20socio/histogramme%20tweet%20train.png" width="800px" height="auto">

## CONCLUSION

Dans cette étude nous avons extraire des tweets que nous avons stocké dans différentes
bases de donnée puis nous les avons pré-traité et analysé. Il faut noter que le modèle entraîné
pour classifier les sentiment des tweets nous donne un bon score mais avec les modèles
utilisant les réseaux de neurones cela peut être amélioré. Mon objectif en procédant ainsi
était de détecter en temps réel les tweets négatifs puis visualiser leur origine et évolution avec grafana mais j’étais limité en ressources matériels c’est à dire capacité d’ordinateur insuffisante. J’espère refaire un tutoriel encore plus sophistiqué une fois que j’aurai une bonne capacité d’ordinateur pouvant supporter tout les calculs découlant et les outils.

