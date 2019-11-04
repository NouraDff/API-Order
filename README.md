# Projet de session

## Installation

Installer les pakages nécessaire suivant : 
```
$ pip install flask pytest pytest-flask peewee
```

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

