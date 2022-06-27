# Betterlife2050

## Objectifs de l'application
Cette application sert à créer et gérer des projets. Les opérations CRUD sont contrôlées par le système de [permissions](#permissions) de django.

## Diagramme Entité Relation (ERD)
![ERD](https://puu.sh/J8f6Z/4b1efcbe5a.png)
Un utilisateur peut être à la fois un membre de projet et un membre d'organisation, j'ai donc utilisé des tables n:m.

## Views
J'ai utilisé ModelViewSet pour l'ensemble de mes vues. Ce Viewsets est rapide à mettre en place et couvre toutes les opérations CRUD.
![exempleview1](https://puu.sh/J8fgZ/dc01eed646.png)<br>
*get_queryset* et *perform_create* sont des fonctions déjà définit par le ModelViewSet.
En les redéfinissant, j'ai pu contrôler et ajouter les logiques dont j'avais besoin.<br>
![exempleview2](https://puu.sh/J8fsf/8fb8c1362a.png)<br>
ModelViewSet permet également de gérer les permissions facilement.

## Permissions
J'ai créé des permissions en utilisant la classe **BasePermission** fournit par DRF.<br>
Une permission est créée pour chaque rôle d'utilisateur.<br>
Les autorisations sont ensuite données à l'utilisateur :
- En fonction de l'objet.
- S'il correspond aux logiques de la permission.

Exemple:<br>
![exemplepermission](https://puu.sh/J8flH/d57ade8840.png)


## Authentification
Pour accéder à l'application il est nécessaire d'être authentifié.
J'ai utilisé le système d'authentification basique proposé par DRF en le déclarant dans mon projet settings.py <br>
![drfauth](https://puu.sh/J8fqB/91fd5a23e9.png)

## Requirements.txt
Installez django et djangorestframework en exécutant la commande `pip install -r requirements.txt` dans le répertoire de l'application.

## Postman
Lien des endpoints postman [ici](https://documenter.getpostman.com/view/18150156/UzBsK5Wf)
## WIP
Je mettrai à jour l'application au fur et à mesure pour qu'elle réponde le mieux aux spécifications demandées.