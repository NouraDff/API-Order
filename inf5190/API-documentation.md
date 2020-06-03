# Documentation API

Ce document a été réalisé en se basant très fortement sur l'énoncé du travail de session réalisé dans le cadre du cours INF5190 enseigné par Jean-Philippe Caissy à l'automne 2019. Voici le lien : [Énoncé du travail de session](https://github.com/jpcaissy/INF5190-19A/blob/b55de3f413234b3217d6df2f0cf9f5f52880f2dd/travail-de-session/enonce.md#service-de-paiement-distant)


____

Cette requête permet de récupérer les produits. 

---

```
GET /
Content-Type: application/json

200 OK
```
Réponse : 
```json
{
   "products" : [
      {
         "name" : "Hapiness Bottle",
         "weight" : 450,
         "id" : 123,
         "in_stock" : true,
         "description" : "An incredible bottle filled with happiness and joy. One of a kind!",
         "price" : 5999,
         "image": "http://caissy.dev/shops/images/image.png"
      },
      {
         "description" : "A limited edition special Flying Squirrel. Hurry up, it won't last long!",
         "image": "http://caissy.dev/shops/images/image.png",
         "in_stock" : false,
         "id" : 456,
         "name" : "Flying Squirrel Limited Edition",
         "weight" : 220,
         "price" : 3149
      }
   ]
}
```

Cette requête permet de faire une commande :

```
POST /order
Content-Type: application/json
```

```json
{ "product": { "id": 123, "quantity": 2 } }
```

```
302 Found
Location: /order/<int:order_id>
```

S'il manque l'objet `product`, ou que l'objet `product` ne contient pas le champ `id` ou `quantity`, un message
d'erreur doit être retourné.


```
422 Unprocessable Entity
```

```json
{
   "errors" : {
       "product": {
           "code": "missing-fields",
           "name": "La création d'une commande nécessite un produit"
        }
   }
}
```

Si l'item représenté par l'identifiant unique `product_id` 
est en inventaire (`in_stock == True`), un processus d'achat commence. Si le produit n'est pas en inventaire, l'API doit retourner une
erreur avec le code HTTP 422 et le message d'erreur suivant :

```
422 Unprocessable Entity
```

```json
{
   "errors" : {
       "product": {
           "code": "out-of-inventory",
           "name": "Le produit demandé n'est pas en inventaire"
        }
   }
}
```



Une fois le processus d'achat commencé, on peut récupérer la commande complète à tout moment avec cette requête GET.

```
GET /order/<int:order_id>
Content-Type: application/json

200 OK
```


```json
{
   "order" : {
      "id" : 6543,
      "total_price" : 9148,
      "email" : null,
      "credit_card": {},
      "shipping_information" : {},
      "paid": false,
      "transaction": {},
      "product" : {
         "id" : 123,
         "quantity" : 1
      },
      "shipping_price" : 1000
   }
}
```


Par défaut, une commande ne contient aucune information sur le client. On doit fournir le courriel et l'adresse
d'expédition du client.

```
PUT /order/<int:order_id>
Content-Type: application/json
```

```json
{
   "order" : {
      "email" : "nouradjaffri@gmail.com",
      "shipping_information" : {
         "country" : "Canada",
         "address" : "123, rue des Érables",
         "postal_code" : "H2X 3Y7",
         "city" : "Montréal",
         "province" : "QC"
      }
   }
}
```

```
200 OK
Content-Type: application/json
```

```json
{
   "order" : {
      "shipping_information" : {
         "country" : "Canada",
         "address" : "123, rue des Érables",
         "postal_code" : "H2X 3Y7",
         "city" : "Montréal",
         "province" : "QC"
      },
      "credit_card" : {},
      "email" : "nouradjaffri@gmail.com",
      "total_price" : 9148,
      "transaction": {},
      "paid": false,
      "product" : {
         "id" : 123,
         "quantity" : 1
      },
      "shipping_price" : 1000,
      "id" : 6543
   }
}
```

S'il manque un champ, l'API doit retourner une erreur en conséquence.

```
PUT /order/<int:order_id>
Content-Type: application/json
```

```json
{
   "order" : {
      "shipping_information" : {
         "country" : "Canada",
         "province" : "QC"
      },
   }
}
```

```
422 Unprocessable Entity
Content-Type: application/json
```

```json
{
   "errors" : {
       "order": {
           "code": "missing-fields",
           "name": "Il manque un ou plusieurs champs qui sont obligatoire",
       }
   }
}
```




Lorsque la commande contient toutes les informations, on peut la payer avec une carte de crédit.

NOTE : Précédemment ce projet utilisait une API distante pour gérer le paiment. Cependant, l'API n'est plus disponible. 

Autrement, voici comment aurait fonctionner les requête avec l'API
```
PUT /order/<int:order_id>
Content-Type: application/json
```

```json
{
   "credit_card" : {
      "name" : "John Doe",
      "number" : "4242 4242 4242 4242",
      "expiration_year" : 2024,
      "cvv" : "123",
      "expiration_month" : 9
   }
}

```

```
200 OK
Content-Type: application/json
```

```json
{
   "order" : {
      "shipping_information" : {
         "country" : "Canada",
         "address" : "123, rue des Érables",
         "postal_code" : "H2X 3Y7",
         "city" : "Montréal",
         "province" : "QC"
      },
      "email" : "nouradjaffri@gmail.com",
      "total_price" : 9148,
      "paid": true, 
      "product" : {
         "id" : 123,
         "quantity" : 1
      },
      "credit_card" : {
         "name" : "John Doe",
         "first_digits" : "4242",
         "last_digits": "4242",
         "expiration_year" : 2024,
         "expiration_month" : 9
      },
      "transaction": {
          "id": "wgEQ4zAUdYqpr21rt8A10dDrKbfcLmqi",
          "success": true,
          "amount_charged": 10148
      },
      "shipping_price" : 1000,
      "id" : 6543
   }
}
```


Exemple d'une commande qui a déjà été payée

```
PUT /order/<int:order_id>
Content-Type: application/json
```

```json
{
   "credit_card" : {
      "name" : "John Doe",
      "number" : "4242 4242 4242 4242",
      "expiration_year" : 2024,
      "cvv" : "123",
      "expiration_month" : 9
   }
}

```

```
422 Unprocessable Entity
Content-Type: application/json
```

```json
{
   "errors" : {
       "order": {
           "code": "already-paid",
           "name": "La commande a déjà été payée."
       }
   }
}
```

Exemple d'une carte de crédit refusé par le service distant :

```
PUT /order/<int:order_id>
Content-Type: application/json
```

```json
{
   "credit_card" : {
      "name" : "John Doe",
      "number" : "4000 0000 0000 0002",
      "expiration_year" : 2024,
      "cvv" : "123",
      "expiration_month" : 9
   }
}

```

```
422 Unprocessable Entity
Content-Type: application/json
```

```json
{
    "credit_card": {
        "code": "card-declined",
        "name": "La carte de crédit a été déclinée."
    }
}
```



## Service de paiement distant

Voici le service de paiement distant. En revanche, ce service était disponible dans le cadre du cours INF5190 - Programmation Web avancée enseigné par Jean-Philippe Caissy à l'automne 2019, il n'est plus disponible. 

Lorsque l'API `/order/<int:order_id>` est appelé avec une carte de crédit, il doit communiquer avec l'API distant de
paiement. Cette API est disponible à l'adresse `https://caissy.dev/shops/pay`.

```
POST /shops/pay
Host: caissy.dev
Content-Type: application/json

```
```json
{
   "credit_card" : {
      "name" : "John Doe",
      "number" : "4242 4242 4242 4242",
      "expiration_year" : 2024,
      "cvv" : "123",
      "expiration_month" : 9
   },
   "amount_charged": 10148 # <- montant total incluant les frais d'expédition
}
```

```
200 OK
```
```json
{
   "credit_card" : {
      "name" : "John Doe",
      "first_digits" : "4242",
      "last_digits": "4242",
      "expiration_year" : 2024,
      "expiration_month" : 9
   },
   "transaction": {
       "id": "wgEQ4zAUdYqpr21rt8A10dDrKbfcLmqi",
       "success": true,
       "amount_charged": 10148
   }
}
```

Les informations de la transaction doivent être stockées sur la commande.

En cas d'erreur, l'API distant va retourner une erreur de type :

```
POST /shops/pay
Host: caissy.dev
Content-Type: application/json

```
```json
{
   "credit_card" : {
      "name" : "John Doe",
      "number" : "4000 0000 0000 0002",
      "expiration_year" : 2024,
      "cvv" : "123",
      "expiration_month" : 9
   },
   "amount_charged": 10148 # <- montant total incluant les frais d'expédition
}
```


```
422 Unprocessable Entity

```

```json
{
   "errors" : {
       "credit_card": {
           "code": "card-declined",
           "name": "La carte de crédit a été déclinée"
        }
   }
}
```

Seuls les 2 cartes de crédits de tests vont être acceptés :

* `4242 4242 4242 4242` : carte de crédit valide
* `4000 0000 0000 0002` : carte de crédit déclinée

Tout autre numéro de carte retourne le code `incorrect-number`.

Les champs `expiration_year` et `expiration_month` doivent être des entiers représentant une date d'expiration valide.
L'API va retourner une erreur si la carte est expirée.

Le champ `cvv` doit obligatoirement être un string contenant 3 chiffres.



Lorsqu'une commande est payée, l'API doit retourner toutes les informations de la commande : 

```
GET /order/<int:order_id>
Content-Type: application/json

200 OK
```

```json
{
   "order" : {
      "shipping_information" : {
         "country" : "Canada",
         "address" : "201, rue Président-Kennedy",
         "postal_code" : "H2X 3Y7",
         "city" : "Montréal",
         "province" : "QC"
      },
      "email" : "caissy.jean-philippe@uqam.ca",
      "total_price" : 9148,
      "paid": true,
      "product" : {
         "id" : 123,
         "quantity" : 1
      },
      "credit_card" : {
         "name" : "John Doe",
         "first_digits" : "4242",
         "last_digits": "4242",
         "expiration_year" : 2024,
         "expiration_month" : 9
      },
      "transaction": {
          "id": "wgEQ4zAUdYqpr21rt8A10dDrKbfcLmqi",
          "success": true,
          "amount_charged": 10148
      },
      "shipping_price" : 1000,
      "id" : 6543
   }
}
```



