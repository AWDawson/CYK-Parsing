import sys
TestInputFile = sys.argv[1]
GrammarFile = sys.argv[2]
TextOutputFile = sys.argv[3]

class Node:
    def __init__(self, symbol, prob, child1, child2=None):
        self.symbol = symbol
        self.child1 = child1
        self.child2 = child2
        self.prob = prob

def load_grammar(file_path):
    with open(file_path) as fp:
        grammar = fp.readlines()
        grammar = [x.replace('->','').replace('[','').replace(']','').replace("'",'').split() for x in grammar]
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
    
grammar_rule = {}
grammar = load_grammar(GrammarFile)
convert_CNF(grammar)

def CYK(words):
    global grammar_rule
    length = len(words)
    parse_table = [[[] for x in range(length+1)] for y in range(length+1)]
    for i in range(length):
        for key, value in grammar_rule.items():
            for item in value:
                if words[i] == item[0]:
                    prob = item[1]
                    parse_table[i][i+1].append(Node(key,prob,words[i]))
    for span in range(2,length+1):
        for begin in range(0,length-span+1):
            end = begin + span
            for split in range(begin+1, end):
                left_cell = parse_table[begin][split]
                right_cell = parse_table[split][end]
                for non_term, rule_list in grammar_rule.items():
                    for rule in rule_list:
                        left_nodes = [node for node in left_cell if node.symbol == rule[0]]
                        if left_nodes:
                            right_nodes = [node for node in right_cell if node.symbol == rule[1]]
                            if right_nodes:
                                prob = left_nodes[0].prob*right_nodes[0].prob*rule[2]
                                if non_term not in [node.symbol for node in parse_table[begin][end]]:
                                    parse_table[begin][end].append(Node(non_term,prob,left_nodes[0],right_nodes[0]))
                                else:
                                    pre_node = [node for node in parse_table[begin][end] if node.symbol == non_term]
                                    if prob >= pre_node[0].prob:
                                        parse_table[begin][end].remove(pre_node[0])
                                        parse_table[begin][end].append(Node(non_term,prob,left_nodes[0],right_nodes[0]))
    if not parse_table[0][length]:
        #print('FAIL to parse',words)
        return []
    else:
        return parse_table

def remove_cnf(parse_table):
    for node in parse_table[0][len(parse_table)-1]:
        if '|' in node.symbol:
            pair = node.symbol.split('|')
            for non_term, rule_list in grammar_rule.items():
                if '|' not in non_term:
                    for rule in rule_list:
                        if rule[0] == pair[0] and rule[1] == pair[1]:
                            node.symbol = non_term
                            node.prob = rule[2]*node.prob
    return parse_table

def generate_tree(node):
    if node.child2 is None:
        return f"[{node.symbol} {node.child1}]"
    if '|' in node.symbol:
        return f"{generate_tree(node.child1)} {generate_tree(node.child2)}"
    return f"[{node.symbol} {generate_tree(node.child1)} {generate_tree(node.child2)}]"


def create_treebank(parse_table):
    if not parse_table:
        #print('FAIL')
        result = 'FAIL'
    else:
        node_list = parse_table[0][len(parse_table)-1]
        prob_list = [node.prob for node in node_list]
        index = prob_list.index(max(prob_list))
        result = generate_tree(parse_table[0][len(parse_table)-1][index])
        #print(result)
    return result

filepath1 = TestInputFile
with open(filepath1) as fp:
    lines = fp.readlines()
    # remove the last rows '/n'
    cnt = 0
    for line in lines:
        if len(line.strip()) == 0:
            cnt+=1
    for i in range(cnt):
        lines.remove('\n')
    for i in range(len(lines)):
        lines[i] = lines[i].strip()



#filepath2 = 'TestingRaw.txt'
#with open(filepath2) as fp:
#    lines = fp.readlines()
#    # remove the last row '\n'
#    lines.pop()


fp = open(TextOutputFile,"w+")


for i in range(len(lines)):
    result = CYK(lines[i].split())
    if result:
        result = remove_cnf(result)
        my_tree = create_treebank(result)
        fp.write(my_tree)
        fp.write('\n')
    else:
        fp.write('FAIL\n')
    '''
    if my_tree == given_answer[i]:
        print('TRUE')
    else:
        print('FALSE')
    '''

fp.close()



#result = CYK(['take', 'the', 'block', 'on', 'the', 'green', 'circle'])
#create_treebank(result)


#[S [Verb take] [NP [Det the] [Noun block] [PP [Prep on] [NP [Det the] [Adj green] [Noun circle]]]]]
#[S [Verb|NP [Verb take] [NP [Det the] [Noun block]]] [PP [Prep on] [NP [Det|Adj [Det the] [Adj green]] [Noun circle]]]]
#[S [Verb take] [NP [Det the] [Noun block]] [PP [Prep on] [NP [Det the] [Adj green] [Noun circle]]]]