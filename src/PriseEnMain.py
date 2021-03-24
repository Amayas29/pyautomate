# -*- coding: utf-8 -*-

from automate import Automate
from state import State
from transition import Transition
from copy import deepcopy
import itertools

print("Debut des tests")

s1 = State(1, True, False)
s2 = State(2, False, False)
s3 = State(3, False, True)

t = []

t.append(Transition(s1, 'a', s2))
t.append(Transition(s1, 'b', s1))

t.append(Transition(s2, 'b', s3))
t.append(Transition(s2, 'a', s2))

t.append(Transition(s3, 'a', s3))
t.append(Transition(s3, 'b', s3))


auto1 = Automate(t, [s1, s2, s3])

t = []
t.append(Transition(s1, 'b', s2))

t.append(Transition(s2, 'b', s2))
t.append(Transition(s2, 'a', s3))

t.append(Transition(s3, 'a', s3))
t.append(Transition(s3, 'b', s2))

auto2 = Automate(t, [s1, s2, s3])

# auto = Automate([t1, t2, t3, t4, t5, t6])
# print(auto)
# print(auto.getListInitialStates())
# auto.show("auto")
# print(auto1)
# auto1.show("auto1")
# print(auto1.getListTransitionsFrom(s0))

# auto2 = Automate.creationAutomate("auto2.txt")
# print(auto2)
# auto2.show("auto2")

"""
print("Remove transition")
t = Transition(s0, 'a', s1)
auto.removeTransition(t)
print(auto)

print("Remove transition")
auto.removeTransition(t1)
print(auto)

print("Add transition")
auto.addTransition(t1)
print(auto)

print("Remove state")
auto.removeState(s1)
print(auto)

print("Add state")
auto.addState(s1)
print(auto)

print("Add state")
s = State(0, True, False)
auto.addState(s)
print(auto)

liste = auto1.getListTransitionsFrom(s1)
print(liste)
"""

def succ(auto, listeState, lettre):

    succsByLetter = set()

    for state in listeState:
        succsByLetter = succsByLetter.union(auto.succElem(state, lettre))
        
    return list(succsByLetter)


def accepte(auto, word):

    listStates = auto.getListInitialStates()

    for letter in word:
        listStates = succ(auto, listStates, letter)

    return State.isFinalIn(listStates)      


def estComplet(alphabet, auto):

    if auto.getListInitialStates() == [] :
        return False

    listStates = auto.listStates
    alphabet = set(alphabet)

    for state in listStates :
        
        for letter in alphabet:
          
            succLetter = succ(auto, [state], letter)
           
            if len(succLetter) == 0 :
                return False
           
    return True


def estDeter(auto):

    if len(auto.getListInitialStates()) == 1 :
        return False
    
    listStates = auto.listStates
    alphabet = auto.getAlphabetFromTransitions()

    for state in listStates :
        
        for letter in alphabet:
           
            succLetter = succ(auto, [state], letter)
           
            if len(succLetter) > 1 :
                return False
           
    return True

def compl(auto, alphabet):
    if auto == None:
        return None

    alpha = deepcopy(auto)
    alphabet = set(alphabet)
    well = State(-1, False, False, "T")
    alpha.addState(well)
    listStates = alpha.listStates

    rmWell = True
    for state in listStates:
       
        for letter in alphabet:
           
            succLetter = succ(auto, [state], letter)
           
            if len(succLetter) == 0 :
                
                alpha.addTransition(Transition(state, letter, well))
                
                if not (state is well) :
                    rmWell = False

    if rmWell :
        alpha.removeState(well)

    return alpha

def deterr(auto):
    if auto == None:
        return None

    init = auto.getListInitialStates()

    if init == [] :
       return None

    alphabet = auto.getAlphabetFromTransitions()
    listStates = set()    
    listTransation = list()

    listMultipe = list()
    listMultipesOfStates = list()

    listStatesOfActual = init
    stateid= ''.join(st.label for st in list(listStatesOfActual))
    stateLabel = ','.join(st.label for st in list(listStatesOfActual))
    actual = State(stateid, True, State.isFinalIn(listStatesOfActual), stateLabel)

    listMultipe.append(actual)
    listMultipesOfStates.append(listStatesOfActual)

    while listMultipe != []:
        
        actual = listMultipe.pop()
        listStatesOfActual = listMultipesOfStates.pop()
       
        listStates.add(actual)

        for letter in alphabet:
            a = succ(auto, listStatesOfActual, letter)
            a = sorted(a, key=lambda state: state.label)
            
            if a == []:
                continue

            stateid= ''.join(st.label for st in a)
            stateLabel = ','.join(st.label for st in a)

            dest = State(stateid, False, State.isFinalIn(a), stateLabel)
        
            print("t",dest,"t",sep="")
            if dest not in listStates and not dest == actual:
                listMultipe.append(dest)
                listMultipesOfStates.append(a)
            
            listStates.add(dest)
            t = Transition(actual, letter, dest)
            if t not in listTransation:
                listTransation.append(t) 
  
    detAuto = Automate(listTransation, listStates)
    return detAuto

def compli(auto, alphabet):
    if auto == None:
        return None

    alpha = deterr(auto)
    alpha = compl(alpha, alphabet)

    if alpha == None:
        return None

    listStates = alpha.listStates

    for state in listStates:
        state.fin = not state.fin

    return alpha


def inter(auto1, auto2):

    listStatesTuple = list(itertools.product(auto1.listStates, auto2.listStates))
    listInitStates = list(itertools.product(auto1.getListInitialStates(), auto2.getListInitialStates()))
    listFinalStates = list(itertools.product(auto1.getListInitialStates(), auto2.getListInitialStates()))

    listeStates = []
    
    for state1, state2 in listStatesTuple:

        id = str(state1.id) + str(state2.id)
        label = str(state1.id) + "," + str(state2.id)

        s = State(id, (state1, state2) in listInitStates, (state1, state2) in listFinalStates, label)
        listeStates.append(s)
  
    print(listeStates)
    # listTransation = []

    for s1, s2 in listStatesTuple:
        for s1p, s2p in listStatesTuple:
           
            t1 = auto1.getListTransitionsFrom(s1)
            t2 = auto2.getListTransitionsFrom(s2)
            
            print(t1)
            print(t2)
            l1=list(filter(lambda t:t.stateDest==s1p, t1))
            l2=list(filter(lambda t:t.stateDest==s2p, t2))

            print(s1, "  ", s1p, "  ", l1)
            print(s2, "  ", s2p, "  ", l2)

            print("\n")
            


print("\n************ \n")

# auto1.show("auto1")
# auto2.show("auto2")

# inter(auto1, auto2)

"""

auto1.getListInitialStates
auto2 = compli(auto1, ['a', 'b'])
auto2.show("auto2")


auto1.show("auto1")
d = deterr(auto1)
print(d)
d.show("d")


a = compl(auto1)
a.show("a")


alphabet = ['a', 'b']
print(estComplet(alphabet, auto1))

print(estDeter(auto1))

s = input(" : ")
if s == "y":
    auto1.show("auto1")

"""