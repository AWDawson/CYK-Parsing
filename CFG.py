'''
Converting txt to PCFG, then output to a txt file
'''
from nltk import Tree
from nltk.corpus import treebank
from nltk import Nonterminal
from nltk import induce_pcfg

productions = []

filepath = 'TrainingTree.txt'
with open(filepath) as fp:
   line = fp.readline()
   while line:
       line = line.replace('[','(').replace(']',')')
       t = Tree.fromstring(line)
       productions += t.productions()
       line = fp.readline()


S = Nonterminal('S')
grammar = induce_pcfg(S, productions)

with open("grammar.txt", "w") as text_file:
    for item in grammar._productions:
        text_file.write(str(item,)+'\n')