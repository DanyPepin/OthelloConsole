from othello.planche import Planche
from othello.joueur import JoueurOrdinateur, JoueurHumain
from othello.piece import Piece

class Partie:
    def __init__(self, nom_fichier = None):
        """
        Méthode d'initialisation d'une partie. On initialise 4 membres:
        - planche: contient la planche de la partie, celui-ci contenant le dictionnaire de pièces.
        - couleur_joueur_courant: le joueur à qui c'est le tour de jouer.
        - tour_precedent_passe: un booléen représentant si le joueur précédent a passé son tour parce qu'il
           n'avait aucun coup disponible.
        - deux_tours_passes: un booléen représentant si deux tours ont été passés de suite, auquel cas la partie
           devra se terminer.
        - coups_possibles : une liste de tous les coups possibles en fonction de l'état actuel de la planche,
           initialement vide.

        On initialise ensuite les joueurs selon la paramètre nom_fichier. Si l'utilisateur a précisé un nom_fichier,
        on fait appel à la méthode self.charger() pour charger la partie à partir d'un fichier. Sinon, on fait appel
        à self.initialiser_joueurs(), qui va demander à l'utilisateur quels sont les types de joueurs qu'il désire.
        """

        # La planche possede des None aux emplacementss vide (non prévu dans l'énnoncé) pour plus de facilité dans son parcours
        self.planche = Planche()    

        # Le joueur noir commence
        self.couleur_joueur_courant = "noir"

        self.tour_precedent_passe = False

        self.deux_tours_passes = False

        self.coups_possibles = []
  
        self.couleur_joueur_courant = "noir"

        if nom_fichier is not None:
            self.charger(nom_fichier)
        else:
            self.initialiser_joueurs()

    def initialiser_joueurs(self):
        """
        On initialise ici trois attributs : joueur_noir, joueur_blanc et joueur_courant (initialisé à joueur_noir).

        Pour créer les objets joueur, faites appel à demander_type_joueur()
        """
        self.joueur_blanc = self.demander_type_joueur("blanc")
        self.joueur_noir = self.demander_type_joueur("noir")
        self.joueur_courant = self.joueur_noir

    def demander_type_joueur(self, couleur):
        """
        Demande à l'usager quel type de joueur ('Humain' ou 'Ordinateur') il désire pour le joueur de la couleur.

        Tant que l'entrée n'est pas valide, on continue de demander à l'utilisateur.

        Faites appel à self.creer_joueur() pour créer le joueur lorsque vous aurez le type.

        Args:
            couleur: La couleur pour laquelle on veut le type de joueur.

        Returns:
            Un objet Joueur, de type JoueurHumain si l'usager a entré 'Humain', JoueurOrdinateur s'il a entré
            'Ordinateur'.
        """
        
        reponse = input("Quel type de joueur sera " + couleur + " ?")
        while reponse not in ['Humain', 'Ordinateur']:
            print("Vous devez repondre Ordinateur ou Humain !!")
            reponse = input("Quel type de joueur sera " + couleur + " ?")
        
        return self.creer_joueur(reponse, couleur)

    def creer_joueur(self, type, couleur):
        """
        Crée l'objet Joueur approprié, selon le type passé en paramètre.

        Pour créer les objets, vous n'avez qu'à faire appel à leurs constructeurs, c'est-à-dire à
        JoueurHumain(couleur), par exemple.

        Args:
            type: le type de joueur, "Ordinateur" ou "Humain"
            couleur: la couleur du pion joué par le jouer, "blanc" ou "noir"

        Returns:
            Un objet JoueurHumain si le type est "Humain", JoueurOrdinateur sinon
        """
        
        if type == "Ordinateur":
            return JoueurOrdinateur(couleur)
        else:
            return JoueurHumain(couleur)


    def valider_position_coup(self, position_coup):
        """
        Vérifie la validité de la position désirée pour le coup. On retourne un message d'erreur approprié pour
        chacune des trois situations suivantes :

        1) Le coup tenté ne représente pas une position valide de la planche de jeu.

        2) Une pièce se trouve déjà à la position souhaitée.

        3) Le coup ne fait pas partie de la liste des coups valides.

        ATTENTION: Utilisez les méthodes et attributs de self.planche ainsi que la liste self.coups_possibles pour
                   connaître les informations nécessaires.
        ATTENTION: Bien que cette méthode valide plusieurs choses, les méthodes programmées dans la planche vous
                   simplifieront la tâche!

        Args:
            position_coup: La position du coup à valider.

        Returns:
            Un couple où le premier élément représente la validité de la position (True ou False), et le
            deuxième élément est un éventuel message d'erreur.
        """
        
        coup_valide = False
        message_erreur = ""
        # 1) Le coup tenté représente une position valide de la planche de jeu.
        if self.planche.position_valide(position_coup):
            # 2) Aucune pièce se trouve déjà à la position souhaitée.
            if self.planche.cases[(position_coup)] is None:
                # 3) Le coup fait partie de la liste des coups valides.
                if position_coup in self.coups_possibles:
                    coup_valide = True
                else:
                    message_erreur = "Le coup ne fait pas partie de la liste des coups valides \n"
            else:
                message_erreur = "Une piece se trouve deja a cette position \n"
        else:
            message_erreur = "La position n est pas sur la planche de jeu \n"

        return (coup_valide, message_erreur)

    def tour(self):
        """
        Cette méthode simule le tour d'un joueur, et doit effectuer les actions suivantes:
        - Demander la position du coup au joueur courant. Tant que la position n'est pas validée, on continue de
          demander. Si la position est invalide, on affiche le message d'erreur correspondant.
           Pour demander la
          position, faites appel à la fonction choisir_coup de l'attribut self.joueur_courant, à laquelle vous
          devez passer la liste de coups possibles. Pour valider le coup retourné, pensez à la méthode de validation
          de coup que vous avez déjà à implémenter.
        - Jouer le coup sur la planche de jeu, avec la bonne couleur.
        - Si le résultat du coup est "erreur", afficher un message d'erreur.

        ***Vous disposez d'une méthode pour demander le coup à l'usager dans cette classe et la classe planche
        possède à son tour une méthode pour jouer un coup, utilisez-les !***
        """
        if self.joueur_courant.obtenir_type_joueur() == "Ordinateur":
            coup_ordinateur = self.joueur_courant.choisir_coup(self.planche.lister_coups_possibles_de_couleur(self.couleur_joueur_courant))
            self.planche.jouer_coup(coup_ordinateur, self.couleur_joueur_courant)

        if self.joueur_courant.obtenir_type_joueur() == "Humain":

            # L utilisateur choisit un coup qui fonctionne
            position_choisie = self.joueur_courant.choisir_coup(self.planche.lister_coups_possibles_de_couleur(self.joueur_courant.couleur))

            # Tant que la position choisie n est pas correct on lui redemande
            while not self.valider_position_coup(position_choisie)[0]:
                print(self.valider_position_coup(position_choisie)[1])
                position_choisie = self.joueur_courant.choisir_coup(self.planche.lister_coups_possibles_de_couleur(self.joueur_courant.couleur))
            # On joue le coup choisi
            print (self.planche.jouer_coup(position_choisie, self.joueur_courant.couleur))

    def passer_tour(self):
        """
        Affiche un message indiquant que le joueur de la couleur courante ne peut jouer avec l'état actuel de la
        planche et qu'il doit donc passer son tour.
        """


        print("Le joueur {} ne peut pas jouer et passe son tour".format(self.couleur_joueur_courant))
        self.changerTour()


    def partie_terminee(self):
        """
        Détermine si la partie est terminée, Une partie est terminée si toutes les cases de la planche sont remplies
        ou si deux tours consécutifs ont été passés (pensez à l'attribut self.deux_tours_passes).
        """

        # Si deux tours sont passés de suite la partie est terminee
        if self.deux_tours_passes:
            self.determiner_gagnant()
            return True
        
        # Si il reste aucune case vide la partie est terminee
        is_partie_terminee = True
        for case in self.planche.cases.values():
            if case is None:
                is_partie_terminee = False

        # partie terminee on indique le gagnant
        if is_partie_terminee:
            self.determiner_gagnant()
            return True
        return False
        

    def determiner_gagnant(self):
        """
        Détermine le gagnant de la partie. Le gagnant est simplement la couleur pour laquelle il y a le plus de
        pions sur la planche de jeu.

        Affichez un message indiquant la couleur gagnante ainsi que le nombre de pièces de sa couleur ou encore
        un message annonçant un match nul, le cas échéant.
        """
        nombre_de_noir = 0
        nombre_de_blanc = 0

        for case in self.planche.cases.values():
            if type(case) is Piece:
                if case.couleur == "noir":
                    nombre_de_noir += 1
                else:
                    nombre_de_blanc += 1
        if nombre_de_blanc > nombre_de_noir:
            print("Les blancs ont gagné !!!")
        if nombre_de_blanc < nombre_de_noir:
            print("Les noirs ont gagné !!!")
        if nombre_de_blanc == nombre_de_noir:
            print("Egalité...")


    def jouer(self):
        """
        Démarre une partie. Tant que la partie n'est pas terminée, on fait les choses suivantes :

        1) On affiche la planche de jeu ainsi qu'un message indiquant à quelle couleur c'est le tour de jouer.
           Pour afficher une planche, faites appel à print(self.planche)

        2) On détermine les coups possibles pour le joueur actuel. Pensez à utiliser une fonction que vous avez à
           implémenter pour Planche, et à entreposer les coups possibles dans un attribut approprié de la partie.

        3) Faire appel à tour() ou à passer_tour(), en fonction du nombre de coups disponibles pour le joueur actuel.
           Mettez aussi à jour les attributs self.tour_precedent_passe et self.deux_tours_passes.

        4) Effectuer le changement de joueur. Modifiez à la fois les attributs self.joueur_courant et
           self.couleur_joueur_courant.

        5) Lorsque la partie est terminée, afficher un message mentionnant le résultat de la partie. Vous avez une
           fonction à implémenter que vous pourriez tout simplement appeler.
        """
        while not self.partie_terminee():
            print(self.planche)

            print("C'est au tour de {}".format(self.couleur_joueur_courant))

            self.coups_possibles = self.planche.lister_coups_possibles_de_couleur(self.couleur_joueur_courant)
            


            if len(self.coups_possibles) == 0:
                if self.tour_precedent_passe:
                    self.deux_tours_passes = True
                self.tour_precedent_passe = True
                self.passer_tour()
            else:
                self.tour()
                self.changerTour()

            
            
    def changerTour(self):
        """
        Change la couleur du joueur courant
        """
        if self.couleur_joueur_courant == "noir":
            self.couleur_joueur_courant = "blanc"
            self.joueur_courant = self.joueur_blanc
        else:
            self.couleur_joueur_courant = "noir"
            self.joueur_courant = self.joueur_noir


    def sauvegarder(self, nom_fichier):
        """
        Sauvegarde une partie dans un fichier. Le fichier condiendra:
        - Une ligne indiquant la couleur du joueur courant.
        - Une ligne contenant True ou False, si le tour précédent a été passé.
        - Une ligne contenant True ou False, si les deux derniers tours ont été passés.
        - Une ligne contenant le type du joueur blanc.
        - Une ligne contenant le type du joueur noir.
        - Le reste des lignes correspondant à la planche. Voir la méthode convertir_en_chaine de la planche
         pour le format.

        ATTENTION : L'ORDRE DES PARAMÈTRES SAUVEGARDÉS EST OBLIGATOIRE À RESPECTER.
                    Des tests automatiques seront roulés lors de la correction et ils prennent pour acquis que le
                    format plus haut est respecté. Vous perdrez des points si vous dérogez du format.

        Args:
            nom_fichier: Le nom du fichier où sauvegarder, un string.
        """
        # On ouvre (crée si il n'existe pas) un fichier texte
        mon_fichier = open(nom_fichier, 'w')
        mon_fichier.write(self.couleur_joueur_courant + '\n')
        mon_fichier.write(str(self.tour_precedent_passe) + '\n')
        mon_fichier.write(str(self.deux_tours_passes) + '\n')
        mon_fichier.write(self.joueur_blanc.obtenir_type_joueur() + '\n')
        mon_fichier.write(self.joueur_noir.obtenir_type_joueur() + '\n')
        mon_fichier.write(self.planche.convertir_en_chaine())

    def charger(self, nom_fichier):
        """
        Charge une partie dans à partir d'un fichier. Le fichier a le même format que la méthode de sauvegarde.

        Args:
            nom_fichier: Le nom du fichier à charger, un string.
        """
        # On converti le fichier en une liste pour plus de facilité la tache
        lines = []
        f = open(nom_fichier,'r')
        for line in f:
            lines.append(line)
        f.close()

        # On remplie la partie selon la liste
        for i in range(len(lines)):
            if i == 0:
                self.couleur_joueur_courant = lines[0].strip('\n')
            elif i == 1:
                self.tour_precedent_passe = eval(lines[1].strip('\n')) #eval va venir evaluer l'expression si on a false
            elif i == 2:
                self.deux_tours_passes = eval(lines[2].strip('\n')) #regarde si on a false et donc 2 tour passer
            elif i == 3:
                self.joueur_noir = self.creer_joueur(lines[3].strip('\n'),"noir")
            elif i == 4:
                self.joueur_blanc = self.creer_joueur(lines[4].strip('\n'),"blanc")
            else:
                self.planche.charger_dune_chaine(lines[i].strip('\n'))

        # Selon la couleur du joueur courant on met a jour le joueur_courant
        if self.couleur_joueur_courant is "noir":
            self.joueur_courant = self.joueur_noir
        else :
            self.joueur_courant = self.joueur_blanc

        
        
