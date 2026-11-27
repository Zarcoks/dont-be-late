## Cahier de labo

### Séance du 03/09/2026

- Brainstorming sur l'idée
- Rédaction du cahier des charges
- Cadrage

### Séance du 11/09/2026

**Deraina :**

- Formation Django
- Mise en place du Gantt

**Basma :**

- Formation Django
- Création du repo GitHub

**Victor :**

- Analyse de l'API RATP
- Rédaction des fonctionnalités possibles

### Séance du 16/09/2026

- Finalisation du Gantt
- Étude de faisabilité
- Création du modèle de données de base

### Séance du 24/09/2026

**Victor :**
- Signup et login utilisateur suivant le modèle de Django

### Séance du 01/10/2026

**Deraina :**
Etude des données de sorties de l'API Prim et formation celery
https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html

**Victor :**
- Début de l'implémentation de l'import calendriers (reste à faire import des évènements)

### Séance du 08/10/2026

**Deraina :**
Reformalisation des fonctionnalités attendus dans le cahier des charges

**Victor :**
- Implémentation des Locations. Grace à elles l'import des évènements pourra etre faite.


### Séance du 15/10/2026 et week-ends

**Deraina :**
Début d'implémentation du worker celery pour récupérer les données de retard

**Victor :**
- Construction des pages HTML / CSS pour l'import du calendrier et du location. 
- J'ai enlevé le système qui forcait l'utilisateur à renseigner son lieu de vie parce que c'était trop complexe par rapport au temps qu'il nous reste.
- Au final j'ai commencé un plus gros refactor pour simplifier l'app au maximum au vu du peu de temps qu'il reste

### Séance du 04/11/2026 et week-ends
**Victor :**
- Formulaire du Locations

**Deraina :**
Etant en cours d'implementation du worker 1, on s'est finalement rendu compte qu'il n'avait pas de réel utilité en tant que tel car lorsque notre worker préviendra d'un retard il sera déjà forcément trop tard.
Modif : 
On va d'abord faire le worker 2 qui s'active la veille et qui va se baser sur les travaux ou les perturbations qui concernent toute la ligne (les travaux qui sont spécifiques ne sont pas encore pris en compte)
On ne prend pas encore les severité bloquant pour les arrêts non desservis.
On fera l'implem de la fonction regex pour récupérer le temps exact après
(?P<nb_heure>\d+)\s*h\w*\s*\w*\s*(?P<nb_minutes>\d+)\s*min\w*

### Séance du 05/11/2026
**Victor :**
- Formulaire de création de trajets / lignes
- On est parti pour enregistrer les données de la RATP sur l'id des lignes et des arrets pour pouvoir faire des selects
à l'utilisateur utilisable. 
- J'ai pu finir les views ou presque, il faut faire les templates du formulaire. 

### 12/11/2026

**Deraina :**
Le worker 1 est peut-être finalement utile pour indiquer à l'utilisateur d'emprunter un autre trajet s'il s'avère qu'elle a eu des perturbations juste avant son départ car il est possible que le trafic ne soit pas encore réellement rétabli. 
TODO : terminer le worker 1 puis le 2 car ils se complètent
Ex :
Départ prévu à 8h avec la D et je me réveille à 7h pour me préparer.
L'application me signale une perturbation à 7h30 et me dit que le trafic ne se rétablira qu'à 8h30.
Je peux adapter mon départ pour emprunter le bus de 7h45 pour arriver à l'heure sans prendre la D.

### Weekend du 17/11/2026
**Victor :**
- Possibilité d'assigner des locations aux events

### Séance du 25/11/2026
**Victor :**
- 

TODO une vue admin pour importer les données IDFM

**Deraina :**
IDFM ne fournit pas la durée du retard, seulement la gravité et la période. On prendra donc une  marge qui est une estimation par gravité (BLOQUANTE : 1h, PERTURBEE : 30 min) affinée par la durée trouvée dans le message quand elle existe