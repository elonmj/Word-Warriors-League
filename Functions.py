import random as rd
from datetime import datetime, timedelta

def samedi(date):
    while date.weekday() != 5:  # 2 correspond à mardi (lundi = 0, mardi = 1, ...)
        date -= timedelta(days=1)
    return date

def duplicate(original, double):
    with open(original, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(double, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line)
   
def listing(names, nb_by_group= 0 ,minimum_ajout_by_group = 2):
    names = sorted(names)
    
    category = {}
    
    i = 0
    while len(names):
        if len(names) >= nb_by_group:
            choosen = rd.sample(names, k = nb_by_group)
            category[chr(65 + i)] = choosen
            [names.remove(elt) for elt in choosen]
            i += 1
        else:
            cat = rd.choice(list(category.keys()))
            choosen = rd.sample(names, k = minimum_ajout_by_group if len(names)> minimum_ajout_by_group else len(names))
            category[cat] += choosen
            [names.remove(elt) for elt in choosen]
        

    return category


def matching_and_writing(groups, filename, date):
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Date: {date.strftime('%d-%m-%Y')}\n\n")

        for category, members in groups.items():
            file.write(f"Category {category}:\n")
            matches = []

            rd.shuffle(members)

            for i in range(0, len(members), 2):
                if i + 1 < len(members):
                    matches.append((members[i], members[i + 1]))
                else:
                    exempt = rd.choice(matches)
                    matches.append((members[i], f"(Loser of {exempt[0]} vs {exempt[1]})"))

            for match in matches:
                file.write(f"\t{match[0]} vs. {match[1]} :\n")
            file.write("\n")
    

def read_matches(filename, current_date):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    date_str = lines[0].strip().split(': ')[1]
    date = datetime.strptime(date_str, '%d-%m-%Y')
    
    moment = date.strftime('%d-%m-%Y') != current_date.strftime('%d-%m-%Y')
    results = {}
     
    current_category = None
    for line in lines[2:]:
        line = line.strip()

        if line.startswith("Category"):
            current_category = line.split(':')[0].split(' ')[1]
            if current_category == '':
                print("Erreur: le nom d'une catégorie n'a pas été trouvé")
                exit()

        elif line != '' and "vs." in line:
            match_info = line.replace(' ', '').split(":")
            joueurs = match_info[0].split("vs.")
            
            if joueurs[1].startswith("(Loserof"):
                match = joueurs[1].replace("Loserof", '')
                if match in results:
                    joueurs[1] = results[match][1]  # on prend le perdant
                else:
                    print("Erreur: match non trouvé pour le perdant")
                    continue

            result = match_info[1] if len(match_info) > 1 else ''

            if result == '':
                if moment:
                    result = rd.choice(joueurs)
                    result += " (Random)"  # Indique que le résultat est aléatoire
                else:
                    continue
            
            if result not in joueurs and not result.endswith("(Random)"):
                trouve = False
                for elt in joueurs:
                    if result in elt and elt.startswith("(Loserof"):
                        trouve = True
                if not trouve:
                    print("Erreur: le gagnant ne fait pas partie des joueurs pour le match joué")
                    print("Liste de joueurs détectée", joueurs)
                    print("Gagnant détecté", result)
                    exit()

            match = f'({joueurs[0]}vs{joueurs[1]})'
            winner = result.split(" (Random)")[0] if result.endswith("(Random)") else result

            if len(joueurs) != 2:
                print("Erreur: plus de deux joueurs détectés pour un match")
                print("Liste de joueurs détectée", joueurs)
                print("Gagnant détecté", result)
                exit()
            if joueurs[0] == joueurs[1]:
                print("Erreur: un joueur joue contre lui-même")
                print("Liste de joueurs détectée", joueurs)
                print("Gagnant détecté", result)
                exit()
            
            loser = next(elt for elt in joueurs if elt != winner)

            results[match] = [winner, loser, current_category, "Random" if result.endswith("(Random)") else ""]
    
    return date, results, moment





def update_category(groups, results):
    # if faut faire pour les winners à part et pour les perdants à part à cause des rachats possibles
    achivements = []
    for elt in results:
        winner = results [elt][0]
        category = results[elt][2]
        if category !='A':
            next = chr(ord(category)-1)
            
            groups[category].remove(winner)
            groups[next].append(winner)
        achivements.append(winner)
    # En fait puisqu'il peut avoir des rachats on va d'abord faire la mise à jour des gagnants et puis après
    # faire celle des perdants
    for elt in results:

        loser = results[elt][1]
        if loser.startswith("(Loserof"):
            continue
        category = results[elt][2]
        if loser in achivements:
            #vérifier s'il a joué un match qu'il a gagné donc c'est du rachat
            rachat =False
            for elt in results:
                if loser in elt:
                    if results[elt][0]== loser:
                        rachat =True
                        break
            if rachat == False:
                print("I don't understand why this person is a loser mais a été enregistré comme un winner sans rachat")
                print(achivements)
                print("Individu",loser)
                print(results)
                break
            continue
        if chr(ord(category)+1) in groups:
            next = chr(ord(category)+1)
           
            groups[category].remove(loser)
            groups[next].append(loser)
    return groups


def write_groups(filename, date, groups):
    with open(filename, 'w', encoding='utf-8') as file:

        file.write(f"Date: {date.strftime('%d-%m-%Y')}\n\n")
        
        for category, members in groups.items():
            file.write(f"Category {category}:\n")
            for member in members:
                file.write(f"\t{member}\n")
            file.write("\n")

def read_groups(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    date_str = lines[0].strip().split(': ')[1]
    date = datetime.strptime(date_str, '%d-%m-%Y')
    groups = {}
    
    current_category = None
    for line in lines[2:]:
        line = line.strip()
        if line.startswith("Category "):
            current_category = line.split(' ')[1]
            current_category = current_category.split(':')[0]
            groups[current_category] = []
        elif line != '':
            groups[current_category].append(line)
    
    return date, groups


def update_parcours(filename, results, categories, date):
    last_achievements = {}
    for elt in results:
        winner = results[elt][0]
        category = results[elt][2]
        is_random = results[elt][3] == "Random"
        random_indicator = " (R)" if is_random else ""
        
        if category == 'A':
            last_achievements[winner] = f'{category} ↔{random_indicator} '
        else:
            last_achievements[winner] = f'{category} ↑{random_indicator} '
    
    for elt in results:
        loser = results[elt][1]
        category = results[elt][2]
        is_random = results[elt][3] == "Random"
        random_indicator = " (R)" if is_random else ""
        
        if loser in last_achievements:
            rachat = False
            for match in results:
                if loser in match and results[match][0] == loser:
                    rachat = True
                    break
            if not rachat:
                print(f"Erreur: {loser} est enregistré comme perdant mais aussi comme gagnant sans rachat")
                print(last_achievements)
                print("Individu", loser)
                print(results)
                break
            continue
        
        if chr(ord(category)+1) in categories:
            last_achievements[loser] = f'{category} ↓{random_indicator} '
        else:
            last_achievements[loser] = f'{category} ↔{random_indicator} '
    
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    new_lines = []
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        components = line.split(':')
        person = components[0].split('(')[0].strip()
        if person in last_achievements:
            new_lines.append(line + last_achievements[person])
            del last_achievements[person]
        else:
            new_lines.append(line)
    
    if len(last_achievements) > 0:
        for elt in last_achievements:
            new_lines.append(f"{elt}({date.strftime('%d-%m-%Y')}) : {last_achievements[elt]}")
    
    with open(filename, "w", encoding="utf-8") as file:
        for line in new_lines:
            file.write(line + "\n\n")

# def update_parcours( filename, results, categories, date):
#     last_achivements = {}
#     for elt in results:
#         winner = results[elt][0]
#         category = results[elt][2]
#         if category =='A':
#             last_achivements[winner] = f'{category} ↔ '
#         else:
#             last_achivements[winner] = f'{category} ↑ '
        
#     # En fait puisqu'il peut avoir des rachats on va d'abord faire la mise à jour des gagnants et puis après
#     # faire celle des perdants
#     for elt in results:

#         loser = results[elt][1]
#         category = results[elt][2]
#         if loser in last_achivements:
#             #vérifier s'il a joué un match qu'il a gagné donc c'est du rachat
#             rachat =False
#             for elt in results:
#                 if loser in elt:
#                     if results[elt][0]== loser:
#                         rachat =True
#                         break
#             if rachat == False:
#                 print("I don't understand why this person is a loser mais a été enregistré comme un winner sans rachat")
#                 print(last_achivements)
#                 print("Individu",loser)
#                 print(results)
#                 break
#             continue
#         if chr(ord(category)+1) in categories:
    
#             last_achivements[loser] = f'{category} ↓ '
#         else:

#             last_achivements[loser] = f'{category} ↔ '
        
#     with open(filename, "r", encoding="utf-8") as file:
#         lines = file.readlines()
#     new_lines = []
#     for line in lines:
#         line = line.strip()
#         if line =="":
#             continue
#         components = line.split(':')
#         person = components[0].split('(')[0].strip()
#         if person in last_achivements:
#             new_lines.append(line +last_achivements[person])
#             del last_achivements[person]
#         else:
#             new_lines.append(line)
    
#     if len(last_achivements)>0:
#         for elt in last_achivements:
#             new_lines.append(f"{elt}({date.strftime('%d-%m-%Y')}) : {last_achivements[elt]}")
    
#     with open(filename, "w", encoding="utf-8") as file:
#         for line in new_lines:
#             file.write(line+"\n\n")

# def degrade_parcours( filename):
#     with open(filename, 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#     for line in lines :
#         if line == "\n":
#             continue
#         print(len(line),"  ", end="")
#         line = line[:-3] + "\n"
#         print(len(line))
#     with open(filename, 'w', encoding='utf-8') as file:
#         for line in lines:
#             file.write(line)


# def read_matches(filename, current_date):
#     with open(filename, 'r', encoding='utf-8') as file:
#         lines = file.readlines()

#     date_str = lines[0].strip().split(': ')[1]
#     date = datetime.strptime(date_str, '%d-%m-%Y')
    
#     moment = date.strftime('%d-%m-%Y')!=current_date.strftime('%d-%m-%Y')
#     results =  { }
     
#     current_category = None
#     for line in lines[2:]:

#         line = line.strip()

#         if line.startswith("Category"):
#             current_category = line.split(':')[0].split(' ')[1]
#             if current_category =='':
#                 print("Euh le nom d'une catégorie n'a pas été trouvée")
#                 exit()

#         elif line != '' and "vs." in line:
            
#             match_info = line.replace(' ', '').split(":")

#             joueurs = match_info[0].split("vs.")
            
#             if joueurs[1].startswith("(Loserof"):
#                 match = joueurs[1].replace("Loserof", '')
#                 if match in results:
#                     joueurs[1] = results[match][1]## ici on prend le perdant
#                 else :
#                     print("Liste de joueurs détectée", joueurs)
#                     print("Winner détecté", result)
#                     continue

#             result = match_info[1]
            

#             if result == '':
#                 if moment == True :
#                     result = rd.choice(joueurs)
#                 else :
#                     continue
#             if result not in joueurs :
#                 trouve = False
#                 for elt in joueurs:
#                     if result in elt and elt.startswith("(Loserof"):
#                         trouve = True
#                 if trouve == False:
#                     print("Euh, je ne comprends pas pourquoi ce winner ne fait pas partie des joueurs pour le match joué")
#                     print("Liste de joueurs détectée", joueurs)
#                     print("Winner détecté", result)
#                     exit()

#             match = f'({joueurs[0]}vs{joueurs[1]})'
#             winner = result 

#             if len(joueurs)!= 2:
#                 print("Euh , je ne comprends pas pourquoi joueurs il a choppé plus de deux éléments")  
#                 print("Liste de joueurs détectée", joueurs)
#                 print("Winner détecté", result)
#                 exit()
#             if joueurs[0] == joueurs[1]:
#                 print("Euh, une doublure se promène")      
#                 print("Liste de joueurs détectée", joueurs)
#                 print("Winner détecté", result)
#                 exit()    
#             for elt in joueurs:
#                 if elt!=winner:
#                     loser = elt
#             # ici c'est sûr à 100% que quelque chose est assigné à loser, donc pas de contrôle
#             # sur le fait que loser existe comme ça le contraire nous signalera directement l'erreur

#             results[match] = [winner, loser, current_category]
    
#     return date, results, moment