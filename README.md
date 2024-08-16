(provisoire)
# Organisateur de Duels pour le Club de Scrabble

Ce script Python a été spécialement développé pour simplifier et automatiser le processus d'organisation des duels hebdomadaires au sein de notre club de scrabble. Il offre plusieurs fonctionnalités pour gérer les catégories des joueurs, générer des duels aléatoires, suivre les résultats et mettre à jour les classements.

## Fonctionnalités

- **Catégories de Joueurs :** Le script permet de classer les joueurs en différentes catégories en fonction de leurs performances passées. Cela facilite la compétition équilibrée entre les membres du club.

- **Génération Automatique de Duels :** Chaque semaine, vous pouvez utiliser le script pour générer automatiquement des duels aléatoires. Les duels sont créés en prenant en compte les catégories des joueurs, assurant ainsi des matchs équitables.

- **Suivi des Résultats :** Les résultats de chaque duel sont enregistrés avec précision. Cela permet de maintenir un historique des performances de chaque joueur.

- **Parcours des Joueurs :** Le script conserve un suivi détaillé du parcours de chaque joueur. Il indique si un joueur a été promu, relégué ou s'il est resté dans la même catégorie. De plus, la date de début de chaque joueur est enregistrée, vous permettant de suivre l'ancienneté des membres du club.

## Utilisation

1. **Initialisation :** Au début de la saison ou lorsque de nouveaux membres rejoignent le club, exécutez le script en activant l'option `RESET`. Cela initialise les catégories des joueurs en les répartissant aléatoirement dans des groupes.

2. **Génération Hebdomadaire des Duels :** Chaque semaine, exécutez le script pour générer les duels de la semaine. Les duels sont enregistrés dans le fichier `MATCHES.txt`, assurant ainsi une répartition aléatoire et équitable des adversaires.

3. **Mise à Jour des Résultats :** Après les duels de la semaine, enregistrez soigneusement les résultats dans le fichier `MATCHES.txt`. Cette étape est essentielle pour maintenir des classements précis.

4. **Mise à Jour des Catégories :** Le script met automatiquement à jour les catégories des joueurs en fonction de leurs performances. Les joueurs qui réussissent bien sont promus, tandis que ceux qui rencontrent des difficultés sont relégués. Vous avez également la possibilité de réinitialiser les catégories au besoin.

5. **Parcours des Joueurs :** Le script maintient un suivi du parcours de chaque joueur, y compris les promotions, les relégations et le nombre de matchs joués. Vous pouvez consulter ce parcours dans le fichier `Parcours.txt`.

## Personnalisation

- Vous avez la flexibilité de personnaliser le script en fonction de vos besoins spécifiques, que ce soit pour ajuster le nombre de joueurs par groupe, les noms des joueurs, les catégories de départ, etc. Le script a été conçu pour s'adapter au club de scrabble.
