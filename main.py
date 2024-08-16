import random as rd
from datetime import datetime
from copy import  deepcopy

from Functions import *

RESET_TO_OLD = False
RESET = False
CHANGE = True
CURRENT_DATE = vendredi(datetime.now())
OLD_DATE = vendredi(datetime.now()-timedelta(weeks =1))
SEED = CURRENT_DATE.day

rd.seed(SEED)
Nb_by_group = 4
names = [
    'Gerse3',
    'sessi7',
    'fofolle24',
    'Mya17',
    '20067s',
    'YasminaS',
    'bado',
    'joselonm',
    'Toxicboy',
    'Gabimaru9',
    'Divino',
    'Orens',
    'Caerys',
    'Kpalingan',
    'kras30',
    'Oswalde'
]

if RESET == True:
    category = listing(names, Nb_by_group)
    write_groups("Categories.txt", CURRENT_DATE, category)
    matching_and_writing(category, "Matches.txt",CURRENT_DATE)
    write_groups("OldCategories.txt", CURRENT_DATE, category)
    with open("Parcours.txt", 'w'):
        pass
    exit()    

if RESET_TO_OLD == True:
    date, category = read_groups("OldCategories.txt")
    write_groups("Categories.txt", date, category)
    duplicate("OldMatches.txt", "Matches.txt")
    duplicate("OldParcours.txt", "Parcours.txt")
    exit() 


#Voir l'update actuel des  category
 
 # Récupération de l'état passé
date_classment , groups = read_groups("Categories.txt")
print("Old groups\n",groups, "\n\n")
 
 # Récupération des résultats des matchs joués
date_matchs, results, moment = read_matches("Matches.txt", CURRENT_DATE)
print("Results\n",results, "\n\n")

 # Current new classment

new_groups = update_category(deepcopy(groups), results)
print("NEW GROUPS","\n",new_groups, "\n\n")



#Génération de nouveaux matchs si...
if CHANGE and moment :
    #mise à jour des groups
    write_groups("Categories.txt", CURRENT_DATE, new_groups)
    write_groups("OldCategories.txt", date_classment, groups)

    #mise à jour du matching
    duplicate("Matches.txt", "OldMatches.txt")
    duplicate("Parcours.txt", "OldParcours.txt")
    matching_and_writing(new_groups, "Matches.txt", CURRENT_DATE)
    update_parcours("Parcours.txt", results,  list(new_groups.keys()), date_matchs )


