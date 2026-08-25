import os
import sys
import time as tm

simple = "\033[0m"
rouge = "\033[1m\033[91m"
vert = "\033[1m\033[92m"

def arret() :
    sys.exit(1)

class VERROU :
    def __init__(self, proprietaire, montant, temps_deverrouillage, nombre_semaine) :
        self.proprietaire = proprietaire
        self.montant = montant
        self.temps_deverrouillage = temps_deverrouillage
        self.nombre_semaine = nombre_semaine
        self.retire = False

class COFFRE_FORT_CFC :
    POINTS_BASES_FRAIS = 10
    DURE_MIN_VERROU = 604_800 # une semaine le minimum

    def __init__(self, destinataire_frais : str) :
        self.destinataire_frais = destinataire_frais
        self.verrous = {}
        self.prochain_id_verrou = 0

    def verrouiller(self, p, m, d, t) : # p : propriétaire, m : montant, d = durée en seconde, t : temps actu
        global semaine
        if m <= 0 :
            print(f"{rouge} Montant nul {simple}")
            return
        if d < self.DURE_MIN_VERROU :
            print(f"{rouge} Durée trop courte{simple}")
            return
    
        nouveau_verrou = VERROU(p, m, d + t, d // semaine)
        id_verrou = self.prochain_id_verrou
        self.verrous[id_verrou] = nouveau_verrou
        self.prochain_id_verrou += 1

        print(f"{vert} SUCCES  : id = {id_verrou} {simple}")
        print("Aucun frais prélévé.")
        return id_verrou

    def prolonger_verrou(self, id_verrou, p, sp) : # p : propriétaire, sp : seconde supplémentaire
        global semaine
        if id_verrou not in self.verrous.keys() :
            print(f"{rouge} KeyError {simple}")
            return

        if sp < semaine : # C'est un choix assumer : prolonger de 1 seconde ne sert pas il faut y penser
            print(f"{rouge} Le prolongement minimal est d'une semaine.{simple}")
            return

        if self.verrous[id_verrou].proprietaire != p :
            print(f"{rouge} Mauvais propriétaire {simple}")
            return

        if self.verrous[id_verrou].retire != False :
            print(f"{rouge} Somme déja retirée {simple}")
            return

        self.verrous[id_verrou].temps_deverrouillage += sp
        self.verrous[id_verrou].nombre_semaine += (sp//semaine)
        print(f"{vert} SUCCES {simple}")
        print("Aucun frais prélévé.")

    def deverrouiller(self, id_verrou, p, t) : # p : propriétaire , t : temps actu
        if id_verrou not in self.verrous.keys() :
            print(f"{rouge} KeyError {simple}")
            return
        if self.verrous[id_verrou].proprietaire != p :
            print(f"{rouge} Mauvais propriétaire {simple}")
            return
        if self.verrous[id_verrou].retire == True :
            print(f"{rouge} Somme déja retirée {simple}")
            return
        if self.verrous[id_verrou].temps_deverrouillage > t :
            print(f"{rouge} Temps de déverouillage pas atteint {simple}")
            return

        frais = self.verrous[id_verrou].montant * self.POINTS_BASES_FRAIS // 10_000
        self.verrous[id_verrou].retire = True
        print(f"{vert} Retrait effectué avec succès {simple}")
        print(f"Frais : {frais}")
        return {"montant_recu" : self.verrous[id_verrou].montant - frais , "frais" : frais}

    def obtenir_verrou(self, p) : # p : propriétaire
        global semaine
        resultat = {}
        for i in self.verrous.keys() :
            if self.verrous[i].proprietaire == p and self.verrous[i].retire == False :
                temporaire = {}
                temporaire["montant"] = self.verrous[i].montant
                temporaire["nombre_semaine"] = (self.verrous[i].nombre_semaine)
                temporaire["retirée"] = self.verrous[i].retire
                resultat[i] = temporaire

        return resultat

def afficher() :
    print("\n=========MENU=========")
    print("1 : 🔒 Créer un verrou")
    print("2 : ⏳ Prolonger un verrou")
    print("3 : 🔓 Déverrouiller")
    print("4 : 📋 Voir mes verrous")
    print("5 : Nettoyer")
    print("6 : 🚪 Quitter l'application.")

def option_1 () :
    global client, semaine
    try : 
        p = demande_proprietaire()
        m = input("Entrez le montant : ")
        d = input("Pour la durée entrée le nombre de semaine : ")
        client.verrouiller(p, int(m), int(d) * semaine, int(tm.time())) # je remplace temporairement tm.time() par 0

    except Exception as e : 
        print(e)
        print("\n\n")

def option_2() :
    global client, semaine
    try : 
        id_ = demande_id()
        p = demande_proprietaire()
        sp = input("Entrez le nombre de semaine : ")
        client.prolonger_verrou(id_, p, int(sp) * semaine)

    except Exception as e :
        print(e)
        print("\n\n")

def demande_proprietaire() : # ya une répétition de plus de 2 fois on en fais une fonction
    return input("Entrez votre nom : ")
def demande_id() :
    return int(input("Entrez votre id : "))

def option_3() :
    global client
    try :
        id_ = demande_id()
        p = demande_proprietaire()
        client.deverrouiller(id_, p, tm.time())
    except Exception as e :
        print(e)
        print("\n\n")
    
def option_4() :
    try : 
        p = demande_proprietaire()
        resultat = client.obtenir_verrou(p)

        if resultat :
            for i, info in resultat.items() :
                print("\n======INFO======")
                print(f"ID : {i}")
                print(f"Montant : {info['montant']}, Temps_en_semaine : {info['nombre_semaine']}, Retirée : {info['retirée']}")
        else : 
            print("Aucun résultat.")
    except Exception as e :
        print(e)
        print("\n\n")

def main() :
    while True :
        afficher()
        choix = input("choix : ")
        match choix :
            case "1" : 
                option_1()
            case "2" :
                option_2()
            case "3" : 
                option_3()
            case "4" :
                option_4()
            case "5" : 
                os.system("clear")
            case "6" : 
                print("Fermeture...")
                arret()

            case _ : print("Erreur de saisi.")
    

if __name__=="__main__" :
    semaine = 604_800
    client = COFFRE_FORT_CFC("SASORI")
    main()
