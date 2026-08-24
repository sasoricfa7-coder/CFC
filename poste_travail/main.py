import sys
import time as tm

simple = "\033[0m"
rouge = "\033[1m\033[91m"
vert = "\033[1m\033[92m"

def arret() :
    sys.exit(1)

class VERROU :
    def __init__(self, proprietaire, montant, temps_deverrouillage) :
        self.proprietaire = proprietaire
        self.montant = montant
        self.temps_deverrouillage = temps_deverrouillage
        self.retire = False

class COFFRE_FORT_CFC :
    POINTS_BASES_FRAIS = 10
    DURE_MIN_VERROU = 604_800 # une semaine le minimum

    def __init__(self, destinataire_frais : str) :
        self.destinataire_frais = destinataire_frais
        self.verrous = {}
        self.prochain_id_verrou = 0

    def verrouiller(self, p, m, d, t) : # p : propriétaire, m : montant, d = durée en seconde, t : temps actu
        if m <= 0 :
            print(f"{rouge} Montant nul {simple}")
            arret()
        if d < DURE_MIN_VERROU :
            print(f"{rouge} Durée trop courte{simple}")
            arret()
    
        nouveau_verrou = VERROU(p, m, d + t)
        id_verrou = self.prochain_id_verrou
        self.verrous[id_verrou] = nouveau_verrou
        self.prochain_id_verrou += 1

        print(f"{vert} SUCCES  {simple}")
        print("Aucun frais prélévé.")
        return id_verrou

    def prolonger_verrou(self, id_verrou, p, sp) : # p : propriétaire, sp : seconde supplémentaire
        if id_verrou not in self.verrous.keys() :
            print(f"{rouge} KeyError {simple}")
            arret()

        if sp < 604_800 : # C'est un choix assumer : prolonger de 1 seconde ne sert pas il faut y penser
            print(f"{rouge} Le prolongement minimal est d'une semaine.{simple}")
            arret()

        if self.verrous[id_verrou].proprietaire != p :
            print(f"{rouge} Mauvais propriétaire {simple}")
            arret()

        if not self.verrous[id_verrou].retire :
            print(f"{rouge} Somme déja retirée {simple}")
            arret()

        self.verrous[id_verrou].temps_deverrouillage += sp
        print(f"{vert} SUCCES {simple}")
        print("Aucun frais prélévé.")

    def deverrouiller(self, id_verrou, p, t) : # p : propriétaire , t : temps actu
        if id_verrou not in self.verrous.keys() :
            print(f"{rouge} KeyError {simple}")
            arret()
        if self.verrous[id_verrou].proprietaire != p :
            print(f"{rouge} Mauvais propriétaire {simple}")
            arret()
        if not self.verrous[id_verrou].retire :
            print(f"{rouge} Somme déja retirée {simple}")
            arret()
        if self.verrous[id_verrou].temps_deverrouillage > t :
            print(f"{rouge} Temps de déverouillage pas atteint {simple}")
            arret()

        frais = self.verrous[id_verrou].montant * POINTS_BASES_FRAIS // 10_000
        print(f"{vert} Retrais effectué avec succès {simple}")
        print(f"Frais : {frais}")
        return {"montant_recu" : self.verrous[id_verrou].montant - frais , "frais" : frais}

    def obtenir_verrou(self, p) : # p : propriétaire
        resultat = {}
        for i in self.verrous.keys() :
            if self.verrous[i].proprietaire == p :
                resultat[i] = self.verrous[i]

        return resultat

def afficher() :
    print("1 : 🔒 Créer un verrou")
    print("2 : ⏳ Prolonger un verrou")
    print("3 : 🔓 Déverrouiller")
    print("4 : 📋 Voir mes verrous")
    print("5 : 🚪 Quitter l'application.")

def option_1 () :
    global client
    p = demande_proprietaire()
    m = input("Entrez le montant : ")
    d = input("Entrez la durée : (Minimum une semaine)")
    client.verrouiller(p, float(m), float(d), tm.time())   

def option_2() :
    global client
    id_ = demande_id()
    p = demande_proprietaire()
    sp = input("Entrez la durée supplémentaire : (Minimum une semaine) ")
    client.prolonger_verrou(id_, p, float(sp))

def demande_proprietaire() : # ya une répétition de plus de 2 fois on en fais une fonction
    return input("Entrez votre nom : ")
def demande_id() :
    return int(input("Entrez votre id : "))

def option_3() :
    global client
    id_ = demande_id()
    p = demande_proprietaire()
    client.deverrouiller(id_, p, tm.time())
    
def option_4() :
    p = demande_proprietaire()
    resultat = client.obtenir_verrou(p)

    for i , info in resultat.items() :
        print(i, info)

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
            case "5" : print("Fermeture...")
                arret()

            case _ : print("Erreur de saisi.")
    

if __name__=="__main__" :
    client = COFFRE_FORT_CFC("SASORI")
    main()
