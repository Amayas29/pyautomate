# -*- coding: utf-8 -*-
"""
Code modifiable.
"""
from automate import Automate
from state import State
from transition import Transition
from parser import *

s0 = State(0, True, False)
s1 = State(1, False, False)
s2 = State(2, False, True)

t1 = Transition(s0, 'a', s0)
t2 = Transition(s0, 'b', s1)
t3 = Transition(s1, 'a', s2)
t4 = Transition(s1, 'b', s2)
t5 = Transition(s2, 'a', s0)
t6 = Transition(s2, 'b', s1)

auto1 = Automate([t1, t2, t3, t4, t5, t6], [s0, s1, s2])

# Exercice de base

# Test fonction succ

suc01_a = auto1.succ([s0, s1], 'a')
print("La liste des successeur de 0 et de 1 avec la lettre a sont :",suc01_a)

# Test fonction accepte

if Automate.accepte(auto1,"abba"):
    print("L'automate accepte le mot abba")
else:
    print("L'automate n'accepte pas le mot abba")

if Automate.accepte(auto1,"aba"):
    print("L'automate accepte le mot aba")
else:
    print("L'automate n'accepte pas le mot aba")

# Test fonction estComplet

if Automate.estComplet(auto1, "ab"):
    print("L'automate est complet pour l'alphabet ab")
else:
    print("L'automate n'est pas complet pour l'alphabet ab")

if Automate.estComplet(auto1, "abc"):
    print("L'automate est complet pour l'alphabet abc")
else:
    print("L'automate n'est pas complet pour l'alphabet abc")

# Test fonction estDeterministe

if Automate.estDeterministe(auto1):
    print("L'automate est deterministe")
else:
    print("L'automate n'est pas deterministe")

t1_ = Transition(s0, 'a', s2)
t2_ = Transition(s0, 'b', s2)
nondeter = Automate([t1, t2, t3, t1_, t2_, t4])
# nondeter.show("Non_deterministe")

if Automate.estDeterministe(nondeter):
    print("L'automate est deterministe")
else:
    print("L'automate n'est pas deterministe")

# Test fonction completeAutomate

auto1_complet = Automate.completeAutomate(auto1, "abc")
# auto1_complet.show("auto1_complet_abc")

# Test fonction determinsation

deter = Automate.determinisation(nondeter)

if Automate.estDeterministe(deter):
    print("L'automate est deterministe")
else:
    print("L'automate n'est pas deterministe")

# deter.show("Determinise")

# Test fonction complementaire

compelem = Automate.complementaire(auto1, "ab")
# compelem.show("complementaire1")

compelem2 = Automate.complementaire(nondeter, "ab")
# compelem2.show("complementaire2")

# Test fonction intersection

auto3 = Automate([Transition(s0, 'a', s2), Transition(s1, 'a', s1), Transition(s0, 'b', s0), Transition(s2, 'a', s0), Transition(s1, 'b', s2)])

inter = Automate.intersection(auto1, auto3)
# inter.show("Intersection")

# Test fonction union

inter = Automate.union(auto1, auto3)
# inter.show("union")

# Test fonction concatenation

conca = Automate.concatenation(auto1, auto3)
# conca.show("concatenation")

# Test fonction etoile

etoile = Automate.etoile(auto1)
# etoile.show("etoile")