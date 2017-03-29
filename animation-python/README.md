# Tutorial

## Description

Les scripts python dans ce dossier permet de visualiser les données de mouvement de la plateforme Amigo en temps réel ou sous forme de fichier de vidéo. 

## Installation

Les programmes sont développés en Python 3.6 et dépendent de deux librairies :
* Matplotlib

  L'installation de cette librairie peut se faire en installant le package de distribution [Anaconda](https://www.continuum.io/downloads) ou vous pouvez suivre son documentation [ici](http://matplotlib.org/users/installing.html).

* Pyqtgraph

  L'installation de Pyqtgraph est fait via le fichier binaire sur son [site](http://www.pyqtgraph.org/).
  
* Ffmpeg (pour création de fichier vidéo avec Matplotlib)

  Si vous voulez utiliser le script anim_matplotlib.py pour sauvegarder la visualisation en vidéo, il vous faut un logiciel d'écriture de vidéo comme [ffmpeg](https://ffmpeg.org/). Sous Windows, il faut juste mettre le fichier *ffmpeg.exe* dans le même répertoire que le script.

## utils.py - Lire des données depuis les fichiers exportés

Dans le script on définit deux fonctions qui permet de lire les données nécessaires pour la visualisation.

### csv

Le fichier csv lisible par la fonction *read_from_csv* est le fichier contenant les positions des markers à chaque frame (sans d'autres données comme les angles). La fonction donne un tableau sous forme de Dataframe de librairie Pandas et le nombre total de frame :

.|.|0|1|...|
-|-|-|-|---|
marker name 1|x|position 0|position 1|...|
.|y|position 0|position 1|...|
.|z|position 0|position 1|...|
marker name 2|x|position 0|position 1|...|
|...|

### mkr

Le fichier mkr est un fichier de text contenant la liste des markers et les liaisons entre eux. Voici un [exemple](https://github.com/AmigoCap/sportcapture/blob/master/data/Arnaud.mkr).

La fonction *read_from_mkr* retourne une liste des noms de ces markers et une autre des liaisons
```python
  markers = ['name1', 'name2',...]
  segments = [['start marker name 1', 'end marker name 1'], ...]
```

## anim_matplotlib.py - animation avec matplotlib

L'animation en utilisant Matplotlib suit les étapes principaux ci-dessous : 

1. Lecture des données
  
2. Calculer la vitesse linéaire
    On estime la vitesse lineaire par rapport à frame : v(f) = p(f+1) - p(f)
    ```python
    speed_vec = datas.ix[:,:].subtract(datas.ix[:,1:].rename(columns=lambda x: x-1))
    speed_scal = np.sqrt(np.square(speed_vec.ix[0::3].reset_index(level=1).drop('level_1',1)).add(
                         np.square(speed_vec.ix[1::3].reset_index(level=1).drop('level_1',1))).add(
                         np.square(speed_vec.ix[2::3].reset_index(level=1).drop('level_1',1)))).fillna(value=0.1).add(0.00000001)
    ```
3. Créer la figure et mettre les limites des axes
4. Définir la fonction de mise à jour de figure
    ```python
    def update_lines(num)
    ```
    Cette fonction renouvelle les coordonnées des segments à frame num en lisant les données récupérées dans les étapes 1 et 2.
5. Lancer l'animation en temps réel ou la stocker en vidéo
    ```python
    line_ani = animation.FuncAnimation(fig, update_lines, frames, interval=10, blit=False)
    line_ani.save(filename+'.mp4')
    plt.show()
    ```
## anim_pyqtgraph.py - animation avec pyqtgraph

L'animation en utilisant Pyqtgraph suit à peu près les mêmes principes que celle avec Matplotlib.

1. Lecture des données

    La lecture des données n'a pas utilisé la fonction définie dans *utils.py* parce que les données sous forme de DataFrame ralentit beaucoup l'exécution de Pyqtgraph. Donc dans le script on rédéfinit une fonction pour nous retourner les données sous forme de dictionnaire.
  
2. Créer la figure et mettre les limites des axes
3. Définir la fonction de mise à jour de figure
    ```python
    def update()
    ```
    Son corps est presque identique que celle dans la partie Matplotlib. A chaque appellation de cette fonction, on met à jour les coordonnées par les données du frame suivant.
4. Créer un Timer pour mise à jour de la figure
    ```python
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(15)
    ```
    Ceci est un timer de Qt, il va appeler la fonction donnée (update) répétitivement avec une intervale de temps fixée (ici 15ms).
5. Lancer l'animation en temps 
    ```python
    QtGui.QApplication.instance().exec_()
    ```
