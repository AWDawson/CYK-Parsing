def load_grammar(file_path):
    with open(file_path) as fp:
        grammar = fp.readlines()
        grammar = [x.replace('->','').replace('[','').replace(']','').split() for x in grammar]
        for rule in grammar:
            rule[-1] = float(rule[-1])
    return grammar

def add_rule(rule):
    global grammar_rule
    if rule[0] not in grammar_rule:
        grammar_rule[rule[0]] = []
    elif '|' in rule[0]:
        return 
    grammar_rule[rule[0]].append(rule[1:])


def convert_CNF(grammar):
    for rule in grammar:
        if len(rule) <= 4:
            add_rule(rule)
        elif len(rule) == 5:
            rule1 = [rule[0], rule[1]+'|'+rule[2],rule[3],rule[4]]
            add_rule(rule1)
            rule2 = [rule[1]+'|'+rule[2],rule[1],rule[2],1]
            add_rule(rule2)
        elif len(rule) == 6:
            rule1 = [rule[1]+'|'+rule[2],rule[1],rule[2],1]
            rule2 = [rule[1]+'|'+rule[2]+'|'+rule[3],rule[1]+'|'+rule[2],rule[3],1]
            rule3 = [rule[0],rule[1]+'|'+rule[2]+'|'+rule[3],rule[4],rule[5]]
            add_rule(rule1)
            add_rule(rule2)
            add_rule(rule3)
            continue
    

grammar_rule = {}
grammar = load_grammar('grammar.txt')
convert_CNF(grammar)
print('a')