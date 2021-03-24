# -*- coding: utf-8 -*-
from typing import Dict, List, Set
from transition import *
from state import *
import os
import copy
#from sp import *
#from parser import *
from itertools import product
from automateBase import AutomateBase


class Automate(AutomateBase):
        
    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs

    def succ (self, listStates:List, lettre:str):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        # Un set pour empecher la duplication des etats
        successeursLettre:Set = set()
        # state: State
        for state in listStates:
            # On ajoute pour chaque etat ces successeurs à partir de la lettre 
            successeursLettre = successeursLettre.union(self.succElem(state, lettre))

        return list(successeursLettre)

    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """
    @staticmethod
    def accepte(auto,mot:str) :
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """
        listStates:List = auto.getListInitialStates() # On reccupere la liste des etats initaux
        # lettre: str
        for lettre in mot: # On parcours le mot
            listStates = auto.succ(listStates, lettre) # On reccupere les successeurs de la liste a chaque fois
        return State.isFinalIn(listStates) # On verifie si à la fin qu'on a obtenu des etat finals pour que le mot soit accepte

    @staticmethod
    def estComplet(auto,alphabet:str) :
        """ Automate x str -> booltransaction
         rend True si auto est complet pour alphabet, False sinon
        """    
        # Si la liste des etats initial est vide alors il n'est pas complet
        if auto.getListInitialStates() == []:
            return False

        # state:State
        # On parcours les etats de l'automate
        for state in auto.listStates: 
            # lettre: str
            # On parcours l'alphabet
            for lettre in alphabet:
                # Si un etat n'a pas de successeur avec la lettre
                if auto.succElem(state, lettre) == []:
                    # Donc l'automate n'est pas complet
                    return False 

        # Si tout est ok alors il est complet
        return True 

    @staticmethod
    def estDeterministe(auto) :
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """
        # Si l'automate n'existe oas ou si on a pas un seul etat initial alors l'automate n'est pas deterministe
        if auto == None or len(auto.getListInitialStates()) != 1:
            return False

        # state: State
        # On parcours les etats
        for state in auto.listStates:
            # On parcours l'alphabet
            for lettre in auto.getAlphabetFromTransitions():
                 # Si on plus d'un Transition sortante d'un etat avec une meme lettre 
                if len(auto.succElem(state, lettre)) > 1:
                    # l'automate n'est pas deterministe
                    return False
        
         # Sinon il est deterministe
        return True

    @staticmethod
    def completeAutomate(auto,alphabet) :
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """
        # Si l'automate n'existe pas
        if auto == None:
            return None
        # alpha : Automate
        alpha = copy.deepcopy(auto) # On copie l'automate

        # Si il est complet on le retourne directement
        if Automate.estComplet(alpha, alphabet):
            return alpha
       
        # puit: State
        # puit = State(-1, False, False, "T")
        puit = State("T", False, False) # L'etat puit (T pour id pour garantir l'unicite)
        alpha.addState(puit) 

        # state: State | On parcours les etats
        for state in alpha.listStates:
            # lettre: str | Pour chaque lettre 
            for lettre in alphabet: 
                # Si on a pas de Transition sortante de l'etat avec une lettre
                if alpha.succElem(state, lettre) == []:
                    # On ajoute une Transition vers l'etat puit
                    alpha.addTransition(Transition(state, lettre, puit)) 

        return alpha       

    @staticmethod
    def determinisation(auto) :
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
        # SI l'automate n'existe pas ou bien on a pas d'etats initial
        if auto == None or auto.getListInitialStates() == []:
            return None
        # Si il est deterministe on retourne sa copie
        if Automate.estDeterministe(auto):
            return copy.deepcopy(auto)

        # dictFin: dict[State, List(State)] un dictionnaitre pour garder les etat deja traite
        dictFin:Dict = {} 
        # listTransitions: List(Transition)
        listTransitions:List = []
        # Un compteur pour les id
        id:int = 0
        #  On reccupere l'alphabet
        alphabet:List = list(auto.getAlphabetFromTransitions()) 
        # Pour avoir à chaque fois le même resultat car getAlphabetFromTransitions ne retourne pas le meme ordre
        alphabet.sort()
        
        # init: List(State) la liste des etats initiaux
        init:List = auto.getListInitialStates()
        # On crée l'etat initial qui est compose de tous les etats initiaux
        state:State = State(id, True, State.isFinalIn(init), "{" + ','.join( str(st.id) for st in init) + "}")
        # file: List[(List(State), State)] : une file d'attente pour les etat non traite (une liste d'etat qui compose l'etat obtenu)
        file = [(init, state)]
        # On ajoute l'etat créer au dictionnaire pour ne pas le recreer
        dictFin[state] = init

        # Tantque il reste des etats a traite
        while file != []:
            # On reccupere l'etat avec sa liste des etats qui le compose
            (lstate, state) = file.pop(0)
            # lettre: str, on parcours l'alphabet
            for lettre in alphabet:
                # On reccupere la liste des successeurs de la liste
                listSuccs = auto.succ(lstate, lettre)
                if listSuccs == []: # Si la liste est vide on passe l'etat
                    continue
 
                dest = None
                # On parcours le dictionnaire pour savoir si on a deja traité l'etat
                for s, l in dictFin.items():
                    # On compare la liste des etats qui composent un etat du dictionnaire à la liste des successeurs obtenue 
                    # (un set pour ne pas se socier de l'ordre)
                    if set(l) == set(listSuccs):
                        dest = s # On reccupere l'etat
                        break

                # Si on a rien reccuperer donc le sommet est un nouveau sommet, on l'ajoute
                if dest == None:
                    id += 1 # On incremente les id
                    # On crée l'etat
                    dest = State(id, False, State.isFinalIn(listSuccs), "{" + ','.join( str(st.id) for st in listSuccs) + "}")
                    dictFin[dest] = listSuccs # On l'ajoute au dictionnaire
                    file.append((listSuccs, dest)) # On l'ajoute à la file d'attente

                listTransitions.append(Transition(state, lettre, dest)) # On cree une Transition de l'etat courant et l'etat destination
            
        # A la fin on retourne l'automate obtenu
        return Automate(listTransitions)

    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        # On complete l'automate
        alpha = Automate.completeAutomate(auto, alphabet) 
        # On le determinise
        alpha = Automate.determinisation(alpha) 

        if alpha == None: # Si il n'existe pas 
            return None
        # state: State
        # On parcous la liste des etats
        for state in alpha.listStates:
            # Et on inverse les etat finaux 
            state.fin = not state.fin 

        return alpha

    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        # Si l'un des automate n'existe pas
        if auto0 == None or auto1 == None:
            return None
        # alphabet: List(str) | on reccupere l'alphabet des deux automate
        alphabet = list(set(auto0.getAlphabetFromTransitions()).union(auto1.getAlphabetFromTransitions()))
        alphabet.sort()

        # dictStates: dict[(State, State), State] un dictionnaire pour garder l'etat construit a partir d'un couple d'etat
        dictStates:Dict = {}
        # La liste des transition
        listTransitions:List = []
        # Le id des etats
        id:int = 0
        # On reccupere la liste des etats initiaux
        listProd = list(product(auto0.getListInitialStates(), auto1.getListInitialStates())) 
        # Si il n'existe pas on retourne None
        if listProd == []: 
            return None

        # On parcours la liste des etats initial
        for (s0, s1) in listProd: 
            # On creer l'etat compose obtenu
            dictStates[(s0, s1)] = State(id, True, s0.fin and s1.fin, "(" + s0.label + "," + s1.label + ")")
            id += 1

        # Tantque il reste des etats à ajouter
        while listProd != []:
            # On reccupere un couple d'etat
            (s0, s1) = listProd.pop(0) 

            # On parcours l'alphabet
            for lettre in alphabet:
                 # On reccupere les liste des successeurs
                succ0, succ1 = auto0.succElem(s0, lettre), auto1.succElem(s1, lettre)
                # Si un des liste est vide on passe le couple
                if succ0 == [] or succ1 == []: 
                    continue

                # On parcours les couples obtenu par le produit cartesien des liste de successeurs
                for (d0, d1) in list(product(succ0, succ1)): 
                    # Si on a pas deja traite le couple on l'ajoute
                    if (d0, d1) not in dictStates: 
                        # On l'ajoute au dictionnaire
                        dictStates[(d0, d1)] = State(id, False, d0.fin and d1.fin, "(" + d0.label + "," + d1.label + ")") 
                        # On ajoute le couple à la liste
                        listProd.append((d0,d1)) 
                        id += 1

                    # On ajoute la Transition
                    listTransitions.append(Transition(dictStates[(s0, s1)], lettre, dictStates[(d0, d1)]))
                
        return Automate(listTransitions)

    @staticmethod       
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
         # On complete les automates
        auto0 = Automate.completeAutomate(auto0, auto0.getAlphabetFromTransitions())
        auto1 = Automate.completeAutomate(auto1, auto1.getAlphabetFromTransitions())
        
        # La meme chose que l'intersection juste que un etat final peut etre final si l'un des etats qui le compose est final
        if auto0 == None or auto1 == None:
            return None

        alphabet = list(set(auto0.getAlphabetFromTransitions()).union(auto1.getAlphabetFromTransitions()))
        alphabet.sort()

        dictStates, id, listTransitions = {}, 0, []       
        listProd = list(product(auto0.getListInitialStates(), auto1.getListInitialStates()))
        
        if listProd == []:
            return None

        for (s0, s1) in listProd:
            dictStates[(s0, s1)] = State(id, True, s0.fin or s1.fin, "(" + s0.label + "," + s1.label + ")")
            id += 1

        while listProd != []:
            (s0, s1) = listProd.pop(0)
            for lettre in alphabet:
                succ0, succ1 = auto0.succElem(s0, lettre), auto1.succElem(s1, lettre)

                if succ0 == [] or succ1 == []:
                    continue

                for (d0, d1) in list(product(succ0, succ1)):
                    if (d0, d1) not in dictStates:
                        dictStates[(d0, d1)] = State(id, False, d0.fin or d1.fin, "(" + d0.label + "," + d1.label + ")")
                        listProd.append((d0,d1))
                        id += 1

                    listTransitions.append(Transition(dictStates[(s0, s1)], lettre, dictStates[(d0, d1)]))
                
        return Automate(listTransitions)

    @staticmethod
    def concatenation (auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        if auto1 == None or auto2 == None: # Si un des automate n'existe pas
           return None
    
        # On copie l'automate 1
        automate = copy.deepcopy(auto1)
        # On ajoute les Transition de l'automate 2 qui n'existe pas dans l'automate 1 
        for t in auto2.listTransitions:
            # On ajoute la copie de la Transition
            automate.addTransition(copy.deepcopy(t)) 

        # On reccupere la liste des etats initiaux
        init1, init2 = auto1.getListInitialStates(), auto2.getListInitialStates()

        # On parcours les Transitions de l'automate 1 
        for t in auto1.listTransitions:
            # Si l'etat destination de la Transition est final
            if t.stateDest.fin: 
                # On parcours la liste des etats initiaux de l'automate 2
                for s in init2: 
                    # On ajoute les Transitions de l'etat final 1 vers les etats initiaux 2
                    automate.addTransition(Transition(t.stateSrc, t.etiquette, s))
        
        # Si les etats initiaux 1 ne contient pas un etat final
        if not State.isFinalIn(init1): 
            # Pour tout les etat de l'automate
            for state in automate.listStates: 
                # Pour tous les etats initial 2 qui ne sont pas dans la liste des initiaux 1
                if state.init and state in init2 and state not in init1: 
                    # On enleve le fait qu'il est initial
                    state.init = False 
        return automate

    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        # Si l'automate n'existe pas
        if auto == None:
            return None
        
        # On copie l'automate
        automate = copy.deepcopy(auto) 
        # On reccupere la liste des etats initiaux
        init = automate.getListInitialStates() 

        # On parcours le Transitions
        for t in automate.listTransitions: 
            # Si la destination est un etat final
            if t.stateDest.fin:
                # On parcours les etats initials
                for i in init:
                    # On ajoute les Transitions
                    automate.addTransition(Transition(t.stateSrc, t.etiquette, i)) 

        # On ajoute un etat final et initial pour le mot vide
        automate.addState(State('J', True, True))
        return automate