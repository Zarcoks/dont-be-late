Quoi de pire que d'arriver en retard ? En FISA, le retard a beaucoup fait débat dernièrement, c'est pourquoi nous souhaitons 
développer une application web pour définitivement régler ce problème de retard. 

Notre vision de l'application se décompose en 3 grandes étapes: 
1. collection des données: Nous collectons betement les données de Ile de France Mobilité et Météo France
2. traitement: Nous prédisons et rendons compte des retards de train
3. action: nous informons l'utilisateur des retards et proposons des solutions


L'application se fait en Django, 3 services principaux: postgres, django, et workers celery (collection des données)

Voici les fonctionnalités visées:
1. Enregistrement de l’emploi du temps (on enregistre l’heure de début des cours pour chaque jour avec où on doit se trouver) 
	1.1 Pour chaque matière matinale du .ics, on demande à l’utilisateur de renseigner le lieu où il doit se trouver
	1.2 Assigner un lieu pour toutes les matières en meme temps, ou un groupe spécifique
2. Enregistrement de trajets: lignes que le user va traquer
	2.1 En fonction de source et destination, propose des combos de lignes, arrêts, et fill automatique des données déduites (durée théorique de voyage, temps d’attente estimé entre correspondance = moyenne, temps de marche prévu (avant / après), avance minimale, et le « partir à » maximal. On peut aussi déduire les tranches min et max auxquelles on s’attend à ce que les trains doivent arriver.
3. Analyse des données court terme
	3.1 Vers 5h du matin, scrute en direct toutes les 5 minutes les transports et vérifie qu’ils sont dans les temps, et informe l’utilisateur si son avance sera théoriquement suffisante ou pas
4. Analyse des données moyen terme
	4.1 Chaque soir vers 20h pour le lendemain, scrutage de Messages Info Trafic et des horaires annoncés pour vérifier si le trafic est normal ou perturbé 
5. Analyse des données long terme
	5.1 Tous les jours pour les semaines qui viennent, l’application regarde Message Info Trafic pour anticiper les problèmes futurs, préviens l’utilisateur si problème et affiche les rappels semaine, 3 jours avant, puis 1 jour avant
6. Analyse des données météorologiques 
	6.1 Traduire les données de l’API météo en probabilité d’impact en fonction des jours
7. Basé sur toutes les données, API proposition d’heure de réveil en GET