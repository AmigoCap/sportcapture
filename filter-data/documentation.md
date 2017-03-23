Ce document décrit les scripts présents dans le dossier filter-data.

# filter-joints.py

## description du script

Ce script prends en entré un fichier CSV contenant des données de type "Joints" exportées par Nexus.
Le nom du fichier est à renseigner dans le script, dans la variable `filename`.
Les traitements suivants sont effectués successivement :
 - Extraction des données "Joints" parmis le fichier
 - Lissage des mesures d'angles
 - Calcul de la vitesse angulaire et acceleration angulaire par dérivation successive sur chaque composante
 - Jointure des composantes sur chaque articulation au moyen d'une norme (pour l'instant norme 2)
 - Enregistrement des données traitées au format JSON avec la structure décrite ci-après
 
 ## structure des données de sortie
 
 ```json
    {
        "right_shoulder" : {
            "angle" : [... time serie],
            "angular_speed" : [...],
            "angular_acceleration" : [...]
        },
        "right_elbow" : {
         ...
        },
        ...
    }
```