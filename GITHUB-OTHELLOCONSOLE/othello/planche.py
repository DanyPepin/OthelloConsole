from othello.piece import Piece


class Planche:
    """
    Classe représentant la planche d'un jeu d'Othello.
    """

    def __init__(self):
        """
        Méthode spéciale initialisant une nouvelle planche.
        """
        # Dictionnaire de cases. La clé est une position (ligne, colonne), et la valeur une instance de la classe Piece.
        self.cases = {}

        # On joue au Othello 8x8
        self.nb_cases = 8

        # Appel de la méthode qui initialise une planche par défaut.
        self.initialiser_planche_par_default()

    def get_piece(self, position):
        """
        Récupère une pièce dans la planche.

        Args:
            position: La position où récupérer la pièce, un tuple de coordonnées matricielles (ligne, colonne).

        Returns:
            La pièce à cette position s'il y en a une, None autrement.
        """
        if self.position_valide(position) and self.cases[position] is not None:
            return self.cases[position]
        return None

    def position_valide(self, position):
        """
        Vérifie si une position est valide (chaque coordonnée doit être dans les bornes).

        Args:
            position: Un couple (ligne, colonne), tuple de deux éléments.

        Returns:
            True si la position est valide, False autrement
        """
        return 0 <= position[0] <= 7 and 0 <= position[1] <= 7  # va retourner un booleen

    def obtenir_positions_mangees(self, position, couleur):
        """
        Détermine quelles positions seront mangées si un coup de la couleur passée est joué à la position passée.

        ***RETOURNEZ SEULEMENT LA LISTE DES POSITIONS MANGÉES, NE FAITES PAS APPEL À piece.echange_couleur() ICI.***

        Ici, commencez par considérer que, pour la position évaluée, des pièces peuvent être mangées dans 8 directions
        distinctes représentant les 8 cases qui entourent la position évaluée. Vous devez donc vérifier, pour chacune
        de ces directions, combien de pièces sont mangées et retourner une liste regroupant les pièces mangées dans
        toutes les directions.

        Ici, une direction représente une liste de 2 entiers pour la déplacement en x et y. Par exemple, pour la
        direction diagonale où en explore vers le bas et vers la droite, on utiliserait la liste [1, 1]. De même, pour
        la direction gauche, on utiliserait la liste [-1, 0]. Il y a donc un total de 8 directions, représentant les
        8 positions auxquelles la position actuelle peut toucher.

        Pensez à faire appel à la fonction obtenir_positions_mangees_direction().

        Args:
            position: La position du coup à jouer.
            couleur: La couleur du coup à jouer.

        Returns:
            une liste contenant toutes les positions qui seraient mangées par le coup.
        """
        
        # Liste des 8 directions (sens horaire)
        liste_directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

        # Liste des positions que le coup va manger
        liste_positions_mangees = []

        for direction in liste_directions:
            liste_positions_mangees.extend(self.obtenir_positions_mangees_direction(couleur, direction, position))
        return liste_positions_mangees

    def obtenir_positions_mangees_direction(self, couleur, direction, position):
        """
        Détermine les positions qui seront mangées si un coup de couleur "couleur" est joué à la position "position",
        si on parcourt la planche dans une direction "direction".

        Pour une direction donnée, vous devez parcourir la planche de jeu dans la direction. Tant que votre déplacement
        vous mène sur une pièce de la couleur mangée, vous continuez de vous déplacer. Trois situations surviennent
        alors pour mettre un terme au parours dans la direction :

        1) Vous arrivez sur une case vide. Dans ce cas, aucune pièce n'est mangée.

        2) Vous arrivez sur une case extérieure à la planche. Encore une fois, aucune pièce n'est mangée.

        3) Vous arrivez sur une case de la même couleur que le coup initial. Toutes les pièces de la couleur opposée
        que vous avez alors rencontrées dans votre parcours doivent alors être ajoutées à grande liste des pièces
        mangées cumulées.

        N.B. : Cette méthode peut être implémentée par au moins deux techniques différentes alors laissez place à votre
        imagination et explorez ! Une méthode faisant une boucle d'exploration complète et une méthode de parcours
        récursif  sont quelques-unes des façons de faire que vous pouvez explorer. Il se peut même que votre solution
        ne soit pas dans les solutions énumérées précédemment.

        Args:
            couleur: La couleur du coup évalué
            direction: La direction de parcours évaluée
            position: La position du coup évalué

        Returns:
            La liste (peut-être vide) de toutes les positions mangées à partir du coup et de la direction donnés.
        """
        x, y = position
        x_direction, y_direction = direction
        autre_couleur = "noir" if couleur == "blanc" else "blanc"
        liste_positions_mangees_direction = []

        # On recupere toutes les pieces qui vont possiblement etre mangées
        while self.position_valide((x + x_direction, y + y_direction)) and self.cases[(x + x_direction, y + y_direction)] is not None and self.cases[(x + x_direction, y + y_direction)].couleur == autre_couleur:
            x += x_direction
            y += y_direction
            liste_positions_mangees_direction.append((x, y))   
        
        # On vérifie qu'elles soient bien encerclées par deux pieces de la meme couleur
        encercle = False
        if len(liste_positions_mangees_direction) > 0:
            if self.position_valide((x + x_direction, y + y_direction)) and self.cases[(x + x_direction, y + y_direction)] is not None and self.cases[(x + x_direction, y + y_direction)].couleur == couleur:
                encercle = True
            
        if not encercle:
            liste_positions_mangees_direction.clear()

        return liste_positions_mangees_direction


    def coup_est_possible(self, position, couleur):
        """
        Détermine si un coup est possible. Un coup est possible si au moins une pièce est mangée par celui-ci. ET SI LA POSITION NEST PAS DEJA PRISE

        Args:
            position: La position du coup évalué
            couleur: La couleur du coup évalué

        Returns:
            True, si le coup est valide, False sinon
        """

        return len(self.obtenir_positions_mangees(position,couleur)) > 0 and type(self.cases[position]) is not Piece



    def lister_coups_possibles_de_couleur(self, couleur):
        """
        Fonction retournant la liste des coups possibles d'une certaine couleur. Un coup est considéré possible
        si au moins une pièce est mangée quand la couleur "couleur" joue à une certaine position, ne l'oubliez pas!

        ATTENTION: ne dupliquez pas de code déjà écrit! Réutilisez les fonctions déjà programmées!

        Args:
            couleur: La couleur ("blanc", "noir") des pièces dont on considère le déplacement, un string

        Returns:
            Une liste de positions de coups possibles pour la couleur "couleur"
        """
        coups_possible = []
        for case in self.cases:      
            # Si il y a des coups possibles pour cette case                           
            if self.coup_est_possible((case[0], case[1]), couleur):
                coups_possible.append((case[0], case[1]))            

        return coups_possible

    def jouer_coup(self, position, couleur):
        """
        Joue une pièce de la couleur "couleur" à la position "position".

        Cette méthode doit également:
        - Ajouter la pièce aux pièces de la planche.
        - Faire les changements de couleur pour les pièces mangées par le coup.
        - Retourner un message indiquant "ok" ou "erreur".

        ATTENTION: Ne dupliquez pas de code! Vous savez déjà qu'un coup est valide si au moins une pièce est mangée
                   par celui-ci. Vous avez une méthode qui fait exactement ce travail à programmer !

        Args:
            position: La position du coup.
        couleur: La couleur du coup.

        Returns:
            "ok" si le déplacement a été effectué car il est valide, "erreur" autrement.
        """

        if self.coup_est_possible(position,couleur):
        # On pose la piece
            self.cases[(position[0],position[1])] = Piece(couleur)
            # On retourne les pieces mangées
            positions_mangees = self.obtenir_positions_mangees(position, couleur)
            for pos in positions_mangees:
                self.get_piece(pos).echange_couleur()
            return "ok"
        return "erreur"

    def convertir_en_chaine(self):
        """
        Retourne une chaîne de caractères où chaque case est écrite sur une ligne distincte.
        Chaque ligne contient l'information suivante :
        ligne,colonne,couleur

        Cette méthode pourrait par la suite être réutilisée pour sauvegarder une planche dans un fichier.

        Returns:
            La chaîne de caractères.
        """

        # dictionaire { "key" : "value"}
        # planche {"position" : "piece"}


        chaine = ""
        # On regarde les items du dictionnaires sous forme de tuple (key,value) = (position,piece)
        # rappel notre
        for position, piece in self.cases.items():
            if type(piece) is Piece:
                chaine += str(position[0]) + ',' # on ajoute ',' car on veut format ligne,colonne,couleur
                chaine += str(position[1]) + ','
                chaine += piece.couleur
                chaine += "\n"
        return chaine
            
    def charger_dune_chaine(self, chaine):
        """
        Remplit la planche à partir d'une chaîne de caractères comportant l'information d'une pièce sur chaque ligne.
        Chaque ligne contient l'information suivante :
        ligne,colonne,couleur

        Args:
            chaine: La chaîne de caractères, un string.
        """
        info_chaine = chaine.split(",")
        self.cases[(int(info_chaine[0]), int(info_chaine[1]))] = Piece(info_chaine[2])

    def initialiser_planche_par_default(self):
        """
        Initialise une planche de base avec la position initiale des pièces.
        """
        self.cases.clear()
        self.remplirCasesDeNone()
        self.cases[(3, 3)] = Piece("blanc")
        self.cases[(3, 4)] = Piece("noir")
        self.cases[(4, 3)] = Piece("noir")
        self.cases[(4, 4)] = Piece("blanc")

    def remplirCasesDeNone(self):
        """
        Rempli la planche de None afin d'eviter les keyError et faciliter le parcourt
        """
        for i in range(self.nb_cases):
            for j in range(self.nb_cases):
                self.cases[(i, j)] = None

    def __repr__(self):
        """
        Cette méthode spéciale permet de modifier le comportement d'une instance de la classe Planche pour l'affichage.
        Faire un print(une_planche) affichera la planche à l'écran. 
        Legere modification pour prendre en compte les None
        """
        s = "  +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"
        for i in range(0, self.nb_cases):
            s += str(i)+" | "
            for j in range(0, self.nb_cases):
                if ((i, j) in self.cases and self.cases[(i, j)] is not None):
                    s += str(self.cases[(i, j)])+" | "
                else:
                    s += "  | "
            s += str(i)
            if i != self.nb_cases - 1:
                s += "\n  +---+---+---+---+---+---+---+---+\n"

        s += "\n  +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"

        return s