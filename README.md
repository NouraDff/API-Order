# Projet de session

Ce projet est une API qui permet de gérer le paiement d'une commande.  


## Installation


### Créer l'environnement virtuelle

Cela permet d'isoler notre environnement de développement lorsque l'on va installer les librairie nécessaire, etc. 

1. Créer un dossier env
   ```
   > mkdir env
   ```
2. Créer l'environnement virtuelle
   ```
   > virtualenv -p python3 env
   ```
3. Activer l'environnement virtuelle
   ```
   > source env/bin/activate
   ```

4. Pour désactiver l'environnement
   ```
    > deactivate
   ```


### Installer les pakages 

Se placer dans le dossier inf5190/ avant de lancer cette commande. (Ensuite retourner à la racine du projet pour la suite)
 
```
$ pip3 install -r requirements.txt
```

### Créer la base de donnée

Ensuite, il faut initialiser la base de donnée en utilisant la ligne de commande suivante : 
 ```
$ FLASK_DEBUG=True FLASK_APP=inf5190 flask init-db

 ```
 

## Lancer le programme
Pour lancer le site web suffit de lancer cette commande : 

```
$ FLASK_DEBUG=True FLASK_APP=inf5190 flask run
```
L'application web se retrouvera à cette addresse: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)



## Tests
Pour lancer les test il suffit de lancer cette commande :

```
$ python3 -m pytest tests/
```

## Auteure
Noura Djaffri


